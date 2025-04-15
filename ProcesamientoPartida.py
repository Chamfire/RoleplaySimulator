from llama_cpp import Llama
from Global import Global
import threading
from deep_translator import GoogleTranslator
from huggingface_hub import hf_hub_download
import numpy as np
import random
import datetime
import sys
import os
import contextlib
from maquina_de_estados.Maquina_de_estados import Maquina_de_estados

@contextlib.contextmanager
def suppress_stdout_stderr():
    with open(os.devnull, "w") as fnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = fnull
        sys.stderr = fnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

class ProcesamientoPartida:
    def __init__(self, seed_random):
        self.prompt = None
        self.generation_kwargs = None
        self.llm = None
        self.numJugadores = None
        self.GLOBAL = Global()
        self.response_good = None
        self.DMVoice = None
        self.currentPartida = None
        random.seed = seed_random #para reproducir los resultados si le pasamos una semilla fija

    def initialize(self,numJugadores,DMVoice, currentPartida):
        self.numJugadores  = numJugadores
        self.DMVoice = DMVoice
        self.currentPartida = currentPartida


    #Hilo de carga de partida
    def prepararPartida(self):
        #8B de parámetros, quantificado, de roleplay y en español exclusivamente 
        #model_name = "mradermacher/Hermes-3-Llama-3.1-8B_ODESIA-i1-GGUF"
        #model_file = "Hermes-3-Llama-3.1-8B_ODESIA.i1-Q4_K_M.gguf"
        model_name = "bartowski/Llama-3.2-3B-Instruct-GGUF"
        model_file = "Llama-3.2-3B-Instruct-Q4_K_M.gguf"
        model_path = hf_hub_download(model_name, filename=model_file)

        print("Progreso: 0%")
        with suppress_stdout_stderr():
            self.llm = Llama(
                model_path=model_path,
                n_ctx=1024,  # Context length to use
                n_threads=32,            # Number of CPU threads to use
                n_gpu_layers=0,        # Number of model layers to offload to GPU
                seed= random.randint(1,100000)
            )
        ## Generation kwargs
        self.generation_kwargs = {
            "max_tokens":300,
            "stop":["</s>"],
            "echo":False, # Echo the prompt in the output
            "top_p": 0.85, #top_p y temperatura le da aleatoriedad
            "temperature": 0.8
        }


        # Generación de mensaje de bienvenida:
        hora_actual = datetime.datetime.now().time()
        if(hora_actual.hour < 15):
            momento = "Buenos días"
        elif(hora_actual.hour >=15 and hora_actual.hour < 20):
            momento = "Buenas tardes"
        else:
            momento = "Buenas noches"

        if(self.numJugadores == 1):
            bienvenida = "bienvenido"
            intro = "Por si no me conoces"
            fin = " ¿Estás preparado para lo que vino, viene, y vendrá?"
            c1 = "a tu jugador"
            consideracion = " Solo tienes 1 jugador escuchando, y ya se ha creado a su personaje. No hagas referencia a nada de su personaje."
        else:
            bienvenida = "bienvenidos"
            intro = "Para los que no me conozcais"
            fin = " ¿Estáis preparados para lo que vino, viene, y vendrá?"
            c1 = "a tus jugadores"
            consideracion = " Tienes varios jugadores escuchando, y ya se han creado sus personajes. No hagas referencia a nada de sus personajes."

        self.prompt = """{Eres un dungeon master de Dnd 5e y quieres presentarte"""+c1+""".}<|eot_id|><|start_header_id|>user<|end_header_id|>
                        {Completa la siguiente frase, en un mismo párrafo: "¡"""+momento+""", y """+bienvenida+"""! """+intro+""", soy Leia, la Dungeon Master. <Genera un texto de presentación general de d&d aquí, sin dar detalles sobre nada de la partida brevemente. """+consideracion+""">.}
                        <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
        
        #Para omitir el output que da por consola
        res = self.llm(self.prompt, **self.generation_kwargs) # Res is a dictionary
        ## Unpack and the generated text from the LLM response dictionary and print it
        self.response_good = res["choices"][0]["text"]
        if "." in self.response_good:
            self.response_good = self.response_good.rsplit(".", 1)[0] + "."  # Para devolver un párrafo completo
        self.response_good = self.response_good.lstrip()
        self.response_good= self.response_good+fin
        #print(self.response_good)
        print("Progreso: 7%")

        #Generación del primer estado de la máquina
        #TODO: Modificar para cargar máquina de estados de la bbdd
        maquina = Maquina_de_estados(self.DMVoice,self.volEffects,self.currentPartida)
        maquina.crearEstadoInicial(self.response_good)
        #procesamiento....
        maquina.initExecution()

