import os

from PySide6.QtCore import QObject, Slot
from src.core.watchfish import VideoTypes
from src.core.player.play_videos import play
from loguru import logger

class AppCentral(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.video_type = VideoTypes.NEWS

    @Slot(result=bool)
    def force_play(self) -> bool:
        logger.debug("Forcing play")
        play(self.video_type)
        return True

    @Slot()
    def normal_play(self) -> None:
        logger.info("Starting normal play")
        play(VideoTypes.UNKNOWN)

    @Slot(str)
    def video_type_changed(self, new_type: str) -> None:
        logger.info(f"Video type changed to: {new_type}")
        match new_type:
            case "News":
                self.video_type = VideoTypes.NEWS
            case "Documentary":
                self.video_type = VideoTypes.DOCUMENTARY
            case _:
                logger.warning("Unknown video type received.")

    @Slot()
    def new_timeline(self) -> None:
        logger.info("New timeline requested.")
        # todo: implement new timeline functionality

    @Slot()
    def open_github(self) -> None:
        os.system("start https://github.com/Purrbyte-zdy/automatic-video-player")