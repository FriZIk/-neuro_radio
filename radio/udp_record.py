#!/usr/bin/env python3

import pyaudio
import socket
from vosk import Model, KaldiRecognizer
import sys
import signal

model = Model(r"/home/opencyb/neuro_radio/gnuradio/vosk-model-small-ru-0.15")
rec = KaldiRecognizer(model, 48000)

chunk = 2048
rate = 48000
channels = 1
sample_format = pyaudio.paInt16

# GNURADIO stream socket
host = '127.0.0.1'
port = 7355
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port)) # Connect to socket

# Create an interface to PortAudio
p = pyaudio.PyAudio()

# Open stream
stream = p.open(format=sample_format,
                channels=channels,
                rate=rate,
                output=True,
                frames_per_buffer=chunk)

# Ctrl+C SIGING register
def signal_handler(sig, frame):
    print('Exiting...')

    stream.stop_stream()
    stream.close()
    
    p.terminate()

    print(rec.FinalResult())
    
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Work with socket data
data, addr = s.recvfrom(chunk) # buffer size is 1024 bytes

while data != '':
    # Push data to audio stream
    stream.write(data)

    if rec.AcceptWaveform(data):
        if rec.PartialResult() != "":
            print(rec.Result())

    # Get data from stream socket
    data, addr = s.recvfrom(chunk) # buffer size is 1024 bytes

stream.stop_stream()
stream.close()

p.terminate()
