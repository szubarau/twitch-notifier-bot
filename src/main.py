import time
from config import Config
from twitch_monitor import TwitchMonitor
from telegram_notifier import TelegramNotifier


def main():
    config = Config()
    monitor = TwitchMonitor()
    notifier = TelegramNotifier(config)
    streamer = "zumich"

    print("Бот запущен. Мониторинг стримов...")
    while True:
        stream_data = monitor.check_stream(streamer)
        if stream_data:
            notifier.send_notification(stream_data)
            time.sleep(3600)  # Не спамить при долгих стримах
        else:
            time.sleep(300)  # Проверка каждые 5 минут


if __name__ == "__main__":
    main()
