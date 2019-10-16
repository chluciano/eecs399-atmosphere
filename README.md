If you have 2 versions of python installed you might have to do this

`
python3 -m venv env
source env/bin/activate
pip3 install ibm_watson ibm_cloud_sdk_core Flask pyaudio wave 
python3 spotify.py
`
Anytime you want to run the program:
cd into repo
`
source env/bin/activate
python3 spotify.py
`




Otherwise just do this
`
python -m venv env
source env/bin/activate
pip install ibm_watson ibm_cloud_sdk_core Flask pyaudio wave 
python spotify.py
`
Anytime you want to run the program:
cd into repo
`
source env/bin/activate
python spotify.py
`

