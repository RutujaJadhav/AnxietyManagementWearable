# mysp=__import__("my-voice-analysis")
from pydub import AudioSegment
from my_audio_analysis import *
import os
import pyrebase
import pyaudio
import wave
import numpy as np
import datetime
import contextlib


"""
Records audio from local mic for given duration
param: duration - length of recording; chunk - size of each audio byte (?); channels - number of channels for audio recording; rate - sampling rate of audio recording; outfile - filename for audio recording
return: no object returned, audio recording written to local working directory
"""

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

"""
Calculates the audio features of a speech
param: file - name of speech audio file, must be in .wav format; audio_path - path to speech audio file
return:  dictionary containing the audio features of the file
"""
def calculate_features(file, audio_path):
    if ".wav" in file:   # if filename still contains ".wav" extract just the filename
        filename = file.split(".wav")[0]
    
    with contextlib.closing(wave.open(str(audio_path + '/' + file),'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        seconds = int(frames / float(rate))
        duration = str(datetime.timedelta(seconds=seconds))

    pronunciation = round(mysppron(filename, audio_path),2)      #Calculate the pronunciation posteriori probablity score
    articulation = myspatc(filename, audio_path)    # Calculate the articulation (speed) syllables/sec
    filler = mysppaus(filename, audio_path)     # Calculate the number of pauses/filler words used
    speech_rate = myspsr(filename, audio_path)    # Calculate the rate of speech
    
    features = {'pronunciation' : pronunciation, 'articulation' : articulation, 'filler' : filler, 'speech_rate' : speech_rate, "duration" : duration}
    return features

""" 
Calculates the difference between the features of two speeches
param: current - dictionary containing features from current speech; previous - dictionary containing features from previous speech
return: dictionary containing percent difference between current and previous features
"""
def calculate_difference(current, previous):
    # print(previous)
    # get prev speech duration in seconds
    prev_dur = (int(previous['duration'].split(":")[1])*60) + int(previous['duration'].split(":")[2]) 

    # get curr speech duration in seconds
    curr_dur = (int(current['duration'].split(":")[1])*60) + int(current['duration'].split(":")[2]) 


    # Save difference data into dictionary
    feat_diff = {'pronunciation_diff': round(((current['pronunciation'] - previous["pronunciation"])/previous["pronunciation"]) * 100, 2),
                'articulation_diff': round(((current['articulation'] - previous["articulation"])/previous["articulation"]) * 100, 2),
                'filler_diff': round(((current['filler'] - previous["filler"])/previous["filler"]) * 100, 2),
                'speech_rate_diff': round(((current['speech_rate'] - previous["speech_rate"])/previous["speech_rate"]) * 100, 2),
                "duration_diff": round(((curr_dur - prev_dur)/prev_dur) * 100, 2)}
    
    current.update(feat_diff)
       
    return current