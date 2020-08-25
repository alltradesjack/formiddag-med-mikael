def create_playlist_name(episode_link):
    return "Formiddag med Mikael " + episode_link[-10:]


def get_existing_playlists(sp, user, limit=50):
    playlists = sp.user_playlists(user, limit=limit, offset=0)
    return [playlist['name'] for playlist in playlists['items']]


def get_track_ids(sp, artists, tracks):
    track_ids = []
    for artist, track in zip(artists, tracks):
        
        results = sp.search(q='artist:' + artist + ' track:' + track, type='track', limit=1)
        for track_info in results['tracks']['items']:
            track_ids.append(track_info['id'])

    return track_ids