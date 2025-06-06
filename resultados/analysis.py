import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
        print("* Descripción de las variables:")
        print(" -------------------------------------------------")
        for var in self.df_encuestas.columns:
            if(var != "id"):
                print(self.df_encuestas[var].describe())
                print("------------------------------------------------------")
        print(" -------------------------------------------------")

        self.df_encuestas_sin_id = self.df_encuestas.drop('id', axis=1)
        # Transformo las variables númericas para que empiecen a de 0-3, y así poder imprimir a la vez en el gráfico la sd:
        numeric_cols = self.df_encuestas_sin_id.select_dtypes(include='number').columns

        self.df_encuestas_sin_id_interfaz = self.df_encuestas_sin_id[["Interfaz del menú","Interfaz de la configuración","Interfaz de la selección de partidas","Interfaz de la configuración de partidas","Interfaz de la pantalla 1 de creación de personajes","Interfaz de la pantalla 2 de creación de personajes","Interfaz de la partida","Interfaz del inventario"]]

    def printResultadoDeCadaVar(self):
        for pregunta in self.df_encuestas_sin_id_interfaz:
            respuestas = self.df_encuestas_sin_id_interfaz[pregunta]

            # Valores posibles (0 a 3)
            posibles_respuestas = [1, 2, 3, 4]

            # Calculo el % de cada respuesta
            porcentajes_por_respuesta = respuestas.value_counts(normalize=True) * 100

            # Obtener porcentaje para cada valor, poner 0 si no aparece
            porcentajes = []
            for respuesta in posibles_respuestas:
                if respuesta in porcentajes_por_respuesta.index:
                    porcentajes.append(porcentajes_por_respuesta[respuesta])
                else:
                    porcentajes.append(0)

            # Establecimiento de las características de la gráfica
            plt.figure(figsize=(6,4))
            barras = plt.bar(posibles_respuestas, porcentajes, color='skyblue', edgecolor='black')
            plt.title(f'{pregunta}')
            plt.xlabel('Calificación de la pantalla de 1 a 4')
            plt.ylabel('Porcentaje de respuestas (%)')
            plt.ylim(0, 110)  
            plt.xticks(posibles_respuestas)

            # Indicar % de cada respuesta
            for barra, pct in zip(barras, porcentajes):
                plt.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 1, f'{pct:.1f}%', ha='center')

            plt.tight_layout()
            plt.show()

    def printGraficaDescripcionPreguntasInterfaz(self):
        descripciones = self.df_encuestas_sin_id_interfaz.describe()
        descripciones.T[['mean', 'std', 'min', 'max']].plot(kind='barh', figsize=(12,6))
        
        plt.title("Resultados de la evaluación de las distintas pantallas de la interfaz gráfica de la plataforma")
        plt.xlabel("Puntuación de 0 a 3, donde 0 es muy pobre y 3 es excelente")
        plt.grid(True)
        plt.tight_layout()
        plt.show()


analisis = Analisis()
analisis.describePreguntas()
analisis.printResultadoDeCadaVar()