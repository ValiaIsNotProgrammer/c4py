import datetime
import time
from typing import Union

import io
from loguru import logger
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.common.exceptions import WebDriverException
from django.core.files.images import ImageFile
from contextlib import contextmanager


# --------------- Для использования в Докер --------------------
chromedriver_path = chromedriver_autoinstaller.install(cwd=True)
logger.info("Chrome driver path: {}".format(chromedriver_path))


class WebScreenshotMaker:
    EXCEPTIONS_RESPONSE = {
        "ERR_SSL_VERSION_OR_CIPHER_MISMATCH":
            "SSL version mismatch. Please check your URL if 'www' part for correct SSL certificate.",
        "ERR_NAME_NOT_RESOLVED":
            "Name not resolved. Please try again with a different URL.",
    }

    """
    Класс для создания скриншотов через selinium
    """

    def __init__(self):
        "Метод инициализции для сохрания драйвера и определения воркеров селери. На данный момент не доступен функционал селери"
        logger.info("Initializing Web Screenshot Maker")
        self.driver = None
        # if not celery.current_app.control.inspect().ping():
        logger.warning("Celery workers is not found. Web Screenshot Maker will work with default synchronously.")
        self.is_celery_running = False

    def get_image(self, url: str) -> Union[ImageFile, str]:
        "Метод для сохранения скриншота в нужном формате (ImageFile) передачи в сериализатор"
        logger.info(f'Screenshot start making')
        response = self._get_screenshot(url)
        if type(response) != bytes:
            return response
        image = ImageFile(io.BytesIO(response))
        logger.info(f'Screenshot is got')
        return image

    def _get_screenshot(self, url: str) -> Union[bytes, str]:
        "Метод для получения скришота или сообщерния ошибки"
        try:
            if self.is_celery_running:
                logger.info("Web Screenshot Maker make screenshot with celery worker.")
                return self._make_screenshot_with_worker.delay(url)
            logger.info("Web Screenshot Maker make screenshot without celery worker.")
            return self._make_screenshot(url)
        except WebDriverException as ex:
            return self._get_webdriver_exception_msg(ex)

    def _make_screenshot(self, url: str) -> bytes: #AsyncResult]:
        "Метод для создания скриншота через selenium"
        logger.info("Getting screenshot from {}".format(url))
        with self.__enter__():
            self.driver.get(url)
            logger.info("Driver get url {}".format(url))
            screenshot = self.driver.get_screenshot_as_png()
            logger.success("Screenshot made at {}".format(url))
            return screenshot

    def _get_webdriver_exception_msg(self, ex: WebDriverException) -> str:
        "Метод для обработки возможных ошибок"
        ex.msg = ex.msg.split('\n')[0]
        logger.warning("Web Screenshot Maker get exception {}".format(ex.msg))
        if "ERR_NAME_NOT_RESOLVED" in ex.msg:
            return "Name not resolved. Please try again with a different name."
        elif "ERR_SSL_VERSION_OR_CIPHER_MISMATCH" in ex.msg:
            return "SSL version mismatch. Please check your URL if 'www' part for correct SSL certificate."
        return f"Something went wrong. Please check your URL and try again: {ex.msg}"

    def __enter__(self):
        "Контектсный менеджер для входа в драйвер"
        logger.info("Entering Web Screenshot Maker")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        logger.info("Web Screenshot Maker get driver {}".format(self.driver))
        logger.info("Web Screenshot Maker get options {}".format(options))
        return self.driver

    def __exit__(self, exc_type, exc_value, traceback):
        "Контекстный менеджер для выхода из драйвера"
        if self.driver:
            self.driver.quit()
        logger.info("Exiting Web Screenshot Maker")

    @staticmethod
    def get_domain(url: str) -> str:
        "Метод для получения домена"
        domain = url.split("https://")[1].split(".")[0]
        logger.info("Domain: {}".format(domain))
        return domain  # TODO: добавить поддержку http

    @staticmethod
    def get_name_for_image(data: dict) -> str:
        "Метод для получения имени скриншота от уже имеющихся данных в модели Screenshot"
        logger.info(f"Get image for {data['url']}")
        domain = screenshot_maker.get_domain(data['url'])
        date_object = datetime.datetime.strptime(data['uploaded_at'], "%Y-%m-%d %H:%M:%S")
        uploaded_at = time.mktime(date_object.timetuple())
        name = f'{uploaded_at}_{data["user"]}_{domain}.png'
        logger.info("Edit image name to '{}'. UNIX time used".format(name))
        return name


    # @staticmethod
    # @shared_task
    # async def _make_screenshot_with_worker(screenshot_url: str) -> bytes:
    #     logger.info(f"Making screenshot {screenshot_url}")
    #     result = WebScreenshotMaker()._make_screenshot(screenshot_url)
    #     while True:
    #         if result.ready():
    #             logger.success("Screenshot made")
    #             return result.get()
    #         elif result.failed():
    #             logger.error(f"Screenshot failed: {result.info}; {result.get()}")
    #             return result.get()

    # @staticmethod
    # @contextmanager
    # def temporary_image(image_bytes: bytes):
    #     ""
    #     temp_image = io.BytesIO(image_bytes)
    #     try:
    #         yield temp_image
    #     finally:
    #         temp_image.close()



screenshot_maker = WebScreenshotMaker()