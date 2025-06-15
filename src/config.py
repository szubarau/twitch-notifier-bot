import os

class Config:
    @staticmethod
    def get_env(var_name: str) -> str:
        value = os.getenv(var_name)
        if not value:
            raise ValueError(f"Missing environment variable: {var_name}")
        return value

    TWITCH_CLIENT_ID = get_env('TWITCH_CLIENT_ID')
    TWITCH_CLIENT_SECRET = get_env('TWITCH_CLIENT_SECRET')
    TELEGRAM_TOKEN = get_env('TELEGRAM_BOT_TOKEN')
    CHANNEL_ID = get_env('TELEGRAM_CHANNEL_ID')