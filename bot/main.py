import asyncio
import sys

from loguru import logger

from bot.misc import bot


async def main():
    logger.info("Router included")
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    await bot.start()

    # if USE_WEBHOOK:
    #     executor.start_webhook(**WEBHOOK_SERVER)
    # else:
    #     executor.start_polling()


if __name__ == '__main__':
    asyncio.run(main())