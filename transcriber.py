from __future__ import print_function
import json
from os.path import join, dirname
from collections import defaultdict
from ibm_watson import SpeechToTextV1, NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import threading


speech_to_text_authenticator = IAMAuthenticator('Ie8T4DP8IqRzCSz3Ww8B1padPbY5sbrx_BvQu_IeeMFo')
sentiment_analysis_authenticator = IAMAuthenticator('9a-GE9xAuObCOU7mc31DPCs9Qbh8iuRnT7FC38Y7aVmK')

# Example using websockets
class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        print(transcript)

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_hypothesis(self, hypothesis):
        print(hypothesis)

    def on_data(self, data):
        print(data)

def transcribe():
    print("Transcribing...")
    # If service instance provides API key authentication
    service = SpeechToTextV1(authenticator=speech_to_text_authenticator)

    # service = SpeechToTextV1(
    #     username='YOUR SERVICE USERNAME',
    #     password='YOUR SERVICE PASSWORD',
    #     url='https://stream.watsonplatform.net/speech-to-text/api')



    model = service.get_model('en-US_BroadbandModel').get_result()

    with open(join(dirname(__file__), 'test.wav'),
              'rb') as audio_file:
        transcript = json.dumps(
            service.recognize(
                audio=audio_file,
                content_type='audio/wav').get_result(),
            indent=2)

    print("Finished transcribing...")
    print(transcript)
    return transcript



def sentiment_analysis(transcript):
    print("Initialize sentiment analysis...")
    service = NaturalLanguageUnderstandingV1(
        version='2018-03-16',
        authenticator=sentiment_analysis_authenticator
    )

    response = service.analyze(
        text=transcript,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
            keywords=KeywordsOptions(emotion=True, sentiment=True,
                                     limit=2))).get_result()
    print("Analyzed sentiment...")
    print(response)
    return handle_sentiment(response)

def handle_sentiment(sentiment):
    keywords = [];
    emotions = ["sadness", "joy", "fear", "disgust", "anger"]
    emotion_weights = defaultdict(int)

    for keyword in sentiment["keywords"]:
        keywords.append(keyword["text"])
        relevance = keyword["relevance"]
        for emotion in emotions:
            emotion_weights[emotion] += relevance * keyword["emotion"][emotion]
  
    return find_emotion(emotion_weights)
    
def find_emotion(emotion_weights):
    total_weight = 0

    for k,v in emotion_weights.items():
        total_weight += v
    for k,v in emotion_weights.items():
        emotion_weights[k] = v/total_weight

    # logic about picking emotion based on gracenote mood list

    emotions = sorted(emotion_weights.items(), key=lambda x: x[1], reverse=True)    
    print(emotions)

    # placeholder
    return "sadness"

def main():
    transcript = transcribe()
    emotion = sentiment_analysis(transcript)
    print(emotion)
    return emotion

if __name__ == "__main__":
    main()