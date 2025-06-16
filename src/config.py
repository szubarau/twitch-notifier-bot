import os
import sys

class Config:
    def __init__(self):
        self.client_id = os.getenv('TWITCH_CLIENT_ID')
        self.client_secret = os.getenv('TWITCH_CLIENT_SECRET')
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_channel = os.getenv('TELEGRAM_CHANNEL_ID')

        missing_vars = []
        if not self.client_id:
            missing_vars.append('TWITCH_CLIENT_ID')
        if not self.client_secret:
            missing_vars.append('TWITCH_CLIENT_SECRET')
        if not self.telegram_token:
            missing_vars.append('TELEGRAM_BOT_TOKEN')
        if not self.telegram_channel:
            missing_vars.append('TELEGRAM_CHANNEL_ID')

        if missing_vars:
            print(f"Error: Missing required environment variables: {', '.join(missing_vars)}", file=sys.stderr)
            sys.exit(1)

    def __repr__(self):
        return (f"Config(client_id={self.client_id}, "
                f"client_secret={'***' if self.client_secret else None}, "
                f"telegram_token={'***' if self.telegram_token else None}, "
                f"telegram_channel={self.telegram_channel})")
