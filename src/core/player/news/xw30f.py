from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from src.core.playVideos import PlayNews
from src.core.watchfish import Timer
from loguru import logger

class Play(PlayNews):
    def __init__(self) -> None:
        super().__init__()
        self.url = "https://tv.cctv.com/lm/xw30f/"

    @property
    def format_cctv_time(self) -> str:
        now = Timer.time()
        year, month, day, _, hour, _, _ = now

        if hour < 13:
            now = Timer.time(1)
        year, month, day, _, hour, _, _ = now

        cctv_time = f"{year:04d}{month:02d}{day:02d}"
        logger.debug(f"CCTV time: {cctv_time}")
        return cctv_time

    def open_page(self) -> bool:
        if not self.driver:
            return False

        try:
            self.driver.get(self.url)
            WebDriverWait(self.driver, 1).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            logger.success(f"News list page loaded:{self.url}")

            target_xpath = (
                f'//a[contains(text(), "新闻30分") and contains(text(), "{self.format_cctv_time}") '
                'and child::i[@class="sql0" and text()="完整版"]]'
            )

            news_item = WebDriverWait(self.driver, 2).until(
                ec.element_to_be_clickable((By.XPATH, target_xpath))
            )
            logger.success(f"Find the target news item:{news_item.text.strip()}")

            news_item.click()
            return True
        except TimeoutException:
            return False