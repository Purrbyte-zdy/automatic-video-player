from loguru import logger

from core.python.utils import VideoTypes
from core.python.utils.watchfish import Timer


class Videos(Timer):
    def __init__(self) -> None:
        super().__init__()

    def get_video_type(self) -> VideoTypes:
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
