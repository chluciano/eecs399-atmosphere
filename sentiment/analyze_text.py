from ibm_watson import SpeechToTextV1, NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from collections import defaultdict
from operator import itemgetter
import json

sentiment_analysis_authenticator = IAMAuthenticator('9a-GE9xAuObCOU7mc31DPCs9Qbh8iuRnT7FC38Y7aVmK')

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
    return response

def handle_sentiment(sentiment):
    keywords = [];
    emotions = ["sadness", "joy", "fear", "disgust", "anger"]
    emotion_weights = defaultdict(int)
    
    for keyword in sentiment["keywords"]:
        keywords.append(keyword["text"])
        relevance = keyword["relevance"]
        for emotion in emotions:
            emotion_weights[emotion] += relevance * keyword["emotion"][emotion]
  
    return emotion_weights
    
def find_emotions(emotion_weights):
    total_weight = 0

    for k,v in emotion_weights.items():
        total_weight += v
    for k,v in emotion_weights.items():
        emotion_weights[k] = v/total_weight

    # logic about picking emotion based on gracenote mood list

    emotions = sorted(emotion_weights.items(), key=lambda x: x[1], reverse=True)    

    # placeholder
    return emotions

def analyze_sentiment(transcript):
    analyzed_sentiment_results = sentiment_analysis(transcript)
    emotion_weights = handle_sentiment(analyzed_sentiment_results)
    emotions = find_emotions(emotion_weights)
    return emotions

