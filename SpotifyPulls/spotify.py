import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '2fd46a7902e043e4bcb8ccda3d1381b2'
client_secret = 'c059fdd2c9aa40c9be2a740ddc6151f9'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#print(sp.search(q='track:Bottle Service', type='track'))

id = '4k0ZX0KlMBEOlTp5vexIrT'

#print(sp.audio_features(id))
#print(sp.track(id))


playlists = sp.user_playlists('spotify')
playlist_list = list(playlists['items'])

playlist_id = playlist_list[0]['id']
print('playlist id:', playlist_id, 'playlist name:', playlist_list[0]['name'])
user_id = '9l4ypaf0dsx8vkjtxhu28hxhm'

playlist_tracks = sp.user_playlist_tracks('spotify', playlist_id)

for item in sp.user_playlist_tracks('spotify', playlist_id)['items']:
    print(sp.audio_features(item['track']['id']))

#List all spotify playlists
"""
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None

"""