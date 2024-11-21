import httpx
import telegram

from points_collection.yaml_config import config_manager

message_channel = config_manager.config.get("message", {}).get("channel")

ntfy_server = config_manager.config.get("message", {}).get("ntfy", {}).get("server")
ntfy_topic = config_manager.config.get("message", {}).get("ntfy", {}).get("topic")
telegram_token = (
    config_manager.config.get("message", {}).get("telegram", {}).get("token")
)
chat_id = config_manager.config.get("message", {}).get("telegram", {}).get("chat_id")


async def send_message(message: str):
    if message_channel == "telegram":
        bot = telegram.Bot(telegram_token)
        await bot.send_message(text=message, chat_id=chat_id)
    elif message_channel == "ntfy":
        response = httpx.post(f"{ntfy_server}{ntfy_topic}", content=message)
        if response.status_code != 200:
            raise RuntimeError("Message sending failed")
