import os

from truepositive_test_task.config.settings import WORK_DIR
from selenium import webdriver
# TODO: добавить валидацию ссылки


class WebScreenshotMaker:
    def __init__(self):
        self.driver = None

    def set_option(self, args: str = '--headless') -> None:
        options = webdriver.ChromeOptions()
        options.add_argument(options)
        self.driver = webdriver.Chrome(options=options)

    def get_screenshot_(self, url: str) -> bytes:
        with self.__enter__():
            self.driver.get(url)
            screenshot = self.driver.get_screenshot_as_png()
            return screenshot

    def __enter__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        return self.driver

    def __exit__(self, exc_type, exc_value, traceback):
        if self.driver:
            self.driver.quit()


screenshot_maker = WebScreenshotMaker()