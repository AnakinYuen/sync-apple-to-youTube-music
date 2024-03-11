import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from typing import List
from src.domain.entities.song import Song
from src.application.repositories.song_repository import SongRepositoryInterface
from src.application.services import ConfigServiceInterface


DISJUNCTIONS_LIMIT = 30

class SongRepository(SongRepositoryInterface):
    def __init__(self, ConfigService: ConfigServiceInterface):
        firebase_credentials_path = ConfigService.get_firebase_credentials_path()
        cred = credentials.Certificate(firebase_credentials_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        self.songs_collection = db.collection("Songs")

    def get_songs_by_apple_song_id(self, apple_song_ids: List[str]) -> List[Song]:
        ids_chunks = [apple_song_ids[i:i+DISJUNCTIONS_LIMIT] for i in range(0, len(apple_song_ids), DISJUNCTIONS_LIMIT)]
        result = []
        for ids in ids_chunks:
            docs = self.songs_collection.where(filter=FieldFilter("appleSongId", "in", ids)).get()
            for doc in docs:
                song_dict = doc.to_dict()
                result.append(Song(song_dict["name"], song_dict["artistName"], song_dict["url"], song_dict["ytSongId"], song_dict["appleSongId"]))
        return result

    def create_song(self, song: Song):
        # return
        self.songs_collection.document(song.apple_song_id).set(song.to_json())