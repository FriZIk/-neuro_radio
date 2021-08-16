# Dependencies

## Apt

```
sudo apt install python3-pip
sudo apt install python3-pyaudio
sudo apt install gnuradio (3.8)
sudo apt install gr-osmosdr
sudo apt install pulseaudio
```

## Pip
```
pip3 install vosk
```

## Pulseaudio

You can add a sink with

```
pacmd load-module module-null-sink sink_name=MySink
pacmd update-sink-proplist MySink device.description=MySink
```

You can add a loopback device with the command

```
pacmd load-module module-loopback sink=MySink
```

