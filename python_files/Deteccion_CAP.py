"""
    Este archivo no es para ejecutar. 
    Contiene las funciones necesarias para la detección de los eventos CAP.
    La función principal es Eventos_de_la_señal, que recibe el tiempo y la señal de un archivo y devuelve los eventos CAP encontrados
"""
from matplotlib import pyplot as plt
from pathlib import Path
import numpy as np
import math
import mne 
from tqdm import tqdm
from scipy.linalg import toeplitz, solve_toeplitz
from scipy.signal import butter, filtfilt, iirnotch
from scipy.signal import hilbert
from scipy import signal

import os  
from python_files.preprocesamiento import Preprocesamiento
### Funciones de utileria
def RMS_Threshold(segmentos):
    # Unimos los segmentos en un solo array
    segmentos = np.concatenate(segmentos)
    return np.sqrt(np.mean(segmentos**2))

##
def Eventos_por_epoca(segmentos, Fc, indice, Te):
# Calculan estadisticas de la epoca
    epoca           = np.concatenate(segmentos[indice-1:indice+2])
    segmento_central= segmentos[indice]

    S               = 1.6
    X_epoc          = np.mean(epoca)
    V_epoc          = np.var(epoca) 
    Fc_2            = Fc // 2
    
    V_segundos  = []
    V_r         = []

# se calculan la varianza del segmento central
    for i in range(0, len(segmento_central), Fc):
        segundo      = segmento_central[i:i+Fc]
        segundo_var  = np.var(segundo)
        V_segundos.append(segundo_var)
        V_r.append( segundo_var / V_epoc)
# Se reculan las varianzas ahora usando un threshold de validacion
    N_s         = [i for i in V_r if i < S]
    V_s         = np.var(N_s)

    V_rs        = [seg/V_s for seg in V_r ] 
    V_INST      = [1 if seg > Fc_2 else 0 for seg in V_rs ]

    V_INST      = [1 if seg > Fc_2 else 0 for seg in V_rs ]

# Un calculo adicional. Se calcula la envolvente de la señal
    hilbert     = signal.hilbert(segmento_central)
    parte_real  = np.real(hilbert)
    parte_img   = np.imag(hilbert)

    envolvente           =[]
    for i in range(len(segmento_central)):
        envolvente.append(math.sqrt(parte_real[i]**2 + parte_img[i]**2))
    
# Se aplica un promedio movil ponderado
    N = len(envolvente)
    M = (Fc // 2) - 1
    mitad_seg = (M + 1) // 2
    envolvente_s = np.zeros_like(envolvente)

    for k in range(mitad_seg, N - mitad_seg):
        sum_values = sum((mitad_seg - j) * (envolvente[k - j] + envolvente[k + j]) for j in range(1, mitad_seg))
        envolvente_s[k] = (sum_values + mitad_seg * envolvente[k]) / M
# Se aplica el mismo prosedimiento para sacar el promedio por segundo del segmento central
    Y_s = []
    for i in range(0, len(envolvente), Fc):
        segundo      = envolvente[i:i+Fc]
        Y_s.append(np.sum(segundo)/Fc)

# Se marca como un evento, si y solo si es un evento en ambos casos
    len(Y_s)
    for i,anotado in enumerate(V_INST):
        V_INST[i] = 1 if anotado and Y_s[i] > Te else 0

    return V_INST   
##
def Eventos_por_segundos(segmentos, Fc):
    V_INST_TOTALES  = []
    Te              = 1.5 * RMS_Threshold(segmentos)
    for i in tqdm(range(1,len(segmentos)-1)):
        V_INST = Eventos_por_epoca(segmentos, Fc, i, Te)
        V_INST_TOTALES.append(V_INST)     
    return V_INST_TOTALES
##

## Ajuste que se dio en el siguiente paper
# file:///home/juventino-lvh/Maestria/Primer_semestre/PDS/Proyecto/Bibliografia/Automatic%20Cyclic%20Alternating%20Pattern%20(CAP)%20Multitread%20Approaches.pdf
def Normalizado(eventos):
    eventos = np.concatenate(eventos)
    for i in range(1,len(eventos)-1):
        #Eventos aislados
        if(eventos[i-1] == 0 and eventos[i+1] == 0):
            eventos[i] = 0

        if(eventos[i-1] == 1 and eventos[i+1] == 1):
            eventos[i] = 1
    return eventos

def Eventos_de_la_señal(tiempo,data,fs):

    SEG_TAMAÑO                      = 30 * fs
    tiempo_v, s_baja, s_alta, s     = Preprocesamiento(tiempo,data,  SEG_TAMAÑO, fs)

    eventos_altos                   = Eventos_por_segundos(s_alta, fs )
    eventos_bajos                   = Eventos_por_segundos(s_baja, fs )
    eventos_altos_n                 = Normalizado(eventos_altos )
    eventos_bajos_n                 = Normalizado(eventos_bajos )

    return [eventos_bajos_n, eventos_altos_n ]
        
