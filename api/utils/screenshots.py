import datetime
from typing import Union

import celery
from PIL.ImageFile import ImageFile
from celery import shared_task
from loguru import logger
from selenium import webdriver
import io

from contextlib import contextmanager

from selenium.common.exceptions import WebDriverException


class WebScreenshotMaker:
    EXCEPTIONS_RESPONSE = {
        "ERR_SSL_VERSION_OR_CIPHER_MISMATCH": "SSL version mismatch. Please check your URL if 'www' part for correct SSL certificate.",
        "ERR_NAME_NOT_RESOLVED": "Name not resolved. Please try again with a different name.",
    }

    def __init__(self, pass_=False):
        logger.info("Initializing Web Screenshot Maker")
        self.driver = None
        if not celery.current_app.control.inspect().ping():
            logger.warning("Celery workers is not found. Web Screenshot Maker will work with default synchronously.")
            self.is_celery_running = False
        else:
            logger.info("Web Screenshot Maker fount celery workers.")
            self.is_celery_running = True

    def _set_option(self, args: str = '--headless') -> None:
        options = webdriver.ChromeOptions()
        options.add_argument(options)
        self.driver = webdriver.Chrome(options=options)
        logger.info("Web Screenshot Maker get options {}".format(args))

    def get_screenshot(self, url: str) -> Union[bytes, str]:
        try:
            if self.is_celery_running:
                logger.info("Web Screenshot Maker make screenshot with celery worker.")
                return self._make_screenshot_with_worker.delay(url)
            logger.info("Web Screenshot Maker make screenshot without celery worker.")
            return self._make_screenshot(url)
        except WebDriverException as ex:
            return self.__get_webdriver_exception(ex)

    def get_image(self, url: str) -> Union[ImageFile, str]:
        logger.info(f'Screenshot start making')
        response = self.get_screenshot(url)
        if type(response) != bytes:
            return response
        domain = screenshot_maker.get_domain(url)
        filename = "screenshots/" + domain + ".png"
        image = ImageFile(io.BytesIO(response), name=filename)
        logger.info(f'Screenshot is got')
        return image

    def _make_screenshot(self, url: str) -> bytes: #AsyncResult]:
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
        if self.is_valid(url):
            return url
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

    @staticmethod
    @shared_task
    async def _make_screenshot_with_worker(screenshot_url: str) -> bytes:
        logger.info(f"Making screenshot {screenshot_url}")
        result = WebScreenshotMaker()._make_screenshot(screenshot_url)
        while True:
            if result.ready():
                logger.success("Screenshot made")
                return result.get()
            elif result.failed():
                logger.error(f"Screenshot failed: {result.info}; {result.get()}")
                return result.get()  # TODO: нормально обработать ошибку в случае неудачи


    def __get_webdriver_exception(self, ex):
        ex.msg = ex.msg.split('\n')[0]
        logger.warning("Web Screenshot Maker get exception {}".format(ex.msg))
        if "ERR_NAME_NOT_RESOLVED" in ex.msg:
            return "Name not resolved. Please try again with a different name."
        elif "ERR_SSL_VERSION_OR_CIPHER_MISMATCH" in ex.msg:
            return "SSL version mismatch. Please check your URL if 'www' part for correct SSL certificate."
        return f"Something went wrong. Please check your URL and try again: {ex.msg}"


screenshot_maker = WebScreenshotMaker()
