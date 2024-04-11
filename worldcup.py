# -*- coding: utf-8 -*-
"""worldCup.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10M0V8-nvRyPH3lEwP31MHfmc_e3uizwJ
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests

# Definir set receptor de datos
stages = ["Fase de Grupos", 'Octavos de Final', 'Cuartos de Final', 'Semifinales', 'Tercer Lugar', 'Final']
partidosStage = [48, 8, 4, 2, 1, 1]

def extraccionPartidos (s):
  matches = s.find_all('div', class_ = 'footballbox')

  home = []
  score = []
  away = []

  for match in matches:
    home.append(match.find('th', class_ = 'fhome').get_text())
    score.append(match.find('th', class_ = 'fscore').get_text())
    away.append(match.find('th', class_ = 'faway').get_text())

  return list(zip(home, score, away))

# Extraer el contenido y request de URL
web = 'https://en.wikipedia.org/wiki/2022_FIFA_World_Cup#Results'
respuesta = requests.get(web)
content = respuesta.text
s = BeautifulSoup(content, 'lxml')

# Correr la función
todosPartidos = extraccionPartidos(s)

#Divir partidos por etapa
data = []
i = 0

for stage, count in zip(stages, partidosStage):
  for _ in range(count):
    home, score, away = todosPartidos[i]
    data.append({'Local':home, 'Resultado':score, 'Visitante':away, 'Etapa':stage})
    i += 1

df=pd.DataFrame(data)

df.head()

pd.set_option('display.max_rows', None)

df.to_csv("FifaMundialQatar2022.csv")