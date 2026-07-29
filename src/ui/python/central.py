import os
import sys

from typing import Optional, Any, Protocol

from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtWidgets import QApplication

from core.utils.json_loader import ConfigEditor
from directories import DRIVER_PATH, PathManager, QML_PATH
from core.parser import VideoTypes
from core.player import play
from loguru import logger


class QmlContextWindow(Protocol):
    engine: Any


class AppCentral(QObject):
    _instance: Optional[AppCentral] = None
    initialized = Signal()

    def __init__(self) -> None:  # 初始化
        super().__init__()

        if AppCentral._instance is not None:
            raise RuntimeError("AppCentral is a singleton. Use AppCentral.instance() instead.")
        AppCentral._instance = self

        self._initialize_cores()
        logger.info("AppCentral initialization completed.")

        self.setup = Setup()

    def _initialize_cores(self) -> None:
        self.app_instance: Optional[QApplication] = QApplication.instance()
        self.path_manager: PathManager = PathManager()  # 统一路径管理



    @Slot()
    def init(self) -> None:
        self._continue_init()

    def _continue_init(self) -> None:
        self.initialized.emit()  # 发送信号
        logger.info(f"Initialization completed.")

    def setup_qml_context(self, window: QmlContextWindow) -> None:
        context = window.engine.rootContext()
        window.engine.addImportPath(QML_PATH)
        context.setContextProperty("AppCentral", self)
        context.setContextProperty("PathManager", self.path_manager)

    @Slot()
    def force_play(self) -> None:
        self.setup.force_play()

    @Slot()
    def normal_play(self) -> None:
        self.setup.normal_play()

    @Slot(str)
    def video_type_changed(self, new_type: str) -> None:
        self.setup.video_type_changed(new_type)

    @Slot()
    def new_timeline(self) -> None:
        self.setup.new_timeline()

    @Slot()
    def open_github(self) -> None:
        self.setup.open_github()

    @Slot()
    def open_driver_folder(self) -> None:
        self.setup.open_driver_folder()

    @Slot(str)
    def set_browser_driver_name(self, driver_name: str) -> None:
        self.setup.set_browser_driver_name(driver_name)

    @Slot(int, int, int)
    def set_time(self, hour: int, minute: int, time_type: int) -> None:
        self.setup.set_time(hour, minute, time_type)


class Setup(object):
    def __init__(self) -> None:
        self.force_play_class = ForcePlay()

    def video_type_changed(self, new_type: str) -> None:
        self.force_play_class._video_type_changed(new_type)

    def force_play(self) -> None:
        self.force_play_class._force_play()

    def normal_play(self) -> None:
        VideoPlay.normal_play()

    def new_timeline(self) -> None:
        logger.info("New timeline requested.")
        # todo: implement new timeline functionality

    def open_github(self) -> None:
        os.system("start https://github.com/Purrbyte-zdy/automatic-video-player")

    def open_driver_folder(self) -> None:
        logger.info(f"Opening driver folder: {DRIVER_PATH}")
        os.startfile(DRIVER_PATH)

    def set_browser_driver_name(self, driver_name: str) -> None:
        if not driver_name:
            logger.error("set_browser_driver_name called with an empty string!")
            return
        logger.info(f"Setting browser driver name to: {driver_name}")
        config_editor = ConfigEditor()
        config_editor.setconfig("driver_name", driver_name)

    def set_time(self, hour: int, minute: int, time_type: int) -> None:
        match time_type:
            case 0:
                logger.info(f"Setting Playback Time to {hour:02d}:{minute:02d}")
            case 1:
                logger.info(f"Setting End Time to {hour:02d}:{minute:02d}")

        # todo: edit the schedule configuration with the new time


class VideoPlay(object):
    def __init__(self) -> None:
        self.video_type = VideoTypes.NEWS

    @staticmethod
    def normal_play() -> None:
        logger.info("Starting normal play")
        play(VideoTypes.UNKNOWN)


class ForcePlay(VideoPlay):
    def __init__(self) -> None:
        super().__init__()

    def _video_type_changed(self, new_type: str) -> None:
        logger.info(f"Video type changed to: {new_type}")
        match new_type:
            case "News":
                self.video_type = VideoTypes.NEWS
            case "Documentary":
                self.video_type = VideoTypes.DOCUMENTARY
            case _:
                logger.warning("Unknown video type received.")

    def _force_play(self) -> bool:
        logger.debug("Forcing play")
        play(self.video_type, force_mode=True)
        return True
