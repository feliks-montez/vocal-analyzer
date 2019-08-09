#! /usr/bin/python3

import numpy
import time
import pyaudio
import sys
import wave
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
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

  if (input_file == 'record'):
    mic = Microphone()
    mic.record_to_file(1, 'output.wav')
    input_file = 'output.wav'
  
  speaker = Speaker()
  speaker.play_file(input_file)
    
  rate, data = wavfile.read(input_file)

  plt.subplots_adjust(hspace=0.5)
  plt.subplot(2,1,1)
  plt.plot(data)
  plt.title("Original from %s" % (input_file))

  data_fft = numpy.fft.fft(data) # calculate fourier transform (complex numbers list)
  freq = (numpy.abs(data_fft[:len(data_fft)]))
  
  plt.subplot(2,1,2)
  plt.plot(freq,'r') 
  plt.title("Fourier output")
  plt.xlim(20, 20_000)
  plt.xscale('log')
  plt.show()
