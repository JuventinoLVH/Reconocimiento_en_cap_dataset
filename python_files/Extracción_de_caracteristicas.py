"""
    Este archivo no se ejecuta.
    Contiene una única función. Cuyo dominio son los eventos bajos y altos de una señal y devuelve las características del CAP.
"""

from matplotlib import pyplot as plt
from pathlib import Path
from tqdm import tqdm
import numpy as np
import mne 

from scipy.linalg import toeplitz, solve_toeplitz
from scipy.signal import butter, filtfilt, iirnotch
from scipy import signal

import os  
from python_files.Deteccion_CAP import Eventos_de_la_señal 
## 
def Extraer_caracteristicas_de_eventos(eventos_bajos, eventos_altos):
    eventos_traslape    = np.logical_or(eventos_bajos, eventos_altos)
    eventos_and         = np.logical_and(eventos_bajos, eventos_altos)

    Tiempo_total_bajos  = np.sum(eventos_bajos) - np.sum(eventos_and)
    Tiempo_total_altos  = np.sum(eventos_altos)
    Tiempo_total_CAP    = np.sum(eventos_traslape)

    CAP_Rate            = (Tiempo_total_CAP/len(eventos_traslape)) * 100

    Bajos_Rate          = 0 if Tiempo_total_CAP == 0 else (( Tiempo_total_bajos* 100)/Tiempo_total_CAP)
    Altos_Rate          = 0 if Tiempo_total_CAP == 0 else ( Tiempo_total_altos* 100)/Tiempo_total_CAP

    Bajos_por_hora      = Tiempo_total_bajos/(60*60)
    Altos_por_hora      = Tiempo_total_altos/(60*60)
    
    # Metemos en un diccionario cada una de las caracteristicas
    resultado = {
        'CAP_Rate'      : CAP_Rate,
        'Bajos_Rate'    : Bajos_Rate,
        'Altos_Rate'    : Altos_Rate,
        'Bajos_por_hora': Bajos_por_hora,
        'Altos_por_hora': Altos_por_hora
    }

    return resultado
## 

## ARCHIVO CON LOS DATOS DEL DATASET
if __name__ == "__main__":
    CAP_TRAIN_DB     = Path.home() / "Maestria" / "Primer_semestre" / "PDS" / "databases" / "CAP_database" / "eventos_train"
    REGISTROS       = list(CAP_TRAIN_DB.iterdir())
    len(REGISTROS)

    TIPO_ARCHIVO    = ['brux', 'sdb', 'rbd', 'plm', 'nfle', 'narco', 'n', 'ins']
    CANALES         = ['ROC-LOC', 'Fp2-F4','F4-C4', 'C4-P4', 'C4-A1', 'P4-O2', 'EMG1-EMG2', 'ECG1-ECG2']
    CANAL_USADO     = CANALES[2]
    

## Archivo de prueba
    INDICE_PRUEBA   = 5
    archivo_prueba = REGISTROS[INDICE_PRUEBA]

    file_name       = REGISTROS[ INDICE_PRUEBA ].name
    file_name       = file_name.split('.')[0]

    eventos_bajos =  np.load(str(CAP_TRAIN_DB / file_name) + '.npz')['eventos_bajos'] 
    eventos_altos =  np.load(str(CAP_TRAIN_DB / file_name) + '.npz')['eventos_altos'] 

## DATOS PARA LA VENTANA
