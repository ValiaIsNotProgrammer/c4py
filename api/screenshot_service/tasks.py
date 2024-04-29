from celery import shared_task
from loguru import logger

# from api.utils.screenshots import screenshot_maker


# @shared_task
# async def make_screenshot(screenshot_url: str) -> bytes:
#     logger.info(f"Making screenshot {screenshot_url}")
#     screenshot = screenshot_maker.make_screenshot(screenshot_url)
#     logger.success("Screenshot made")
#     return screenshot
