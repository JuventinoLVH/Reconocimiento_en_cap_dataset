# Funciónes mágicas para re-importar los modulos
"""
    Archivo de prueba. El clasificador implementado aquí ahora esta en el archivo de 'main.py'
"""
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

##

if __name__ == "__main__":
    CAP_TRAIN_DB     = Path.home() / "Maestria" / "Primer_semestre" / "PDS" / "databases" / "CAP_database" / "eventos_train"
    REGISTROS       = list(CAP_TRAIN_DB.iterdir())
    len(REGISTROS)

    TIPO_ARCHIVO    = ['brux', 'sdb', 'rbd', 'plm', 'nfle', 'narco', 'n', 'ins']
    CANALES         = ['ROC-LOC', 'Fp2-F4','F4-C4', 'C4-P4', 'C4-A1', 'P4-O2', 'EMG1-EMG2', 'ECG1-ECG2']
    CANAL_USADO     = CANALES[2]
    K               = 2
    

    def Discriminar_tipo_archivo(archivo, tipo):
        archivo = archivo.split('/')[-1]
        len_tipo = len(tipo)
        if archivo[:len_tipo] == tipo and archivo[len_tipo] in ['0','1','2','3','4','5','6','7','8','9']:
            return True
        return False
    def Archivo_to_Eventos(archivo ):
        eventos_bajos =  np.load(str(archivo) )['eventos_bajos'] 
        eventos_altos =  np.load(str(archivo) )['eventos_altos'] 

        return eventos_bajos, eventos_altos, Extraer_caracteristicas_de_eventos(eventos_bajos, eventos_altos)


## Archivo de prueba
    x_set       = []
    y_labels    = []
    nombres     = []
    for archivo in tqdm(REGISTROS):
        bajos,altos, caracteristicas = Archivo_to_Eventos(archivo)

        x_set.append(list(caracteristicas.values()))
        y_labels.append(int(Discriminar_tipo_archivo(archivo.name, 'n')))
        nombres.append(archivo.name) 

## Entrenamiento
    kmeans = KMeans(n_clusters=2, random_state=0)
    kmeans.fit(x_set)

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
    plt.show()

## Matriz de confucion
    y_pred = kmeans.predict(x_set)
    y_pred     
    print(accuracy_score(y_labels, y_pred))
    print(classification_report(y_labels, y_pred))
    print(confusion_matrix(y_labels, y_pred))
    ConfusionMatrixDisplay(confusion_matrix(y_labels, y_pred)).plot()
    plt.show() 

## Archivo de prueba
