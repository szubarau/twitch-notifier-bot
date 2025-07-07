import os
import sys
import logging
import random
from typing import Optional
from telegram import Bot
from telegram.constants import ParseMode

CACHE_DIR = "stream_cache"
ID_PATH = os.path.join(CACHE_DIR, "last_stream_id.txt")


class TelegramNotifier:
    def __init__(self, config):
        self.config = config
        self.bot = Bot(token=self.config.telegram_token)
        os.makedirs(CACHE_DIR, exist_ok=True)

    async def send_if_new(self, stream_data: dict):
        stream_id = str(stream_data.get("id"))
        last_id = self._get_last_sent_id()

        if last_id == stream_id:
            logging.info("🛑 Стрим уже анонсирован. Завершаем пайплайн.")
            sys.exit(0)

        await self._send_announcement(stream_data)
        self._save_last_sent_id(stream_id)

    async def _send_announcement(self, data: dict):
        title = data.get("title", "Без названия")
        game = data.get("game_name", "Не указана")
        thumbnail_url = data.get("thumbnail_url", "").replace("{width}", "640").replace("{height}", "360")

        caption = random.choice([
            f"🎬 <b>Стрим начался!</b>\n\n📺 <b>{title}</b>\n🎮 Игра: <b>{game}</b>\n▶️ <a href='https://twitch.tv/zumich'>Смотреть</a>",
            f"🔥 <b>Zumich в эфире!</b>\n\n🕹 <b>{game}</b>\n🗣 <b>{title}</b>\n🔴 <a href='https://twitch.tv/zumich'>Присоединяйся</a>",
            f"🚀 <b>Прямой эфир!</b>\n\n🎮 <b>{game}</b>\n🎙 <b>{title}</b>\n▶️ <a href='https://twitch.tv/zumich'>Twitch канал</a>",
        ])

        try:
            await self.bot.send_photo(
                chat_id=self.config.telegram_channel,
                photo=thumbnail_url,
                caption=caption,
                parse_mode=ParseMode.HTML
            )
            logging.info("✅ Анонс отправлен.")
        except Exception as e:
            logging.error(f"❌ Ошибка при отправке Telegram-сообщения: {e}")

    def _get_last_sent_id(self) -> Optional[str]:
        if os.path.exists(ID_PATH):
            try:
                with open(ID_PATH, "r") as f:
                    return f.read().strip()
            except Exception as e:
                logging.warning(f"⚠️ Не удалось прочитать ID: {e}")
        return None

    def _save_last_sent_id(self, stream_id: str):
        try:
            with open(ID_PATH, "w") as f:
                f.write(stream_id)
            logging.info("💾 ID стрима сохранён.")
        except Exception as e:
            logging.error(f"❌ Ошибка при сохранении ID: {e}")



