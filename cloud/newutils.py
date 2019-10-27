import requests
import spotipy
import secretstuff
from schema import Playlist

def apple_req(url, **kwargs):
    """Send a request to the apple API."""
    req = requests.get('https://api.music.apple.com' + url,
                       headers={
                           'Music-User-Token': secretstuff.apple_userkey,
                           'Authorization': 'Bearer ' + secretstuff.apple_devkey
                       }, **kwargs)
    resp = req.json()
    if 'data' not in resp:
        raise ValueError(resp)
    return resp

def parse_apple_playlist(playlist):
    image = None
    if 'artwork' in playlist['attributes']:
        image = playlist['attributes']['artwork']['url']

    return Playlist(id=playlist['id'],
                    name=playlist['attributes']['name'],
                    image=image)

def apple_playlists(token):
    resp = apple_req('/v1/me/library/playlists')
    for playlist in resp['data']:
        yield parse_apple_playlist(playlist)
    if 'next' in resp:
        raise Exception('More playlists')

def playlist_to_catalogids(url):
    """Return the list of catalog ids in an apple playlist."""
    resp = apple_req(url)
    for track in resp['data']:
        if 'playParms' not in track['attributes']:
            continue
        yield track['attributes']['playParams']['catalogId']
    if 'next' in resp:
        yield from playlist_to_catalogids(resp['next'])

def cids_to_isrcs(cids):
    """Convert catalog ids to isrcs."""
    if len(cids) > 100:
        median = len(cids) // 2
        return cids_to_isrcs(cids[:median]) + cids_to_isrcs(cids[median:])

    resp = apple_req('/v1/catalog/us/songs', params={
        'ids': ','.join(cids)
    })
    results = resp['data']
    if len(results) != len(cids):
        print('Track returned wrong number of isrcs (expected {} but got {})'.format(len(cids), len(results)))
    return [result['attributes']['isrc'] for result in results]

def apple_track_isrcs(playlist_id, token):
    url = '/v1/me/library/playlists/' + playlist_id + '/tracks'
    cids = list(playlist_to_catalogids(url))
    return cids_to_isrcs(cids)

def next_or_null(it):
    if len(it) > 0:
        return it[0]
    return None

def spotify_playlists(token):
    sp = spotipy.Spotify(auth=token)
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        yield Playlist(id=playlist['id'],
                       name=playlist['name'],
                       image=next_or_null(playlist['images'])
        )
