import os
import sys

class Config:
    def __init__(self):
        self.client_id = os.getenv("TWITCH_CLIENT_ID")
        self.client_secret = os.getenv("TWITCH_CLIENT_SECRET")
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_channel = os.getenv("TELEGRAM_CHANNEL_ID")

        missing = []
        if not self.client_id: missing.append("TWITCH_CLIENT_ID")
        if not self.client_secret: missing.append("TWITCH_CLIENT_SECRET")
        if not self.telegram_token: missing.append("TELEGRAM_BOT_TOKEN")
        if not self.telegram_channel: missing.append("TELEGRAM_CHANNEL_ID")

        if missing:
            print(f"Error: Missing required environment variables: {', '.join(missing)}", file=sys.stderr)
            sys.exit(1)
