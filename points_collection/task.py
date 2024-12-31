import asyncio
import random
import string
import typing

from playwright.async_api import BrowserContext

import points_collection.playwrights as playwrights
import points_collection.yaml_config as yaml_config
from points_collection.logger import logger

execution_interval = yaml_config.config_manager.config.get("execution_interval", 2000)
is_headless = yaml_config.config_manager.config.get("headless", True)
# see https://github.com/microsoft/playwright/blob/main/packages/playwright-core/src/server/deviceDescriptorsSource.json
pc_devices = yaml_config.config_manager.config.get("pc_devices", "Desktop Chrome")
phone_devices = yaml_config.config_manager.config.get("phone_devices", "iPhone 15")


@playwrights.with_async_context(
    context_file_path="./user_data/state.json",
    headless=is_headless,
    slow_mo=execution_interval,
    target_devices=pc_devices,
)
async def pc_search(
    search_word: str,
    *,
    browser_context: typing.Optional[BrowserContext] = None,
) -> None:
    logger.info(f"start to pc search:{search_word}")
    await _execute_search(search_word, browser_context)
    logger.info(f"end pc search:{search_word}")


@playwrights.with_async_context(
    context_file_path="./user_data/state.json",
    headless=is_headless,
    slow_mo=execution_interval,
    target_devices=phone_devices,
)
async def phone_search(
    search_word: str,
    *,
    browser_context: typing.Optional[BrowserContext] = None,
) -> None:
    logger.info(f"start to phone search:{search_word}")
    await _execute_search(search_word, browser_context)
    logger.info(f"end phone search:{search_word}")


async def _execute_search(
    search_word: str,
    browser_context: typing.Optional[BrowserContext] = None,
):
    page = await browser_context.new_page()  # type: ignore
    await page.goto(
        f"https://www.bing.com/search?q={search_word}&form={generate_random_string(4)}&cvid={generate_random_string(32)}"
    )
    await asyncio.sleep(2)
    await page.reload()
    await smooth_scroll_to_bottom(page)
    await asyncio.sleep(2)


def generate_random_string(length):
    # 定义字符集：包含大写字母、小写字母和数字
    characters = string.ascii_letters + string.digits
    # 随机选择字符并组成字符串
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


async def smooth_scroll_to_bottom(page):
    """
    平滑滚动到页面底部
    """
    scroll_script = """
    const scroll = async () => {
        document.documentElement.scrollIntoView({ behavior: 'smooth', block: 'end' });
    };
    scroll();
    """
    await page.evaluate(scroll_script)
