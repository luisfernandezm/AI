# -*- coding: utf-8 -*-
"""Luis_Fernandez_369986_ejercicio2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aOnKNNlXUaMOvk6pMsy9xk4SZ9Ehf5K-
"""

import requests
from zipfile import ZipFile
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
import random
from keras.models import Sequential
from keras.layers import Dense, Flatten, LeakyReLU
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping

# Descomprimir el archivo
# !unzip images.zip

# Obtener las imagenes
imgRoute = '/content/DeepWeeds/DeepWeeds-master/labels/train_subset0.csv'

# Mostrar las primeras 5 imagenes del folder
!ls /content/DeepWeeds/DeepWeeds-master/labels/train_subset0.csv | head -5

# Guardar las imagenes en un array
imgs5 = [
    '20171109-175921-2.jpg',
    '20170714-142019-3.jpg',
    '20170718-101402-2.jpg'
]

# Definir el tamaño de las imagenes
plt.figure(figsize = (15, 3))

# Mostrar imagenes
for i, img5 in enumerate(imgs5):
  imgRoute = f'/content/DeepWeeds/DeepWeeds-master/labels/{img5}'
  img = Image.open(imgRoute)

  # Configuración de subplot
  plt.subplot(1, 3, i + 1)
  plt.imshow(img)
  plt.axis("off")
  plt.title(img5)

plt.tight_layout()
plt.show()

# Mostrar el otro tipo de imagenes
!ls /content/data/train/dog | head -5

# Definición de carpeta
main = '/content/data'
test = '/content/data/train'
train = '/content/data/train'
validation = '/content/data/validation'

# Preprocesamiento de datos
data = []
talla = 100
categorias = ['nativa', 'invasora']

for categoria in categorias:
  folder = os.path.join(train, categoria)
  label = categorias.index(categoria)

  for imagen in os.listdir(folder):

    #Excepto archivos gift
    if imagen.endswith('.gif'):
      continue

    imagenPath = os.path.join(folder, imagen)
    imagenArray = cv2.imread(imagenPath, cv2.IMREAD_GRAYSCALE)

    # Redimensionar la imagen
    try:
      imagenArray = cv2.resize(imagenArray, (talla, talla))
      data.append([imagenArray, label])

    except Exception as e:
      print(str(e))

# Separar imagenes y etiquetas
xTrain = []
yTrain = []

for imagenes, labels in data:
  xTrain.append(imagenes)
  yTrain.append(labels)

# Normalizar los datos
xTrain = np.array(xTrain).reshape(-1, talla, talla, 1)
yTrain = np.array(yTrain)

xTrain = xTrain / 255.0

# Entrenando la red neuronal
modelo = tf.keras.models.Sequential()
# Capa de entrada
modelo.add(tf.keras.layers.Flatten(input_shape = (talla, talla, 1)))
# Primera capa oculta
modelo.add(tf.keras.layers.Dense(256, activation = 'relu'))
# Segunda capa oculta
modelo.add(Dense(128, activation = 'swish'))
# Tercera capa de salida
modelo.add(Dense(64))
modelo.add(LeakyReLU(alpha = 0.01))
# Capa de salida
modelo.add(tf.keras.layers.Dense(2, activation = 'softmax'))
# Compilar el modelo
modelo.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics = 'accuracy')

# Early stoppings
earlyStop = EarlyStopping(monitor = 'val_loss', patience = 5, restore_best_weights = True)