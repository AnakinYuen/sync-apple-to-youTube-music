import os
import shutil
from typing import List
from ytmusicapi import YTMusic as YT
from src.domain.entities import YTMusicSong, YTMusicSearchResult
from src.application.services.config_service import ConfigServiceInterface

JPOP_NOW_PLAYLIST_ID = 'PL98CgvQL1x4Nh92E8oMisnSXLtge_oyy2'
LANGUAGE = 'ja'

class YTMusicService:
    def __init__(self, ConfigService: ConfigServiceInterface):
        youtube_credentials_path = ConfigService.get_youtube_credentials_path()
        language = ConfigService.get_yt_music_language()
        playlist_id = ConfigService.get_yt_music_playlist_id()
        credentials_path = self._clone_credential(youtube_credentials_path)
        self.yt = YT(auth=credentials_path, language=language)
        self.playlist_id = playlist_id
        
    def search_song(self, keyword: str) -> YTMusicSearchResult | None:
        search_results = self.yt.search(keyword)
        result = next((item for item in search_results if item["resultType"] == "song" and keyword.startswith(item["title"])), None)
        if result is None:
            return None
        return YTMusicSearchResult(result["title"], self._get_first_artist_name(result["artists"]), result["videoId"])

    def get_playlist(self) -> List[YTMusicSong]:
        playlist = self.yt.get_playlist(self.playlist_id)
        return [YTMusicSong(track["title"], self._get_first_artist_name(track["artists"]), track["videoId"], track["setVideoId"]) for track in playlist["tracks"]]

    def add_playlist_items(self, results: List[YTMusicSearchResult]):
        if len(results) > 0:
            self.yt.add_playlist_items(self.playlist_id, [result.song_id for result in results])
    
    def remove_playlist_items(self, songs: List[YTMusicSong]):
        if len(songs) > 0:
            self.yt.remove_playlist_items(self.playlist_id, [song.to_dict() for song in songs])

    def _get_first_artist_name(self, artists: List) -> str:
        if len(artists) == 0:
            return ""
        return artists[0]["name"]
    
    def _clone_credential(self, source_file: str) -> str:
        filename = os.path.basename(source_file)
        destination_file = f"/tmp/{filename}"
        shutil.copyfile(source_file, destination_file)
        return destination_file
