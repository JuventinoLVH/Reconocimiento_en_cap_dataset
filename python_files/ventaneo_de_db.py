"""
    ARCHIVO EN DES-USO
"""
## Imports
# Funciónes mágicas para re-importar los modulos
#%load_ext autoreload
#%autoreload 2

from matplotlib import pyplot as plt
from pathlib import Path
import numpy as np
import mne 

import os  
from python_files.preprocesamiento import Preprocesamiento
## ARCHIVO CON LOS DATOS DEL DATASET
if __name__ == "__main__":
    CAP_DATABASE    = Path.home() / "Maestria" / "Primer_semestre" / "PDS" / "databases" / "CAP_database"
    REGISTROS       = list(CAP_DATABASE.iterdir())

    TIPO_ARCHIVO    = ['brux', 'sdb', 'rbd', 'plm', 'nfle', 'narco', 'n', 'ins']
    CANALES         = ['ROC-LOC', 'Fp2-F4','F4-C4', 'C4-P4', 'C4-A1', 'P4-O2', 'EMG1-EMG2', 'ECG1-ECG2']
    TARGET_CHANEL   = CANALES[2]

    def Discriminar_tipo_archivo(archivo, tipo):
        len_tipo = len(tipo)
        if archivo[:len_tipo] == tipo and archivo[len_tipo] in ['0','1','2','3','4','5','6','7','8','9']:
            return True
        return False



## EDA De la forma del dataset
    num_ch          = set()
    ch_names        = set()
    frecuencias     = set()
    sin_F           = set()
    for file in REGISTROS:
        aux = mne.io.read_raw_edf(file)
        num_ch.add(len(aux.ch_names))
        frecuencias.add(aux.info["sfreq"])
        for chanel in aux.ch_names:
            ch_names.add(chanel)
## 
    num_ch
    len(ch_names)
    ch_names
    frecuencias

## Se buscan los archivos que no tengan el canal objetivo
    files_without_target = set()
    for file in REGISTROS:
        aux = mne.io.read_raw_edf(file)
        if TARGET_CHANEL not in aux.ch_names:
            files_without_target.add(file.name)

## 
    TARGET_CHANEL
    print(len(files_without_target), ' : ', files_without_target)


## Archivo de prueba
    INDICE_PRUEBA   = 3
    DATA_FILE       = mne.io.read_raw_edf(REGISTROS[ INDICE_PRUEBA ])

## 
    data , tiempo   = DATA_FILE[TARGET_CHANEL]
    data            = data[0]
    file_freq       = int(DATA_FILE.info["sfreq"])
    
    print(REGISTROS[ INDICE_PRUEBA ].name, ' : ', file_freq)
## DATOS PARA LA VENTANA
    PE_ALPHA            = 0.97
    SEG_TAMAÑO          = 30 * file_freq
    SEG_TRASLAPE        = 0.5
    h_alpha_1           = 0.54
    h_alpha_2           = 1 - h_alpha_1

    señal_procesada     = Preprocesamiento(data, PE_ALPHA, SEG_TAMAÑO, SEG_TRASLAPE, h_alpha_1, h_alpha_2)

## visualización de las ventanas
    print(len(señal_procesada)) 
    print("Cantidad de segmentos: ",len(señal_procesada)) 
    print("Tamaño de los segmentos: ",len(señal_procesada[0]))
    plt.subplot(2,2,1)
    plt.plot(señal_procesada[2])
    plt.subplot(2,2,2)
    plt.plot(señal_procesada[3])
    plt.subplot(2,2,3)
    plt.plot(señal_procesada[4])
    plt.subplot(2,2,4)
    plt.plot(señal_procesada[5])
    plt.savefig("plots/segmentos_procesados.png")
## 
