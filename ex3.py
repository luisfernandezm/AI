# -*- coding: utf-8 -*-
"""Luis_Fernandez_369986_ejercicio3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gXnxfn_6Pq61U2NOqmOrwEaZGTQErK6S
"""

# Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn .preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import yfinance as yf
from sklearn.utils import validation
from scipy.optimize import optimize

# Descarga de datos
tickers = ['BTC-USD', 'ETH-USD']
allData = {ticker: yf.download(ticker, start = '2020-01-01', end = '2023-01-01') for ticker in tickers}

# Dataframe
df = pd.DataFrame({ticker: data['Close'] for ticker, data in allData.items()})
print(df.head())

# Data visualization
df.plot(figsize = (15, 7))
plt.title('Close Price 2020 - 2023')
plt.ylabel('Close Price')
plt.xlabel('Date')
plt.legend(tickers)
plt.grid(True)
plt.show

# Save data in csv
for ticker, data in allData.items():
  data.to_csv(f'{ticker}-2020-2023')

# Scale data
scaler = MinMaxScaler(feature_range=(0, 1))
scaledData = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

# Create sequences X, Y
X = []
Y = []

sequence = 60

for i in range(sequence, len(scaledData)):
    X.append(scaledData[i - sequence:i])
    Y.append(scaledData[i, 0])

X, Y = np.array(X), np.array(Y)

# Divide data
trainSize = int(0.8 * len(X))
Xtrain, Ytrain = X[:trainSize], Y[:trainSize]
Xtest, Ytest = X[trainSize:], Y[trainSize:]

Xtrain.shape, Xtest.shape

# Building LSTM model
model = Sequential()

# First layer
model.add(LSTM(units=50, return_sequences=True, input_shape=(Xtrain.shape[1], 1)))
model.add(Dropout(0.2))

# Second layer
model.add(LSTM(units=30, return_sequences=False))
model.add(Dropout(0.1))

# Third layer
model.add(Dense(units=20, activation='tanh'))

# Last layer
model.add(Dense(units = 1))

# Compile model
model.compile(optimizer='adam', loss='mean_squared_error')

# Early Stopping
EarlyStop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
history = model.fit(Xtrain, Ytrain, epochs = 100, batch_size = 32, validation_data = (Xtest, Ytest), callbacks=[EarlyStop], verbose = 1)

# Loss function
loss = model.evaluate(Xtest, Ytest, verbose = 1)

# Price prediction
predictedPrices = model.predict(Xtest)
predictedPrices = scaler.inverse_transform(predictedPrices)

# Generar predicciones con modelo
predictedPricesScaled = model.predict(Xtest)
predictedPrices = scaler.inverse_transform(predictedPricesScaled)

# Inversión de transformación de escala para obtener los precios reales en la escala original
realPrices = scaler.inverse_transform(Ytest.reshape(-1, 1))

# Visualización de predicciónes vs Precios Reales
plt.figure(figsize = (14, 7))
plt.plot(data.index[-len(Ytest):], realPrices, label = 'Real Prices', color = 'blue')
plt.plot(data.index[-len(Ytest):], predictedPrices, label = 'Predictions', color = 'red', linestyle = 'dashed')
plt.title('Predictions vs Real Prices')
plt.xlabel('Date')
plt.ylabel('Closed Price ($)')
plt.legend()
plt.show()

# Cargar el conjunto de datos de bitcoin (BTC) y etherium (ETH)
data_btc = pd.read_csv('/content/BTC-USD-2020-2023', date_parser=True)
data_btc.set_index('Date', inplace=True)

data_eth = pd.read_csv('/content/ETH-USD-2020-2023', date_parser=True)
data_eth.set_index('Date', inplace=True)

# Escalar los datos
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data_btc = scaler.fit_transform(data_btc['Close'].values.reshape(-1, 1))
scaled_data_eth = scaler.fit_transform(data_eth['Close'].values.reshape(-1, 1))

# Crear secuencias
X_btc = []
y_btc = []
sequence_length = 60
for i in range(sequence_length, len(scaled_data_btc)):
    X_btc.append(scaled_data_btc[i-sequence_length:i])
    y_btc.append(scaled_data_btc[i, 0])

X_btc, y_btc = np.array(X_btc), np.array(y_btc)

X_eth = []
y_eth = []
sequence_length = 60
for i in range(sequence_length, len(scaled_data_eth)):
    X_eth.append(scaled_data_eth[i-sequence_length:i])
    y_eth.append(scaled_data_eth[i, 0])

X_eth, y_eth = np.array(X_eth), np.array(y_eth)

# Dividir los datos en conjuntos de entrenamiento y prueba
train_size_btc = int(0.8 * len(X_btc))
X_train_btc, y_train_btc = X_btc[:train_size_btc], y_btc[:train_size_btc]
X_test_btc, y_test_btc = X_btc[train_size_btc:], y_btc[train_size_btc:]

train_size_eth = int(0.8 * len(X_eth))
X_train_eth, y_train_eth = X_eth[:train_size_eth], y_eth[:train_size_eth]
X_test_eth, y_test_eth = X_eth[train_size_eth:], y_eth[train_size_eth:]

# Predicciones con el modelo
predicted_prices_scaled_btc = model.predict(X_test_btc)
predicted_prices_btc = scaler.inverse_transform(predicted_prices_scaled_btc)

predicted_prices_scaled_eth = model.predict(X_test_eth)
predicted_prices_eth = scaler.inverse_transform(predicted_prices_scaled_eth)

# Precios reales en la escala original
real_prices_btc = scaler.inverse_transform(y_test_btc.reshape(-1, 1))
real_prices_eth = scaler.inverse_transform(y_test_eth.reshape(-1, 1))

# Visualizar predicciones vs precios reales
import matplotlib.pyplot as plt
plt.figure(figsize=(14, 7))
plt.plot(data_btc.index[-len(y_test_btc):], real_prices_btc, label='Precios reales BTC', color='blue')
plt.plot(data_btc.index[-len(y_test_btc):], predicted_prices_btc, label='Predicciones BTC', color='red', linestyle='dashed')
plt.plot(data_eth.index[-len(y_test_eth):], real_prices_eth, label='Precios reales ETH', color='green')
plt.plot(data_eth.index[-len(y_test_eth):], predicted_prices_eth, label='Predicciones ETH', color='orange', linestyle='dashed')
plt.title('Predicciones vs Precios reales (BTC y ETH)')
plt.xlabel('Fecha')
plt.ylabel('Precio de cierre ($)')
plt.legend()
plt.show()

"""
A) El proceso de preparación de datos para una LSTM es fundamental para el aprendizaje secuencial y la memoria a corto y largo plazo que estos modelos proporcionan descarga de datos, escalado de datos, secuencias y división de datos
B) La arquitectura LSTM está diseñada para capturar dependencias temporales y secuenciales en los datos. En el contexto de los precios de las criptomonedas las capas permiten que el modelo recuerde y utilice info anterior, eldropout para no forzar el modelo y la capa densa para una predicción final
C) ara mejorar el modelo se deberian de incluir mas datos historicos, agregar mas epocas y capas (de diversos tipos) así se enriquesería
"""