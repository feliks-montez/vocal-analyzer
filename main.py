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

def compare():
  mic = Microphone()
  mic.record_to_file(1, 'person1.wav')
  input('press enter to record the second person')
  mic.record_to_file(1, 'person2.wav')

  rate, data1 = wavfile.read('person1.wav')
  rate, data2 = wavfile.read('person2.wav')

  data1_fft = numpy.fft.fft(data1) # calculate fourier transform (complex numbers list)
  data2_fft = numpy.fft.fft(data2)
  freq1 = (numpy.abs(data1_fft[:len(data1_fft)]))
  freq2 = (numpy.abs(data2_fft[:len(data2_fft)]))

  plt.subplots_adjust(hspace=0.5)
  plt.subplot(2,1,1)
  plt.plot(data1,'r',data2,'c')
  plt.title("Original from %s" % (input_file))
  
  plt.subplot(2,1,2)
  plt.plot(freq1,'r',freq2,'c') 
  plt.title("Fourier output")
  plt.xlim(20, 20_000)
  plt.xscale('log')
  plt.show()

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

  if (input_file == 'compare'):
    compare()
  else:
    # speaker = Speaker()
    # speaker.play_file(input_file)
      
    rate, data = wavfile.read(input_file)

    data_fft = numpy.fft.fft(data) # calculate fourier transform (complex numbers list)
    freq = (numpy.abs(data_fft[:len(data_fft)]))

    plt.subplots_adjust(hspace=0.5)
    plt.subplot(2,1,1)
    plt.plot(data,'r')
    plt.title("Original from %s" % (input_file))
    
    plt.subplot(2,1,2)
    plt.plot(freq,'r') 
    plt.title("Fourier output")
    plt.xlim(20, 20_000)
    plt.xscale('log')
    plt.show()
