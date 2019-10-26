import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = '2fd46a7902e043e4bcb8ccda3d1381b2'
CLIENT_SECRET = 'c059fdd2c9aa40c9be2a740ddc6151f9'


def get_spotify():
    client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)


spotify = get_spotify()


def get_val_from_request(request, key):
    request_json = request.get_json()
    if request.args and key in request.args:
        return request.args.get(key)
    elif request_json and key in request_json:
        return request_json[key]


def isrc_to_id(isrc):
    return spotify.search(q='isrc:{}'.format(isrc), type='track')['tracks']['items'][0]['id']


def id_to_isrc(spotify_id):
    return spotify.track(spotify_id)['external_ids']['isrc']


def features_from_id(spotify_id):
    return spotify.audio_features(spotify_id)[0]


def get_playlist(user, playlist):
    return spotify.user_playlist_tracks(user, playlist)['items']


def isrc_to_facts(isrc):
    track = spotify.track(isrc_to_id(isrc))
    return {'name': track['name'], 'artist': track['artists'][0]['name']}
