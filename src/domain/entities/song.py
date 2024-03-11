class Song:
    def __init__(self, name: str, artist_name: str, url: str, yt_song_id: str, apple_song_id: str):
        self.name = name
        self.artist_name = artist_name
        self.url = url
        self.yt_song_id = yt_song_id
        self.apple_song_id = apple_song_id
    
    def to_json(self):
        return {
            "name": self.name,
            "artistName": self.artist_name,
            "url": self.url,
            "ytSongId": self.yt_song_id,
            "appleSongId": self.apple_song_id,
        }
