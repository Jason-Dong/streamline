import spotipy
import requests
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

<<<<<<< Updated upstream
def get_user_playlists(user_id):
    return spotify.user_playlists(user_id)
=======
def apple_req(url, devkey, key, **kwargs):
    r = requests.get('https://api.music.apple.com' + url,
                     headers={
                         'Music-User-Token': key,
                         'Authorization': 'Bearer ' + devkey
                     }, **kwargs)
    resp = r.json()
    if 'data' not in resp:
        raise ValueError(resp)
    return resp

def apple_playlists(devkey, key):
    resp = apple_req('/v1/me/library/playlists', devkey, key)
    for playlist in resp['data']:
        yield parseplaylist(playlist, devkey, key)
    if 'next' in resp:
        raise Exception('More playlists')

def parseplaylist(playlist, devkey, key):
    p = {
        'id': playlist['id'],
        'name': playlist['attributes']['name'],
    }
    if 'description' in playlist['attributes']:
        p['description'] = playlist['attributes']['description']['standard']
    if 'artwork' in playlist['attributes']:

        p['artwork'] = playlist['attributes']['artwork']['url']
    if 'relationships' in playlist:
        p['tracks'] = []
        addTracks(playlist['relationships']['tracks']['data'], p['tracks'])
        if 'next' in playlist['relationships']['tracks']:
            print('adding more')
            addMoreTracks(playlist['relationships']['tracks']['next'], p['tracks'], devkey, key)
    return p

def addTracks(ptracks, otracks):
    for track in ptracks:
        if 'playParams' not in track['attributes']:
            print('Track does not have playParams', track)
            continue
        otracks.append({
            'id': track['id'],
            'artist': track['attributes']['artistName'],
            'genres': track['attributes']['genreNames'],
            'name': track['attributes']['name'],
            'album': track['attributes']['albumName'],
            'catalogId': track['attributes']['playParams']['catalogId']
        })

def addMoreTracks(url, tracks, devkey, key):
    resp = apple_req(url, devkey, key)
    addTracks(resp['data'], tracks)
    if 'next' in resp:
        print('adding more more')
        addMoreTracks(resp['next'], tracks, devkey, key)
>>>>>>> Stashed changes
