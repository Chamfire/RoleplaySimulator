import pygame
import os
import random
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
import os
import sys
import contextlib
import csv

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

class Prueba:
    def __init__(self):
        self.font = 'agencyfbnormal'
        pygame.font.init()
        pygame.init()
        self.screen = None
        self.backgroundPic = pygame.image.load("images/background.png")
        self.capa = pygame.image.load("images/capa.png")
        self.buttonPic = pygame.image.load("images/button.png")
        self.fuente = pygame.font.SysFont(self.font, 70)
        self.color_white = (255,255,255)
        self.back = self.fuente.render('Volver al menú', True, self.color_white)
        self.printPrueba()

    def consultarAlDM(self,prompt,fin):
        model_name = "bartowski/Llama-3.2-3B-Instruct-GGUF"
        model_file = "Llama-3.2-3B-Instruct-Q4_K_M.gguf"
        model_path = hf_hub_download(model_name, filename=model_file)
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
            "max_tokens":400,
            "stop":["</s>"],
            "echo":False, # Echo the prompt in the output
            "top_p": 0.85, #top_p y temperatura le da aleatoriedad
            "temperature": 0.8
        }
        res = self.llm(prompt, **self.generation_kwargs) # Res is a dictionary
        ## Unpack and the generated text from the LLM response dictionary and print it
        response_good = res["choices"][0]["text"]
        if "." in response_good:
            response_good = response_good.rsplit(".", 1)[0] + "."  # Para devolver un párrafo completo
        response_good = response_good.lstrip()
        if(fin != None):
            response_good= response_good+fin



        return response_good

    def printPrueba(self):
        #printeo de casillas        
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) 
        #self.screen = pygame.display.set_mode((1500,600)) #para pruebas de tamaño 1
        self.screen = pygame.display.set_mode((974,550)) #para pruebas de tamaño 2
        info = pygame.display.Info()
        # --------------SEMILLA ----------------------
        #seed_random = 33
        seed_random = random.randint(0,10000) #por defecto es aleatoria, pero se puede poner la de arriba
        rel = (info.current_w/info.current_h)
        if(1.7 <= rel <= 1.8): #aprox 16 x 9 -> 1.77
            self.width,self.height= (self.screen.get_width(), self.screen.get_height())
            #se queda Fullscreen
            pass
        elif(rel < 1.7):
            temp_width,temp_height= (self.screen.get_width(), self.screen.get_height())
            for i in reversed(range(0,temp_height)):
                n_rel = temp_width/i
                if(1.7 <= n_rel <= 1.8):
                    self.width,self.height= (temp_width,i)
                    break
                else:
                    pass

        else: #mayor de 1.8
            temp_width,temp_height= (self.screen.get_width(), self.screen.get_height())
            for i in reversed(range(0,temp_width)):
                n_rel = i/temp_height
                if(1.7 <= n_rel <= 1.8):
                    self.width,self.height= (i,temp_height)
                    break
                else:
                    pass


        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        self.screen.fill((0,0,0))
        
        
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
        self.letterwidth2 = (self.width/3.4286)/20 #cálculo de la base en píxeles 
        self.lettersize2 = int(self.letterwidth2 + 0.5 * self.letterwidth2) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente3 = pygame.font.SysFont(self.font,self.lettersize2)
        # Estadísticas
        ending_time = "Tiempo requerido: 1234566778 ms"
        mobs = "Monstruos descubiertos: 5"
        cofres = "Sarcófagos abiertos: 10"
        rooms = "Habitaciones descubiertas: 7/14"
        objetos = "Objetos destruidos: 20"

        duracion = 123455666
        mobsT = 5
        cofresT = 10
        roomsT = 7
        objetosT = 20

        row = [duracion, mobsT, cofresT, roomsT,  objetosT]
        with open('resultados/estadisticas.csv', mode='a',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)
        

        text1 = self.fuente3.render(ending_time, True, self.color_white)
        text2 = self.fuente3.render(mobs, True, self.color_white)
        text3 = self.fuente3.render(cofres, True, self.color_white)
        text4 = self.fuente3.render(rooms, True, self.color_white)
        text5 = self.fuente3.render(objetos, True, self.color_white)

        #los renderizamos 
        self.screen.blit(text1, (self.width/13.6364, self.height/14.2857)) #88 49
        self.screen.blit(text2, (self.width/13.6364, self.height/5.5118)) #88 127
        self.screen.blit(text3, (self.width/13.6364, self.height/3.4146)) #88 205
        self.screen.blit(text4, (self.width/13.6364, self.height/2.4648)) #88 284
        self.screen.blit(text5, (self.width/13.6364, self.height/1.9337)) #88 362


        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
        self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
        pygame.display.update() 
        while(True):
            pass
prueba = Prueba()