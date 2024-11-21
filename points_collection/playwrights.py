import functools
import os
import typing
from contextlib import asynccontextmanager, contextmanager

from playwright.async_api import BrowserContext as AsyncBrowserContext
from playwright.async_api import async_playwright
from playwright.sync_api import BrowserContext as SyncBrowserContext
from playwright.sync_api import sync_playwright


def with_async_context(
    func: typing.Optional[typing.Callable] = None,
    *,
    headless: bool = True,
    load_file_first: bool = True,
    context_file_path: str = "./state.json",
    local: str = "zh-ZH",
    timezone: str = "Asia/Shanghai",
    slow_mo: typing.Optional[float] = None,
    target_devices: typing.Optional[str] = None
) -> typing.Callable:
    @asynccontextmanager
    async def create_playwright_context(
        *, load_file_first: bool, context_file_path: str
    ) -> typing.AsyncGenerator:
        async with async_playwright() as playwright:
            chromium = playwright.chromium
            browser = await chromium.launch(headless=headless, slow_mo=slow_mo)
            devices = playwright.devices[target_devices] if target_devices else {}
            if not load_file_first:
                context = await browser.new_context(
                    **devices,
                    locale=local,
                    timezone_id=timezone,
                )
            else:
                if not (context_file_path and os.path.exists(context_file_path)):
                    context = await browser.new_context(
                        **devices,
                        locale=local,
                        timezone_id=timezone,
                    )
                else:
                    context = await browser.new_context(
                        **devices,
                        storage_state=context_file_path,
                        locale=local,
                        timezone_id=timezone,
                    )
            try:
                yield context
            finally:
                await context.close()
                await browser.close()

    async def is_context_already_exit(*args, **kwargs) -> bool:
        if kwargs.get("browser_context", None):
            return True
        for arg in args:
            if isinstance(arg, AsyncBrowserContext):
                return True
        return False

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if await is_context_already_exit(*args, **kwargs):
                return await func(*args, **kwargs)
            else:
                async with create_playwright_context(
                    load_file_first=load_file_first, context_file_path=context_file_path
                ) as browser_context:
                    kwargs["browser_context"] = browser_context
                    return await func(*args, **kwargs)

        return wrapper

    return decorator


def with_sync_context(
    func: typing.Optional[typing.Callable] = None,
    *,
    headless: bool = True,
    load_file_first: bool = True,
    context_file_path: str = "./state.json"
) -> typing.Callable:
    @contextmanager
    def create_playwright_context(
        *, load_file_first: bool, context_file_path: str
    ) -> typing.Generator:
        with sync_playwright() as playwright:
            chromium = playwright.chromium
            browser = chromium.launch(headless=headless)
            if not load_file_first:
                context = browser.new_context()
            else:
                if not (context_file_path and os.path.exists(context_file_path)):
                    context = browser.new_context()
                else:
                    context = browser.new_context(storage_state=context_file_path)
            try:
                yield context
            finally:
                context.close()
                browser.close()

    def is_context_already_exit(*args, **kwargs) -> bool:
        if kwargs.get("browser_context", None):
            return True
        for arg in args:
            if isinstance(arg, SyncBrowserContext):
                return True
        return False

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if is_context_already_exit(*args, **kwargs):
                return func(*args, **kwargs)
            else:
                with create_playwright_context(
                    load_file_first=load_file_first, context_file_path=context_file_path
                ) as browser_context:
                    kwargs["browser_context"] = browser_context
                    return func(*args, **kwargs)

        return wrapper

    return decorator
