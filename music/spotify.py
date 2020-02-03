import requests
import json

def generate_headers(token, scope):
	headers = {
		'Authorization' : token,
		'scope' : scope
	}
	return headers

def generate_min_tunable_attributes(user_state):
	# TODO logic for generating the minimum for tunable attributes based on user_state
	pass

def generate_max_tunable_attributes(user_state):
	# TODO logic for generating the maximum for tunable attributes based on user_state
	pass

def generate_seed_genres(user_state=None):
	# TODO logic for generating genres based on user_state
	happy_genres = "acoustic, dance, edm, pop"
	sad_genres = "chill, ambient, piano, soundtracks"

	return happy_genres

def generate_playlist(token, scope, user_state=None):
	min_acousticness = 0.0
	min_danceability = 0.0
	min_energy = 0.5
	min_instrumentalness = 0.25
	# mode = 0
	min_tempo = 90.0
	min_valence = 0.0

	max_acousticness = 1.0
	max_danceability = 1.0
	max_energy = 1.0
	max_instrumentalness = 1.0
	max_tempo = 200.0
	max_valence = 1.0

	
	seed_genres = generate_seed_genres()

	params = {
		('market', 'PH'),
		('seed_genres', seed_genres),
		('min_acousticness', min_acousticness),
		('min_danceability', min_danceability),
		('min_energy', min_energy),
		('min_instrumentalness', min_instrumentalness),
		('min_tempo', min_tempo),
		('min_valence', min_valence),
		('max_acousticness', max_acousticness),
		('max_danceability', max_danceability),
		('max_energy', max_energy),
		('max_instrumentalness', max_instrumentalness),
		('max_tempo', max_tempo),
		('max_valence', max_valence)
	}

	endpoint = "https://api.spotify.com/v1/recommendations/"
	headers = generate_headers(token, scope)
	response = requests.get(
		endpoint,
		headers = headers,
		params = params
	).json()

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

