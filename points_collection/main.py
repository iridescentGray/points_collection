import asyncio
import time

import schedule

from points_collection import auth, message_sender, search_worker
from points_collection.logger import logger
from points_collection.yaml_config import config_manager

is_debug = config_manager.config.get("debug", False)


async def core_job_inner():
    try:
        await message_sender.send_message(
            "points collection start!",
        )
        await auth.ensure_login()
        await search_worker.do_search()
        await message_sender.send_message(
            "search success, see https://rewards.bing.com/redeem/"
        )
    except Exception as e:
        await message_sender.send_message("error happened,please see logs")
        logger.exception(e)


def core_job():
    asyncio.run(core_job_inner())


def main():
    if is_debug:
        core_job()
    else:
        schedule.every().day.at("12:30").do(core_job)
        while True:
            schedule.run_pending()
            time.sleep(1)
