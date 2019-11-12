#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Spectrogram of an audio.wav file - Apr/2014
@author: Kaw
Adapted from: www.frank-zalkow.de/en/code-snippets/create-audio-spectrograms-with-python.html
"""
import numpy as np
from numpy.lib import stride_tricks
from matplotlib import pyplot as plt
import scipy.io.wavfile as wav

import pyaudio
import wave
import sys

CHUNK_SIZE = 1024

def play_wav(wav_filename, chunk_size=CHUNK_SIZE):
    ''' Toca no sistema de som (auto-falante) o arquivo WAV
    denominado wav_filename. '''
    try:
        print('Tocando o arquivo "' + wav_filename + '"...')
        wf = wave.open(wav_filename, 'rb')
    except IOError as ioe:
        sys.stderr.write('IOError no arquivo ' + wav_filename + '\n' + \
        str(ioe) + '. Pulando...\n')
        return
    except EOFError as eofe:
        sys.stderr.write('EOFError no arquivo' + wav_filename + '\n' + \
        str(eofe) + '. Pulando...\n')
        return
    p = pyaudio.PyAudio()                  # Instanciando PyAudio (objeto)
    # Abre o fluxo de bits (auto-falante)
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
             channels = wf.getnchannels(), rate = wf.getframerate(), output=True)
    data = wf.readframes(chunk_size)       # lendo um pedaço do arq. WAV
    while len(data) > 0:
        stream.write(data)                 # grava dados do arq. WAV no fluxo
        data = wf.readframes(chunk_size)   # lendo outro pedaço do arq. WAV    
    stream.stop_stream()                   # pára o fluxo de bits (auto-falante)
    stream.close()
    p.terminate()                          # Fecha PyAudio
    
def stft(sig, frameSize, overlapFac=0.5, window=np.hanning):
    """ transformada de fourier de curta duração de um sinal de áudio """
    win = window(frameSize)     # janela com a qtde de amostras/quadro
    hopSize = int(frameSize - np.floor(overlapFac * frameSize))  # tam. do salto
    # zeros no início (logo, o centro da primeira janela seria para a amostra nr. 0)
    samples = np.append(np.zeros(int(np.floor(frameSize/2.0))), sig)    
    # cols para aplicar a janela (janelamento)
    cols = np.int(np.ceil((len(samples) - frameSize) / float(hopSize))) + 1
    # zeros no final (logo, amostras podem ser completamente cobertas pelos quadros)
    samples = np.append(samples, np.zeros(frameSize))
    frames = stride_tricks.as_strided(samples, shape=(cols, frameSize), 
             strides=(samples.strides[0]*hopSize, samples.strides[0])).copy()
    frames *= win
    return np.fft.rfft(frames)    
    
def logscale_spec(spec, sr=44100, factor=20.):
    """ o eixo das frequências está escalado logaritmicamente """    
    timebins, freqbins = np.shape(spec)
    scale = np.linspace(0, 1, freqbins) ** factor
    scale *= (freqbins-1)/max(scale)
    scale = np.unique(np.round(scale))
    scale = scale.astype(np.int32)
    # cria o espectrograma com novos intervalos de freq (bins)
    newspec = np.complex128(np.zeros([timebins, len(scale)]))
    for i in range(0, len(scale)):
        if i == len(scale)-1:
            newspec[:,i] = np.sum(spec[:,scale[i]:], axis=1)
        else:        
            newspec[:,i] = np.sum(spec[:,scale[i]:scale[i+1]], axis=1)
    # lista a freq central dos bins
    allfreqs = np.abs(np.fft.fftfreq(freqbins*2, 1./sr)[:freqbins+1])
    freqs = []
    for i in range(0, len(scale)):
        if i == len(scale)-1:
            freqs += [np.mean(allfreqs[scale[i]:])]
        else:
            freqs += [np.mean(allfreqs[scale[i]:scale[i+1]])]
    return newspec, freqs

def plotstft(audiopath, binsize=2**10, plotpath = None, colormap = "jet"):
    """ traça o espectrograma de um arquivo WAV """
    samplerate, samples = wav.read(audiopath)
    print("Taxa de Amostragem (Arq. WAV):", samplerate, "amostra/s:")
    s = stft(samples, binsize)    # transf. de Fourier de curto prazo (quadros)
    sshow, freq = logscale_spec(s, factor = 1.0, sr = samplerate)
    ims = 20.*np.log10(np.abs(sshow)/10e-6)    # amplitude em decibel (dB)
    timebins, freqbins = np.shape(ims)
    plt.figure(figsize = (15, 7))
    plt.imshow(np.transpose(ims), origin = "lower", aspect = "auto", 
               cmap = colormap, interpolation = "none")
    plt.colorbar()                             # mostra a escala de cores
    plt.xlabel("tempo (s)"); plt.ylabel(u"frequência (Hz)")
    plt.xlim([0, timebins-1]); plt.ylim([0, freqbins])
    xlocs = np.float32(np.linspace(0, timebins-1, 5))
    plt.xticks(xlocs,["%.02f" % l for l in ((xlocs*len(samples)/timebins)+(0.5*binsize))/samplerate])
    ylocs = np.int16(np.round(np.linspace(0, freqbins-1, 10)))
    plt.yticks(ylocs, ["%.02f" % freq[i] for i in ylocs])
    if plotpath:
        plt.savefig(plotpath, bbox_inches = "tight")
    else:
        plt.show()
    # plt.clf()

plotstft("shesellsseashells.wav")
play_wav("shesellsseashells.wav")
