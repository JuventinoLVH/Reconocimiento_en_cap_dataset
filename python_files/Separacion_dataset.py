"""
    Primer archivo a ejecutar:
    Antes de ejecutar este archivo se necesita localizar la carpeta con el database y crear 3 carpetas, test_dataset, train_dataset y unused_dataset. El archivo se encarga de crear enlaces simbolicos de los archivos en la base de datos a la respectiva carpeta.  
    Las carpetas estan estratificadas y tienen una proporcion de 70-30 para los archivos con patologia y sin patologia. respectivamente.


"""
## Imports
# Funciónes mágicas para re-importar los modulos
%load_ext autoreload
%autoreload 2

from matplotlib import pyplot as plt
from pathlib import Path
import numpy as np
import mne 

from scipy.linalg import toeplitz, solve_toeplitz
from scipy.signal import butter, filtfilt, iirnotch
from scipy import signal

import os  
from os.path import isfile, join
from python_files.preprocesamiento import Preprocesamiento

## Funciones de utileria
    def Discriminar_tipo_archivo(archivo, tipo):
        archivo = archivo.split('/')[-1]
        len_tipo = len(tipo)
        if archivo[:len_tipo] == tipo and archivo[len_tipo] in ['0','1','2','3','4','5','6','7','8','9']:
            return True
        return False

    def Mover_archivo(archivo, destino):
        nombre_archivo  = archivo.split('/')[-1]
        destino_archivo = destino / nombre_archivo

        os.symlink(archivo, destino_archivo)

    def Intentar_preload_archivo(archivo):
        DATA_FILE       = mne.io.read_raw_edf(archivo, preload=True)

        todos   = True
        uno     = True
        try:
            for channel in CANALES_USADOS:
                aux = DATA_FILE[channel]

        except Exception as e:
            todos = False

        try:
            aux = DATA_FILE[CANAL_USADO]
            archivo_un_canal.append(archivo)
        except Exception as e:
            uno = False

        return todos, uno

    def Obtener_archivos_disponibles():
        archivos_todos      = []
        archivo_un_canal    = [] 

        for archivo in REGISTROS:
            DATA_FILE       = mne.io.read_raw_edf(archivo)

            try:
                for channel in CANALES_USADOS:
                    aux = DATA_FILE[channel]
                archivos_todos.append(archivo)
            except Exception as e:
                None

            try:
                aux = DATA_FILE[CANAL_USADO]
                archivo_un_canal.append(archivo)
            except Exception as e:
                None
        return archivos_todos, archivo_un_canal
## 

## ARCHIVO CON LOS DATOS DEL DATASET
if __name__ == "__main__":
    CAP_DATABASE    = Path.home() / "Maestria" / "Primer_semestre" / "PDS" / "databases" / "CAP_database"
    CAP_TEST        = CAP_DATABASE / "test_dataset"
    CAP_TRAIN       = CAP_DATABASE / "train_dataset"
    CAP_UNUSED      = CAP_DATABASE / "unused_dataset"

    REGISTROS       = [join(CAP_DATABASE,f) for f in list(CAP_DATABASE.iterdir()) if isfile(join(CAP_DATABASE, f))]

    TIPO_ARCHIVO    = ['brux', 'sdb', 'rbd', 'plm', 'nfle', 'narco', 'n', 'ins']
    CANALES         = ['ROC-LOC', 'Fp2-F4','F4-C4', 'C4-P4', 'C4-A1', 'P4-O2', 'EMG1-EMG2', 'ECG1-ECG2']
    CANALES_USADOS  = [CANALES[2], CANALES[3], CANALES[4], CANALES[5] ]
    CANAL_USADO     = CANALES[2]

## EJEMPLO Vamos a crear un symlink para el archivo de prueba
    INDICE_PRUEBA   = 61
    DIR_ARCHIVO     = REGISTROS[ INDICE_PRUEBA ]
    
    DATA_ARCHIVO    = mne.io.read_raw_edf(DIR_ARCHIVO)
## Checamos los archivos que no tienen el canal objetivo
    archivos_todos, archivo_un_canal = Obtener_archivos_disponibles()

### Abrimos los archivos que no se pudieron abrir sin el preload
    v_no_todos          = []
    v_no_uno            = []
    for archivo in REGISTROS:
        if archivo not in archivos_todos:
            todos , uno = Intentar_preload_archivo(archivo)
            if not todos:
                v_no_todos.append(archivo)
            if not uno:
                v_no_uno.append(archivo)

## Movemos los archivos que no se pudieron abrir
    for archivo in REGISTROS:
        if archivo in v_no_uno:
            Mover_archivo(archivo, CAP_UNUSED)
## Nos quedamos con los archivos que si se pudieron abrir y los separamos los que presentan patologia
    REGISTROS_UTILES    = [archivo for archivo in REGISTROS if archivo not in v_no_uno]
    R_PATOLOGIA         = [archivo for archivo in REGISTROS_UTILES if not Discriminar_tipo_archivo(archivo, 'n')] 
    R_NO_PATOLOGIA      = [archivo for archivo in REGISTROS_UTILES if Discriminar_tipo_archivo(archivo, 'n')]
    R_PATOLOGIA
## Separacion de los archivos en train y test con proporcion ~ 70-30
    np.random.seed(42)
    np.random.shuffle(R_PATOLOGIA)
    np.random.shuffle(R_NO_PATOLOGIA)

    train_p = R_PATOLOGIA[:int(0.7*len(R_PATOLOGIA))]
    test_p  = R_PATOLOGIA[int(0.7*len(R_PATOLOGIA)):]

    train_n = R_NO_PATOLOGIA[:int(0.7*len(R_NO_PATOLOGIA))]
    test_n  = R_NO_PATOLOGIA[int(0.7*len(R_NO_PATOLOGIA)):]

    for archivo in train_p:
        Mover_archivo(archivo, CAP_TRAIN)

    for archivo in test_p:
        Mover_archivo(archivo, CAP_TEST)

    for archivo in train_n:
        Mover_archivo(archivo, CAP_TRAIN)

    for archivo in test_n:
        Mover_archivo(archivo, CAP_TEST)
## Se revisa el tamaño de los conjuntos
    print(len(train_p), ' : ', len(test_p), ' : ', len(train_n), ' : ', len(test_n))
