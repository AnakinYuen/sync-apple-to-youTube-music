from typing import List
from src.domain.entities import AppleMusicSong, Song, YTMusicSong, YTMusicSearchResult
from src.application.services import AppleMusicService, YTMusicService
from src.application.repositories import SongRepositoryInterface


def _diff_updated_songs(
        songs: List[Song],
        apple_music_playlist: List[AppleMusicSong],
        yt_music_playlist: List[YTMusicSong]
) -> tuple[list[YTMusicSearchResult], list[YTMusicSong]]:
    apple_music_song_dict = {
        apple_music_song.song_id: apple_music_song for apple_music_song in apple_music_playlist
    }
    song_by_apple_song_id_dict = {song.apple_song_id: song for song in songs}
    song_by_yt_song_id_dict = {song.yt_song_id: song for song in songs}
    yt_playlist_song_by_apple_id_dict = {
        song_by_yt_song_id_dict[yt_music_song.song_id].apple_song_id:
            song_by_yt_song_id_dict[yt_music_song.song_id]
        for yt_music_song in yt_music_playlist
        if yt_music_song.song_id in song_by_yt_song_id_dict
    }
    added = [
        YTMusicSearchResult(
            song_by_apple_song_id_dict[apple_song_id].name,
            song_by_apple_song_id_dict[apple_song_id].artist_name,
            song_by_apple_song_id_dict[apple_song_id].yt_song_id
        )
        for apple_song_id in apple_music_song_dict
        if apple_song_id in song_by_apple_song_id_dict and
        apple_song_id not in yt_playlist_song_by_apple_id_dict
    ]
    removed = [
        yt_music_song for yt_music_song in yt_music_playlist
        if yt_music_song.song_id not in song_by_yt_song_id_dict
    ]
    return (added, removed)


def _diff_new_apple_music_songs(
        apple_music_playlist: List[AppleMusicSong],
        songs: List[Song]
) -> List[AppleMusicSong]:
    apple_music_song_dict = {
        apple_music_song.song_id: apple_music_song for apple_music_song in apple_music_playlist
    }
    song_dict = {song.apple_song_id: song for song in songs}
    return [
        apple_music_song_dict[apple_song_id]
        for apple_song_id in apple_music_song_dict
        if apple_song_id not in song_dict
    ]

def _log_apple_music_playlist(apple_music_playlist: List[AppleMusicSong]):
    for i, song in enumerate(apple_music_playlist):
        index = "{:03d}".format(i + 1)
        print(f"{index} {song.name} - {song.artist_name}")

def _log_yt_music_playlist(yt_music_playlist: List[YTMusicSong]):
    for i, song in enumerate(yt_music_playlist):
        index = "{:03d}".format(i + 1)
        print(f"{index} {song.name} - {song.artist_name} <{song.song_id}>")

def _log_add_playlist_items(results: List[YTMusicSearchResult]):
    for i, song in enumerate(results):
        index = "{:03d}".format(i + 1)
        print(f"{index} {song.name} - {song.artist_name} ({song.song_id})")

def _log_remove_playlist_items(songs: List[YTMusicSong]):
    for i, song in enumerate(songs):
        index = "{:03d}".format(i + 1)
        print(f"{index} {song.name} - {song.artist_name} ({song.song_id})")

def sync_playlist(
    song_repository: SongRepositoryInterface,
    apple_music_service: AppleMusicService,
    yt_music_service: YTMusicService
):
    # Get songs from Apple Music playlist
    print("\nGetting songs from Apple Music playlist")
    apple_music_playlist = apple_music_service.get_playlist()
    _log_apple_music_playlist(apple_music_playlist)
    # Get song's YouTube videoId from Database
    print("\nGetting YouTube videoId from Database")
    apple_song_ids = [
        apple_music_song.song_id for apple_music_song in apple_music_playlist]
    songs = song_repository.get_songs_by_apple_song_id(apple_song_ids)
    # Fetch YouTube videoId for cache miss songs
    print("\nFetching YouTube videoId for cache miss songs")
    new_apple_music_songs = _diff_new_apple_music_songs(
        apple_music_playlist, songs)
    for apple_music_song in new_apple_music_songs:
        yt_music_search_result = yt_music_service.search_song(
            apple_music_song.search_word)
        if yt_music_search_result is None:
            print(f"{apple_music_song.search_word} not found")
            continue
        song = Song(apple_music_song.name,
                    apple_music_song.artist_name,
                    apple_music_song.url,
                    yt_music_search_result.song_id,
                    apple_music_song.song_id
                    )
        songs.append(song)
        # Save missing songs
        song_repository.create_song(song)
        print(f"\ncreate song: {song.name} <{song.yt_song_id}> ({song.url})")
    # Get songs from YouTube Music playlist
    print("\nGetting songs from YouTube Music playlist")
    yt_music_playlist = yt_music_service.get_playlist()
    _log_yt_music_playlist(yt_music_playlist)
    # Prepare list of YouTube videoId for adding song / remove songs
    new_yt_music_search_results, remove_yt_music_songs = _diff_updated_songs(
        songs, apple_music_playlist, yt_music_playlist)
    # Add songs to YouTube playlist
    print(f"\nAdding {len(new_yt_music_search_results)} songs to YouTube playlist")
    _log_add_playlist_items(new_yt_music_search_results)
    yt_music_service.add_playlist_items(new_yt_music_search_results)
    # Remove songs from YouTube playlist
    print(f"\nRemoving {len(remove_yt_music_songs)} songs from YouTube playlist")
    _log_remove_playlist_items(remove_yt_music_songs)
    yt_music_service.remove_playlist_items(remove_yt_music_songs)
    return
