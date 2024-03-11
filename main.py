from src.application.use_cases import sync_playlist
from src.application.services import AppleMusicService, YTMusicService
from src.infrastructure.external_services import AppleMusicPlaylistFetcherService, ConfigService
from src.infrastructure.repositories import SongRepository

if __name__ == "__main__":
    config_service = ConfigService()

    song_repository = SongRepository(config_service)

    apple_music_playlist_fetcher_service = AppleMusicPlaylistFetcherService()
    apple_music_service = AppleMusicService(
        apple_music_playlist_fetcher_service,
        config_service.get_apple_music_playlist_url()
    )

    yt_music_service = YTMusicService(config_service)

    sync_playlist(song_repository, apple_music_service, yt_music_service)
