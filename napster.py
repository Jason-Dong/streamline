API_KEY = 'NWRhNzc3NTgtN2U2ZC00Mjk5LThkNzItODZlMzM5MzdmYWM'

import requests
import json
import sys

def req(url, **params):
  return requests.get('http://api.napster.com/v2.2' + url,
                      params={'apikey': API_KEY, **params})

def tracks(query):
  """All tracks that match a query."""
  r = req('/search', query=query, type='track').json()
  return r['search']['data']['tracks']

def oldmatchingtracks(name, album, artist):
  """All tracks with the given name, album, and artist."""
  name = name.lower()
  album = album.lower()
  artist = artist.lower()
  for track in tracks(name + ' ' + artist):
    if track['name'].lower() == name and track['albumName'].lower() == album and track['artistName'].lower() == artist:
      yield track

def oldtrack(name, album, artist):
  """The track with given name, album, and artist with the greatest number of genres."""
  matches = list(matchingtracks(name, album, artist))
  if len(matches) == 0:
      raise ValueError('No such track found')
  return sorted(matches, key=lambda m: len(m['links']['genres']['ids']))[-1]

def track(isrc):
  matches = list(matchingtracks(isrc))
  if len(matches) == 0:
      raise ValueError('No such track found')
  def numids(m):
      if 'genres' in m['links']:
          return len(m['links']['genres']['ids'])
      return 0
  return sorted(matches, key=numids)[-1]

def matchingtracks(isrc):
  r = req('/tracks/isrc/' + isrc).json()
  return r['tracks']

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
# info(track('isrc'))


#### GENRE MAP CODE

for p in playlists():
    isrcs = appleisrcs(p['tracks'])
    for i, t in enumerate(isrcs):
        try:
            print('.', end='')
            sys.stdout.flush()
            #info(track(t))
            genres = [genre(g)['name'] for g in track(t)['links']['genres']['ids']]
            for g in genres:
                if g in genremap:
                    genremap[g].append(t)
                else:
                    genremap[g] = [t]
            #print()
        except:
            print('Could not find track', p['tracks'][i]['name'])
#print(list(playlists()))
print(json.dumps(genremap))
