import os
from dotenv import load_dotenv
from src.application.services import ConfigServiceInterface

load_dotenv()

def _get_env(key: str):
    value = os.getenv(key)

    if not value:
        raise ValueError(f"{key} environment variable is not set.")

    return value

class ConfigService(ConfigServiceInterface):
    @staticmethod
    def get_firebase_credentials_path() -> str:
        return _get_env("FIREBASE_CREDENTIALS_PATH")
    
    @staticmethod
    def get_youtube_credentials_path() -> str:
        return _get_env("YOUTUBE_CREDENTIALS_PATH")
    
    @staticmethod
    def get_apple_music_playlist_url() -> str:
        return _get_env("APPLE_MUSIC_PLAYLIST_URL")
    
    @staticmethod
    def get_yt_music_playlist_id() -> str:
        return _get_env("YT_MUSIC_PLAYLIST_ID")

    @staticmethod
    def get_yt_music_language() -> str:
        return _get_env("YT_MUSIC_LANGUAGE")