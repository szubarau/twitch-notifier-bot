import os
import logging
import random
from telegram import Bot
from telegram.constants import ParseMode

class TelegramNotifier:
    def __init__(self, config):
        self.config = config
        self.bot = Bot(token=self.config.telegram_token)
        self.id_file = "last_stream_id.txt"

    def send_if_new(self, stream_data):
        stream_id = str(stream_data.get("id"))
        if stream_id == self._get_last_sent_id():
            logging.info("🔁 Стрим уже анонсирован ранее.")
            return

        message = self._format_message(stream_data)
        self.bot.send_message(
            chat_id=self.config.telegram_channel,
            text=message,
            parse_mode=ParseMode.HTML
        )
        logging.info("✅ Сообщение отправлено в Telegram.")
        self._save_last_sent_id(stream_id)

    def _get_last_sent_id(self):
        if os.path.exists(self.id_file):
            with open(self.id_file) as f:
                return f.read().strip()
        return None

    def _save_last_sent_id(self, stream_id):
        with open(self.id_file, "w") as f:
            f.write(stream_id)

    @staticmethod
    def _format_message(data: dict) -> str:
        templates = [
            (
                "🎉 <b>Прямо сейчас стартует стрим!</b>\n\n"
                f"📺 <b>{data.get('title', 'Без названия')}</b>\n"
                f"🎮 Игра: <b>{data.get('game_name', 'Не указана')}</b>\n"
                f"🔗 Смотри тут: https://twitch.tv/zumich"
            ),
            (
                "🚨 <b>Zumich вышел в эфир!</b>\n\n"
                f"🔴 Название: <b>{data.get('title', 'Без названия')}</b>\n"
                f"🕹 Сейчас играет: <b>{data.get('game_name', 'Не указана')}</b>\n"
                f"➡️ Подключайся: https://twitch.tv/zumich"
            ),
            (
                "🔥 <b>Новый стрим уже начался!</b>\n\n"
                f"📢 <b>{data.get('title', 'Без названия')}</b>\n"
                f"🎲 Игра в эфире: <b>{data.get('game_name', 'Не указана')}</b>\n"
                f"👀 Смотри: https://twitch.tv/zumich"
            ),
            (
                "📡 <b>Внимание! Прямой эфир на канале Zumich!</b>\n\n"
                f"🎥 Стрим: <b>{data.get('title', 'Без названия')}</b>\n"
                f"🎮 Играет в: <b>{data.get('game_name', 'Не указана')}</b>\n"
                f"▶️ Летс гоу: https://twitch.tv/zumich"
            ),
        ]
        return random.choice(templates)

