class YTMusicSong:
    def __init__(self, name: str, artist_name: str, song_id: str, set_video_id: str):
        self.name = name
        self.artist_name = artist_name
        self.song_id = song_id
        self._set_video_id = set_video_id

    def to_dict(self):
        return {
            "videoId": self.song_id,
            "setVideoId": self._set_video_id,
        }
