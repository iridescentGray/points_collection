import re
import typing

from playwright.async_api import BrowserContext, expect

from points_collection import message_sender, playwrights, yaml_config
from points_collection.logger import logger
from points_collection.yaml_config import config_manager

microsoft_user = config_manager.config.get("microsoft", {}).get("user", "")
password = config_manager.config.get("microsoft", {}).get("password", "")
is_headless = config_manager.config.get("headless", True)
devices = yaml_config.config_manager.config.get("devices", "Desktop Edge")


async def is_login(browser_context: typing.Optional[BrowserContext] = None) -> bool:
    try:
        page = await browser_context.new_page()

        await page.goto(
            "https://account.microsoft.com/profile/", wait_until="domcontentloaded"
        )
        is_login = "https://account.microsoft.com/profile" in page.url
        await page.close()
        return is_login
    except Exception as e:
        logger.info(e)
        return False


async def login_and_save_status(
    browser_context: typing.Optional[BrowserContext] = None,
):
    try:
        page = await browser_context.new_page()
        await page.goto("https://login.live.com/")
        await page.get_by_test_id("i0116").fill(microsoft_user)
        await page.get_by_test_id("i0116").press("Enter")
        login_method = page.get_by_test_id("credentialPickerLink")
        await expect(login_method).to_be_enabled(timeout=2000)
        await login_method.click()
        await page.get_by_role(
            "button", name=re.compile(r"(使用我的密码|Use\s*my\s*password)")
        ).click()
        await page.get_by_test_id("i0118").click()
        await page.get_by_test_id("i0118").fill(password)
        await page.get_by_test_id("textButtonContainer").get_by_role(
            "button", name=re.compile(r"(登录|Sign\s*in)")
        ).click()
        await page.get_by_label(
            re.compile(r"(保持登录状态?|Stay\s*signed\s*in?)")
        ).click()
        await page.wait_for_url(url="https://account.microsoft.com/**", timeout=30000)
        await browser_context.storage_state(path="./user_data/state.json")
        return True
    except Exception as e:
        await message_sender.send_message("login error!")
        logger.exception(e)
        return False


@playwrights.with_async_context(
    context_file_path="./user_data/state.json",
    headless=is_headless,
    target_devices=devices,
)
async def ensure_login(browser_context: typing.Optional[BrowserContext] = None) -> bool:
    if is_headless == True:
        # TODO 无头模式暂时无法登录,未解决
        return False

    logger.info("ensure_login execute")
    is_login_bool = await is_login(browser_context)
    if is_login_bool:
        return True
    logger.info(f"is_login: {is_login_bool}")
    if not is_login_bool:
        login_result = await login_and_save_status(browser_context)
        logger.info(f"login success: {login_result}")
        return login_result
