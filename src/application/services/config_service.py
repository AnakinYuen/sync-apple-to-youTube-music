from abc import ABC, abstractmethod

class ConfigServiceInterface(ABC):
    @staticmethod
    @abstractmethod
    def get_firebase_credentials_path() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_youtube_credentials_path() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_apple_music_playlist_url() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_yt_music_playlist_id() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_yt_music_language() -> str:
        pass
