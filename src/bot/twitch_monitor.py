import requests
import time
from typing import Optional, Dict
from src.config import Config


class TwitchMonitor:
    def __init__(self):
        self._token_expires = 0
        self._access_token = None

    def _get_auth_token(self) -> str:
        """Получает OAuth-токен Twitch с кэшированием"""
        if time.time() < self._token_expires:
            return self._access_token

        auth_url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": Config.TWITCH_CLIENT_ID,
            "client_secret": Config.TWITCH_CLIENT_SECRET,
            "grant_type": "client_credentials"
        }
        response = requests.post(auth_url, params=params)
        data = response.json()

        self._access_token = data["access_token"]
        self._token_expires = time.time() + data["expires_in"] - 300  # Запас 5 минут
        return self._access_token

    def check_stream(self, streamer: str) -> Optional[Dict]:
        """Проверяет статус стрима"""
        headers = {
            "Client-ID": Config.TWITCH_CLIENT_ID,
            "Authorization": f"Bearer {self._get_auth_token()}"
        }
        response = requests.get(
            f"https://api.twitch.tv/helix/streams?user_login={streamer}",
            headers=headers,
            timeout=10
        )
        return response.json().get("data", [{}])[0] if response.json().get("data") else None