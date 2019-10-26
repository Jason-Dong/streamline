import spotipy
import spotipy.util as util

def add_tracks(token, username, playlist_id, track_ids):
	if token:
	    sp = spotipy.Spotify(auth=token)
	    sp.trace = False
	    results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
	    print(results)
	else:
	    print("Can't get token for", username)

def get_playlists(token, username):
	if token:
	    sp = spotipy.Spotify(auth=token)
	    playlists = sp.user_playlists(username)
	    results = []
	    for playlist in playlists['items']:
	        results.append(playlist['id'])
	    return results
	else:
	    print("Can't get token for", username)