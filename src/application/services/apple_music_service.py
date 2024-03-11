from abc import ABC, abstractmethod
from typing import List, Dict
from src.domain.entities.apple_music_song import AppleMusicSong

class AppleMusicPlaylistFetcherServiceInterface(ABC):
    @abstractmethod
    def fetch(self, playlist_url: str) -> List[Dict[str, str]]:
        pass

class AppleMusicService:
    def __init__(self, fetcher: AppleMusicPlaylistFetcherServiceInterface, playlist_url: str):
        self.fetcher = fetcher
        self.playlist_url = playlist_url
        
    def get_playlist(self) -> List[AppleMusicSong]:
        songs = self.fetcher.fetch(self.playlist_url)
        return list(map(self._transform_to_apple_music_song, songs))

    def _transform_to_apple_music_song(self, og_song: dict) -> AppleMusicSong:
        """Transform record of ogSongs into AppleMusicSong object"""
        attributes = og_song["attributes"]
        return AppleMusicSong(og_song["id"], attributes["url"], attributes["name"], attributes["artistName"])