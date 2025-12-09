"""
    Segundo archivo necesario de ejecucion

    -> Cuando se llama ha ejecutar como script, se calculan los eventos de todos los archivos en la base de datos de entrenamiento.

    -> La función principal es Procesar_archivo, la cual es útil cuando se necesite calcular los eventos del conjunto de prueba.
"""
# DATA_FILE mágicas para re-importar los modulos

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
from joblib import Parallel, delayed
## Funciones de utileria
def Abrir_archivo_señales(archivo, CANAL_USADO):
    try:
        DATA_FILE       = mne.io.read_raw_edf(archivo)
        aux = DATA_FILE[CANAL_USADO]
        return DATA_FILE
    except Exception as e:
        DATA_FILE       = mne.io.read_raw_edf(archivo, preload=True)
        aux = DATA_FILE[CANAL_USADO]
        return DATA_FILE

def Procesar_archivo(archivo,CANAL_USADO,CAP_EVENTOS,save=True):
        file_name       = archivo.name
        file_name       = file_name.split('.')[0]

        ARCHIVO_P = Abrir_archivo_señales(archivo,CANAL_USADO)
        data , tiempo   = ARCHIVO_P[CANAL_USADO]
        data = data[0]

        file_freq       = int(ARCHIVO_P.info["sfreq"])

        eventos_altos, eventos_bajos    = Eventos_de_la_señal (tiempo,data,  file_freq)

        if save:
            np.savez( CAP_EVENTOS / file_name, eventos_bajos= eventos_bajos, eventos_altos= eventos_altos)
        return eventos_altos, eventos_bajos

## ARCHIVO CON LOS DATOS DEL DATASET
if __name__ == "__main__":
    CAP_TRAIN_DB    = Path.home() / "Maestria" / "Primer_semestre" / "PDS" / "databases" / "CAP_database" / "train_dataset"
    CAP_EVENTOS     = Path.home() / "Maestria" / "Primer_semestre" / "PDS" / "databases" / "CAP_database" / "eventos_train"
    REGISTROS       = list(CAP_TRAIN_DB.iterdir())

    TIPO_ARCHIVO    = ['brux', 'sdb', 'rbd', 'plm', 'nfle', 'narco', 'n', 'ins']
    CANALES         = ['ROC-LOC', 'Fp2-F4','F4-C4', 'C4-P4', 'C4-A1', 'P4-O2', 'EMG1-EMG2', 'ECG1-ECG2']
    CANAL_USADO     = CANALES[2]


## Archivo de prueba
    for archivo in REGISTROS:
        try:
            Procesar_archivo(archivo,CANAL_USADO,CAP_EVENTOS)
        except Exception as e:
            print(archivo)
            print(e)
            continue

### Archivo de prueba
    Parallel(n_jobs=6)(delayed(Procesar_archivo)(archivo,CANAL_USADO,CAP_EVENTOS) for  archivo in tqdm(REGISTROS))

### Archivo de prueba
#    archivo_prueba  = REGISTROS[0]
#    archivo_prueba
#    ARCHIVO_data    = Abrir_archivo_señales(archivo_prueba)
#    data , tiempo = ARCHIVO_data[CANAL_USADO]
#    data = data[0]
#    file_freq       = int(ARCHIVO_data.info["sfreq"])
#    eventos_altos, eventos_bajos    = Eventos_de_la_señal (tiempo,data,  file_freq)
