from llama_cpp import Llama
from Global import Global
import threading
from deep_translator import GoogleTranslator
from huggingface_hub import hf_hub_download
import torch
import numpy as np
import random


class ConsultaDescripcion:
    def __init__(self,seed_random):
        self.prompt = None
        self.generation_kwargs = None
        self.llm = None
        self.GLOBAL = Global()
        self.response_good = None
        random.seed = seed_random #para reproducir los resultados si le pasamos una semilla fija
    
    def initialize(self,personaje,model_path):
        self.prompt = None
        self.generation_kwargs = None
        self.llm = None
        self.response_good = None
        self.personaje = personaje
        self.model_path = model_path

    def getResponse(self):
        return self.response_good
    
    def cambiarScreenThread(self): #tiene que ser un hilo, puesto que Lock() es de threading
        self.GLOBAL.setRefreshScreen("seleccionPersonaje2")


    def consultaDescripcion(self):
        ## Instantiate model from downloaded file
        model_name = "NousResearch/Hermes-3-Llama-3.2-3B-GGUF"
        model_file = "Hermes-3-Llama-3.2-3B.Q4_K_M.gguf" # this is the specific model file we'll use in this example. It's a 4-bit quant, but other levels of quantization are available in the model repo if preferred
        model_path = hf_hub_download(model_name, filename=model_file)

        self.llm = Llama(
            model_path=self.model_path,
            n_ctx=128,  # Context length to use
            n_threads=32,            # Number of CPU threads to use
            n_gpu_layers=0,        # Number of model layers to offload to GPU
            seed= random.randint(1,100000)
        )
        ## Generation kwargs
        self.generation_kwargs = {
            "max_tokens":100,
            "stop":["</s>"],
            "echo":False, # Echo the prompt in the output
            "top_p": 0.85, #top_p y temperatura le da aleatoriedad
            "temperature": 0.8
        }
        if(self.personaje.tipo_raza == "Elfo"):
            raza = "elf"
        elif(self.personaje.tipo_raza == "Enano"):
            raza = "dwarf"
        if(self.personaje.tipo_clase == "Bárbaro"):
            clase = "barbarian"
        elif(self.personaje.tipo_clase == "Explorador"):                    
            clase = "ranger"
                
        ## Run inference
        self.prompt = """<|im_start|>system
                    You are a dungeon master, of Dnd 5th generation, and you are helping me to create a character.<|im_end|>
                <|im_start|>user
                    Describe the physical appearance of an"""+raza+ """ """+clase+""" ("""+self.personaje.peso+"""kg, """+self.personaje.edad+""" years old) in just one paragraph. Be creative and funny, and start saying "The """+raza+ """ """+clase+""" is <|im_end|>
                <|im_start|>assistant"""
        res = self.llm(self.prompt, **self.generation_kwargs) # Res is a dictionary
        ## Unpack and the generated text from the LLM response dictionary and print it
        self.response_good = res["choices"][0]["text"]
        if "." in self.response_good:
            self.response_good = self.response_good.rsplit(".", 1)[0] + "."  # Para devolver un párrafo completo
        self.response_good = self.response_good[2:] #quitamos los caracteres de espacio del pcpio
        print(self.response_good)
        translator = GoogleTranslator(source='auto', target='es')
        translated = False    
        while(translated == False):
            try:
                self.response_good = translator.translate(self.response_good)
                translated = True
            except Exception as e:
                print(e)

        #print(self.response_good)

        hiloCambiaScreen = threading.Thread(target=self.cambiarScreenThread)
        hiloCambiaScreen.start()

