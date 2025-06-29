import logging
from config import Config
from bot.twitch_monitor import TwitchMonitor
from bot.telegram_notifier import TelegramNotifier

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
    config = Config()
    monitor = TwitchMonitor(config)
    notifier = TelegramNotifier(config)

    stream = monitor.check_stream_live()
    if stream:
        notifier.send_if_new(stream)
    else:
        logging.info("👀 Нечего отправлять.")

if __name__ == "__main__":
    main()

