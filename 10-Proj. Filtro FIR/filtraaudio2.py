# -*- coding: utf-8 -*-
""" File...: filtraaudio2.py
    Do.....: filtra áudio gravado em arquivo .wav com FPB, fc = 1,2 kHz
    Date...: Thu May 30 11:50:09 2019
    @Author: Prof. Kaw """

import numpy, pylab, scipy.signal
import os, scipy.io.wavfile, pyaudio
# print os.getcwd()
os.chdir('E:\\mdp\\Curso\\disc.s\\pds\\_Lab\\_Roteiros\\10-Projeto de Filtros FIR')

# leitura do sinal de entrada do filtro
fs, x = scipy.io.wavfile.read('1324.wav')
Ns = len(x)                        # qtde de amostras do sinal original

# Tocando o sinal de entrada...
porta = pyaudio.PyAudio()          # criando uma ligação com a placa de áudio
fluxo = porta.open(format = porta.get_format_from_width(x[0].nbytes),
                   channels = 1, rate = fs, output = True) # fluxo de bits de áudio
fluxo.write(x, Ns)                 # envia arquivo de áudio para placa de áudio
fluxo.close()                      # finaliza fluxo de bits
porta.terminate()                  # finaliza ligação com a placa de áudio

# Espectro de magnitude do sinal original, 'x'
X = numpy.fft.fft(x)/Ns

# Filtrando o sinal 'x'
# fpb FIR projetado com janela de Hanning, N = 82, fs = 16 kHz
b =   [ -3.32068167e-04,  -1.90797017e-04,   4.81271714e-19,
         2.08803781e-04,   3.96750328e-04,   5.21909714e-04,
         5.46164320e-04,   4.44282762e-04,   2.13492030e-04,
        -1.19251950e-04,  -4.95493105e-04,  -8.31538250e-04,
        -1.03351754e-03,  -1.01945575e-03,  -7.43903791e-04,
        -2.18739070e-04,   4.76702204e-04,   1.20149406e-03,
         1.77692860e-03,   2.02554567e-03,   1.81787026e-03,
         1.11574783e-03,  -1.97170777e-18,  -1.32788135e-03,
        -2.57515086e-03,  -3.41611075e-03,  -3.56908770e-03,
        -2.87532435e-03,  -1.35984572e-03,   7.44121790e-04,
         3.01911484e-03,   4.93724016e-03,   5.97294799e-03,
         5.73257730e-03,   4.07115243e-03,   1.16591617e-03,
        -2.47753955e-03,  -6.09759101e-03,  -8.82095808e-03,
        -9.85466250e-03,  -8.68660914e-03,  -5.24879089e-03,
         4.57735440e-18,   6.10186842e-03,   1.17462802e-02,
         1.55178286e-02,   1.62031834e-02,   1.30972634e-02,
         6.24225391e-03,  -3.45948927e-03,  -1.42968066e-02,
        -2.39727672e-02,  -2.99718911e-02,  -3.00122158e-02,
        -2.25009193e-02,  -6.90539607e-03,   1.60377170e-02,
         4.43263125e-02,   7.49219110e-02,   1.04174182e-01,
         1.28372724e-01,   1.44331652e-01,   1.49903728e-01,
         1.44331652e-01,   1.28372724e-01,   1.04174182e-01,
         7.49219110e-02,   4.43263125e-02,   1.60377170e-02,
        -6.90539607e-03,  -2.25009193e-02,  -3.00122158e-02,
        -2.99718911e-02,  -2.39727672e-02,  -1.42968066e-02,
        -3.45948927e-03,   6.24225391e-03,   1.30972634e-02,
         1.62031834e-02,   1.55178286e-02,   1.17462802e-02,
         6.10186842e-03,   4.57735440e-18,  -5.24879089e-03,
        -8.68660914e-03,  -9.85466250e-03,  -8.82095808e-03,
        -6.09759101e-03,  -2.47753955e-03,   1.16591617e-03,
         4.07115243e-03,   5.73257730e-03,   5.97294799e-03,
         4.93724016e-03,   3.01911484e-03,   7.44121790e-04,
        -1.35984572e-03,  -2.87532435e-03,  -3.56908770e-03,
        -3.41611075e-03,  -2.57515086e-03,  -1.32788135e-03,
        -1.97170777e-18,   1.11574783e-03,   1.81787026e-03,
         2.02554567e-03,   1.77692860e-03,   1.20149406e-03,
         4.76702204e-04,  -2.18739070e-04,  -7.43903791e-04,
        -1.01945575e-03,  -1.03351754e-03,  -8.31538250e-04,
        -4.95493105e-04,  -1.19251950e-04,   2.13492030e-04,
         4.44282762e-04,   5.46164320e-04,   5.21909714e-04,
         3.96750328e-04,   2.08803781e-04,   4.81271714e-19,
        -1.90797017e-04,  -3.32068167e-04]
a = [1.]
y = scipy.signal.lfilter(b,a,x)
yy = numpy.int16(y)

# Tocando o sinal de saída...
porta = pyaudio.PyAudio()          # criando uma ligação com a placa de áudio
fluxo = porta.open(format = porta.get_format_from_width(yy[0].nbytes),
                   channels = 1, rate = fs, output = True) # fluxo de bits de áudio
fluxo.write(yy, Ns)                # envia arquivo de áudio para placa de áudio
fluxo.close()                      # finaliza fluxo de bits
porta.terminate()                  # finaliza ligação com a placa de áudio

# Espectro de magnitude do sinal filtrado, 'y'
Y = numpy.fft.fft(yy)/Ns
W = numpy.arange(0,Ns/2)*fs/float(Ns)
# Gráficos
print "Elaborando gráficos..."
''' espera longa demais para traçar com 'stem', que seria o correto...'''
pylab.subplot(211); pylab.plot(W,numpy.abs(X[:Ns/2])); pylab.title('Original')
pylab.subplot(212); pylab.plot(W,numpy.abs(Y[:Ns/2])); pylab.xlabel('freq. (Hz)')
pylab.title('Filtrado'); pylab.show()