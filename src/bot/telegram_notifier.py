from telegram import Bot
from telegram.ext import Updater
from telegram.constants import ParseMode
from config import Config

class TelegramNotifier:
    def __init__(self):
        self.bot = Bot(token=Config.TELEGRAM_TOKEN)
        self.updater = Updater(token=Config.TELEGRAM_TOKEN, use_context=True)

    def send_notification(self, stream_data: dict):
        message = self._format_message(stream_data)
        self.bot.send_message(
            chat_id=Config.CHANNEL_ID,
            text=message,
            parse_mode=ParseMode.HTML
        )

    @staticmethod
    def _format_message(data: dict) -> str:
        return (
            "🎥 <b>Новый стрим начался!</b>\n\n"
            f"📺 <b>{data.get('title', 'Без названия')}</b>\n"
            f"🕹 Игра: <b>{data.get('game_name', 'Не указана')}</b>\n"
            f"🔗 Смотреть: https://twitch.tv/zumich"
        )