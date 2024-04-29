from time import time
from typing import Union
from urllib.parse import urlparse

from aiogram.client.session import aiohttp
from aiogram.types import BufferedInputFile
from loguru import logger

from bot.model import Screenshot


def timer(func):
    async def wrapper(*args, **kwargs) -> Union[Screenshot, tuple[Screenshot, time]]:
        start_time = time()
        result = await func(*args, **kwargs)
        end_time = round(time() - start_time, 2)
        logger.info(f"[{func.__name__}] {end_time} seconds")
        if kwargs.get("get_time", None):
            return result, end_time
        return result

    return wrapper


def get_language_from(button_name: str) -> str:
    return button_name[:2]


async def download_file(url: str):
    if "127.0.0.1" in url:
        url = url.replace("http://127.0.0.1:8000", "/home/valiaisnotprogrammer/PycharmProjects/truepositive_test_task/api")
        return open(url[:-1], "rb").read()
        # return FSInputFile(path=url[:-1])
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                file_contents = await response.read()
                print("Файл успешно скачан")
                return file_contents
            else:
                print(f"Не удалось скачать файл. Код состояния: {response.status}")
                return None


async def get_png_from(screenshot: Screenshot) -> BufferedInputFile:
    logger.info("Getting PNG from screenshot {}".format(screenshot))
    screenshot_bytes = await download_file(screenshot.image)
    png = BufferedInputFile(screenshot_bytes, filename=f"{screenshot.image}.png")
    logger.success("PNG screenshot was get successfully")
    return png


def get_valid_url(raw_url: str) -> str:
    logger.info("Getting raw url {}".format(raw_url))
    url = to_correct(raw_url)
    logger.info("Returning url {}".format(url))
    return url


def to_correct(url: str) -> str:
    if is_valid(url):
        return url
    url = "https://" + url
    if "www." in url:
        url = url.replace("www.", "")
    return url


def is_valid(url: str) -> bool:
        if "https://" in url or "http://" in url:
            return True
        return False


# urls = [
#     "http://www.example.com",
#     "https://example.com",
#     "http://subdomain.example.com/page",
#     "https://www.example.com/path/to/page.html",
#     "http://example.com:8080"
#     "www.example.com",
#     "example.com",
#     "ftp://example.com",
#     "http://example",
#     "http://example..com",
#     "http://.example.com",
#     "http://example..com/page",
#     "http://example.com:8080/path/to/page.html"
# ]



