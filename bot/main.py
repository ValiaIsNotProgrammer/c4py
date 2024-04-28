import asyncio

from loguru import logger

from bot.misc import dp, bot
from bot.handlers import commands

dp.include_router(commands.router)
logger.info("Router included")

async def main():
    logger.info("Starting bot")
    await dp.start_polling(bot)

    # if USE_WEBHOOK:
    #     executor.start_webhook(**WEBHOOK_SERVER)
    # else:
    #     executor.start_polling()


if __name__ == '__main__':
    asyncio.run(main())