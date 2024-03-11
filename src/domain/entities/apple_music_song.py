class AppleMusicSong:
    def __init__(self, song_id: str, url: str, name: str, artist_name: str):
        self.song_id = song_id
        self.url = url
        self.name = name
        self.artist_name = artist_name

    @property
    def search_word(self):
        return f"{self.name} {self.artist_name}"
