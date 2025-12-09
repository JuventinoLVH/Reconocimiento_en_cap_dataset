# Funciónes utilizadas a lo largo de el proyecto
import numpy as np
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from matplotlib import pyplot as plt
from pathlib import Path
from tqdm import tqdm
import numpy as np
import mne 

import pandas as pd

from scipy.linalg import toeplitz, solve_toeplitz
from scipy.signal import butter, filtfilt, iirnotch
from scipy import signal

import os  
from python_files.Extracción_de_caracteristicas import Extraer_caracteristicas_de_eventos
from python_files.Extractor_de_eventos import Procesar_archivo

## Clasificación de patologías del sueño. 
#   El proyecto se inspiro en la base de datos presentada en
#           https://archive.physionet.org/physiobank/database/capslpdb/
#   Donde se teorisa que las patologías del sueño pueden ser clasificadas analizando los ciclos CAP del sueño.
#   Los ciclos CAP son patrones de actividad cerebral que ocurren durante el sueño no REM y se caracterizan por una
#   alternancia entre fases de activación (fase A) y fases de estabilidad (fase B). 
#   La fase A representa *eventos* de activación cerebral, mientras que la fase B se interpreta como un evento de
#   calma o estabilidad.
#
#   Parte de la hipótesis del proyecto es que se pueden reconocer los ciclos CAP automaticamente ( Mediante
#   reconocer los eventos ). La otra hipótesis es que se puede clasificar las patologías del sueño a partir de las
#   los eventos. 
#   En esté proyecto se implemento un clasificador ( K-means ) que intenta agrupar los eventos. Para
#   agrup
#  
#   La base de datos se recupero de :
#           https://physionet.org/content/capslpdb/1.0.0/ 
#   Cada tipo de archivo tiene 92 registros, de los cuales 16 no tienen patologías y el resto si. 
#   Hay 7 diferentes tipos de patologías, pero las clases tienen mucho desvalance entre ellas.
#
#  NOTE: EL archivo main NO se debe de ejecutar primeramente. Antes hay que procesar los archivos de la base de
#  datos. Para esto hay que ejecutar los scripts en el siguiente orden:
#   1. Separacion_dataset.py
#   2. Extractor_de_eventos.py



if __name__ == "__main__":
    # =======================================================
    #  : : : : :    Definición de constantes   : : : : : : : 
    #  : : : : : : : : : : : : : : : : : : : : : : : : : : : 

    # _______________________________________________________
    # Rutas de los bases de datos
    
    CAP_TRAIN_DB   = Path.home() / "Maestria" / "Primer_semestre" / "PDS" / "databases" / "CAP_database" / "eventos_train"
    REGISTROS      = list(CAP_TRAIN_DB.iterdir())
    CAP_TEST_DB    = Path.home() / "Maestria" / "Primer_semestre" / "PDS" / "databases" / "CAP_database" / "test_dataset"
    REGISTROS_TEST = list(CAP_TEST_DB.iterdir())
    CAP_EVENTOS_TS = Path.home() / "Maestria" / "Primer_semestre" / "PDS" / "databases" / "CAP_database" / "eventos_test"

    # _______________________________________________________
    # Características a usar de los archivos. 
    TIPO_ARCHIVO    = ['brux', 'sdb', 'rbd', 'plm', 'nfle', 'narco', 'n', 'ins']
    CANALES         = ['ROC-LOC', 'Fp2-F4','F4-C4', 'C4-P4', 'C4-A1', 'P4-O2', 'EMG1-EMG2', 'ECG1-ECG2']
    CANAL_USADO     = CANALES[2]
    K               = 2

    # _______________________________________________________
    # Funciones de utileria para mapear el nombre del archivo a un dígito (F("sdb0.edf") -> 1 )
    def Discriminar_tipo_archivo(archivo, tipo):
        archivo = archivo.split('/')[-1]
        len_tipo = len(tipo)
        if archivo[:len_tipo] == tipo and archivo[len_tipo] in ['0','1','2','3','4','5','6','7','8','9']:
            return True
        return False

    # _______________________________________________________
    # Utileria para leer las características de los archivos procesados
    def Archivo_to_Eventos(archivo ):
        eventos_bajos =  np.load(str(archivo) )['eventos_bajos'] 
        eventos_altos =  np.load(str(archivo) )['eventos_altos'] 

        return eventos_bajos, eventos_altos, Extraer_caracteristicas_de_eventos(eventos_bajos, eventos_altos)

    # =======================================================
    #  : : : : : : : : :   Entrenamiento   : : : : : : : : : 
    #  : : : : : : : : : : : : : : : : : : : : : : : : : : : 

    # _______________________________________________________
    # Lectura de las características de los archivos procesados
    x_set       = []
    y_labels    = []
    nombres     = []
    for archivo in tqdm(REGISTROS):
        bajos,altos, caracteristicas = Archivo_to_Eventos(archivo)

        x_set.append(list(caracteristicas.values()))
        y_labels.append(int(Discriminar_tipo_archivo(archivo.name, 'n')))
        nombres.append(archivo.name) 

    # _______________________________________________________
    ## Simple k-means sobre las caracteristicas, 
    kmeans = KMeans(n_clusters=K, random_state=0)
    kmeans.fit(x_set)

    # =======================================================
    #  : : : : : : : : :   Evaluación  : : : : : : : : : : : 
    #  : : : : : : : : : : : : : : : : : : : : : : : : : : : 

    # _______________________________________________________
    ## Visualizacion de los clusters
    x = np.array(x_set)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_
    plt.scatter(x[:,0 ], x[:, 1], c=labels, cmap='viridis', marker='o', edgecolor='k')
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='x', s=200, label='Centroides')
    plt.title('Agrupamiento k-means')
    plt.xlabel('Característica 1')
    plt.ylabel('Característica 2')
    plt.legend()

    # _______________________________________________________
    ## Matriz de confucion
    y_pred = kmeans.predict(x_set)
    print(accuracy_score(y_labels, y_pred))
    print(classification_report(y_labels, y_pred))
    print(confusion_matrix(y_labels, y_pred))
    ConfusionMatrixDisplay(confusion_matrix(y_labels, y_pred)).plot()
    plt.show() 



    # =======================================================
    #  : : : : : : : : : :   Validación  : : : : : : : : : : 
    #  : : : : : : : : : : : : : : : : : : : : : : : : : : : 

    # _______________________________________________________
    ## Se procesan los archivos de test
    #  NOTE: Este bloque tarda un buen rato y solo se necesita correr una vez para generar los archivos de eventos. Se
    #  puede ejecutar cualquiera de los dos bloques (secuencial o paralelo), pero solo uno.
    #  Esto se hace así para ser transparente y que el usuario pueda ver como es el proceso de clasificación desde el
    #  archivo EDF original.    
    #
    #    # Codigo en secuencial
    #    for archivo in REGISTROS_TEST:
    #        Procesar_archivo(archivo,CANAL_USADO,CAP_EVENTOS_TS)
    #    # Codigo en paralelo
    #    Parallel(n_jobs=6)(delayed(Procesar_archivo)(archivo,CANAL_USADO,CAP_EVENTOS_TS) for  archivo in tqdm(REGISTROS_TEST))

    # _______________________________________________________
    # Lectura de los archivos
    x_test = []
    y_test = []

    CAP_EVENTOS_TS_REG = list(CAP_EVENTOS_TS.iterdir())
    for archivo in tqdm(CAP_EVENTOS_TS_REG):
        bajos,altos, caracteristicas = Archivo_to_Eventos(archivo)

        x_test.append(list(caracteristicas.values()))
        y_test.append(int(Discriminar_tipo_archivo(archivo.name, 'n')))
        nombres.append(archivo.name) 

    # _______________________________________________________
    ## Evaluamos el predictor
    y_test_pred = kmeans.predict(x_test)
    print(accuracy_score(y_test, y_test_pred))
    print(classification_report(y_test, y_test_pred))
    print(confusion_matrix(y_test, y_test_pred))
    ConfusionMatrixDisplay(confusion_matrix(y_test, y_test_pred)).plot()
    plt.show() 

    # _______________________________________________________
    ## Prueba individual con un archivo de test
    Archivo_test_prueba     = 2
    Direccion_test_prueba   = CAP_EVENTOS_TS_REG[Archivo_test_prueba]
    bajos , altos, caracteristicas   = Archivo_to_Eventos(Direccion_test_prueba)
    label   = Discriminar_tipo_archivo(Direccion_test_prueba.name,'n')
    pred    = kmeans.predict([list(caracteristicas.values())])
    print("Archivo : ", Direccion_test_prueba.name)
    print("Etiqueta : ", label)
    print("Prediccion : ", pred)
    print(caracteristicas)


