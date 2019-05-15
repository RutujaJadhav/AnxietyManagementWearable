# mysp=__import__("my-voice-analysis")
from pydub import AudioSegment
from my_audio_analysis import *
import os
import pyrebase
import pyaudio
import wave
import numpy as np
from datetime import datetime
import contextlib

# os.chdir("/Users/louis/Google Drive/adele-rutuja-louis/data/")


def record_audio(duration, chunk = 1024, channels = 2, rate = 44100, outfile = "output.wav"):
    FORMAT = pyaudio.paInt16  # declare audio format
    p = pyaudio.PyAudio()   # initialize PyAudio object

    # Open audio stream with declared options
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("* started recording")

    frames = [] # initialize array to contain audio data

    # Set loop to execute for desired recording length
    for i in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)  # read audio data
        frames.append(data)     # append recorded audio data to array

    print("* done recording")
    stream.stop_stream() # stop audio stream
    stream.close()  # close audio stream
    p.terminate()   # terminate PyAudio object

    wf = wave.open(outfile, 'wb')  # declare .wav output file
    wf.setnchannels(channels)   # set number of audio output channels
    wf.setsampwidth(p.get_sample_size(FORMAT))  # set sample width for recording
    wf.setframerate(rate)   # set recording frame rate
    wf.writeframes(b''.join(frames))    # write recorded audio from array to .wav file
    wf.close()  # close .wav file

def calculate_features(file, audio_path):
    if ".wav" in file:   # if filename still contains ".wav" extract just the filename
        filename = file.split(".wav")[0]
    
    with contextlib.closing(wave.open(str(audio_path + '/' + file),'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        seconds = int(frames / float(rate))
        minutes = int(round((frames / float(rate))/60, 0))
        duration = str(minutes) + ":" + str(seconds)

    pronunciation = mysppron(filename, audio_path)      #Calculate the pronunciation posteriori probablity score
    articulation = myspatc(filename, audio_path)    # Calculate the articulation (speed) syllables/sec
    filler = mysppaus(filename, audio_path)     # Calculate the number of pauses/filler words used
    speech_rate = myspsr(filename, audio_path)    # Calculate the rate of speech
    
    features = {'pronunciation' : pronunciation, 'articulation' : articulation, 'filler' : filler, 'speech_rate' : speech_rate, "duration" : duration}
    return features
