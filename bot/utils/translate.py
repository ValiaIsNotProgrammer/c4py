import json

from loguru import logger


def get_answer(lang, answer):
    "Функция для получения нужного ответа из answers.json в зависимости от языка и ответа"
    with open('utils/answers.json', 'r') as file:
        logger.trace(f"Reading answers from {lang}: {answer}")
        data = json.load(file)

    return data[lang][answer]