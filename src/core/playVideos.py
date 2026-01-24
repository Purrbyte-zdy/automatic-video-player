from json import load
from os import path
from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot
from loguru import logger
from src.core.watchfish import Videos, VideoTypes

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

def play(video_type: VideoTypes) -> None:
    if video_type == VideoTypes.NEWS:
        logger.info("Playing news video...")
        from src.core.player.news.xw30f import Play
        player = Play()
        player.open_page()

    elif video_type == VideoTypes.DOCUMENTARY:
        logger.info("Playing documentary video...")
        player = PlayDocumentary()
    else:
        logger.warning("Unknown video type. Cannot play video.")

class PlayNews(object):
    def __init__(self):
        config_file = Path(__file__).parent.parent.parent / "configs" / "settings.json"
        with open(config_file, 'r', encoding='UTF-8') as f:
            config = load(f)
        try:
            driver_path = Path(__file__).parent.parent.parent / "drivers" / config["driver_path"]
            if not path.exists(driver_path):
                logger.error(f"Missing Driver：{driver_path}")
                self.driver = None

            edge_options = Options()

            edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            edge_options.add_experimental_option("useAutomationExtension", False)

            service = Service(executable_path=driver_path)
            driver = webdriver.Edge(service=service, options=edge_options)
            logger.success("The Browser has been started.")
            driver.maximize_window()
            self.driver = driver

        except Exception as e:
            logger.error(f"The Browser has no started: {e}")
            self.driver = None

class PlayDocumentary(object):
    pass

class AppCentral(QObject):
    def __init__(self) -> None:
        super().__init__()

    @Slot(result=bool)
    def force_play(self) -> bool:
        logger.debug("Forcing play")
        videos = Videos()
        video_type: VideoTypes = videos.get_video_type()
        logger.info(f"Today's video type: {video_type}")
        play(video_type)
        return True