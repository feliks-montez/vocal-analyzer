import pyaudio 
import wave

class Microphone():
  RECORD_SECONDS = 2
  WAVE_OUTPUT_FILENAME = "output.wav"
  
  def __init__(self, chunk_size=1225, format=pyaudio.paInt16, channels=1, rate=44100):
    # chunk_size=1225 because rate=44100 is a multiple of it
    self.chunk_size = chunk_size #ADC information [8 bit = 2⁸ steps]
    self.format = format # pyaudio.paInt16 means 16-bit encoding
    self.channels = channels
    self.rate = rate # sample rate
    self.p = pyaudio.PyAudio()
    
    print("----------------------record device list---------------------")
    info = self.p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                if (self.p.get_device_info_by_host_api_device_index(0, i).get('name') == 'pulse'): self.device_index = i
                print("Input Device id ", i, " - ", self.p.get_device_info_by_host_api_device_index(0, i).get('name'))

    print("-------------------------------------------------------------")

    if (not self.device_index): self.device_index = int(input("Use which device index? "))
    print("using input device %i" % self.device_index)
    
  def record(self, seconds=RECORD_SECONDS):
    stream = self.p.open(format=self.format,
      channels=self.channels,
      rate=self.rate,
      input=True,
      input_device_index=self.device_index,
      frames_per_buffer=self.chunk_size) #buffer
      
    print("* recording")
    frames = []
    for i in range(0, int(self.rate / self.chunk_size * seconds)):
      data = stream.read(self.chunk_size)
      frames.append(data) # 2 bytes(16 bits) per channel
    print("* done recording")

    stream.stop_stream()
    stream.close()
    
    return frames
  
  def record_chunk(self):
    stream = self.p.open(format=self.format,
      channels=self.channels,
      rate=self.rate,
      input=True,
      input_device_index=self.device_index,
      frames_per_buffer=self.chunk_size) #buffer
      
    data = stream.read(self.chunk_size)

    stream.stop_stream()
    stream.close()
    
    return data
    
  def record_to_file(self, seconds, filename=WAVE_OUTPUT_FILENAME):
    frames = self.record(seconds)
    
    wf = wave.open(filename, 'wb')
    wf.setnchannels(self.channels)
    wf.setsampwidth(self.p.get_sample_size(self.format))
    wf.setframerate(self.rate)
    wf.writeframes(b''.join(frames))
    wf.close()
