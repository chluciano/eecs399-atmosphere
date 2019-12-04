from os.path import join, dirname
from ibm_watson import SpeechToTextV1, NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import threading
import json

speech_to_text_authenticator = IAMAuthenticator('Ie8T4DP8IqRzCSz3Ww8B1padPbY5sbrx_BvQu_IeeMFo')

def transcribe():
    print("Transcribing...")
    service = SpeechToTextV1(authenticator=speech_to_text_authenticator)
    model = service.get_model('en-US_NarrowbandModel').get_result()

    with open('SENTIMENT.wav','rb') as audio_file:
        transcript = json.dumps(
            service.recognize(
                audio=audio_file,
                content_type='audio/wav').get_result(),
            indent=2)

    print("Finished transcribing...")
    return transcript

if __name__ == "__main__":
    transcribe()
