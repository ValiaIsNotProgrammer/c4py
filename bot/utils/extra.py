from time import time
from typing import Union

from aiogram.client.session import aiohttp
from aiogram.types import BufferedInputFile
from loguru import logger

from model import Screenshot


def get_language_from(button_name: str) -> str:
    "Метод для получения языка из названия кнопки"
    return button_name[:2]


async def download_file(url: str):
    "Метод для загрузки скриншота по указаному url"
    logger.info(f"Downloading {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                file_contents = await response.read()
                logger.success(f"Downloaded {url}")
                return file_contents
            else:
                logger.error(f"Failed to download {url}. Code: {response.status}. Error: {response.text}")
                return None


async def get_png_from(screenshot: Screenshot) -> BufferedInputFile:
    "Метод для получения нужного формата png для API TELEGRAM из Screenshot.image"
    logger.info("Getting PNG from screenshot {}".format(screenshot))
    screenshot_bytes = await download_file(screenshot.image)
    png = BufferedInputFile(screenshot_bytes, filename=f"{screenshot.image}.png")
    logger.success("PNG screenshot was get successfully")
    return png


def get_valid_url(raw_url: str) -> str:
    "Метод для получения валидного URL, полученным пользователем"
    logger.info("Getting raw url {}".format(raw_url))
    url = to_correct(raw_url)
    logger.info("Returning url {}".format(url))
    return url


def to_correct(url: str) -> str:
    "Метод для корректировки URL, полученным пользователем"
    if is_valid(url):
        return url
    url = "https://" + url
    if "www." in url:
        url = url.replace("www.", "")
    return url


def is_valid(url: str) -> bool:
    "Метод для валидации корректности url, полученным пользователем"
    if "https://" in url or "http://" in url:
        return True
    return False




