from os.path import join, dirname
from ibm_watson import SpeechToTextV1, NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import threading
import json

speech_to_text_authenticator = IAMAuthenticator('Ie8T4DP8IqRzCSz3Ww8B1padPbY5sbrx_BvQu_IeeMFo')

FILE_NAME = "EXAMPLE.wav"

def transcribe():
    print("Transcribing...")
    service = SpeechToTextV1(authenticator=speech_to_text_authenticator)
    model = service.get_model('en-US_NarrowbandModel').get_result()

    with open(FILE_NAME,'rb') as audio_file:
        api_result = service.recognize(
                audio=audio_file,
                content_type='audio/wav', model='en-US_NarrowbandModel').get_result()

    print("Finished transcribing...")
    transcript = concatenate_transcription(api_result)
    return transcript

def concatenate_transcription(api_result):
    final_transcript = ''
    print(json.dumps(api_result, indent=2, sort_keys=True))
    results = api_result['results']
    for result in results:
        final_transcript += result['alternatives'][0]['transcript']
    return final_transcript

if __name__ == "__main__":
    transcribe()
