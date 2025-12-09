"""
    Este archivo no se ejecuta.
    Archivo con las funciones necesarias para el procesamiento. 
    La función de Preprocesamiento se encarga de separar la señal en las dos bandas de interes y segmentarla en ventanas de tamaño SEG_TAMAÑO. Devuelve una lista con las ventanas de la señal segmentada en las dos bandas de interes.
"""
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import os 

from scipy.linalg import toeplitz, solve_toeplitz
from scipy.signal import butter, filtfilt, iirnotch
from scipy import signal


##
# Funcion para Filtro pasabandas
def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

def notch_filter(data, notch_freq, fs, bandwidth):
    nyquist = 0.5 * fs
    notch = notch_freq / nyquist
    b, a = iirnotch(notch, bandwidth)
    y = filtfilt(b, a, data)
    return y

def Preprocesamiento(tiempo, señal,  SEG_TAMAÑO,FS):

    def Ventaneo(señal_aux ):
        # Segmentacion con traslape del 50%
        segmentos       = []
        for i in range(0, len(señal_aux) - SEG_TAMAÑO, SEG_TAMAÑO):
            segmentos.append( señal_aux[ i: i+SEG_TAMAÑO] )
        return segmentos


    señal_alta      = bandpass_filter(señal, 7, 25, FS)
    señal_alta      = notch_filter(señal_alta, 13, FS, 4)
    señal_baja      = bandpass_filter(señal, 0.3, 4.5, FS,order=3)
        

    return Ventaneo(tiempo ), Ventaneo(señal_baja) , Ventaneo(señal_alta), Ventaneo(señal)

'''
Leyendo detenidamente el paper. No se calcula la transformada de Fourier ni se aplica la ventana de Hanning.
def Preprocesamiento(tiempo, señal,  SEG_TAMAÑO, SEG_TRASLAPE, h_alpha1, h_alpha2,FS):

    def Ventaneo(señal_aux, H_window = True):
        # Segmentacion con traslape del 50%
        segmentos       = []
        for i in range(0, len(señal_aux) - SEG_TAMAÑO, salto):
            segmentos.append( señal_aux[ i: i+SEG_TAMAÑO] )

        if(not H_window):
            return segmentos

        # Ventaneo para corregir el efecto del truncamiento
        return [ segmento * HAMING_WINDOW for segmento in segmentos ]

    señal_alta      = bandpass_filter(señal, 7, 25, FS)
    señal_alta      = notch_filter(señal_alta, 13, FS, 4)
    señal_baja      = bandpass_filter(señal, 0.3, 4.5, FS,order=3)
    salto           = int(SEG_TAMAÑO *  SEG_TRASLAPE)
    HAMING_WINDOW   = h_alpha1 - h_alpha2 * np.cos(2 * np.pi * np.arange(SEG_TAMAÑO) / (SEG_TAMAÑO - 1))
        
    ventanas_baja = Ventaneo(señal_baja)
    ventanas_alta = Ventaneo(señal_alta)

    datos_baja = []
    datos_alta = []
    for segmento in ventanas_baja:
        fft_segmento = np.fft.fft(segmento)
        datos_baja.append([segmento, fft_segmento])

    for segmento in ventanas_alta:
        fft_segmento = np.fft.fft(segmento)
        datos_alta.append([segmento, fft_segmento])

    return Ventaneo(tiempo, H_window = False), datos_baja , datos_alta
'''

