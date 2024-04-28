from typing import Union

from aiogram.client.session import aiohttp
from aiogram.types import FSInputFile


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



