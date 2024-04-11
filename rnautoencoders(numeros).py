# -*- coding: utf-8 -*-
"""RNautoencoders(numeros).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1seoBgJV9yslOpNbtgyqDwW8XkduoIw1M
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.datasets import mnist
from tensorflow.keras.callbacks import EarlyStopping

(Xtrain, _), (Xtest, _) = mnist.load_data()

Xtrain = Xtrain.astype('float32') / 255.0
Xtest = Xtest.astype('float32') / 255.

# Crear columna
Xtrain = Xtrain.reshape((len(Xtrain), np.prod(Xtrain.shape[1:])))
Xtest = Xtest.reshape((len(Xtest), np.prod(Xtest.shape[1:])))

# Dimensión de capas
inputImg = Input(shape = (784,))

edim = 32

# Capa 1
encoded = Dense(edim, activation = 'relu')(inputImg)

# Capa 2
decoded = Dense(784, activation = 'sigmoid')(encoded)

# Reconstrucción
autoencoder = Model(inputImg, decoded)

# Entrenar red neuronal

# Early Stopping
EarlyStopping = EarlyStopping(monitor='val_loss', patience=5)

# Compilar modelo
autoencoder.compile(optimizer = 'adam', loss = 'binary_crossentropy')

# Entrenamiendo de autoenconder
autoencoder.fit(Xtrain, Xtrain, epochs = 50, batch_size = 256, shuffle = True, validation_data = (Xtest, Xtest), callbacks = [EarlyStopping])

# Recontruir imagen
decodedImg = autoencoder.predict(Xtest)

# Grafica
n = 10
plt.figure(figsize = (20, 4))

for i in range(n):
  x = plt.subplot(2, n, i + 1)
  plt.imshow(Xtest[i].reshape(28, 28))
  plt.gray()
  x.get_xaxis().set_visible(False)
  x.get_yaxis().set_visible(False)

  # Imagen recontruida
  x = plt.subplot(2, n, i + 1 + n)
  plt.imshow(Xtest[i].reshape(28, 28))
  plt.gray()
  x.get_xaxis().set_visible(False)
  x.get_yaxis().set_visible(False)

plt.show