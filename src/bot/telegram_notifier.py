import os
import logging
import random
from datetime import datetime
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

class TelegramNotifier:
    def __init__(self, config):
        self.config = config
        self.bot = Bot(token=self.config.telegram_token)
        self.id_file = "last_stream_id.txt"

    async def send_if_new(self, stream_data):
        stream_id = str(stream_data.get("id"))
        if stream_id == self._get_last_sent_id():
            logging.info("🔁 Стрим уже анонсирован.")
            return

        await self.send_announcement_with_image(stream_data)
        self._save_last_sent_id(stream_id)

    async def send_status(self, stream_active: bool):
        status = "в эфире 🎬" if stream_active else "не в эфире 📴"
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        message = f"🛠 Бот запущен в {timestamp}\nСтатус стрима: {status}"
        await self._send_text(message)

    async def send_announcement_with_image(self, data: dict):
        title = data.get("title", "Без названия")
        game = data.get("game_name", "Не указана")
        thumb = data.get("thumbnail_url", "").replace("{width}", "640").replace("{height}", "360")

        caption_templates = [
            f"🎬 <b>Стрим начался!</b>\n\n📺 <b>{title}</b>\n🎮 Игра: <b>{game}</b>\n<a href='https://twitch.tv/zumich'>▶️ Смотреть стрим</a>",
            f"🔥 <b>Zumich в эфире!</b>\n\n🔴 <b>{title}</b>\n🎲 Играет в: <b>{game}</b>\n👉 <a href='https://twitch.tv/zumich'>Включайся!</a>",
            f"🚀 Прямой эфир уже идёт!\n\n🎮 <b>{game}</b>\n📢 Тема: <b>{title}</b>\n🎥 <a href='https://twitch.tv/zumich'>Смотреть</a>",
        ]

        caption = random.choice(caption_templates)

        try:
            await self.bot.send_photo(
                chat_id=self.config.telegram_channel,
                photo=thumb,
                caption=caption,
                parse_mode=ParseMode.HTML
            )
            logging.info("✅ Анонс с обложкой отправлен.")
        except Exception as e:
            logging.error(f"❌ Ошибка при отправке фото: {e}")

    async def _send_text(self, message: str):
        try:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔴 Смотреть стрим", url="https://twitch.tv/zumich")]
            ])
            await self.bot.send_message(
                chat_id=self.config.telegram_channel,
                text=message,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard
            )
            logging.info("✅ Техническое сообщение отправлено.")
        except Exception as e:
            logging.error(f"❌ Ошибка при отправке текста: {e}")

    def _get_last_sent_id(self):
        if os.path.exists(self.id_file):
            with open(self.id_file) as f:
                return f.read().strip()
        return None

    def _save_last_sent_id(self, stream_id):
        with open(self.id_file, "w") as f:
            f.write(stream_id)


