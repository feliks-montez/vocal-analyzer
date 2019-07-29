import pyaudio 
import wave


class Speaker():
    CHUNK = 1024
  
    def __init__(self):
        self.p = pyaudio.PyAudio()

    def play_file(self, file_name):
        wf = wave.open(file_name)

        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True)

        data = wf.readframes(self.CHUNK)

        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(self.CHUNK)