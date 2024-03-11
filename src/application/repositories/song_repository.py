from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.song import Song

class SongRepositoryInterface(ABC):
    @abstractmethod
    def get_songs_by_apple_song_id(self, apple_song_ids: List[str]) -> List[Song]:
        pass

    @abstractmethod
    def create_song(self, song: Song) -> Song:
        pass
