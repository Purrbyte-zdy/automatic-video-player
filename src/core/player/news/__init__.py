from json import load
from os import path
from pathlib import Path
from loguru import logger

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service

class PlayNews(object):
    def __init__(self):
        root = Path(__file__).parent.parent.parent.parent.parent
        config_file = root / "configs" / "settings.json"
        with open(config_file, 'r', encoding='UTF-8') as f:
            config = load(f)
        try:
            driver_path = root / "drivers" / config["driver_path"]
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