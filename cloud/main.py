from utils import get_val_from_request, isrc_to_id, id_to_isrc, isrc_to_facts, spotify, features_from_id


def get_audio_features(request):
    isrc = get_val_from_request(request, 'isrc')
    if isrc:
        return str(features_from_id(isrc_to_id(isrc)))
    return "Problem with get_audio_features"


def playlist_to_features_dict(request):
    user_id = get_val_from_request(request, 'user')
    playlist_id = get_val_from_request(request, 'playlist')

    if user_id and playlist_id:
        d = {}
        for item in spotify.user_playlist_tracks(user_id, playlist_id)['items']:
            spotify_id = item['track']['id']
            d[id_to_isrc(spotify_id)] = features_from_id(spotify_id)
        return str(d)
    return "Problem with playlist_to_features_dict"


def get_facts(request):
    isrc = get_val_from_request(request, 'isrc')
    if isrc:
        return str(isrc_to_facts(isrc))
    return "Problem with get_facts"
