## Proyecto :  Clasificación de patologías del sueño. 

   El proyecto se inspiro en la base de datos presentada en
           `https://archive.physionet.org/physiobank/database/capslpdb/`
   Donde se teorisa que las patologías del sueño pueden ser clasificadas analizando los ciclos CAP del sueño.
   Los ciclos CAP son patrones de actividad cerebral que ocurren durante el sueño no REM y se caracterizan por una
   alternancia entre fases de activación (fase A) y fases de estabilidad (fase B). 
   La fase A representa *eventos* de activación cerebral, mientras que la fase B se interpreta como un evento de
   calma o estabilidad.

   Parte de la hipótesis del proyecto es que se pueden reconocer los ciclos CAP automaticamente ( Mediante
   reconocer los eventos ). La otra hipótesis es que se puede clasificar las patologías del sueño a partir de las
   los eventos. 
   En esté proyecto se implemento un clasificador ( K-means ) que intenta agrupar los eventos. Para
   agrup
  
   La base de datos se recupero de :
           `https://physionet.org/content/capslpdb/1.0.0/` 
   Cada tipo de archivo tiene 92 registros, de los cuales 16 no tienen patologías y el resto si. 
   Hay 7 diferentes tipos de patologías, pero las clases tienen mucho desvalance entre ellas.

   NOTE: EL archivo main NO se debe de ejecutar primeramente. Antes hay que procesar los archivos de la base de
   datos. Para esto hay que ejecutar los scripts en el siguiente orden:
    1. Separacion_dataset.py
    2. Extractor_de_eventos.py


## Estructura del proyecto

```  
├── Bibliografia
│   └── Documentación hacerca de los patrones de suño
├── main.py ( Archivo que lee los archivos de caracteristicas y ejecuta el clasificador )
├── python_files
│   ├── Clasificador.py         
│   ├── Deteccion_CAP.py                    <- Detección de eventos CAP
│   ├── EDA.py                              <- Análisis exploratorio de datos ( Plots )
│   ├── Extracción_de_caracteristicas.py    <- Extrae las características del CAP a partir de los eventos
│   ├── Extractor_de_eventos.py             <- Segundo archivo a ejecutar
│   ├── preprocesamiento.py                 <- Preprocesamiento de señales
│   ├── Separacion_dataset.py               <- Primer archivo a ejecutar
│   └── ventaneo_de_db.py
├── Reporte_de_proyecto.pdf
└── requeriments.txt
```  

