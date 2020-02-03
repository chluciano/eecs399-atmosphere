## Getting Started
### If you have 2 versions of python on your computer....

~~~
source env/bin/activate
pip3 install ibm_watson ibm_cloud_sdk_core Flask pyaudio wave scipy
python3 start.py
~~~
Anytime you want to run the program:
cd into repo
~~~
source env/bin/activate
python3 start.py
~~~

### Otherwise just do this
~~~
source env/bin/activate
pip install ibm_watson ibm_cloud_sdk_core Flask pyaudio wave scipy
python start.py
~~~
Anytime you want to run the program:
cd into repo
~~~
source env/bin/activate
python start.py
~~~

### Then go to localhost:5000

## Code Structure
```
|-- start.py
|-- transcription
|   |-- recording.py
|   |-- speech_to_text.py
|-- sentiment
|   |-- analyze_speech.py
|   |-- analyze_text.py
|	|-- Vokaturi.py
|	|-- lib
|-- music
|   |-- spotify.py
|-- api
|   |-- Vokaturi stuff
|-- templates
|	|-- index.html

```

## Breakdown
```
start.py
``` 
Imports all the modules, contains a Flask server that authenticates to Spotify. Renders /transcription/index.html.
This file should just be Flask (probably), so we should move any other functions to their respective modules. Also need to move the client ids and secrets into a config file.
**To Do**
- [] Move transcribe_and_analyze() to module.
- [] Move compare_sentiment_analyses() to module
- [] Store client ids, API keys, etc. to config file and import into script

### Transcription Module
```
transcription.recording.py
```
Records audio using pyaudio and saves it to SENTIMENT.wav. There's a few options that you can set to change length of recording, bit rate, etc. Read more about it on the [docs](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.open)

```
transcription.speech_to_text.py
```
Sends recorded audio (SENTIMENT.wav) to Watson's Speech-to-Text API. Results from the API are in chunks, so there's a function to concatenate the final transcription.

**To Do**
- [] Find a way to transcribe faster (explore WebSocket vs. synchronous HTTP vs. async HTTP)

### Sentiment Module
```
sentiment.analyze_speech.py
```
Basically just refactored [Vokaturi API example code](https://developers.vokaturi.com/using/python-sample)

```
sentiment.analyze_text.py
```
Sends transcript to Natural Language Understanding API. Ngl, don't remember what some of the functions do so if anyone wants to figure it out that'd be cool! This is the spot where we can do keyword/entity/concept extraction. Check out the docs for more info or [the demo](https://natural-language-understanding-demo.ng.bluemix.net/)

**To Do**
- [] Figure out what handle_sentiment() and find_emotions() does
- [] Explore entity + keyword extraction with API options

### Music Module
```
music.spotify.py
```
Contains all the API endpoints to control playing music. Also has a function to automatically generate tracklists based on seed genres and attributes.

**To Do**
- [] Research music theory related to the different tunable attributes + genres offered by Spotify
- [] Implement logic for generating genres based on the emotion from sentiment analysis
- [] Implement logic for generating min_tunable attributes based on sentiment analysis results
- [] Implement logic for generating max_tunable attributes based on sentiment analysis results

### api Folder
Vokaturi stuff, don't touch this

### Templates
```
index.html
```
The "front end" code. Really ugly and currently just displays a table with different outputs from each step.

**To Do**
???
We'll probably need tests/refactoring at some point so we can run all the modules separately


## Resources
- https://github.com/watson-developer-cloud/python-sdk
- https://cloud.ibm.com/docs/services/speech-to-text
- https://cloud.ibm.com/apidocs/speech-to-text/speech-to-text
- https://cloud.ibm.com/docs/services/natural-language-understanding
- https://cloud.ibm.com/apidocs/natural-language-understanding/natural-language-understanding
- https://developer.spotify.com/documentation/web-api/reference/browse/get-recommendations/
