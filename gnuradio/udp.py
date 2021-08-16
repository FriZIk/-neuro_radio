import pyaudio
import socket

host = '127.0.0.1'
port = 7355
chunk = 2048
rate = 48000
channels = 1
sample_format = pyaudio.paInt16

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port)) # Connect to socket

p = pyaudio.PyAudio() # Create an interface to PortAudio

stream = p.open(format=sample_format,
                channels=channels,
                rate=rate, # record at 48000 samples per second
                output=True)

data, addr = s.recvfrom(chunk) # buffer size is 1024 bytes

while data != '':
    stream.write(data)
    data, addr = s.recvfrom(chunk) # buffer size is 1024 bytes

stream.stop_stream()
stream.close()

p.terminate()