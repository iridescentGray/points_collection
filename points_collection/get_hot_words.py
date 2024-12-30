import asyncio
import random

import httpx

from points_collection import message_sender

def get_search_word_from_remote(key_word) -> list[str]:
    """获取

    Returns:
        tuple[int, list[str]]: _description_
    """

    explore_words = []
    response = httpx.get(f"https://api.gumengya.com/Api/{key_word}").json()
    if response.get("code") == 200:
        for item in response.get("data", {}):
            explore_words.append(item["title"])
    else:
        asyncio.run_coroutine_threadsafe(
            message_sender.send_message(
                f"get explore words from remote error: {response}"
            ),
            asyncio.get_running_loop(),
        )
        raise RuntimeError("get explore words from remote error")
    return explore_words


def get_explore_words(need_words: int) -> list[str]:
    explore_words = []
    key_words_sources = ["BaiduHot", "TouTiaoHot", "DouYinHot", "WeiBoHot"]
    for _ in range(5):
        random_word = random.choice(key_words_sources)
        remote_words = get_search_word_from_remote(random_word)
        explore_words.extend(remote_words)
        key_words_sources.remove(random_word)

        if need_words < len(explore_words):
            break

    random.shuffle(explore_words)
    return explore_words
