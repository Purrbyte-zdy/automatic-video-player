from json import load

from keyboard import press_and_release
from loguru import logger

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from typing import cast

from src.core.python.directories import CONFIG_PATH


class PlayNews(object):
    def __init__(self) -> None:
        '''
        Init the Browser.
        '''

        '''
        to Ref: Use Selenium Manager to manage the driver instead of download by user.
        For More Information: https://www.selenium.dev/zh-cn/documentation/selenium_manager/
        '''

        '''
        The Selenium Manager can use like this:

        ```python
        def setup_with_selenium_manager():
            driver = webdriver.Chrome()
            return driver
        ```

        it's very convenient. :)
        '''
        
        config_file = CONFIG_PATH / "settings.json" # Reading Config File.
        with open(config_file, 'r', encoding='UTF-8') as f:
            config = load(f)
        try:
            browser_name = config["browser_name"] # :Now

            # Use Selenium Manager directly by not specifying a local driver
            # executable. Selenium (v4+) will manage the correct driver for
            # the requested browser automatically.
            match browser_name: # :Now
                case "Firefox":
                    driver = webdriver.Firefox()
                case "Chrome":
                    driver = webdriver.Chrome()
                case "Edge":
                    driver = webdriver.Edge()
                case "Safari":
                    driver = webdriver.Safari()
                case _:
                    logger.error(f"Unknown Browser Name: {browser_name}")
                    driver = None
                    return

            logger.success("The Browser has been started.")
            driver.maximize_window()
            self.driver = driver

        except Exception as e:
            logger.error(f"The Browser has no started: {e}")
            self.driver = None

    def setup_fullscreen(self) -> bool:
        '''
        This function is to fullscreen the browser.
        It use keyboard press F or Shift And F(Sometimes it may be Chinese) to fullscreen.
        '''

        if not getattr(self, "driver", None):
            logger.warning("No browser driver available for fullscreen setup.")
            return False

        # Cast driver to WebDriver for type checkers and use local variable
        driver = cast(WebDriver, self.driver)

        try:
            press_and_release("f")
            WebDriverWait(driver, 2, 0.1).until(
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
            WebDriverWait(driver, 2, 0.1).until(
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
        '''
        Quiting Browser.
        '''
        if self.driver:
            self.driver.quit()
            logger.info("The Browser has been closed.")