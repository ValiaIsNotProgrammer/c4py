from loguru import logger
from selenium import webdriver
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import io

from contextlib import contextmanager


class WebScreenshotMaker:
    def __init__(self):
        logger.info("Initializing Web Screenshot Maker")
        self.driver = None

    def set_option(self, args: str = '--headless') -> None:
        options = webdriver.ChromeOptions()
        options.add_argument(options)
        self.driver = webdriver.Chrome(options=options)
        logger.info("Web Screenshot Maker get options {}".format(args))

    def get_screenshot(self, url: str) -> bytes:
        logger.info("Getting screenshot from {}".format(url))
        if not self.is_valid(url):
            logger.error("Corrected URL to {}".format(url))
            url = self.to_correct(url)
        with self.__enter__():
            self.driver.get(url)
            logger.info("Driver get url {}".format(url))
            screenshot = self.driver.get_screenshot_as_png()
            logger.success("Screenshot made at {}".format(url))
            return screenshot

    def is_valid(self, url: str) -> bool:
        if "https://" in url:
            return True
        return False

    def __enter__(self):
        logger.info("Entering Web Screenshot Maker")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        return self.driver

    def __exit__(self, exc_type, exc_value, traceback):
        if self.driver:
            self.driver.quit()
        logger.info("Exiting Web Screenshot Maker")

    def to_correct(self, url: str) -> str:
        url = "https://" + url
        if "www." in url:
            url = url.replace("www.", "")
        return url

    @staticmethod
    def get_domain(url: str) -> str:
        domain = url.split("https://")[1].split(".")[0]
        logger.info("Domain: {}".format(domain))
        return domain  # TODO: добавить поддержку http

    @staticmethod
    @contextmanager
    def temporary_image(image_bytes: bytes):
        temp_image = io.BytesIO(image_bytes)
        try:
            yield temp_image
        finally:
            temp_image.close()


screenshot_maker = WebScreenshotMaker()
