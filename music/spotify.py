import requests
import json
import collections

# happy, sadness, anger, fear

def generate_headers(token, scope):
	headers = {
		'Authorization' : token,
		'scope' : scope
	}
	return headers

def generate_min_tunable_attributes(user_state):
	Attributes = collections.namedtuple('Attributes', [
		'min_tempo', 
		'min_acousticness', 
		'min_danceability', 
		'min_energy', 
		'min_instrumentalness',
		'min_valence',
		'mode'
		])
	if (user_state == 'happy'):
		return Attributes(
			min_tempo=156.0, 
			min_acousticness=0.0,
			min_danceability=0.75,
			min_energy=0.75,
			min_instrumentalness=0.0,
			min_valence=0.75,
			mode=1
			)
	elif (user_state == 'sadness'):
		return Attributes(
			min_tempo=24.0, 
			min_acousticness=0.25,
			min_danceability=0.0,
			min_energy=0.0,
			min_instrumentalness=0.0,
			min_valence=0.0,
			mode=0
			)
	elif (user_state == 'anger'):
		return Attributes(
			min_tempo=156.0, 
			min_acousticness=0.0,
			min_danceability=0.0,
			min_energy=0.75,
			min_instrumentalness=0.25,
			min_valence=0.0,
			mode=0
			)
	elif (user_state == 'fear'):
		return Attributes(
			min_tempo=40.0, 
			min_acousticness=0.0,
			min_danceability=0.0,
			min_energy=0.0,
			min_instrumentalness=0.0,
			min_valence=0.0,
			mode=0
			)

def generate_max_tunable_attributes(user_state):
	Attributes = collections.namedtuple('Attributes', [
		'max_tempo', 
		'max_acousticness', 
		'max_danceability', 
		'max_energy', 
		'max_instrumentalness',
		'max_valence',
		'mode'
		])
	if (user_state == 'happy'):
		return Attributes(
			max_tempo=300.0, 
			max_acousticness=1.0,
			max_danceability=1.0,
			max_energy=1.0,
			max_instrumentalness=1.0,
			max_valence=1.0,
			mode=1
			)
	elif (user_state == 'sadness'):
		return Attributes(
			max_tempo=108.0, 
			max_acousticness=0.75,
			max_danceability=0.5,
			max_energy=0.5,
			max_instrumentalness=0.75,
			max_valence=0.3,
			mode=0
			)
	elif (user_state == 'anger'):
		return Attributes(
			max_tempo=250.0, 
			max_acousticness=0.5,
			max_danceability=0.5,
			max_energy=1.0,
			max_instrumentalness=0.75,
			max_valence=0.2,
			mode=0
			)
	elif (user_state == 'fear'):
		return Attributes(
			max_tempo=100.0, 
			max_acousticness=0.5,
			max_danceability=0.25,
			max_energy=0.3,
			max_instrumentalness=0.5,
			max_valence=0.4,
			mode=0
			)


def generate_seed_genres(user_state=None):
	if (user_state == 'happy'):
		genres = "acoustic, dance, edm, pop"
	elif (user_state == 'sadness'):
		genres = "chill, ambient, piano, soundtracks"
	elif (user_state == 'angry'):
		genres = "dubstep, hard-rock, heavy-metal, rock, drum-and-bass"
	elif (user_state == 'fear'):
		genres = "ambient, psych-rock, trip-hop, trance"
	else:
		genres = ""
	return genres
	
def generate_playlist(token, scope, user_state=None):
	min_attributes = generate_min_tunable_attributes(user_state)
	max_attributes = generate_max_tunable_attributes(user_state)
	seed_genres = generate_seed_genres(user_state)

	params = {
		('market', 'PH'),
		('seed_genres', seed_genres),
		('min_acousticness', min_attributes.min_acousticness),
		('min_danceability', min_attributes.min_danceability),
		('min_energy', min_attributes.min_energy),
		('min_instrumentalness', min_attributes.min_instrumentalness),
		('min_tempo', min_attributes.min_tempo),
		('min_valence', min_attributes.min_valence),
		('mode', min_attributes.mode),
		('max_acousticness', max_attributes.max_acousticness),
		('max_danceability', max_attributes.max_danceability),
		('max_energy', max_attributes.max_energy),
		('max_instrumentalness', max_attributes.max_instrumentalness),
		('max_tempo', max_attributes.max_tempo),
		('max_valence', max_attributes.max_valence),
		('min_popularity', 0),
		('max_popularity', 100)
	}

	endpoint = "https://api.spotify.com/v1/recommendations/"
	headers = generate_headers(token, scope)
	response = requests.get(
		endpoint,
		headers = headers,
		params = params
	).json()
	# print(params)
	# print("\n\n\n")
	# print(json.dumps(response, indent=2, sort_keys=True))
	tracks = response['tracks']
	uris = []
	for x in tracks: uris.append(x["uri"])
	return uris


def play_player(token, scope, uris):
	endpoint = "https://api.spotify.com/v1/me/player/play"
	headers = generate_headers(token, scope)
	payload = {
		"uris": uris,
		"position_ms": 35
	}
	requests.put(
		endpoint,
		headers = headers,
		data = json.dumps(payload)
	)
	shuffle_player(token, scope)

def pause_player(token, scope, uris):
	endpoint = 'https://api.spotify.com/v1/me/player/pause'
	headers = generate_headers(token, scope)
	requests.put(
		endpoint,
		headers = headers
	)

def shuffle_player(token, scope):	
	endpoint = "https://api.spotify.com/v1/me/player/shuffle"	
	headers = generate_headers(token, scope)
	requests.put(
		endpoint,
		headers = headers
	)

