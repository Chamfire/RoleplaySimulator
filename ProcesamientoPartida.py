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
import sqlite3
import json
from maquina_de_estados.Maquina_de_estados import Maquina_de_estados
from Personaje import Personaje

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
        self.vinculos = {0:[None,None,None,None,None,None],1:[None,None,None,None,None,None],2:[None,None,None,None,None,None],3:[None,None,None,None,None,None],4:[None,None,None,None,None,None],5:[None,None,None,None,None,None],6:[None,None,None,None,None,None],7:[None,None,None,None,None,None],8:[None,None,None,None,None,None],9:[None,None,None,None,None,None],10:[None,None,None,None,None,None],11:[None,None,None,None,None,None],12:[None,None,None,None,None,None]}
        self.defectos = {0:[None,None,None,None,None,None],1:[None,None,None,None,None,None],2:[None,None,None,None,None,None],3:[None,None,None,None,None,None],4:[None,None,None,None,None,None],5:[None,None,None,None,None,None],6:[None,None,None,None,None,None],7:[None,None,None,None,None,None],8:[None,None,None,None,None,None],9:[None,None,None,None,None,None],10:[None,None,None,None,None,None],11:[None,None,None,None,None,None],12:[None,None,None,None,None,None]}
        self.rasgos_personalidad = {0:[None,None,None,None,None,None,None,None],1:[None,None,None,None,None,None,None,None],2:[None,None,None,None,None,None,None,None],3:[None,None,None,None,None,None,None,None],4:[None,None,None,None,None,None,None,None],5:[None,None,None,None,None,None,None,None],6:[None,None,None,None,None,None,None,None],7:[None,None,None,None,None,None,None,None],8:[None,None,None,None,None,None,None,None],9:[None,None,None,None,None,None,None,None],10:[None,None,None,None,None,None,None,None],11:[None,None,None,None,None,None,None,None],12:[None,None,None,None,None,None,None,None]}
        self.ideales = {0:[None,None,None,None,None,None],1:[None,None,None,None,None,None],2:[None,None,None,None,None,None],3:[None,None,None,None,None,None],4:[None,None,None,None,None,None],5:[None,None,None,None,None,None],6:[None,None,None,None,None,None],7:[None,None,None,None,None,None],8:[None,None,None,None,None,None],9:[None,None,None,None,None,None],10:[None,None,None,None,None,None],11:[None,None,None,None,None,None],12:[None,None,None,None,None,None]}
        self.personaje = Personaje()
        self.currentPartida = None
        random.seed = seed_random #para reproducir los resultados si le pasamos una semilla fija
        self.NPCs = {"bosque,elfo,0":("elfo_vive en el bosque_75_430_de piel verde",75,430),
                "bosque,elfo,1":("elfo_vive en el bosque_78_420_de piel verde",78,420),
                "desierto,elfo,0":("elfo_vive en el desierto_61_465_de piel clara",61,465),
                "desierto,elfo,1": ("elfo_vive en el desierto_80_80_de piel verde",80,80),
                "barco,elfo,0":("elfo_vive en un barco_69_354_de piel verde",69,354),
                "barco,elfo,1":("elfo_vive en un barco_79_493_de piel verde",79,493),
                "aldea medieval,elfo,0":("elfo_vive en una aldea medieval_68_196_de piel clara",68,196),
                "aldea medieval,elfo,1":("elfo_vive en una aldea medieval_80_303_de piel clara",80,303),
                "mazmorra,elfo,0":("elfo_vive en una ciudad antigua subterránea_64_739_de piel clara",64,739),
                "mazmorra,elfo,1":("elfo_vive en una ciudad antigua subterránea_80_649_de piel verde",80,649),
                "ciudad moderna,elfo,0":("elfo_vive en una ciudad moderna_61_257_de piel verde",61,257),
                "ciudad moderna,elfo,1":("elfo_vive en una ciudad moderna_80_326_de piel clara",80,326),
                "bosque,enano,0":("enano_vive en el bosque_45_127_omite referencias al color de piel",45,127),
                "bosque,enano,1":("enano_vive en el bosque_47_255_omite referencias al color de piel",47,255),
                "desierto,enano,0":("enano_vive en el desierto_45_329_omite referencias al color de piel",45,329),
                "desierto,enano,1":("enano_vive en el desierto_59_188_omite referencias al color de piel",59,188),
                "barco,enano,1":("enano_vive en un barco_57_237_omite referencias al color de piel",57,237),
                "aldea medieval,enano,0":("enano_vive en una aldea medieval_51_71_omite referencias al color de piel",51,71),
                "aldea medieval,enano,1":("enano_vive en una aldea medieval_60_278_omite referencias al color de piel",60,278),
                "mazmorra,enano,0":("enano_vive en una ciudad antigua subterránea_52_349_omite referencias al color de piel",52,349),
                "mazmorra,enano,1":("enano_vive en una ciudad antigua subterránea_58_212_omite referencias al color de piel",58,212),
                "ciudad moderna,enano,0":("enano_vive en una ciudad moderna_45_103_omite referencias al color de piel",45,103),
                "ciudad moderna,enano,1":("enano_vive en una ciudad moderna_62_81_omite referencias al color de piel",62,81)}


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
        print("Progreso: 4%")

        #Generación del primer estado de la máquina
        #TODO: Modificar para cargar máquina de estados de la bbdd
        maquina = Maquina_de_estados(self.DMVoice,self.currentPartida)
        maquina.crearEstadoInicial(self.response_good)
        print("Progreso: 7%")

        #Escojo NPC
        conn = sqlite3.connect("simuladordnd.db")
        cur = conn.cursor()
        #cargamos la partida 1, si existe: el orden de las columnas será ese
        cur.execute("SELECT ubicacion_historia FROM partida WHERE numPartida = '"+self.currentPartida+"'")
        rows = cur.fetchall() #para llegar a esta pantalla, la pantalla tiene que existir sí o sí
        if(rows[0] != None):
            ubicacion = rows[0][0]
        conn.close()

        raza = random.randint(0,1) #0: elfo, 1: enano
        if(raza == 0):
            self.personaje.tipo_raza = "elfo"
        else:
            self.personaje.tipo_raza = "enano"
        NPC_aleatorio = random.randint(0,1) #hay 2 posibles NPCs para cada raza
        NPC_final = self.NPCs[ubicacion+","+self.personaje.tipo_raza+","+NPC_aleatorio]
        NPC_imagen_carpeta = "images/NPCs/"+NPC_final[0]+".png"
        NPC_animacion = "animations/NPCs/"+NPC_final[0]+"/walk.png"
        
        #obtengo su descripción del .json
        self.dir = 'descripciones'
        self.file = 'NPCs.json'
        with open(self.dir+'/'+self.file) as f:
            try:
                NPC_descripcion = json.load(f)
            except Exception as e:
                print(e)
        #creo los datos del NPC
        clase = random.randint(0,1) #0:explorador, 1:bárbaro
        if(clase == 0):
            self.personaje.tipo_clase = "explorador"
        else:
            self.personaje.tipo_clase = "bárbaro"

        if(self.personaje.tipo_clase == "Explorador"):
            self.personaje.des = 15
            self.personaje.sab = 14
            self.personaje.fu = 13
            self.personaje.car = 12
            self.personaje.int = 10
            self.personaje.cons = 8
            self.personaje.ca = 11 #10 + 1(Des,12)
            self.personaje.salvaciones_comp["fu"] = True
            self.personaje.salvaciones_comp["des"] = True
            #Dinero: 5d4x 10
            self.personaje.po = (random.randint(1,4)+random.randint(1,4)+random.randint(1,4)+random.randint(1,4)+random.randint(1,4))*10
            if(self.personaje.tipo_raza == "Enano"):
                self.personaje.cons += 2 #tiene un +2 en constitución
                self.personaje.idiomas_competencia["Común"] = True
                self.personaje.idiomas_competencia["Enano"] = True
                #escoger competencias de forma aleatoria
                posibles_competencias = ["Atletismo", "Perspicacia", "Investigación","Trato con Animales", "Naturaleza", "Percepción", "Sigilo", "Supervivencia"]

            else:
                self.personaje.idiomas_competencia["Común"] = True
                self.personaje.idiomas_competencia["Élfico"] = True
                self.personaje.habilidades_comp["Percepción"] = True
                posibles_competencias = ["Atletismo", "Perspicacia", "Investigación","Trato con Animales", "Naturaleza", "Sigilo", "Supervivencia"]
                            
        elif(self.personaje.tipo_clase == "Bárbaro"):
            self.personaje.fu = 15
            self.personaje.car = 14
            self.personaje.cons = 13
            self.personaje.sab = 12
            self.personaje.des = 10
            self.personaje.ca = 10 #10 + Des (0)
            self.personaje.int = 8
            self.personaje.salvaciones_comp["fu"] = True
            self.personaje.salvaciones_comp["cons"] = True
            #Dinero: 2d4x 10
            self.personaje.po = (random.randint(1,4)+random.randint(1,4))*10
            if(self.personaje.tipo_raza == "Enano"):
                self.personaje.cons += 2 #tiene un +2 en constitución
                self.personaje.idiomas_competencia["Común"] = True
                self.personaje.idiomas_competencia["Enano"] = True
                #Escoger competencias de forma aleatoria
                posibles_competencias = ["Atletismo", "Intimidación", "Naturaleza", "Percepción", "Supervivencia", "Trato con Animales"]

            else:
                self.personaje.idiomas_competencia["Común"] = True
                self.personaje.idiomas_competencia["Élfico"] = True
                self.personaje.habilidades_comp["Percepción"] = True
                #Escoger competencias de forma aleatoria
                posibles_competencias = ["Atletismo", "Intimidación", "Naturaleza", "Supervivencia", "Trato con Animales"]
        escogida = random.randint(0,(len(posibles_competencias)-1))
        self.personaje.habilidades_comp[posibles_competencias[escogida]] = True
        posibles_competencias.remove(posibles_competencias[escogida])
        escogida = random.randint(0,(len(posibles_competencias)-1))
        self.personaje.habilidades_comp[posibles_competencias[escogida]] = True
        posibles_competencias.remove(posibles_competencias[escogida])     

        trasfondo = random.randint(0,12)
        if(trasfondo == 0):
            self.personaje.id_trasfondo = ("Acólito",0)
        elif(trasfondo == 1):
            self.personaje.id_trasfondo = ("Artesano Gremial",1)
        elif(trasfondo == 2):
            self.personaje.id_trasfondo = ("Artista",2)
        elif(trasfondo == 3):
            self.personaje.id_trasfondo = ("Charlatán",3)
        elif(trasfondo == 4):
            self.personaje.id_trasfondo = ("Criminal",4)
        elif(trasfondo == 5):
            self.personaje.id_trasfondo = ("Ermitaño",5)
        elif(trasfondo == 6):
            self.personaje.id_trasfondo = ("Forastero",6)
        elif(trasfondo == 7):
            self.personaje.id_trasfondo = ("Héroe del pueblo",7)
        elif(trasfondo == 8):
            self.personaje.id_trasfondo = ("Huérfano",8)
        elif(trasfondo == 9):
            self.personaje.id_trasfondo = ("Marinero",9)
        elif(trasfondo == 10):
            self.personaje.id_trasfondo = ("Noble",10)
        elif(trasfondo == 11):
            self.personaje.id_trasfondo = ("Sabio",11)
        elif(trasfondo == 12):
            self.personaje.id_trasfondo = ("Soldado",12)
        
        vinculo = random.randint(1,6)
        defecto = random.randint(1,6)
        ideal = random.randint(1,6)
        rasgo_personalidad = random.randint(1,8)


        #consulta para recuperar vínculos, defectos, ideales y rasgos de personalidad de la bbdd
        conn = sqlite3.connect("simuladordnd.db")
        cur = conn.cursor()
        cur.execute("SELECT num_id,vinculo FROM vinculos")
        rows = cur.fetchall()
        for i in range(0,78):
            self.vinculos[(i//6)][(i%6)] = rows[i] #cargo los vínculos en el array
        
        cur.execute("SELECT num_id,defecto FROM defectos")
        rows = cur.fetchall()
        for i in range(0,78):
            self.defectos[(i//6)][(i%6)] = rows[i] #cargo los vínculos en el array
        
        cur.execute("SELECT num_id,ideal FROM ideales")
        rows = cur.fetchall()
        for i in range(0,78):
            self.ideales[(i//6)][(i%6)] = rows[i] #cargo los vínculos en el array

        cur.execute("SELECT num_id,rasgo_personalidad FROM rasgos_personalidad")
        rows = cur.fetchall()
        for i in range(0,104):
            self.rasgos_personalidad[(i//8)][(i%8)] = rows[i] #cargo los vínculos en el array
        conn.close()
        
        self.personaje.rasgo_personalidad = (self.rasgos_personalidad[self.personaje.id_trasfondo[1]][rasgo_personalidad-1][1],rasgo_personalidad)
        self.personaje.vinculo = (self.vinculos[self.personaje.id_trasfondo[1]][vinculo-1][1],vinculo)
        self.personaje.defecto = (self.defectos[self.personaje.id_trasfondo[1]][defecto-1][1],defecto)
        self.personaje.ideal = (self.ideales[self.personaje.id_trasfondo[1]][ideal-1][1],ideal)
        self.personaje.edad = self.NPCs[2]
        self.personaje.peso = self.NPCs[1]
        

        #procesamiento....
        maquina.initExecution()


