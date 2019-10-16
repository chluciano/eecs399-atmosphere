from flask import Flask, render_template, redirect, request, Response, jsonify
import base64
import requests
import json
import urllib.parse
import transcriber
import pyaudio
import wave

app = Flask(__name__)

client_id = "7e12cab8110d45088dd8136f0fcdf54f"
client_secret = "13962e5653a940c0ae513501b142538e"
redirect_uri = "http://localhost:5000/player"
app_token = "BQAxHESEFLJLnT_R2dM-IbDRwHZokPOiAVCpx-07QEGfybc7MeU7RZ5AmEj5a1iTve-0TpFG3TANWF_sfwD2Hv7yF1HxDo0TD00wiTy181knOaV5aBdJpcLxaARKA8OVk9SaRryxwFuhTvT3131OD2xh-jgAw-wDH86G5cGGGXVTczE"
sadPlaylistUri = "spotify:user:spotifyluciano3:playlist:4fMQbprrxmFjLSHSOEj6sw"
happyPlaylistUri = "spotify:user:spotifyluciano3:playlist:2i7PJTO3ypWshEfkhY2ja3"
angryPlaylistUri = "spotify:user:spotifyluciano3:playlist:5CnhvCg1AcjuKH97lf1uam"
sadPlaylistId = "4fMQbprrxmFjLSHSOEj6sw"
happyPlaylistId = "2i7PJTO3ypWshEfkhY2ja3"
angryPlaylistId = "5CnhvCg1AcjuKH97lf1uam"
scope = "user-read-private user-read-email user-read-playback-state user-modify-playback-state streaming user-read-birthdate" 


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 15
WAVE_OUTPUT_FILENAME = "test.wav"


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
		user_state = audio()
		current_state = request.values.get('current_state');
		refresh_token = request.values.get('refresh_token')
		access_token = fetch_tokens_with_refresh(refresh_token);
		if (user_state != current_state):
			current_state = user_state
			playlist = fetch_playlist_tracks("Bearer " + access_token, scope, user_state)
			uris = []
			for x in playlist["items"]: uris.append(x["track"]["uri"])
			play_player("Bearer " + access_token, scope, uris)
		return jsonify({'access_token': access_token, 'refresh_token': refresh_token, 'current_state': current_state})

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

def fetch_playlist_tracks(token, scope, user_state=None):
	if user_state == "joy":
		playlistID = happyPlaylistId
	elif user_state == "sadness":
		playlistID = sadPlaylistId
	elif user_state == "anger":
		playlistID = angryPlaylistId
	elif user_state == "fear":
		playlistID = sadPlaylistId
	else:
		playlistID = happyPlaylistId
	endpoint = "https://api.spotify.com/v1/playlists/" + playlistID + "/tracks"
	response = requests.get(
		endpoint,
		headers = {
			'Authorization' : token,
			'scope' : scope
		}
	)
	r = response.json()
	return r

def play_player(token, scope, uris):
	endpoint = "https://api.spotify.com/v1/me/player/play"
	payload = {
		"uris": uris,
		"position_ms": 35
	}
	response = requests.put(
		endpoint,
		headers = {
			'Authorization' : token,
			'scope' : scope
		},
		data = json.dumps(payload)
	)
	shuffle_player(token)

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



def shuffle_player(token):
	endpoint = "https://api.spotify.com/v1/me/player/shuffle"
	response = requests.put(
		endpoint,
		headers = {
			'Authorization' : token,
		},
		params = {
			'state': True
		}
	)

def genHeader(sampleRate, bitsPerSample, channels):
    datasize = 2000*10**6
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o

def audio():
    # start Recording
    audio1 = pyaudio.PyAudio()

    CHUNK = 1024
    sampleRate = 44100
    bitsPerSample = 16
    channels = 2
    wav_header = genHeader(sampleRate, bitsPerSample, channels)

    stream = audio1.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,input_device_index=0,
                    frames_per_buffer=CHUNK)
    print ("recording...")
    frames = []
     
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print( "finished recording")
     
     
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio1.terminate()
     
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio1.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    return transcriber.main()


if __name__ == '__main__':
	app.run(debug=True)
