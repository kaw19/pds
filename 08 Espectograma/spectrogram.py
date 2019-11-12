# -*- coding: utf-8 -*-
"""
Spectrogram of sinus
@author: Kaw
"""
#!/usr/bin/env python
from pylab import subplot, plot, ylabel, title, xlabel, show, specgram, cm, figure
from numpy import arange, where, sin, pi, logical_and, logical_or, fft, linspace
from numpy.random import randn


Fs = 500                    # a frequência de amostragem em Hz
dt = 1./Fs
t = arange(0.0, 20.0, dt)
s1 = sin(2*pi*10*t)         # sinal de 10 Hz
s2 = 5*sin(2*pi*40*t)       # sinal de 40 Hz

# cria um zunido (chirp) transitório
mask1 = where(logical_or(t<10, t>15), 1.0, 0.0)
s1 = s1 * mask1
mask2 = where(logical_and(t>10, t<15), 1.0, 0.0)
s2 = s2 * mask2
nse = 0.01*randn(len(t))    # adiciona algum ruído na mistura
x = s1 + s2 #+ nse           # o sinal final
N = 256                  # o comprimento das janelas dos segmentos

X = fft.fft(x)
freq = linspace(0,Fs/2.,int(Fs/2.*20))

# Pxx é a matriz de 'segmentos' x 'freqs' da potência instantânea, 'freqs' é
# vetor frequência, 'bins' são os centros dos intervalos de tempo nos quais
# a potência é calculada, e 'im' é o objeto matplotlib.image.AxesImage
figure()
ax1 = subplot(311); plot(t,x); ylabel('Amplitude'); title('Espectrograma')
#subplot(312); plot(freq,2*abs(X[:len(X)/2]))
subplot(313,sharex=ax1)
Pxx,freqs,bins,im = specgram(x,NFFT=N,Fs=Fs,cmap=cm.gist_heat)
title(u'Soma de Senos de 10 e 40 Hz e ruído gaussiano')
xlabel('tempo (s)'); ylabel(u'frequência (Hz)')
show()