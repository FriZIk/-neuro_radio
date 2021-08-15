import pyaudio
import socket
import sys

frames = []
hosts = ['127.0.0.1']
port = 7355

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("127.0.0.1", 7355))

# while True:
#     soundData, addr = s.recvfrom(1500 * 2 * 1)
#     print(soundData)

# s.close()

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=48000,
                output=True)

data, addr = s.recvfrom(1024) # buffer size is 1024 bytes

while data != '':
    stream.write(data)
    data, addr = s.recvfrom(1024) # buffer size is 1024 bytes

stream.stop_stream()
stream.close()

p.terminate()