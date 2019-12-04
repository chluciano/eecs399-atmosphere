import pyaudio
import wave

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
    wav_header = genHeader(SAMPLE_RATE, BITS_PER_SAMPLE, CHANNELS)
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=SAMPLE_RATE, input=True,input_device_index=0,
                    frames_per_buffer=CHUNK)
    print ("Recording Audio...")
    frames = []
     
    for i in range(0, int(SAMPLE_RATE / CHUNK * RECORD_SECONDS)):
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
    waveFile.setframerate(SAMPLE_RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
