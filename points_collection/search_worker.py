import asyncio
import random
import typing

from playwright.async_api import BrowserContext

import points_collection.get_hot_words as hot_words
import points_collection.playwrights as playwrights
import points_collection.task as search_task
import points_collection.yaml_config as yaml_config
from points_collection import message_sender
from points_collection.logger import logger

is_headless = yaml_config.config_manager.config.get("headless", True)
pc_search_times = yaml_config.config_manager.config.get("pc_search_times", 15)
phone_search_times = yaml_config.config_manager.config.get("phone_search_times", 15)


@playwrights.with_async_context(
    context_file_path="./user_data/state.json", headless=is_headless
)
async def get_current_points(
    browser_context: typing.Optional[BrowserContext] = None,
) -> dict:
    return {}


async def do_search() -> None:
    expolore_words = hot_words.get_explore_words(pc_search_times + phone_search_times)
    logger.info(
        f"do_search,expolore_words:{expolore_words}",
    )

    for i in range(1, phone_search_times):
        try:
            word = expolore_words[i]
            await search_task.phone_search(word)
            await search_wait(i)
        except Exception as e:
            await message_sender.send_message("error happened in do phone search")
            logger.exception(e)

    for i in range(1, pc_search_times):
        try:
            word = expolore_words[i]
            await search_task.pc_search(word)
            await search_wait(i)
        except Exception as e:
            await message_sender.send_message("error happened in do pc search")
            logger.exception(e)


async def search_wait(search_times):
    await asyncio.sleep(random.randint(20, 30))

    # 每5个 随机休眠16分钟-18分钟
    if search_times % 4 == 0:
        await asyncio.sleep(random.randint(60 * 16, 60 * 18))
