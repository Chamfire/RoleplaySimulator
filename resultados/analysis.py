import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

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
        self.df_encuestas_coherencia = self.df_encuestas_sin_id[["Coherencia de la introducción","Coherencia de las respuestas del NPC","Coherencia de las descripciones del mapa","Coherencia de las descripciones de las acciones de interacción","Coherencia de las descripciones de los monstruos o animales"]]
        self.df_encuestas_sin_id_si_no = self.df_encuestas_sin_id[["Conoce Dungeons & Dragons","Ha jugado previamente a Dungeons & Dragons","Relación de la imagen del NPC con su descripción física","Relación de las respuestas del NPC con las preguntas del jugador","Relación de la imagen del monstruo o animal con su descripción"]]

        self.df_estadisticas_sin_id = self.df_estadisticas.drop('id',axis=1)

    def printResultadoBarrasVar(self):
        df_completo = pd.merge(self.df_encuestas, self.df_estadisticas, on='id', how='left')
        sns.set_theme(style="whitegrid")
        fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(16, 12))
        axes = axes.flatten()

        variables = ['Duración de la prueba','Monstruos o animales encontrados','Sarcófagos abiertos','Salas visitadas','Objetos con los que se ha interactuado']
        variables_titulo = ['Duración de la prueba (segundos)','Número de monstruos o animales encontrados','Número de sarcófagos abiertos','Número de salas visitadas','Número de objetos con los que se ha interactuado']
        cantidad = ['Segundos empleados','Seres encontrados','Sarcófagos abiertos','Salas visitadas','Objetos']

        # Define paleta personalizada para 'Ha jugado antes'
        palette_custom = {
            'Sí': 'green',
            'No': 'blue'
        }

        for i, variable in enumerate(variables):
            sns.barplot(
                x='id',
                y=variable,
                hue='Ha jugado previamente a Dungeons & Dragons',  
                data=df_completo,
                ax=axes[i],
                palette=palette_custom,
                errorbar=None,
                legend=False 
            )
            axes[i].set_title(variables_titulo[i])
            axes[i].set_xlabel('ID de usuario')
            axes[i].set_ylabel(cantidad[i])
            axes[i].tick_params(axis='x')

        # Eliminar gráfico extra si hay
        if len(axes) > len(variables):
            fig.delaxes(axes[-1])
        
        plt.tight_layout(h_pad=3)
        plt.savefig("estadisticas_usuarios_colores.png", dpi=300, bbox_inches='tight')
        plt.show()

        sns.set_theme(style="whitegrid")
        fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(16, 12))
        axes = axes.flatten()

        variables = ['Duración de la prueba','Monstruos o animales encontrados','Sarcófagos abiertos','Salas visitadas','Objetos con los que se ha interactuado']
        variables_titulo = ['Duración de la prueba (segundos)','Número de monstruos o animales encontrados','Número de sarcófagos abiertos','Número de salas visitadas','Número de objetos con los que se ha interactuado']
        cantidad = ['Segundos empleados','Seres encontrados','Sarcófagos abiertos','Salas visitadas','Objetos']

        # Define paleta personalizada para 'Ha jugado antes'
        palette_custom = {
            'Sí': 'pink',
            'No': 'orange'
        }

        for i, variable in enumerate(variables):
            sns.barplot(
                x='id',
                y=variable,
                hue='Conoce Dungeons & Dragons',  
                data=df_completo,
                ax=axes[i],
                palette=palette_custom,
                errorbar=None,
                legend=False 
            )
            axes[i].set_title(variables_titulo[i])
            axes[i].set_xlabel('ID de usuario')
            axes[i].set_ylabel(cantidad[i])
            axes[i].tick_params(axis='x')

        # Eliminar gráfico extra si hay
        if len(axes) > len(variables):
            fig.delaxes(axes[-1])
        
        plt.tight_layout(h_pad=3)
        plt.savefig("estadisticas_usuarios_colores.png", dpi=300, bbox_inches='tight')
        plt.show()


    def printResultadoDeCadaVar(self):
        preguntas = self.df_encuestas_sin_id_interfaz.columns
        num_preguntas = len(preguntas)

        # Definir dimensiones de la cuadrícula (e.g., 3 columnas)
        num_columnas = 3
        num_filas = math.ceil(num_preguntas / num_columnas)

        fig, axs = plt.subplots(num_filas, num_columnas, figsize=(num_columnas*5, num_filas*4))
        axs = axs.flatten()  # Aplanar para indexar fácilmente

        for i, pregunta in enumerate(preguntas):
            respuestas = self.df_encuestas_sin_id_interfaz[pregunta]
            posibles_respuestas = [1, 2, 3, 4]

            porcentajes_por_respuesta = respuestas.value_counts(normalize=True) * 100

            porcentajes = [porcentajes_por_respuesta.get(r, 0) for r in posibles_respuestas]

            ax = axs[i]
            barras = ax.bar(posibles_respuestas, porcentajes, color='skyblue', edgecolor='black')
            ax.set_title(f'{pregunta}')
            ax.set_xlabel('Calificación (1 a 4)')
            ax.set_ylabel('Porcentaje (%)')
            ax.set_ylim(0, 110)
            ax.set_xticks(posibles_respuestas)

            for barra, pct in zip(barras, porcentajes):
                ax.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 1, f'{pct:.1f}%', ha='center')

        # Ocultar ejes no usados
        for j in range(i + 1, len(axs)):
            fig.delaxes(axs[j])

        plt.tight_layout(h_pad=3)
        plt.savefig("estadisticas_interfaz.png", dpi=300, bbox_inches='tight')
        plt.show()

    def printResultadoDeCadaVarCoherencia(self):
        etiquetas_respuestas = ['No tiene coherencia', 'Coherente con muchas frases carentes de sentido', 'Coherente en su mayoría', 'Todo tiene coherencia']
        for pregunta in self.df_encuestas_coherencia:
            respuestas = self.df_encuestas_coherencia[pregunta]

            # Valores posibles (1,2,3,4)
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
            plt.figure(figsize=(13,6))
            barras = plt.bar(posibles_respuestas, porcentajes, color='skyblue', edgecolor='black')
            plt.title(f'{pregunta}')
            plt.xlabel('Nivel de coherencia de la descripción')
            plt.ylabel('Porcentaje de respuestas (%)')
            plt.ylim(0, 110)  
            plt.xticks(posibles_respuestas,etiquetas_respuestas)

            # Indicar % de cada respuesta
            for barra, pct in zip(barras, porcentajes):
                plt.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 1, f'{pct:.1f}%', ha='center')

            plt.tight_layout()
            plt.show()

    def printResultadoDeCadaVarRelacion(self):
        for pregunta in self.df_encuestas_sin_id_si_no:
            respuestas = self.df_encuestas_sin_id_si_no[pregunta]

            # Valores posibles (Sí, No)
            posibles_respuestas = ["Sí","No"]

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
            plt.xlabel('Conocimiento previo')
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
#analisis.printResultadoDeCadaVarCoherencia()
#analisis.printResultadoDeCadaVarRelacion()
#analisis.printResultadoBarrasVar()