from scrape import get_episode_playlist, get_newest_episode
from spotipy_utils import get_track_ids, create_playlist_name, get_existing_playlists
import os
import configparser
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

if os.name == 'nt':
    config = configparser.ConfigParser()
    config.read('config.cfg')
    client_id = config.get('SPOTIFY', 'CLIENT_ID')
    client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')
    redirect_uri = config.get('SPOTIFY', 'REDIRECT_URI')
else:
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    redirect_uri = 'https://formiddag-med-mikael.herokuapp.com:8080'

user = 'chrcarsten'
scope = "playlist-modify-public"

token = util.prompt_for_user_token(
        username=user,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri)

sp = spotipy.Spotify(auth=token)


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
