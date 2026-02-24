from json import load
from os import path

from keyboard import press_and_release
from loguru import logger

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.wait import WebDriverWait

from src.core.python.directories import CONFIG_PATH, DRIVER_PATH


class PlayNews(object):
    def __init__(self):
        config_file = CONFIG_PATH / "settings.json"
        with open(config_file, 'r', encoding='UTF-8') as f:
            config = load(f)
        try:
            driver_path = DRIVER_PATH / config["driver_name"]
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

    def setup_fullscreen(self) -> bool:
        try:
            press_and_release("f")
            WebDriverWait(self.driver, 2, 0.1).until(
                lambda d: d.execute_script("""
                        return !!(document.fullscreenElement || 
                                 document.webkitFullscreenElement || 
                                 document.msFullscreenElement);
                    """)
            )
            logger.success(f"Fullscreen setup successful by F.")
            return True
        except TimeoutException:
            logger.warning("Fullscreen setup by F failed, trying shift&f.")
        try:
            press_and_release("shift")
            press_and_release("f")
            WebDriverWait(self.driver, 2, 0.1).until(
                lambda d: d.execute_script("""
                        return !!(document.fullscreenElement || 
                                 document.webkitFullscreenElement || 
                                 document.msFullscreenElement);
                    """)
            )
            logger.success(f"Fullscreen setup successful by shift&f.")
            return True
        except TimeoutException:
            logger.warning("Fullscreen setup failed.")
        return False

    def exit_playing(self) -> None:
        if self.driver:
            self.driver.quit()
            logger.info("The Browser has been closed.")