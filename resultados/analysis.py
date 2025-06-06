import numpy as np
import pandas as pd

class Analisis:
    def __init__(self):
        # Cargo los resultados de las encuestas
        self.df_encuestas = pd.read_csv('resultados/encuestas.csv')
        self.df_encuestas = pd.DataFrame(self.df_encuestas)
        self.df_estadisticas = pd.read_csv('resultados/estadisticas.csv')
        self.df_estadisticas = pd.DataFrame(self.df_estadisticas)
        #print(self.df_encuestas)
        #print(self.df_estadisticas)

        # Encuestas
        # Numéricas: pregunta_2,pregunta_3,pregunta_4,pregunta_5,pregunta_6,pregunta_7,pregunta_8,pregunta_9,pregunta_12,pregunta_13,pregunta_14,pregunta_15,pregunta_17,pregunta_18
        # Categóricas: pregunta_1,pregunta_10,pregunta_11,pregunta_16
        


    def describePreguntas(self):
        print("------------- Descripción de variables -----------")
        print("* Variables numéricas:")
        print(" -------------------------------------------------")
        print(self.df_encuestas.describe())
        print("* Variables categóricas:")
        print(" -------------------------------------------------")
        print(self.df_encuestas.describe(include='object'))
        print("--------------------------------------------------")




analisis = Analisis()
analisis.describePreguntas()