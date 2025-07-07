import logging
import asyncio
import sys
from config import Config
from bot.twitch_monitor import TwitchMonitor
from bot.telegram_notifier import TelegramNotifier

async def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
    config = Config()
    monitor = TwitchMonitor(config)
    notifier = TelegramNotifier(config)

    stream = monitor.check_stream_live()
    if stream:
        await notifier.send_if_new(stream)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except SystemExit as e:
        sys.exit(e.code)
