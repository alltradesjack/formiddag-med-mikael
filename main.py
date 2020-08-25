import spotipy
from spotipy.oauth2 import SpotifyOAuth
from scrape import get_episode_playlist, get_newest_episode
from spotipy_utils import get_track_ids, create_playlist_name, get_existing_playlists
import os


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public",
                     client_id=str(os.environ.get('CLIENT_ID')),
                     client_secret=str(os.environ.get('CLIENT_SECRET')),
                     redirect_uri=str(os.environ.get('REDIRECT_URI')),
                     username=str(os.environ.get('SPOTIFY_USER'))))

episode_link = get_newest_episode()
artists, tracks = get_episode_playlist(episode_link)
track_ids = get_track_ids(sp, artists, tracks)
playlist_name = create_playlist_name(episode_link)
playlist_date = playlist_name[-10:]
description = f'Tracks played by Mikael Simpson on DR P6 Beat\'s "Formiddag med Simpson" on {playlist_date}.'

if playlist_name not in get_existing_playlists(sp, user, limit=50):
    playlist = sp.user_playlist_create(user, playlist_name, public=True, description=description)
    sp.user_playlist_add_tracks(user, playlist['uri'], track_ids)
    print(f'Added most recent playlist! ({playlist_date})')

else:
    print('Playlist already exists!')
