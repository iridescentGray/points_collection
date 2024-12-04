import asyncio
import random

import httpx

from points_collection import message_sender

poetry_list = [
    "盛年不重来，一日难再晨",
    "千里之行，始于足下",
    "少年易学老难成，一寸光阴不可轻",
    "敏而好学，不耻下问",
    "海内存知已，天涯若比邻",
    "三人行，必有我师焉",
    "莫愁前路无知已，天下谁人不识君",
    "人生贵相知，何用金与钱",
    "天生我材必有用",
    "海纳百川有容乃大；壁立千仞无欲则刚",
    "穷则独善其身，达则兼济天下",
    "读书破万卷，下笔如有神",
    "学而不思则罔，思而不学则殆",
    "一年之计在于春，一日之计在于晨",
    "莫等闲，白了少年头，空悲切",
    "少壮不努力，老大徒伤悲",
    "近朱者赤，近墨者黑",
    "纸上得来终觉浅，绝知此事要躬行",
    "学无止境",
    "天将降大任于斯人也",
    "鞠躬尽瘁，死而后已",
    "书到用时方恨少",
    "天下兴亡，匹夫有责",
    "为中华之崛起而读书",
    "一日无书，百事荒废",
    "岂能尽如人意，但求无愧我心",
    "人生自古谁无死，留取丹心照汗青",
    "吾生也有涯，而知也无涯",
    "生于忧患，死于安乐",
    "读书破万卷，下笔如有神",
    "王侯将相宁有种乎",
]


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
