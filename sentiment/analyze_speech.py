#!/usr/bin/env python3

# OpenVokaWavMean-mac64.py
# public-domain sample code by Vokaturi, 2019-05-30
#
# A sample script that uses the VokaturiPlus library to extract the emotions from
# a wav file on disk. The file has to contain a mono or stereo recording.
#
# Call syntax:
#   python3 OpenVokaWavMean-mac64.py path_to_sound_file.wav
#
# For the sound file hello.wav that comes with OpenVokaturi, the result should be:
#	Neutral: 0.760
#	Happy: 0.000
#	Sad: 0.238
#	Angry: 0.001
#	Fear: 0.000


import sys
import scipy.io.wavfile
from . import Vokaturi
import os
from operator import itemgetter

FILE_NAME = "SENTIMENT.wav"

if sys.platform == "linux":
    platform = "linux"
    lib = "OpenVokaturi-3-3-linux64.so"
elif sys.platform == "darwin":
    platform = "macos"
    lib = "OpenVokaturi-3-3-mac64.dylib"
elif sys.platform == "win32":
    platform = "win"
    lib = "OpenVokaturi-3-3-win64.dll"

dir_path = os.path.dirname(os.path.abspath(__file__))
lib_location = os.path.join(dir_path, 'lib', 'open', platform, lib)
Vokaturi.load(lib_location)

def analyze_sentiment():
	(sample_rate, samples) = scipy.io.wavfile.read(FILE_NAME)
	buffer_length = len(samples)
	c_buffer = Vokaturi.SampleArrayC(buffer_length)
	if samples.ndim == 1:  # mono
		c_buffer[:] = samples[:] / 32768.0
	else:  # stereo
		c_buffer[:] = 0.5*(samples[:,0]+0.0+samples[:,1]) / 32768.0

	voice = Vokaturi.Voice(sample_rate, buffer_length)
	voice.fill(buffer_length, c_buffer)
	quality = Vokaturi.Quality()
	emotionProbabilities = Vokaturi.EmotionProbabilities()
	voice.extract(quality, emotionProbabilities)
	emotion = "None"

	if quality.valid:
		emotion_probabilities_list = [
			('neutral', emotionProbabilities.neutrality),
			('happy', emotionProbabilities.happiness),
			('sad', emotionProbabilities.sadness),
			('angry', emotionProbabilities.anger),
			('fear', emotionProbabilities.fear)
		]
		# print("Neutral: %.3f" % emotionProbabilities.neutrality)
		# print("Happy: %.3f" % emotionProbabilities.happiness)
		# print("Sad: %.3f" % emotionProbabilities.sadness)
		# print("Angry: %.3f" % emotionProbabilities.anger)
		# print("Fear: %.3f" % emotionProbabilities.fear)
	else:
		print("Not enough sonorancy to determine emotions")

	voice.destroy()

	emotions = sorted(emotion_probabilities_list, key=lambda x: x[1], reverse=True)   
	return emotions

if __name__ == "__main__":
	analyze_sentiment()


