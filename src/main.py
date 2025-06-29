import logging
import asyncio
from config import Config
from bot.twitch_monitor import TwitchMonitor
from bot.telegram_notifier import TelegramNotifier

async def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
    config = Config()
    monitor = TwitchMonitor(config)
    notifier = TelegramNotifier(config)

    stream = monitor.check_stream_live()
    await notifier.send_status(stream_active=bool(stream))

    if stream:
        await notifier.send_if_new(stream)

if __name__ == "__main__":
    asyncio.run(main())

