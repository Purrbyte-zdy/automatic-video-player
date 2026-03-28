from datetime import datetime, timedelta
from typing import Any, Dict, Tuple
from time import sleep

import json
from loguru import logger

from core.python.utils import VideoTypes
from src.core.python.directories import CONFIG_PATH


class Timer:
    """
    计时器核心类：
    - 从 `configs/schedule.json` 读取当天的配置（按 weekday 名称索引）
    - 保存开始时间和计算出的结束时间（为 datetime）
    - 提供 `is_time_for_stop()` 判断是否已到停止时间
    """

    config: Dict[str, Any]
    start_time: datetime
    end_time: datetime
    weekday_name: str
    weekday_cfg: Dict[str, Any]

    def __init__(self, force_mode=False) -> None:
        self.force_mode = force_mode
        cfg_path = CONFIG_PATH / "schedule.json"
        logger.debug("Loading schedule config from {}", cfg_path)

        if not cfg_path.exists():
            logger.error("Schedule config not found at {}", cfg_path)
            raise FileNotFoundError(f"Config not found: {cfg_path}")

        try:
            with cfg_path.open("r", encoding="utf-8") as f:
                self.config = json.load(f)
        except json.JSONDecodeError as exc:
            logger.exception("Failed to parse schedule config: {}", exc)
            raise

        # 解析当前时间信息
        year, month, day, weekday_name, hour, minute, second = self.time()
        self.weekday_name = weekday_name

        # 从配置中获取当日停止时间（字符串形式 "HH:MM:SS"）
        self.schedule = self.config.get("schedule")
        for weekday in self.schedule:
            if weekday["weekday"] == self.weekday_name:
                self.weekday_cfg = weekday
                break
        # logger.debug("Schedule config: {}, raw schedule: {}", self.weekday_cfg, self.schedule)
        stopping_method = self.weekday_cfg.get("closingMethod")
        stopping_time_lst = self.weekday_cfg.get("endTime")
        stopping_time_str: str
        # TODO: HERE IS A BUG THAT STRANGERS FORCE MODE CAN CAUSE UNEXPECTED STOP TIME, MAY CAUSE BY TOO MANY NEW OBJECTS. SPILT MIGHT FIX THIS PROBLEM.
        logger.debug(f"force mode: {self.force_mode}")
        if stopping_method == "static" and self.force_mode == False:
            stopping_time_str = str(stopping_time_lst[0][0])+":"+str(stopping_time_lst[0][1])+":"+"00"
        else:
            stopping_time_tpl = Timer.time(minute=-stopping_time_lst[1])
            stopping_time_str = str(stopping_time_tpl[4]) + ":" + str(stopping_time_tpl[5]) + ":" + str(stopping_time_tpl[6])
        logger.debug(f"stopping_time_str: {stopping_time_str}")

        if not stopping_time_str:
            logger.warning("No EndTime configured for weekday '{}', defaulting to 23:59:59", self.weekday_name)
            stopping_time_str = "23:59:59"

        try:
            end_hour, end_minute, end_second = map(int, stopping_time_str.split(":"))
        except Exception as exc:
            logger.exception("Invalid stop_time format '{}' for '{}': {}", stopping_time_str, self.weekday_name, exc)
            # 若格式不正确则使用当天 23:59:59
            end_hour, end_minute, end_second = 23, 59, 59

        # 记录开始时间与结束时间（均为 datetime 类型）
        self.start_time = datetime.now()
        self.end_time = datetime(year, month, day, end_hour, end_minute, end_second)
        logger.debug(
            "Timer initialized: start_time={}, end_time={}, weekday={}",
            self.start_time, self.end_time, self.weekday_name
        )

    @staticmethod
    def time(delta=0, minute=0) -> Tuple[int, int, int, str, int, int, int]:
        """
        返回当前时间的结构化元组：
        (Year, Month, Day, WeekdayName, Hour, Minute, Second)
        所有数值项为 int，weekday 为英文全名（例如 'Monday'）。
        """
        dt = datetime.now() - timedelta(delta, minute)
        return dt.year, dt.month, dt.day, dt.strftime("%A"), dt.hour, dt.minute, dt.second

    def is_time_for_stop(self) -> bool:
        """
        检查当前时间是否已到或超过配置的停止时间。
        返回 True 表示应停止。
        """
        now_dt = datetime.now()
        remaining = (self.end_time - now_dt).total_seconds()
        logger.debug("Checking stop time: now={}, end_time={}, remaining_seconds={}", now_dt, self.end_time, remaining)
        return remaining <= 0

    @staticmethod
    def wait(second: float = 5) -> None:
        sleep(second)


class Videos(Timer):
    """
    视频相关扩展类，继承 Timer 并通过配置确定今天的视频类型。
    """

    def __init__(self) -> None:
        super().__init__()

    def get_video_type(self) -> VideoTypes:
        """
        读取当前 weekday 对应配置中的 `type` 字段并返回 VideoTypes 枚举。
        支持不区分大小写的匹配，默认返回 VideoTypes.UNKNOWN。
        """
        # 直接使用当前 weekday 名称（安全读取）
        weekday = self.weekday_name
        type_str = "unknown"
        for i in self.config["schedule"]:
            if i["weekday"] == weekday:
                type_str = i.get("videoType")
                break

        logger.debug("Determining video type for weekday {}: raw='{}'", weekday, type_str)

        if type_str == "News":
            return VideoTypes.NEWS
        if type_str == "Documentary":
            return VideoTypes.DOCUMENTARY

        return VideoTypes.UNKNOWN
