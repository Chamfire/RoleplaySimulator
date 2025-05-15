from llama_cpp import Llama
from Global import Global
import threading
from deep_translator import GoogleTranslator
from huggingface_hub import hf_hub_download
import numpy as np
import random
import datetime
import sys
import _thread  
import os
import contextlib
import sqlite3
import json
from maquina_de_estados.Maquina_de_estados import Maquina_de_estados
from Personaje import Personaje
from maquina_de_estados.RAG_historia import RAG_historia
import time
from ScriptsGeneracion import Map_generation
import time
import pickle
import base64
import pygame
import pyttsx3
from RAG_music.Consulta_RAG_musica import Consulta_RAG_musica
import random
from pygame import mixer


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
    def __init__(self, seed_random,currentPartida):
        self.generation_kwargs = None
        self.llm = None
        self.numJugadores = None
        self.maquina = None
        self.GLOBAL = Global()
        self.DMVoice = None
        self.width = None
        self.height = None
        self.finished = False
        self.PartidaObjeto = None
        self.jugadorHost = None
        self.ubicacion = None
        self.vinculos = {0:[None,None,None,None,None,None],1:[None,None,None,None,None,None],2:[None,None,None,None,None,None],3:[None,None,None,None,None,None],4:[None,None,None,None,None,None],5:[None,None,None,None,None,None],6:[None,None,None,None,None,None],7:[None,None,None,None,None,None],8:[None,None,None,None,None,None],9:[None,None,None,None,None,None],10:[None,None,None,None,None,None],11:[None,None,None,None,None,None],12:[None,None,None,None,None,None]}
        self.defectos = {0:[None,None,None,None,None,None],1:[None,None,None,None,None,None],2:[None,None,None,None,None,None],3:[None,None,None,None,None,None],4:[None,None,None,None,None,None],5:[None,None,None,None,None,None],6:[None,None,None,None,None,None],7:[None,None,None,None,None,None],8:[None,None,None,None,None,None],9:[None,None,None,None,None,None],10:[None,None,None,None,None,None],11:[None,None,None,None,None,None],12:[None,None,None,None,None,None]}
        self.rasgos_personalidad = {0:[None,None,None,None,None,None,None,None],1:[None,None,None,None,None,None,None,None],2:[None,None,None,None,None,None,None,None],3:[None,None,None,None,None,None,None,None],4:[None,None,None,None,None,None,None,None],5:[None,None,None,None,None,None,None,None],6:[None,None,None,None,None,None,None,None],7:[None,None,None,None,None,None,None,None],8:[None,None,None,None,None,None,None,None],9:[None,None,None,None,None,None,None,None],10:[None,None,None,None,None,None,None,None],11:[None,None,None,None,None,None,None,None],12:[None,None,None,None,None,None,None,None]}
        self.ideales = {0:[None,None,None,None,None,None],1:[None,None,None,None,None,None],2:[None,None,None,None,None,None],3:[None,None,None,None,None,None],4:[None,None,None,None,None,None],5:[None,None,None,None,None,None],6:[None,None,None,None,None,None],7:[None,None,None,None,None,None],8:[None,None,None,None,None,None],9:[None,None,None,None,None,None],10:[None,None,None,None,None,None],11:[None,None,None,None,None,None],12:[None,None,None,None,None,None]}
        id = "autoincrement"
        self.personaje = Personaje(True,currentPartida,id)
        self.currentPartida = None
        self.RAG_historia = None
        random.seed = seed_random #para reproducir los resultados si le pasamos una semilla fija
        self.NPCs = {"bosque,elfo,0":("elfo_vive en el bosque_75_430_de piel verde",75,430,"mujer"),
                "bosque,Elfo,1":("elfo_vive en el bosque_78_420_de piel verde",78,420,"hombre"),
                "desierto,Elfo,0":("elfo_vive en el desierto_61_465_de piel clara",61,465,"hombre"),
                "desierto,Elfo,1": ("elfo_vive en el desierto_80_80_de piel verde",80,80,"mujer"),
                "barco,Elfo,0":("elfo_vive en un barco_69_354_de piel verde",69,354,"mujer"),
                "barco,Elfo,1":("elfo_vive en un barco_79_493_de piel verde",79,493,"hombre"),
                "aldea medieval,Elfo,0":("elfo_vive en una aldea medieval_68_196_de piel clara",68,196,"mujer"),
                "aldea medieval,Elfo,1":("elfo_vive en una aldea medieval_80_303_de piel clara",80,303,"hombre"),
                "mazmorra,Elfo,0":("elfo_vive en una ciudad antigua subterránea_64_739_de piel clara",64,739,"mujer"),
                "mazmorra,Elfo,1":("elfo_vive en una ciudad antigua subterránea_80_649_de piel verde",80,649,"hombre"),
                "ciudad moderna,Elfo,0":("elfo_vive en una ciudad moderna_61_257_de piel verde",61,257,"hombre"),
                "ciudad moderna,Elfo,1":("elfo_vive en una ciudad moderna_80_326_de piel clara",80,326,"mujer"),
                "bosque,Enano,0":("enano_vive en el bosque_45_127_omite referencias al color de piel",45,127,"mujer"),
                "bosque,Enano,1":("enano_vive en el bosque_47_255_omite referencias al color de piel",47,255,"hombre"),
                "desierto,Enano,0":("enano_vive en el desierto_45_329_omite referencias al color de piel",45,329,"mujer"),
                "desierto,Enano,1":("enano_vive en el desierto_59_188_omite referencias al color de piel",59,188,"hombre"),
                "barco,Enano,0":("enano_vive en un barco_46_321_omite referencias al color de piel",46,321,"hombre"),
                "barco,Enano,1":("enano_vive en un barco_57_237_omite referencias al color de piel",57,237,"mujer"),
                "aldea medieval,Enano,0":("enano_vive en una aldea medieval_51_71_omite referencias al color de piel",51,71,"mujer"),
                "aldea medieval,Enano,1":("enano_vive en una aldea medieval_60_278_omite referencias al color de piel",60,278,"hombre"),
                "mazmorra,Enano,0":("enano_vive en una ciudad antigua subterránea_52_349_omite referencias al color de piel",52,349,"mujer"),
                "mazmorra,Enano,1":("enano_vive en una ciudad antigua subterránea_58_212_omite referencias al color de piel",58,212,"hombre"),
                "ciudad moderna,Enano,0":("enano_vive en una ciudad moderna_45_103_omite referencias al color de piel",45,103,"hombre"),
                "ciudad moderna,Enano,1":("enano_vive en una ciudad moderna_62_81_omite referencias al color de piel",62,81,"mujer")}


    def initialize(self,numJugadores,DMVoice, currentPartida,jugadorHost,partida,width,height):
        self.width = width
        self.height = height
        self.numJugadores  = numJugadores
        self.DMVoice = DMVoice
        self.currentPartida = currentPartida
        self.jugadorHost = jugadorHost
        self.PartidaObjeto = partida

    def consultarAlDM(self,prompt,model_path,fin,token_context = 1024,token_gen = 300):
        with suppress_stdout_stderr():
            self.llm = Llama(
                model_path=model_path,
                n_ctx=token_context,  # Context length to use
                n_threads=32,            # Number of CPU threads to use
                n_gpu_layers=0,        # Number of model layers to offload to GPU
                seed= random.randint(1,100000)
            )
        ## Generation kwargs
        self.generation_kwargs = {
            "max_tokens":token_gen,
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
    
    def loadPartidaScreen(self):
        self.PartidaObjeto.changeScreen("partida")

    #Hilo de carga de partida
    def prepararPartida(self):
        #8B de parámetros, quantificado, de roleplay y en español exclusivamente 
        #model_name = "mradermacher/Hermes-3-Llama-3.1-8B_ODESIA-i1-GGUF"
        #model_file = "Hermes-3-Llama-3.1-8B_ODESIA.i1-Q4_K_M.gguf"
        model_name = "bartowski/Llama-3.2-3B-Instruct-GGUF"
        model_file = "Llama-3.2-3B-Instruct-Q4_K_M.gguf"
        model_path = hf_hub_download(model_name, filename=model_file)

        print("Progreso: 0%")
        inicio = time.time()

        if(not os.path.exists('maquina_de_estados/'+self.currentPartida+'/maquina.pickle')):
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

            prompt = """{Eres un dungeon master de Dnd 5e y quieres presentarte"""+c1+""".}<|eot_id|><|start_header_id|>user<|end_header_id|>
                            {Completa la siguiente frase, en un mismo párrafo: "¡"""+momento+""", y """+bienvenida+"""! """+intro+""", soy Leia, la Dungeon Master. <Genera un texto de presentación general de d&d aquí, sin dar detalles sobre nada de la partida brevemente. """+consideracion+""">.}
                            <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
            response_good = self.consultarAlDM(prompt,model_path,fin)

            print("Progreso: 4%")

            #Generación del primer estado de la máquina
            #TODO: Modificar para cargar máquina de estados de la bbdd
            self.maquina = Maquina_de_estados(self.DMVoice,self.currentPartida,self.jugadorHost)
            self.maquina.crearEstadoInicial(response_good)
            print("Progreso: 7%")

            #Escojo NPC
            conn = sqlite3.connect("simuladordnd.db")
            cur = conn.cursor()
            #cargamos la partida 1, si existe: el orden de las columnas será ese
            cur.execute("SELECT ubicacion_historia FROM partida WHERE numPartida = '"+self.currentPartida+"'")
            rows = cur.fetchall() #para llegar a esta pantalla, la pantalla tiene que existir sí o sí
            if(rows[0] != None):
                self.ubicacion = rows[0][0]
            conn.close()

            raza = random.randint(0,1) #0: elfo, 1: enano
            if(raza == 0):
                self.personaje.tipo_raza = "Elfo"
            else:
                self.personaje.tipo_raza = "Enano"
            NPC_aleatorio = random.randint(0,1) #hay 2 posibles NPCs para cada raza
            NPC_final = self.NPCs[self.ubicacion+","+self.personaje.tipo_raza+","+str(NPC_aleatorio)]
            NPC_imagen_carpeta = "images/NPCs/"+NPC_final[0]+".png"
            NPC_animacion = "animations/NPCs/"+NPC_final[0]+"/walk.png"
            
            #obtengo su descripción del .json
            self.dir = 'descripciones'
            self.file = 'NPCs.json'
            with open(self.dir+'/'+self.file,'r',encoding='utf-8') as f:
                try:
                    NPC_descripcion = json.load(f)
                    self.personaje.descripcion_fisica = NPC_descripcion[NPC_final[0]][0]
                except Exception as e:
                    print(e)
                #print(self.personaje.descripcion_fisica)
            #creo los datos del NPC
            clase = random.randint(0,1) #0:explorador, 1:bárbaro
            self.personaje.esta_muerto = False
            if(clase == 0):
                self.personaje.tipo_clase = "Explorador"
            else:
                self.personaje.tipo_clase = "Bárbaro"

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
            self.personaje.edad = NPC_final[2]
            self.personaje.peso = NPC_final[1]
            self.personaje.genero = NPC_final[3]


            alineamiento = random.randint(0,8)
            if(alineamiento == 0):
                self.personaje.tipo_alineamiento = ("Legal Bueno",0)
            elif(alineamiento == 1):
                self.personaje.tipo_alineamiento = ("Neutral Bueno",1)
            elif(alineamiento == 2):
                self.personaje.tipo_alineamiento = ("Caótico Bueno",2)
            elif(alineamiento == 3):
                self.personaje.tipo_alineamiento = ("Legal Neutral",3)
            elif(alineamiento == 4):
                self.personaje.tipo_alineamiento = ("Neutral",4)
            elif(alineamiento == 5):
                self.personaje.tipo_alineamiento = ("Caótico Neutral",5)
            elif(alineamiento == 6):
                self.personaje.tipo_alineamiento = ("Legal Malvado",6)
            elif(alineamiento == 7):
                self.personaje.tipo_alineamiento = ("Neutral Malvado",7)
            elif(alineamiento == 8):
                self.personaje.tipo_alineamiento = ("Caótico Malvado",8)

            #nombre del NPC
            prompt = """{Eres un dungeon master de Dnd 5e y vas a escoger un nombre para un NPC.}<|eot_id|><|start_header_id|>user<|end_header_id|>
                            {Responde únicamente con el nombre escogido para ese NPC, sin dar ningún detalle adicional, y teniendo en cuenta que es """+self.personaje.genero+""".}
                            <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
            nombre = self.consultarAlDM(prompt,model_path,None)
            self.personaje.name = nombre
            #print(self.personaje.name)
            #inicializo el RAG para la historia
            self.RAG_historia = RAG_historia(self.currentPartida)
            prompt = """{Eres un dungeon master de Dnd 5e y vas a describir parte del trasfondo de un NPC, que es """+self.personaje.genero+"""}<|eot_id|><|start_header_id|>user<|end_header_id|>
                            {Genera un párrafo sobre el motivo por el que un NPC (de nombre """+self.personaje.name+""", que es """+self.personaje.tipo_raza+""" y que además es """+self.personaje.tipo_clase+""") podría encontrarse en la siguiente zona: """+self.ubicacion+""". Ten en cuenta en la redacción, que """+self.personaje.name+""" es """+self.personaje.genero+"""}
                            <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

            motivoUbicacion = self.consultarAlDM(prompt,model_path,None)
            # print("-----------------")
            # print(motivoUbicacion)
            # print("-----------------")

            peticion = "Genera 6 párrafos de trasfondo para un NPC que se llama "+self.personaje.name+", que es "+self.personaje.genero+", que es """+self.personaje.tipo_raza+" y que además es "+self.personaje.tipo_clase+". Haz referencia a su familia, a si tiene o no algún romance/matrimonio y detallalo, y a rasgos que podrían ser importantes de su vida"
            prompt = f"Eres un dungeon master de Dnd 5e y vas a describir parte del trasfondo de un NPC, que es {self.personaje.genero}. Usa el siguiente contexto para responder a la petición, y si te falta contexto, inventatelo, siempre que no contradiga al contexto dado: {motivoUbicacion}<|eot_id|><|start_header_id|>user<|end_header_id|>{peticion}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

            infoTrasfondo = self.consultarAlDM(prompt,model_path,None,2024,1024)
            # print("-----------------")
            # print(infoTrasfondo)
            # print("-----------------")

            self.RAG_historia.escribirInfoNPC(self.personaje.name,self.personaje.descripcion_fisica,infoTrasfondo,motivoUbicacion)

            print("Progreso: 11%")

            #listas para las misiones
            lista_objetos_disponibles = {"Armaduras ligeras":["Acolchada", "Cuero tachonado", "De cuero"],
                                        "Armaduras medias": ["Camisote de mallas", "Coraza", "Cota de escamas", "Pieles"],
                                        "Armaduras pesadas": ["Bandas", "Cota de anillas", "Cota de mallas", "Placas"],
                                        "Escudo": ["Escudo básico"],
                                        "Armas a distancia marciales": ["Arco largo", "Ballesta de mano", "Ballesta pesada", "Cerbatana"],
                                        "Armas a distancia simples": ["Arco corto", "Ballesta ligera", "Dardo", "Honda"],
                                        "Armas cc marciales": ["Alabarda", "Atarraga", "Cimitarra", "Espada corta","Espada larga", "Espadón", "Estoque", "Gran hacha", "Guja", "Hacha de batalla", "Lanza de caballería", "Látigo", "Lucero del alba", "Martillo de guerra", "Mayal", "Pica de guerra", "Pica", "Tridente"],
                                        "Armas cc simples": ["Bastón", "Clava", "Daga", "Gran clava", "Hacha de mano", "Hoz", "Jabalina", "Lanza", "Martillo ligero", "Maza"],
                                        "Objetos de almacenaje": ["Mochila"],
                                        "Bebida": ["Odre de agua"],
                                        "Comida": ["Ración"],
                                        "Iluminación": ["Antorcha"],
                                        "Kit": ["De cocina"],
                                        "Mecánico": ["Martillo", "Palanca"],
                                        "Munición": ["Flecha"],
                                        "Otros": ["Cuerda de cáñamo","Pitón", "Yesquero"],
                                        "Refugio": ["Saco de dormir"]
                                        }
            lista_mobs_disponibles = {"mazmorra": ["esqueleto","zombie","slime","beholder","troll"],
                                    "ciudad moderna": ["droide","fantasma","objeto animado de silla", "mimic de cofre", "muñeca animada", "cyborg"],
                                    "bosque": ["lobo wargo", "vampiro", "oso", "hombre lobo"],
                                    "desierto": ["serpiente","cocodrilo", "momia", "esfinge"],
                                    "aldea medieval": ["goblin","cultista","gnoll","elemental de roca"],
                                    "barco": ["sirena","tiburón","hada","kraken"],
                                    "raros": ["dragón","sombras","fénix"],
                                    "medio": ["ankheg","basilísco"],
                                    "comun": ["murciélago","rata","felino salvaje"]}


            tipo_mision_num = random.randint(1,2)
            #tipo_mision_num = 1 #para buscar un lugar
            if(tipo_mision_num == 1):
                tipo_mision = "combate"
                # tipo_mobs = random.randint(0,100)
                mobs = {}
                num_mobs = random.randint(self.numJugadores,self.numJugadores*2)
                n = len(lista_mobs_disponibles[self.ubicacion])-1
                for i in range(0,num_mobs):
                    seleccion = random.randint(0,n)
                    if mobs.get(lista_mobs_disponibles[self.ubicacion][seleccion]) != None:
                        mobs[lista_mobs_disponibles[self.ubicacion][seleccion]] +=1
                    else:
                        mobs[lista_mobs_disponibles[self.ubicacion][seleccion]] = 1
                mision = "Hay que matar "
                variableDeCheck = {}
                for mob_name,num in mobs.items():
                    mision += str(num)+" "+mob_name+","
                    variableDeCheck[mob_name] = [num,0] #5,0 -> 5 de ese tipo a matar, 0 matados
                
            elif(tipo_mision_num == 2):
                tipo_mision = "búsqueda"
                lugar_posible = ["Árbol","Cadáver de dragón","Parte de cadáver de Dragón","Cofre","Armario","Ruina"]
                n = len(lugar_posible)-1
                lugar = random.randint(0,n)
                mision = "Hay que encontrar lo siguiente: "+lugar_posible[lugar]
                variableDeCheck = {}
                variableDeCheck[lugar_posible[lugar]] = False #ninguno de los jugadores lo ha encontrado
            

            print("Progreso: 12%")
            print(tipo_mision)
            print(mision)
            #generamos misión
            if(self.jugadorHost.genero == "hombre"):
                ref = "aventurero"
            else:
                ref = "aventurera"

            prompt =  f"""Eres un dungeon master de Dnd 5e y tienes un NPC que va a proponerme una misión, y se va a referir a mí como "aventurero".<|eot_id|><|start_header_id|>user<|end_header_id|>
                        Vas a generar un único párrafo del diálogo que usaría el NPC para proponerme esta misión: {mision}. Ten en cuenta que el NPC tiene el siguiente trasfondo:
                            {infoTrasfondo}\n. También tiene este motivo para estar en {self.ubicacion}, que es: {motivoUbicacion}. Puedes empezar con frases como "Por cierto, me gustaría proponerte algo..." o
                            "Um. Quizás puedas ayudarme con una cosa...".
                        No indiques cosas como **diálogo de propuesta de misión** o **párrafo motivacional**. 
                            <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
            dialogos_posibles = self.consultarAlDM(prompt,model_path,None,2048,300)
            print("Progreso: 20%")
            self.RAG_historia.escribirInfoMision(mision,dialogos_posibles)
            presentacion_NPC = f"""Eres un dungeon master de Dnd 5e y yo voy a hablar con un NPC por primera vez, y quieres que este NPC se presente, indicando su nombre y el nombre del lugar donde están.<|eot_id|><|start_header_id|>user<|end_header_id|>
                            Genera un único párrafo del diálogo que me diría ese NPC, refiriéndote a mí como "aventurero". Ten en cuenta que el NPC se llama {self.personaje.name}, y que tiene este trasfondo:
                            {infoTrasfondo}, y este motivo para estar en este lugar: {self.ubicacion}, que es este: {motivoUbicacion}. La descripción física de este NPC es esta {self.personaje.descripcion_fisica}. No hagas referencia al motivo
                            por el que el NPC está ahí, ni cuál es su objetivo, solo limítate a presentarle, sin dar muchos detalles. Omite cualquier frase del tipo "Claro, aquí tienes los párrafos" o cosas de por el estilo. Puedes empezar con frases como
                            "¡Hola aventurero! Soy..." o "¡Buenos días! Mi nombre es ... " o frases similares.
                            <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
            dialogos_presentacion = self.consultarAlDM(presentacion_NPC,model_path,None,2048,700)
            print("Progreso: 30%")
            self.RAG_historia.escribirDialogosNPC(dialogos_presentacion)

            #Creo el mapa 
            Mapa = Map_generation.Map_generation(self.ubicacion,self.currentPartida,tipo_mision,variableDeCheck,self.numJugadores,NPC_animacion,self.jugadorHost.id_jugador,self.width,self.height) #que genere el mapa de una mazmorra
            self.GLOBAL.setMAPA(Mapa)

            prompt_puerta_abierta = f"""Eres un dungeon master de Dnd 5e, y un jugador acaba de atravesar un portón de madera.<|eot_id|><|start_header_id|>user<|end_header_id|>
                            Genear una frase muy corta para decir que ha podido abrir la puerta sin problemas, y que se encuentra ahora en un pasillo oscuro con un suelo de baldosas moradas.
                            <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
            prompt_puerta_cerrada = f"""Eres un dungeon master de Dnd 5e, y un jugador ha intentado abrir un portón de madera y no ha podido.<|eot_id|><|start_header_id|>user<|end_header_id|>
                            Genear una frase muy corta para decir que no ha podido abrir la puerta porque está cerrada.
                            <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
            prompt_puerta_abierta_ady = f"""Eres un dungeon master de Dnd 5e, y un jugador acaba de atravesar un portón de madera.<|eot_id|><|start_header_id|>user<|end_header_id|>
                            Genear una frase muy corta para decir que ha podido abrir la puerta sin problemas, y que se encuentra ahora en una galería amplia bastante oscura.
                            <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
            regreso_a_sala = f"""Eres un dungeon master de Dnd 5e, y un jugador acaba de atravesar un portón de madera para regresar a una galería en la que había estado antes.<|eot_id|><|start_header_id|>user<|end_header_id|>
                            Genear una frase muy corta para decir que ha podido abrir la puerta sin problemas, y que se encuentra ahora en dicha galería, oscura.
                            <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
            #Creo el resto de estados de la máquina de estado
            frase_puerta = {}
            for i in Mapa.salas:
                # Paso toda la información que se ha creado en la generación del mapa a la máquina de estados
                frase_puerta[i] = {}
                for j in Mapa.salas[i].daASalas:
                    if(Mapa.salas[i].daASalas[j][1] == "abierto"):
                        if(Mapa.adyacencias[i][j] != 1):
                            descripcionpa = self.consultarAlDM(prompt_puerta_abierta,model_path,None,1048,200)
                            regresosa = self.consultarAlDM(regreso_a_sala,model_path,None,1048,200)
                            frase_puerta[i][j] = [None,descripcionpa,regresosa]
                        else:
                            descripcionpsa = self.consultarAlDM(prompt_puerta_abierta_ady,model_path,None,1048,200)
                            regresosa = self.consultarAlDM(regreso_a_sala,model_path,None,1048,200)
                            frase_puerta[i][j] = [None,descripcionpsa,regresosa]
                    else:
                        if(Mapa.adyacencias[i][j] != 1):
                            puertace = self.consultarAlDM(prompt_puerta_cerrada,model_path,None,1048,200)
                            descripcionpa = self.consultarAlDM(prompt_puerta_abierta,model_path,None,1048,200)
                            regresosa = self.consultarAlDM(regreso_a_sala,model_path,None,1048,200)
                            frase_puerta[i][j] = [puertace,descripcionpa,regresosa]
                        else:
                            puertace = self.consultarAlDM(prompt_puerta_cerrada,model_path,None,1048,200)
                            regresosa = self.consultarAlDM(regreso_a_sala,model_path,None,1048,200)
                            descripcionpsa = self.consultarAlDM(prompt_puerta_abierta_ady,model_path,None,1048,200)
                            frase_puerta[i][j] = [puertace,descripcionpsa,regresosa]
                objetos = ""
                for i_start in range(Mapa.salas[i].pos_x, Mapa.salas[i].size[0]):
                    for j_start in range(Mapa.salas[i].pos_y, Mapa.salas[j].size[1]):
                        if(33 <=Mapa.objetos[j_start][i_start] <=38):
                            objetos += "1 esqueleto, "
                        elif(Mapa.objetos[j_start][i_start] == 39):
                            objetos += "1 zombie, "
                        elif(Mapa.objetos[j_start][i_start] == 40):
                            objetos += "1 slime de color azul, "
                        elif(Mapa.objetos[j_start][i_start] == 41):
                            objetos += "1 beholder, "
                        elif(Mapa.objetos[j_start][i_start] == 42):
                            objetos += "1 troll, "
                        elif(43 <= Mapa.objetos[j_start][i_start] <= 46):
                            objetos += "1 dragón, "
                        elif(Mapa.objetos[j_start][i_start] == 47):
                            objetos += "1 extraña sombra humanoide, "
                        elif(Mapa.objetos[j_start][i_start] == 48):
                            objetos += "1 fénix, "
                        elif(Mapa.objetos[j_start][i_start] == 49):
                            objetos += "1 monstruo con forma de mantis religiosa gigante (un Ankheg), "
                        elif(50 <= Mapa.objetos[j_start][i_start] <= 56):
                            objetos += "1 basilisco, "
                        elif(Mapa.objetos[j_start][i_start] == 57):
                            objetos += "1 murciélago, "
                        elif(Mapa.objetos[j_start][i_start] == 58):
                            objetos += "1 rata, "
                        elif(59 <= Mapa.objetos[j_start][i_start] <= 66):
                            objetos += "1 gato, "
                        elif(Mapa.objetos[j_start][i_start] == 68):
                            objetos += "1 cerezo, "
                        elif(60 <= Mapa.objetos[j_start][i_start] <= 70):
                            objetos += "1 fragmento del cadáver de un dinosaurio, "
                        elif(71 <= Mapa.objetos[j_start][i_start] <= 74):
                            objetos += "1 cofre de gran tamaño, "
                        elif(75 <= Mapa.objetos[j_start][i_start] <= 78):
                            objetos += "1 armario, "
                        elif(Mapa.objetos[j_start][i_start] == 79):
                            objetos += "1 conjunto de ruinas arqueológicas, "
                        elif(91 <= Mapa.objetos[j_start][i_start] <= 94):
                            objetos += "1 tumba de piedra con una runa sobre ella, "
                        elif((95 <= Mapa.objetos[j_start][i_start] <= 97) or (Mapa.objetos[j_start][i_start] == 104)):
                            objetos += "1 canasto de madera con rubíes, "
                        elif((98 <= Mapa.objetos[j_start][i_start] <= 100) or (Mapa.objetos[j_start][i_start] == 105)):
                            objetos += "1 canasto de madera con esmeraldas, "
                        elif((Mapa.objetos[j_start][i_start] == 101) or (Mapa.objetos[j_start][i_start] == 106)):
                            objetos += "1 canasto de madera con algún mineral extraño de color amarillento, "
                        elif(101 <= Mapa.objetos[j_start][i_start] <= 103):
                            objetos += "1 saco de gran tamaño, "
                        elif(107 <= Mapa.objetos[j_start][i_start] <= 110):
                            objetos += "restos de roca por el suelo, "
                        elif(111 <= Mapa.objetos[j_start][i_start] <= 112):
                            objetos += "1 extraño hongo alargado de color azul oscuro, "
                        elif(113 <= Mapa.objetos[j_start][i_start] <= 114):
                            objetos += "setas de color naranja, "
                        elif(115 <= Mapa.objetos[j_start][i_start] <= 117):
                            objetos += "1 roca puntiaguda que sobresale del suelo, "
                        elif(118 <= Mapa.objetos[j_start][i_start] <= 121):
                            objetos += "marcas en el suelo de desgaste, "
                prompt_sala = f"""Eres un dungeon master de Dnd 5e, y un jugador acaba de entrar en una galería de una mina con suelo de piedra.<|eot_id|><|start_header_id|>user<|end_header_id|>
                            Genea un párrafo breve para describir la galería. Ten encuenta que tiene las siguientes cosas en ella: """+objetos+""". Comienza con la frase "En esta galería puedes ver..."<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
                descripcion_sala = self.consultarAlDM(prompt_sala,model_path,None,2048,600)
                self.maquina.crearEstadoSala(self.numJugadores,i,Mapa.salas[i].es_obligatoria,Mapa.salas[i].esInicial,Mapa.salas[i].daASalas,Mapa.salas[i].tienePortales,Mapa.salas[i].contieneLlaves,Mapa.salas[i].esFinal,Mapa.salas[i].orden,Mapa.salas[i].tipo_mision, Mapa.salas[i].size, Mapa.salas[i].pos_x, Mapa.salas[i].pos_y,Mapa,frase_puerta,descripcion_sala)
                # Guardamos las descripciones asociadas a esa sala
                self.RAG_historia.escribirInfoSala(i,frase_puerta,descripcion_sala)
            
            print("Progreso: 90%")
            self.maquina.crearEstadoDeMision(self.numJugadores,self.personaje.descripcion_fisica,motivoUbicacion,infoTrasfondo,NPC_imagen_carpeta)
            self.maquina.crearEstadoDeMisionConcreta(variableDeCheck,0,dialogos_presentacion,dialogos_posibles,self.numJugadores,self.personaje,tipo_mision,mision)
            print("Progreso: 100%")
            string = str(Mapa.playersCurrentPos[Mapa.id_host][0])+","+str(Mapa.playersCurrentPos[Mapa.id_host][1])
            conn = sqlite3.connect("simuladordnd.db")
            cur = conn.cursor()
            print(string,Mapa.id_host,self.currentPartida)
            query_updatej = """UPDATE personaje SET coordenadas_actuales = '"""+str(string)+"""' WHERE id_jugador = '"""+Mapa.id_host+"""' and partida_id = '"""+self.currentPartida+"""';"""
            cur.execute(query_updatej)
            conn.commit()
            conn.close() 


            self.maquina.resetGlobalsForPickle()

            with open('maquina_de_estados/'+self.currentPartida+'/maquina.pickle', "wb") as f:
                pickle.dump(self.maquina, f)
        else:
            conn = sqlite3.connect("simuladordnd.db")
            cur = conn.cursor()
            #cargamos la partida 1, si existe: el orden de las columnas será ese
            cur.execute("SELECT ubicacion_historia FROM partida WHERE numPartida = '"+self.currentPartida+"'")
            rows = cur.fetchall() #para llegar a esta pantalla, la pantalla tiene que existir sí o sí
            if(rows[0] != None):
                self.ubicacion = rows[0][0]
            conn.close()

            with open('maquina_de_estados/'+self.currentPartida+'/maquina.pickle', "rb") as f:
                self.maquina = pickle.load(f)
        mapa = Map_generation.Map_generation(self.ubicacion,self.currentPartida,None,None,None,None,None,self.width,self.height,True)
        self.maquina.setForLoad(mapa,self.jugadorHost)
        self.GLOBAL.setMAPA(mapa)
        #procesamiento....
        fin_time = time.time()
        print('Tiempo de procesamiento: '+str(fin_time - inicio)+" segundos") 

        self.GLOBAL.setActualPartidaState("partida")
        #TODO: Mensaje TCP a todos los jugadores para que cambien sus variables globales de actualPartidaScreen a "partida"
    
        self.maquina.initExecution()
        self.finished = False
        while(not self.finished):
            self.maquina.runNextEstado(self.jugadorHost)
            time.sleep(0.2)
            #Así evitamos la sobrecarga del portátil. Cada 0.2 segundos, se comprueba la máquina de estados


    def buscar_surface(self,obj, nombre_ruta="self.maquina", visitados=None):
        if visitados is None:
            visitados = set()

        obj_id = id(obj)
        if obj_id in visitados:
            return  # Evitar ciclos infinitos
        visitados.add(obj_id)

        if isinstance(obj, pygame.mixer.Sound):
            print(f"🎯 Encontrado pygame.Surface en: {nombre_ruta}")
        elif isinstance(obj, dict):
            for k, v in obj.items():
                self.buscar_surface(v, f"{nombre_ruta}[{repr(k)}]", visitados)
        elif hasattr(obj, '__dict__'):
            for attr, val in vars(obj).items():
                self.buscar_surface(val, f"{nombre_ruta}.{attr}", visitados)
        elif isinstance(obj, (list, tuple, set)):
            for idx, item in enumerate(obj):
                self.buscar_surface(item, f"{nombre_ruta}[{idx}]", visitados)

    def getNPC(self):
        return self.personaje

    def clickBotonPreparado(self):
        # #simulamos que todos le han dado ok al botón
        self.maquina.ordenEstados[self.maquina.salaInicialID].ModifyState(self.jugadorHost,0)#he hecho click en 'ok'

        # # #aquí se ejecutaría en función del personaje del TCP que llegó, o del host si hizo una acción
        # self.maquina.runNextEstado(self.jugadorHost)
        # #simulamos que el jugador le da click al NPC estando a 5 pies de distancia
        # #Sala 0 -> Mision 0 -> Habla NPC
        # self.maquina.ordenEstados[1].ordenEstados[0].ordenEstados[0].ModifyToTrueHablaNPC(self.jugadorHost)
        # self.maquina.runNextEstado(self.jugadorHost)
        # #simulamos que dice ok a ayudar
        # self.maquina.ordenEstados[1].ordenEstados[0].ordenEstados[1].giveMision()
        # self.maquina.runNextEstado(self.jugadorHost)


