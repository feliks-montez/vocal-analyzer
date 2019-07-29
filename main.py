#! /usr/bin/python3

import numpy
import time
import pyaudio
import sys
import wave
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
from microphone import Microphone
from speaker import Speaker

CHUNK_SIZE = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

flatten = lambda l: [item for sublist in l for item in sublist]

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("Plays a wave file.\n\n" +\
      "Usage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)
  input_file = sys.argv[1]

  mic = Microphone()
  mic.record_to_file(1, 'output.wav')
  input_file = 'output.wav'
  
  speaker = Speaker()
  speaker.play_file(input_file)
    
  rate, data = wavfile.read(input_file)

  b=[(point/2**8.)*2-1 for point in data] # this is 8-bit track, b is now normalized on [-1,1)
  c = fft(b) # calculate fourier transform (complex numbers list)
  d = int(len(c)/2)  # you only need half of the fft list (real signal symmetry)
  plt.plot(abs(data[:(d-1)]),abs(c[:(d-1)]),'r') 
  plt.show()
