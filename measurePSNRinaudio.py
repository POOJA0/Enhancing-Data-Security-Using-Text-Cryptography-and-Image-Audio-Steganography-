from scipy.io import wavfile
from math import log10, sqrt

import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

samplerate, y1 = wavfile.read('sample.wav')

samplerate, y2 = wavfile.read('sample.wav')

y2=y1+3;
R=len(y1)
C=2

err = sum((y1-y2)*(y1-y2))/(R*C);

e=sum(abs(err))
print(e)

MSE=sqrt(e);
MAXVAL=65535;
PSNR = 20*log10(MAXVAL/MSE);

import os
import wave

import pylab
def graph_spectrogram(wav_file):
    sound_info, frame_rate = get_wav_info(wav_file)
    pylab.figure(num=None, figsize=(19, 12))
    pylab.subplot(111)
    pylab.title('spectrogram of %r' % wav_file)
    pylab.specgram(sound_info, Fs=frame_rate)
    pylab.savefig('spectrogram.png')
def get_wav_info(wav_file):
    wav = wave.open(wav_file, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.fromstring(frames, 'int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate


graph_spectrogram('sample.wav')

