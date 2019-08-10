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

def plot_fourier_compare(datasets):
  plt.subplots_adjust(hspace=0.5)
  styles = ['r-', 'c-', 'g-', 'y-', 'k-', 'm-']
  signal_names = []

  plotargs = []
  plt.subplot(2,1,1) # original signals
  for i in range(len(datasets)):
    if (not 'style' in datasets[i].keys()): datasets[i]['style'] = styles[i]
    plotargs += [datasets[i]['data'], datasets[i]['style']]
    signal_names.append(datasets[i]['title'])
  plt.plot(*plotargs,alpha=0.7)
  plt.title("Original signals")
  plt.legend(signal_names)

  plotargs = []
  plt.subplot(2,1,2) # fourier output
  for i in range(len(datasets)):
    data_fft = numpy.fft.fft(datasets[i]['data'])
    freq = (numpy.abs(data_fft[:len(data_fft)]))
    plotargs += [freq,datasets[i]['style']]
  plt.plot(*plotargs,alpha=0.7)
  plt.title("Fourier output")
  plt.xlim(20, 20_000)
  plt.xscale('log')
  plt.legend(signal_names)

  plt.show()


def plot_fourier(data):
  data_fft = numpy.fft.fft(data) # calculate fourier transform (complex numbers list)
  freq = (numpy.abs(data_fft[:len(data_fft)]))

  plt.subplots_adjust(hspace=0.5)
  plt.subplot(2,1,1)
  plt.plot(data,'r')

  plt.title("Original from " % (input_file))
  
  plt.subplot(2,1,2)
  plt.plot(freq,'r') 
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

  # speaker = Speaker()
  # speaker.play_file(input_file)

  if (input_file == 'record'):
    mic = Microphone()
    mic.record_to_file(1, 'output.wav')
    input_file = 'output.wav'
    rate, data = wavfile.read(input_file)
    plot_fourier(data)
  elif (input_file == 'compare'):
    mic = Microphone()
    datasets = []

    again = 'y'
    while (again.lower() == 'y'):
      mic.record_to_file(1, 'input.wav')
      rate, data = wavfile.read('input.wav')
      datasets.append({'title': 'sample {}'.format(len(datasets)+1), 'data': data})
      again = input('record again? (N/y) ')

    plot_fourier_compare(datasets)
