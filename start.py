from flask import Flask, render_template, redirect, request, Response, jsonify
import base64
import requests
import json
import urllib.parse
import pyaudio
import wave
from transcription.recording import record_audio
from transcription.speech_to_text import transcribe
from sentiment.analyze_text import analyze_sentiment as analyze_text
from sentiment.analyze_speech import analyze_sentiment as analyze_speech
import music.spotify as spotify
from operator import itemgetter

app = Flask(__name__)

client_id = "7e12cab8110d45088dd8136f0fcdf54f"
client_secret = "13962e5653a940c0ae513501b142538e"
redirect_uri = "http://localhost:5000/player"
app_token = "BQAxHESEFLJLnT_R2dM-IbDRwHZokPOiAVCpx-07QEGfybc7MeU7RZ5AmEj5a1iTve-0TpFG3TANWF_sfwD2Hv7yF1HxDo0TD00wiTy181knOaV5aBdJpcLxaARKA8OVk9SaRryxwFuhTvT3131OD2xh-jgAw-wDH86G5cGGGXVTczE"
scope = "user-read-private user-read-email user-read-playback-state user-modify-playback-state streaming user-read-birthdate" 


@app.route("/")
def auth():
	return redirect('https://accounts.spotify.com/authorize' +
  '?response_type=code' +
  '&client_id=' + client_id +
   '&scope=' + urllib.parse.quote(scope.encode("utf-8")) +
  '&redirect_uri=' + urllib.parse.quote(redirect_uri.encode("utf-8")))

@app.route("/player", methods=['GET', 'POST'])
def start():
	if request.method == 'GET':
		auth_code = request.args.get('code')
		state = request.args.get('state')
		access_token, refresh_token = fetch_tokens_with_auth(auth_code)
	
		return render_template("index.html", access_token=access_token, refresh_token=refresh_token)

@app.route("/audio", methods=['POST'])
def audio():
	if request.method == 'POST':
		(user_state, text_to_sentiment_emotion, speech_to_sentiment_emotion, transcription) = transcribe_and_analyze()
		current_state = request.values.get('current_state');
		refresh_token = request.values.get('refresh_token')
		access_token = fetch_tokens_with_refresh(refresh_token);
		if (user_state != current_state):
			current_state = user_state
			uris = spotify.generate_playlist("Bearer " + access_token, scope, user_state)
			spotify.play_player("Bearer " + access_token, scope, uris)
		return jsonify({
			'access_token': access_token, 
			'refresh_token': refresh_token, 
			'current_state': current_state,
			'text_to_sentiment_emotion': text_to_sentiment_emotion,
			'speech_to_sentiment_emotion': speech_to_sentiment_emotion,
			'transcription': transcription
			})

def fetch_tokens_with_auth(auth_code):
	payload = base64.b64encode(bytes(client_id + ":" + client_secret, 'utf-8')).decode("ascii")
	response = requests.post(
		"https://accounts.spotify.com/api/token",
		headers={
			'Content-Type': 'application/x-www-form-urlencoded',
			'Authorization': 'Basic ' + payload
		},
		data={"grant_type": "authorization_code", "code": auth_code, "redirect_uri": redirect_uri}
	)
	r = response.json()
	#print(r)
	return r['access_token'], r['refresh_token']

def fetch_tokens_with_refresh(refresh_token):
	payload = base64.b64encode(bytes(client_id + ":" + client_secret, 'utf-8')).decode("ascii")
	response = requests.post(
		"https://accounts.spotify.com/api/token",
		headers={
			'Content-Type': 'application/x-www-form-urlencoded',
			'Authorization': 'Basic ' + payload
		},
		data={"grant_type": "refresh_token", "refresh_token": refresh_token, "redirect_uri": redirect_uri}
	)
	r = response.json()
	return r['access_token']

@app.route("/pause", methods=['POST'])
def pause_player(token, scope, uris):
	endpoint = "https://api.spotify.com/v1/me/player/pause"
	response = requests.put(
		endpoint,
		headers = {
			'Authorization' : token,
			'scope' : scope
		}
	)

def transcribe_and_analyze():
	user_state = None
	recorded_audio = record_audio()
	transcription = transcribe()

	text_to_sentiment_analysis = analyze_text(transcription)
	text_to_sentiment_emotion = max(text_to_sentiment_analysis, key=itemgetter(1))

	speech_to_sentiment_analysis = analyze_speech()
	speech_to_sentiment_emotion = max(speech_to_sentiment_analysis, key=itemgetter(1))
	# logic to associate text-to-sentiment and speech-to-sentiment values
	if (text_to_sentiment_emotion[0] == 'disgust' and speech_to_sentiment_emotion[0] != 'neutral'):
		user_state = speech_to_sentiment_emotion[0]
	elif (speech_to_sentiment_emotion[0] == 'disgust'):
		user_state = 'anger'
	elif (speech_to_sentiment_emotion[0] == 'neutral'):
		user_state = text_to_sentiment_emotion[0]

	# default to text-to-sentiment analysis
	else:
		user_state = compare_sentiment_analyses(text_to_sentiment_emotion, speech_to_sentiment_emotion)
	
	return (user_state, text_to_sentiment_analysis, speech_to_sentiment_analysis, transcription)

def compare_sentiment_analyses(tts_emotion, sts_emotion):
	if (tts_emotion[0] == sts_emotion[0]):
		return tts_emotion[0]
	elif (tts_emotion[0] == 'joy' and sts_emotion != 'happy') or (sts_emotion[0] == 'happy' and tts_emotion[0] != 'joy'):
		# handle irony
		return sts_emotion[0]
	else:
		uniq_combo = 6
		tts_confidence = tts_emotion[1]
		sts_confidence = sts_emotion[1]
		# more logic
		return sts_emotion[0]


if __name__ == '__main__':
	app.run(debug=True)
