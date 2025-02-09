# -*- coding: utf-8 -*-
"""practicaP2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1m7UStM9q8VtpV3ThQ0Jbq0x4gJx8x9ON
"""

import requests
from bs4 import BeautifulSoup

# URL de 'Quotes to Scrape'
url = 'http://quotes.toscrape.com/'

# Lista para almacenar las citas
quotes_list = []

# Extraer las primeras 50 citas
for page in range(1, 6):  # Cada página tiene 10 citas
    response = requests.get(f'{url}page/{page}/')
    if response.status_code != 200:
        print(f'Error en la página {page}')
        continue
    soup = BeautifulSoup(response.content, 'html.parser')
    quotes = soup.find_all('span', class_='text')
    for quote in quotes:
        quotes_list.append(quote.text)

# Imprimir las citas extraídas
for index, quote in enumerate(quotes_list, 1):
    print(f'Cita {index}: {quote}\n')

from textblob import TextBlob
import nltk
from nltk.corpus import stopwords

nltk.download('punkt')

# Descargar las stopwords
nltk.download('stopwords')
englishStopWords = stopwords.words('english')

tokenized_quotes = []

# Tokenizar y eliminar stopwords
for quote in quotes_list:
    blob = TextBlob(quote)
    tokens = [word for word in blob.words if word.lower() not in englishStopWords]
    tokenized_quotes.append(tokens)

# Imprimir las citas tokenizadas
for index, tokens in enumerate(tokenized_quotes, 1):
    print(f'Cita {index}: {tokens}\n')

import pandas as pd
from textblob import TextBlob

# Convertir la lista de citas en un DataFrame
quotes_df = pd.DataFrame(quotes_list, columns=['Quote'])

# Calcular la polaridad de cada cita
quotes_df['Polarity'] = quotes_df['Quote'].apply(lambda x: TextBlob(x).sentiment.polarity)

# Clasificar las citas basadas en su polaridad
quotes_df['Sentiment'] = quotes_df['Polarity'].apply(lambda x: 'Positive' if x > 0.5 else ('Negative' if x < -0.5 else 'Neutral'))

# Resaltar las citas más positivas y negativas
most_positive = quotes_df[quotes_df['Polarity'] == quotes_df['Polarity'].max()]
most_negative = quotes_df[quotes_df['Polarity'] == quotes_df['Polarity'].min()]

print('Citas más positivas:')
print(most_positive)
print('\nCitas más negativas:')
print(most_negative)

# Mostrar el DataFrame completo para revisión
print('\nTodas las citas con su clasificación:')
print(quotes_df)

import matplotlib.pyplot as plt
import plotly.express as px

counts = quotes_df['Sentiment'].value_counts()

# Crear la gráfica de barras interactiva
fig = px.bar(counts, x=counts.index, y=counts.values, title='Distribución de Sentimientos en las Citas', labels={'x': 'Sentimiento', 'y': 'Número de Citas'}, color=counts.index, color_discrete_map={'Positive':'green', 'Neutral':'blue', 'Negative':'red'})

# Mostrar la gráfica
fig.show()