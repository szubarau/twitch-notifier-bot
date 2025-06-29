import requests
import logging
import time

class TwitchMonitor:
    def __init__(self, config):
        self.config = config
        self.token = None
        self.expiration = 0

    def _get_app_access_token(self):
        if self.token and time.time() < self.expiration:
            logging.debug("📦 Используем кэшированный Twitch токен.")
            return self.token

        logging.info("🔑 Запрашиваем новый Twitch token...")
        url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "grant_type": "client_credentials"
        }
        resp = requests.post(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        self.token = data["access_token"]
        self.expiration = time.time() + data.get("expires_in", 3600) - 60
        return self.token

    def check_stream_live(self):
        token = self._get_app_access_token()
        headers = {
            "Client-ID": self.config.client_id,
            "Authorization": f"Bearer {token}"
        }
        params = { "user_login": "zumich" }
        url = "https://api.twitch.tv/helix/streams"
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        if data:
            logging.info("🎬 Стрим в эфире!")
            return data[0]
        logging.info("📴 Стрим не идёт.")
        return None
