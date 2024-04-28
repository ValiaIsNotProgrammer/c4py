import json

from loguru import logger


# class Translator:
#
#      @classmethod
#      def get_answers(lang, answer):
#          with open('answers.json', 'r') as file:
#              data = json.load(file)
#
#          return data[lang][answer]

def get_answers(lang, answer):
    with open('utils/answers.json', 'r') as file:
        logger.trace(f"Reading answers from {lang}: {answer}")
        data = json.load(file)

    return data[lang][answer]