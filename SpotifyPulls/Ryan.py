API_KEY = 'NWRhNzc3NTgtN2U2ZC00Mjk5LThkNzItODZlMzM5MzdmYWM'

import requests

def req(url, **params):
  return requests.get('http://api.napster.com/v2.2' + url,
                      params={'apikey': API_KEY, **params})

def tracks(query):
  """All tracks that match a query."""
  r = req('/search', query=query, type='track').json()
  return r['search']['data']['tracks']

def matchingtracks(name, album, artist):
  """All tracks with the given name, album, and artist."""
  name = name.lower()
  album = album.lower()
  artist = artist.lower()
  for track in tracks(name + ' ' + artist):
    if track['name'].lower() == name and track['albumName'].lower() == album and track['artistName'].lower() == artist:
      yield track

def track(name, album, artist):
  """The track with given name, album, and artist with the greatest number of genres."""
  matches = list(matchingtracks(name, album, artist))
  return sorted(matches, key=lambda m: len(m['links']['genres']['ids']))[-1]

# A few caches so we don't send too many requests
tagcache = {}
genrecache = {}

def info(track):
  """Print string representation of track."""
  print('{} ({})'.format(track['name'], track['shortcut']))
  print('{} / {}'.format(track['albumName'], track['artistName']))
  print([genre(g)['name'] for g in track['links']['genres']['ids']])
  # print([tag(t)['name'] for t in track['links']['tags']['ids']])

def genre(id):
  """Look up a genre."""
  if id in genrecache:
    g = genrecache[id]
  else:
    r = req('/genres/' + id).json()['genres']
    if len(r) > 1:
      raise ValueError('More than one genre?')
    g = r[0]
    genrecache[id] = g
  return {
      'name': g['name'],
      'description': g['description']
  }
  # also of note is parentGenres and childGenres

def tag(id):
  """Look up a tag. Tags appear to be like genres but worse."""
  if id in tagcache:
    t = tagcache[id]
  else:
    r = req('/tags/' + id).json()['tags']
    if len(r) > 1:
      raise ValueError('More than one tag?')
    t = r[0]
  return {
      'name': t['name']
  }
  # parentId, childIds, genreId interesting

# Example usage:
# info(track('name', 'album', 'artist'))
