import os
import sys
import logging
import random
from typing import Optional
from telegram import Bot
from telegram.constants import ParseMode


class TelegramNotifier:
    def __init__(self, config):
        self.config = config
        self.bot = Bot(token=self.config.telegram_token)

        # Пусть до артефакта или файл, который будет сохраняться между запусками
        self.id_file = os.path.join(os.getcwd(), "last_stream_id.txt")

    async def send_if_new(self, stream_data: dict):
        stream_id = str(stream_data.get("id"))
        if self._get_last_sent_id() == stream_id:
            logging.info("🛑 Стрим уже был анонсирован. Прерываем пайплайн.")
            sys.exit(0)  # Успешный выход, останавливаем Pipeline

        await self.send_announcement_with_image(stream_data)
        self._save_last_sent_id(stream_id)

    async def send_announcement_with_image(self, data: dict):
        title = data.get("title", "Без названия")
        game = data.get("game_name", "Не указана")
        thumbnail_url = data.get("thumbnail_url", "").replace("{width}", "640").replace("{height}", "360")

        captions = [
            f"🎬 <b>Стрим начался!</b>\n\n📺 <b>{title}</b>\n🎮 Игра: <b>{game}</b>\n<a href='https://twitch.tv/zumich'>▶️ Смотреть</a>",
            f"🔥 <b>Zumich в эфире!</b>\n\n🎮 <b>{game}</b>\n🗣 <b>{title}</b>\n<a href='https://twitch.tv/zumich'>🔴 Присоединяйся</a>",
            f"🚨 <b>Прямой эфир!</b>\n\n🎲 <b>{game}</b>\n🎙 <b>{title}</b>\n▶️ <a href='https://twitch.tv/zumich'>Смотри на Twitch</a>",
        ]
        caption = random.choice(captions)

        try:
            await self.bot.send_photo(
                chat_id=self.config.telegram_channel,
                photo=thumbnail_url,
                caption=caption,
                parse_mode=ParseMode.HTML
            )
            logging.info("✅ Анонс с превью отправлен.")
        except Exception as e:
            logging.error(f"❌ Ошибка при отправке фото: {e}")

    def _get_last_sent_id(self) -> Optional[str]:
        if os.path.exists(self.id_file):
            with open(self.id_file, "r") as f:
                return f.read().strip()
        return None

    def _save_last_sent_id(self, stream_id: str):
        try:
            with open(self.id_file, "w") as f:
                f.write(stream_id)
        except Exception as e:
            logging.error(f"❌ Не удалось сохранить ID стрима: {e}")


