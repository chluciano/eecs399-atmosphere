import pyaudio
import wave

def record_audio():
    # Constants
    WAVE_OUTPUT_FILENAME = "SENTIMENT.wav"
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RECORD_SECONDS = 15
    CHUNK = 1024
    SAMPLE_RATE = 44100
    BITS_PER_SAMPLE = 16
    
    # Initialize recording
    audio = pyaudio.PyAudio()
    wav_header = genHeader(SAMPLE_RATE, BITS_PER_SAMPLE, channels)
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,input_device_index=0,
                    frames_per_buffer=CHUNK)
    print ("Recording Audio...")
    frames = []
     
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print( "Finished recording audio...")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
