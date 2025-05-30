import pyttsx3
from RAG_music.Consulta_RAG_musica import Consulta_RAG_musica
import sqlite3
import pygame
import random
from pygame import mixer
from huggingface_hub import hf_hub_download
from Global import Global
from Lista_Inventario import Lista_Inventario
import time
import json
import os
import sys
import contextlib
from multiprocessing import Queue
from maquina_de_estados import RAG_historia
from llama_cpp import Llama

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

class Estado:
    def __init__(self,isInicial,content,id):
        self.id =  id
        if(isInicial):
            self.esInicial = True
            self.esPuntoDeRespawn = False
            self.tipo_de_estado = "Introducción"
            self.esObligatorio = True
            self.cancion = None #por definir con el RAG
            self.variableDeCheck = {"progreso": False}
            self.dialogoDMIntro = content #mensaje que dirá el DM al iniciar el estado
            self.dialogoDMExit = None
        else:
            self.esInicial = False
            self.esPuntoDeRespawn = None
            self.tipo_de_estado = None
            self.esObligatorio = None
            self.cancion = None
            self.variableDeCheck = {}
            self.dialogoDMIntro = content #mensaje que dirá el DM al iniciar el estado
            self.dialogoDMExit = None
        self.GLOBAL = Global()
        self.estadoAlQuePertenezco = None
        self.estadoPredecesor = None
        self.estadosSucesores = {}
        self.NPCs = {}
        self.jugadores = {}
        self.mobs = {}
        self.objetos = {}
        self.Mapa = None
        self.ordenEstados = {}
        self.soundDoor = pygame.mixer.Sound('sounds/door.wav')
        self.personajeDelHost = None


    def checkIfCanRun(self,player):
        pass

    def checkIfCompleted(self,player):
        pass

    def OnEnterEstadoByPlayer(self,player,DM):
        pass
    def OnExitEstadoByPlayer(self,player,DM):
        pass
    def OnEnterEstadoByAllPlayers(self,DM):
        pass
    def OnExitEstadoByPlayers(self,DM):
        pass
    def resetForPickle(self):
        self.GLOBAL = None
        self.Mapa = None
        self.personajeDelHost = None
        self.soundDoor = None
        if(self.ordenEstados != {}):
            for id,estado in self.ordenEstados.items():
                estado.resetForPickle()

    def setForLoad(self,mapa,jugador):
        self.GLOBAL = Global()
        self.Mapa = mapa
        self.personajeDelHost = jugador
        self.soundDoor = pygame.mixer.Sound('sounds/door.wav')
        if(self.ordenEstados != {}):
            for id,estado in self.ordenEstados.items():
                estado.setForLoad(mapa,jugador)

class EstadoRecolectAndBreak(Estado):
    def __init__(self,isInicial,content,id,obligatorio,personajeDelHost,numJugadores,estado_pred):
        super().__init__(isInicial,content,id)
        # No hay variable de progreso, puesto que se puede recolectar y romper cualquier objeto
        self.isInicial = isInicial
        self.personajeDelHost = personajeDelHost
        self.esObligatorio = obligatorio
        self.numJugadores = numJugadores
        self.esPuntoDeRespawn = False
        self.tipo_de_estado = "recoleccion_y_rotura"
        self.estadosSucesores = estado_pred
        self.mobsEncontrados = {}
        self.ids = 0 
        self.x = None
        self.y = None
        self.ordenEstados = {} #Estados internos de misión
        self.click = {}
        self.click[str(self.personajeDelHost.name)+","+str(self.personajeDelHost.id_jugador)] = False
        for personaje in self.GLOBAL.getListaPersonajeHost():
            self.click[str(personaje.name)+","+str(personaje.id_jugador)] = False 


    def checkIfCanRun(self,DM,personaje):
        canBreak  = self.GLOBAL.getCanBreak()
        self.x = personaje.coordenadas_actuales_r[0]
        self.y = personaje.coordenadas_actuales_r[1]
        if(canBreak[0]):
            if(((personaje.playerAction == "WALK_DOWN") or (personaje.playerAction == "IDLE_DOWN")) and ((self.x == canBreak[1][0]) and (self.y == (canBreak[1][1]-1)))):  
                self.y+=1
                return True
            elif(((personaje.playerAction == "WALK_UP") or (personaje.playerAction == "IDLE_UP")) and ((self.x == canBreak[1][0]) and (self.y == (canBreak[1][1]+1)))):
                self.y-=1
                return True
            elif(((personaje.playerAction == "WALK_LEFT") or (personaje.playerAction == "IDLE_LEFT")) and ((self.x == (canBreak[1][0]+1)) and (self.y == canBreak[1][1]))):
                self.x-=1
                return True
            elif(((personaje.playerAction == "WALK_RIGHT") or (personaje.playerAction == "IDLE_RIGHT")) and ((self.x == (canBreak[1][0]-1)) and (self.y == canBreak[1][1]))):
                self.x+=1
                return True
        return False

    def checkIfCompleted(self,personaje):
        return False 
    
    def consultarAlDM(self,prompt,fin,token_context = 1024,token_gen = 300):
        model_name = "bartowski/Llama-3.2-3B-Instruct-GGUF"
        model_file = "Llama-3.2-3B-Instruct-Q4_K_M.gguf"
        model_path = hf_hub_download(model_name, filename=model_file)
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
        
    def run(self,DM,personaje):
        # SARCÓFAGO
        x = self.x
        y = self.y
        lista_inv = Lista_Inventario()
        if(91 <= self.Mapa.objetos[y][x] <= 94):
            # Si es un sarcófago, hay que comprobar que no tenga objetos, o de lo contrario se perderán
            sala_actual = self.Mapa.getRoomAtPoint(x,y,self.Mapa.room_sizes,self.Mapa.room_start_points)
            if(self.Mapa.salas[sala_actual].cofresSinLoot.get(str([x,y])) != None):
                # El sarcófago está vacío, y se puede romper
                cancion =  pygame.mixer.Sound('sounds/break.wav')
                pygame.mixer.Channel(6).play(cancion)
                cancion = None
                self.Mapa.objetos[y][x] = 0
                texto = "Espera un momento que piense..."
                DM.speak(texto)
                usado = ""
                item_left = personaje.equipo.objeto_equipado_mano_izquierda  
                item_right = personaje.equipo.objeto_equipado_mano_derecha
                if(item_left == None and item_right == None):
                    usado = " con solo mis manos vacías, rompiéndolo a puñetazos"
                if(item_left != None):
                    usado = " teniendo en mi mano izquierda el siguiente objeto: "+item_left[1]
                if(item_right != None):
                    if(item_left != None):
                        usado += " y "
                    usado = " teniendo en mi mano derecha el siguiente objeto: "+item_right[1]
                prompt = """Eres un dungeon master de Dnd 5e y yo voy a romper un sarcófago. El resultado de mi acción, es que el sarcófago queda destruido. En ningún caso puedo recibir daño de tal acción.<|eot_id|><|start_header_id|>user<|end_header_id|>
                            Teniendo en cuenta únicamente el siguiente contexto para responder a la pregunta: Yo como jugador voy a romper el sarcófago """+usado+""". Si llevase algún objeto en mis manos, preferiblemente uso esos objetos para golpear y romper el sarcófago. Si los objetos que llevo no permiten romper el sarcófago, indica que lo rompo con mis propios puños a base de puñetazos. El resultado final es que lo destruyo.
                            Pregunta: ¿Cómo rompo yo el sarcófago?
                            <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
                texto = self.consultarAlDM(prompt,None,1024,400)
                texto.replace("\\n", " ")
                texto = ''.join(c for c in texto if c.isprintable())
                DM.speak(texto)
                a_lista = "El jugador ha destruido un sarcófago, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
                self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
                self.GLOBAL.addBrokenObject()
            else:
                # El sarcófago contiene objeto, y no se puede romper
                texto = "Espera un momento que piense..."
                DM.speak(texto)
                usado = ""
                item_left = personaje.equipo.objeto_equipado_mano_izquierda  
                item_right = personaje.equipo.objeto_equipado_mano_derecha
                if(item_left == None and item_right == None):
                    usado = " con solo mis manos vacías"
                if(item_left != None):
                    usado = " teniendo en mi mano izquierda el siguiente objeto: "+item_left[1]
                if(item_right != None):
                    if(item_left != None):
                        usado += " y "
                    usado = " teniendo en mi mano derecha el siguiente objeto: "+item_right[1]
                prompt = """Eres un dungeon master de Dnd 5e y yo me acerco a un sarcófago. El resultado de mi acción, es que sacudo el sarcófago, pero no lo destruyo porque escucho un ruido de su interior, de algún objeto que al moverse hace un ruido.<|eot_id|><|start_header_id|>user<|end_header_id|>
                            Teniendo en cuenta únicamente el siguiente contexto para responder a la pregunta: Yo como jugador me dirijo al sarcófago """+usado+""". Si llevase algún objeto en mis manos, preferiblemente uso esos objetos para sacudir el sarcófago. Si los objetos que llevo no permiten sacudir el sarcófago, indica que lo sacudo con mis propias manos. El resultado final es que no lo destruyo.
                            Pregunta: ¿Qué sucede al acercarme al sarcófago?
                            <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
                texto = self.consultarAlDM(prompt,None,1024,400)
                texto.replace("\\n", " ")
                texto = ''.join(c for c in texto if c.isprintable())
                DM.speak(texto)
                a_lista = "El jugador ha sacudido un sarcófago, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
                self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
        # Rubíes
        elif((95 <= self.Mapa.objetos[y][x] <= 97) or (self.Mapa.objetos[y][x] == 104)):
            # Como se pueden recolectar, compruebo que haya espacio disponible en el inventario
            lista = lista_inv.getRecolectables()
            rubi = lista["Recoleccion"]["Rubí"]
            cancion =  pygame.mixer.Sound('sounds/break.wav')
            pygame.mixer.Channel(6).play(cancion)
            cancion = None
            self.Mapa.objetos[y][x] = 0
            res = personaje.equipo.addObjectToInventory(rubi,"Recoleccion","Rubí")
            texto = "Espera un momento que piense..."
            DM.speak(texto)
            usado = ""
            item_left = personaje.equipo.objeto_equipado_mano_izquierda  
            item_right = personaje.equipo.objeto_equipado_mano_derecha
            if(item_left == None and item_right == None):
                usado = " con solo mis manos vacías, rompiéndolo a puñetazos"
            if(item_left != None):
                usado = " teniendo en mi mano izquierda el siguiente objeto: "+item_left[1]
            if(item_right != None):
                if(item_left != None):
                    usado += " y "
                usado = " teniendo en mi mano derecha el siguiente objeto: "+item_right[1]
            prompt = """Eres un dungeon master de Dnd 5e y yo voy a destruir un canasto de rubíes que tengo justo delante. El resultado de mi acción, es que destruyo el canasto de rubíes. En ningún caso puedo recibir daño de tal acción.<|eot_id|><|start_header_id|>user<|end_header_id|>
                        Teniendo en cuenta únicamente el siguiente contexto para responder a la pregunta: Yo como jugador me dirijo al canasto de rubíes """+usado+""". Si llevase algún objeto en mis manos, preferiblemente uso esos objetos para romper el canasto de rubíes. Si los objetos que llevo no permiten romper el canasto, indica que lo rompo con mis propias manos. El resultado final es que lo destruyo.
                        Pregunta: ¿Cómo rompo yo el canasto de rubíes?
                        <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
            if(res == -1):
                texto = self.consultarAlDM(prompt," Sin embargo, llevas mucho peso encima, y te ves obligado a tirar los rubíes.",1024,400)
                texto.replace("\\n", " ")
                texto = ''.join(c for c in texto if c.isprintable())
                DM.speak(texto)
            elif(res == -2):
                texto = self.consultarAlDM(prompt,"  Sin embargo, no tienes espacio disponible para cargar con los rubíes, y te ves obligado a tirarlos.",1024,400)
                texto.replace("\\n", " ")
                texto = ''.join(c for c in texto if c.isprintable())
                DM.speak(texto)
            else:
                texto = self.consultarAlDM(prompt,"  Añades uno de esos preciados rubíes a tu inventario.",1024,400)
                texto.replace("\\n", " ")
                texto = ''.join(c for c in texto if c.isprintable())
                DM.speak(texto)
            a_lista = "El jugador ha destruido un canasto de rubíes, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.addBrokenObject()
                

        # Esmeraldas
        elif((98 <= self.Mapa.objetos[y][x] <= 100) or (self.Mapa.objetos[y][x] == 105)):
            # Como se pueden recolectar, compruebo que haya espacio disponible en el inventario
            lista = lista_inv.getRecolectables()
            esmeralda = lista["Recoleccion"]["Esmeralda"]
            cancion =  pygame.mixer.Sound('sounds/break.wav')
            pygame.mixer.Channel(6).play(cancion)
            cancion = None
            self.Mapa.objetos[y][x] = 0
            res = personaje.equipo.addObjectToInventory(esmeralda,"Recoleccion","Esmeralda")
            texto = "Espera un momento que piense..."
            DM.speak(texto)
            usado = ""
            item_left = personaje.equipo.objeto_equipado_mano_izquierda  
            item_right = personaje.equipo.objeto_equipado_mano_derecha
            if(item_left == None and item_right == None):
                usado = " con solo mis manos vacías, rompiéndolo a puñetazos"
            if(item_left != None):
                usado = " teniendo en mi mano izquierda el siguiente objeto: "+item_left[1]
            if(item_right != None):
                if(item_left != None):
                    usado += " y "
                usado = " teniendo en mi mano derecha el siguiente objeto: "+item_right[1]
            prompt = """Eres un dungeon master de Dnd 5e y yo voy a destruir un canasto de esmeraldas que tengo justo delante. El resultado de mi acción, es que destruyo el canasto de esmeraldas. En ningún caso puedo recibir daño de tal acción.<|eot_id|><|start_header_id|>user<|end_header_id|>
                        Teniendo en cuenta únicamente el siguiente contexto para responder a la pregunta: Yo como jugador me dirijo al canasto de esmeraldas """+usado+""". Si llevase algún objeto en mis manos, preferiblemente uso esos objetos para romper el canasto de esmeraldas. Si los objetos que llevo no permiten romper el canasto, indica que lo rompo con mis propias manos. El resultado final es que lo destruyo.
                        Pregunta: ¿Cómo rompo yo el canasto de esmeraldas?
                        <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
            if(res == -1):
                texto = self.consultarAlDM(prompt," Sin embargo, llevas mucho peso encima, y te ves obligado a tirar las esmeraldas.",1024,400)
                texto.replace("\\n", " ")
                texto = ''.join(c for c in texto if c.isprintable())
                DM.speak(texto)
            elif(res == -2):
                texto = self.consultarAlDM(prompt,"  Sin embargo, no tienes espacio disponible para cargar con las esmeraldas, y te ves obligado a tirarlas.",1024,400)
                texto.replace("\\n", " ")
                texto = ''.join(c for c in texto if c.isprintable())
                DM.speak(texto)
            else:
                texto = self.consultarAlDM(prompt,"  Añades una de esas preciadas esmeraldas a tu inventario.",1024,400)
                texto.replace("\\n", " ")
                texto = ''.join(c for c in texto if c.isprintable())
                DM.speak(texto)
            a_lista = "El jugador ha destruido un canasto de esmeraldas, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.addBrokenObject()
        # Mineral extraño
        elif((self.Mapa.objetos[y][x] == 101) or (self.Mapa.objetos[y][x] == 106)):
            # Como se pueden recolectar, compruebo que haya espacio disponible en el inventario
            lista = lista_inv.getRecolectables()
            mineral = lista["Recoleccion"]["Mineral"]
            cancion =  pygame.mixer.Sound('sounds/break.wav')
            pygame.mixer.Channel(6).play(cancion)
            cancion = None
            self.Mapa.objetos[y][x] = 0
            res = personaje.equipo.addObjectToInventory(mineral,"Recoleccion","Mineral")
            texto = "Espera un momento que piense..."
            DM.speak(texto)
            usado = ""
            item_left = personaje.equipo.objeto_equipado_mano_izquierda  
            item_right = personaje.equipo.objeto_equipado_mano_derecha
            if(item_left == None and item_right == None):
                usado = " con solo mis manos vacías, rompiéndolo a puñetazos"
            if(item_left != None):
                usado = " teniendo en mi mano izquierda el siguiente objeto: "+item_left[1]
            if(item_right != None):
                if(item_left != None):
                    usado += " y "
                usado = " teniendo en mi mano derecha el siguiente objeto: "+item_right[1]
            prompt = """Eres un dungeon master de Dnd 5e y yo voy a destruir un canasto de minerales amarillos que tengo justo delante. El resultado de mi acción, es que destruyo el canasto de minerales amarillos. En ningún caso puedo recibir daño de tal acción.<|eot_id|><|start_header_id|>user<|end_header_id|>
                        Teniendo en cuenta únicamente el siguiente contexto para responder a la pregunta: Yo como jugador me dirijo al canasto de minerales amarillas """+usado+""". Si llevase algún objeto en mis manos, preferiblemente uso esos objetos para romper el canasto de minerales amarillos. Si los objetos que llevo no permiten romper el canasto, indica que lo rompo con mis propias manos. El resultado final es que lo destruyo.
                        Pregunta: ¿Cómo rompo yo el canasto de minerales amarillos?
                        <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
            if(res == -1):
                texto = self.consultarAlDM(prompt," Sin embargo, llevas mucho peso encima, y te ves obligado a tirar los minerales amarillos.",1024,400)
                texto.replace("\\n", " ")
                texto = ''.join(c for c in texto if c.isprintable())
                DM.speak(texto)
            elif(res == -2):
                texto = self.consultarAlDM(prompt,"  Sin embargo, no tienes espacio disponible para cargar con los minerales amarillos, y te ves obligado a tirarlos.",1024,400)
                texto.replace("\\n", " ")
                texto = ''.join(c for c in texto if c.isprintable())
                DM.speak(texto)
            else:
                texto = self.consultarAlDM(prompt,"  Añades uno de esos preciados minerales amarillos a tu inventario.",1024,400)
                texto.replace("\\n", " ")
                texto = ''.join(c for c in texto if c.isprintable())
                DM.speak(texto)
            a_lista = "El jugador ha destruido un canasto de minerales amarillos, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.addBrokenObject()
        # Saco de monedas
        elif(101 <= self.Mapa.objetos[y][x] <= 103):
            # Como se pueden recolectar, compruebo que haya espacio disponible en el inventario
            cancion =  pygame.mixer.Sound('sounds/coins.wav')
            pygame.mixer.Channel(6).play(cancion)
            cancion = None
            self.Mapa.objetos[y][x] = 0
            money_value = random.randint(1,5)
            if(money_value == 1):
                num = random.randint(1,100)
                personaje.pc += num
                moneda = "cobre"
            elif(money_value == 2):
                num = random.randint(1,50)
                personaje.pp += num
                moneda = "plata"
            elif(money_value == 3):
                num = random.randint(1,25)
                personaje.pe += num
                moneda = "electro"
            elif(money_value == 4):
                num = random.randint(1,10)
                personaje.po += num
                moneda = "oro"
            elif(money_value == 5):
                num = random.randint(1,3)
                personaje.ppt += num
                moneda = "platino"

            texto = "Espera un momento que piense..."
            DM.speak(texto)
            prompt = """Eres un dungeon master de Dnd 5e y yo me acerco a un saco de cuero tengo justo delante. El resultado de mi acción, es que abro el saco de cuero, y veo que dentro hay """+str(num)+""" monedas de """+moneda+""".<|eot_id|><|start_header_id|>user<|end_header_id|>
                        Teniendo en cuenta únicamente el siguiente contexto para responder a la pregunta: Yo como jugador me dirijo al saco de cuero, y lo abro para ver qué hay dentro. Dentro, encuentro """+str(num)+""" monedas de """+moneda+""".
                        Pregunta: ¿Qué sucede cuando me acerco al saco de cuero que tengo justo delante?
                        <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
            if(num == 1):
                string = " Tras eso, añades "+str(num)+" moneda de "+moneda +" a tu inventario."
            else:
                string = " Tras eso, añades las "+str(num)+" monedas de "+moneda +" a tu inventario."
            texto = self.consultarAlDM(prompt,string,1024,400)
            texto.replace("\\n", " ")
            texto = ''.join(c for c in texto if c.isprintable())
            DM.speak(texto)
            a_lista = "El jugador ha abierto un saco de cuero, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.addBrokenObject()
        # Hongo azul
        elif(111 <= self.Mapa.objetos[y][x] <= 112):
            # Como se pueden recolectar, compruebo que haya espacio disponible en el inventario
            lista = lista_inv.getRecolectables()
            hongo = lista["Recoleccion"]["Hongo"]
            cancion =  pygame.mixer.Sound('sounds/cut.wav')
            pygame.mixer.Channel(6).play(cancion)
            cancion = None
            self.Mapa.objetos[y][x] = 0
            res = personaje.equipo.addObjectToInventory(hongo,"Recoleccion","Hongo")
            texto = "Espera un momento que piense..."
            DM.speak(texto)
            usado = ""
            item_left = personaje.equipo.objeto_equipado_mano_izquierda  
            item_right = personaje.equipo.objeto_equipado_mano_derecha
            if(item_left == None and item_right == None):
                usado = " con solo mis manos vacías, arrancándolo de cuajo"
            if(item_left != None):
                usado = " teniendo en mi mano izquierda el siguiente objeto: "+item_left[1]
            if(item_right != None):
                if(item_left != None):
                    usado += " y "
                usado = " teniendo en mi mano derecha el siguiente objeto: "+item_right[1]
            prompt = """Eres un dungeon master de Dnd 5e y yo me acerco a un hongo azul alargado que tengo justo delante. El resultado de mi acción, es que arranco el hongo azul del suelo de la mazmorra. En ningún caso puedo recibir daño de tal acción.<|eot_id|><|start_header_id|>user<|end_header_id|>
                        Teniendo en cuenta únicamente el siguiente contexto para responder a la pregunta: Yo como jugador me dirijo al hongo azul """+usado+""". Si llevase algún objeto en mis manos, preferiblemente uso esos objetos para arrancar o cortar el hongo. Si los objetos que llevo no permiten romper o arrancar el hongo azul, indica que lo arranco de cuajo con mis propias manos. El resultado final es que lo arranco del suelo.
                        Pregunta: ¿Qué sucede cuando me acerco al hongo azul alargado que tengo justo delante?
                        <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
            if(res == -1):
                texto = self.consultarAlDM(prompt," Sin embargo, llevas mucho peso encima, y te ves obligado a tirar dicho hongo.",1024,400)
                texto.replace("\\n", " ")
                texto = ''.join(c for c in texto if c.isprintable())
                DM.speak(texto)
            elif(res == -2):
                texto = self.consultarAlDM(prompt,"  Sin embargo, no tienes espacio disponible para cargar con el hongo, y te ves obligado a tirarlo.",1024,400)
                texto.replace("\\n", " ")
                texto = ''.join(c for c in texto if c.isprintable())
                DM.speak(texto)
            else:
                texto = self.consultarAlDM(prompt,"Añades dicho hongo a tu inventario.",1024,400)
                texto.replace("\\n", " ")
                texto = ''.join(c for c in texto if c.isprintable())
                DM.speak(texto)
            a_lista = "El jugador ha arrancado un hongo azul, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.addBrokenObject()
        # Seta
        elif(113 <= self.Mapa.objetos[y][x] <= 114):
            # Como se pueden recolectar, compruebo que haya espacio disponible en el inventario
            lista = lista_inv.getRecolectables()
            seta = lista["Recoleccion"]["Seta"]
            cancion =  pygame.mixer.Sound('sounds/cut.wav')
            pygame.mixer.Channel(6).play(cancion)
            cancion = None
            self.Mapa.objetos[y][x] = 0
            res = personaje.equipo.addObjectToInventory(seta,"Recoleccion","Seta")
            texto = "Espera un momento que piense..."
            DM.speak(texto)
            usado = ""
            item_left = personaje.equipo.objeto_equipado_mano_izquierda  
            item_right = personaje.equipo.objeto_equipado_mano_derecha
            if(item_left == None and item_right == None):
                usado = " con solo mis manos vacías, arrancándolo de cuajo"
            if(item_left != None):
                usado = " teniendo en mi mano izquierda el siguiente objeto: "+item_left[1]
            if(item_right != None):
                if(item_left != None):
                    usado += " y "
                usado = " teniendo en mi mano derecha el siguiente objeto: "+item_right[1]
            prompt = """Eres un dungeon master de Dnd 5e y yo me acerco a una seta naranja que tengo justo delante. El resultado de mi acción, es que arranco la seta naranja del suelo de la mazmorra. En ningún caso puedo recibir daño de tal acción.<|eot_id|><|start_header_id|>user<|end_header_id|>
                        Teniendo en cuenta únicamente el siguiente contexto para responder a la pregunta: Yo como jugador me dirijo a la seta naranja """+usado+""". Si llevase algún objeto en mis manos, preferiblemente uso esos objetos para arrancar o cortar la seta. Si los objetos que llevo no permiten romper o arrancar la seta naranja, indica que la arranco de cuajo con mis propias manos. El resultado final es que la arranco del suelo.
                        Pregunta: ¿Qué sucede cuando me acerco a la seta naranja que tengo justo delante?
                        <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
            if(res == -1):
                texto = self.consultarAlDM(prompt," Sin embargo, llevas mucho peso encima, y te ves obligado a tirar dicha seta.",1024,400)
                texto.replace("\\n", " ")
                texto = ''.join(c for c in texto if c.isprintable())
                DM.speak(texto)
            elif(res == -2):
                texto = self.consultarAlDM(prompt,"  Sin embargo, no tienes espacio disponible para cargar con la seta, y te ves obligado a tirarla.",1024,400)
                texto.replace("\\n", " ")
                texto = ''.join(c for c in texto if c.isprintable())
                DM.speak(texto)
            else:
                texto = self.consultarAlDM(prompt,"  Añades dicha seta a tu inventario.",1024,400)
                texto.replace("\\n", " ")
                texto = ''.join(c for c in texto if c.isprintable())
                DM.speak(texto)
            a_lista = "El jugador ha arrancado una seta naranja, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.addBrokenObject()

        # Roca para romperla
        elif(115 <= self.Mapa.objetos[y][x] <= 117):
            cancion =  pygame.mixer.Sound('sounds/break.wav')
            pygame.mixer.Channel(6).play(cancion)
            cancion = None
            self.Mapa.objetos[y][x] = 0
            texto = "Espera un momento que piense..."
            DM.speak(texto)
            usado = ""
            item_left = personaje.equipo.objeto_equipado_mano_izquierda  
            item_right = personaje.equipo.objeto_equipado_mano_derecha
            if(item_left == None and item_right == None):
                usado = " con solo mis manos vacías, rompiéndola a puñetazos"
            if(item_left != None):
                usado = " teniendo en mi mano izquierda el siguiente objeto: "+item_left[1]
            if(item_right != None):
                if(item_left != None):
                    usado += " y "
                usado = " teniendo en mi mano derecha el siguiente objeto: "+item_right[1]
            prompt = """Eres un dungeon master de Dnd 5e y yo voy a destruir una roca puntiaguda que tengo justo delante. El resultado de mi acción, es que destruyo la roca puntiaguda que sobresalía del suelo de la mazmorra. En ningún caso puedo recibir daño de tal acción.<|eot_id|><|start_header_id|>user<|end_header_id|>
                        Teniendo en cuenta únicamente el siguiente contexto para responder a la pregunta: Yo como jugador me dirijo a la roca puntiaguda """+usado+""". Si llevase algún objeto en mis manos, preferiblemente uso esos objetos para romper la roca puntiaguda. Si los objetos que llevo no permiten romper la roca puntiaguda, indica que la hago añicos con mis propias manos. El resultado final, es que la roca se destruye.
                        Pregunta: ¿Qué sucede al acercame a la roca puntiaguda que tengo delante?
                        <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
            texto = self.consultarAlDM(prompt,None,1024,400)
            texto.replace("\\n", " ")
            texto = ''.join(c for c in texto if c.isprintable())
            DM.speak(texto)
            a_lista = "El jugador ha destruido una roca, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.addBrokenObject()

        # Esqueleto
        elif(33 <= self.Mapa.objetos[y][x] <= 38):
            sound = pygame.mixer.Sound('sounds/zombie.mp3')
            pygame.mixer.Channel(6).play(sound)
            sound = None
            info_mob = "Te acercas poco a poco al esqueleto que tienes delante, y ves que se remueve ligeramente. Te muestro una imagen."
            if(self.mobsEncontrados.get(str([x,y])) == None):
                # Leer descripción del mob, y lo añadimos a mobs encontrados
                self.mobsEncontrados[str([x,y])] = "esqueleto"
                # Cogemos la descripción del mob del .json
                self.dir = 'descripciones'
                self.file = 'Monsters.json'
                with open(self.dir+'/'+self.file,'r',encoding='utf-8') as f:
                    try:
                        Monster_descripcion = json.load(f)
                        descripcion = "Delante de ti, ves a un extraño ser. "+Monster_descripcion["no-muerto"][0]
                        descripcion += " "+info_mob
                    except Exception as e:
                        print(e)
            else:
                descripcion = info_mob
            DM.speak(descripcion)
            a_lista = "El jugador se ha acercado a un esqueleto viviente, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.setImagePartida("images/monsters/no-muerto esqueleto.png")
            self.GLOBAL.setShowImage(True)

        # Zombie
        elif(self.Mapa.objetos[y][x] == 39):
            sound = pygame.mixer.Sound('sounds/zombie.mp3')
            pygame.mixer.Channel(6).play(sound)
            sound = None
            info_mob = "Te acercas poco a poco al zombie que tienes delante, y ves que se remueve ligeramente. Te muestro una imagen."
            if(self.mobsEncontrados.get(str([x,y])) == None):
                # Leer descripción del mob, y lo añadimos a mobs encontrados
                self.mobsEncontrados[str([x,y])] = "zombie"
                # Cogemos la descripción del mob del .json
                self.dir = 'descripciones'
                self.file = 'Monsters.json'
                with open(self.dir+'/'+self.file,'r',encoding='utf-8') as f:
                    try:
                        Monster_descripcion = json.load(f)
                        descripcion = "Delante de ti, ves a un extraño ser. "+Monster_descripcion["no-muerto"][0]
                        descripcion += " "+info_mob
                    except Exception as e:
                        print(e)
            else:
                descripcion = info_mob
            DM.speak(descripcion)
            a_lista = "El jugador se ha acercado a un zombie, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.setImagePartida("images/monsters/no-muerto zombie.png")
            self.GLOBAL.setShowImage(True)
        # Slime
        elif(self.Mapa.objetos[y][x] == 40):
            sound = pygame.mixer.Sound('sounds/slime.mp3')
            pygame.mixer.Channel(6).play(sound)
            sound = None
            info_mob = "Te acercas poco a poco al slime que tienes delante, y ves que se remueve ligeramente. Te muestro una imagen."
            if(self.mobsEncontrados.get(str([x,y])) == None):
                # Leer descripción del mob, y lo añadimos a mobs encontrados
                self.mobsEncontrados[str([x,y])] = "slime"
                # Cogemos la descripción del mob del .json
                self.dir = 'descripciones'
                self.file = 'Monsters.json'
                with open(self.dir+'/'+self.file,'r',encoding='utf-8') as f:
                    try:
                        Monster_descripcion = json.load(f)
                        descripcion = "Delante de ti, ves a un extraño ser. "+Monster_descripcion["slime"][0]
                        descripcion += " "+info_mob
                    except Exception as e:
                        print(e)
            else:
                descripcion = info_mob
            DM.speak(descripcion)
            a_lista = "El jugador se ha acercado a un slime, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.setImagePartida("images/monsters/slime.png")
            self.GLOBAL.setShowImage(True)
        # Beholder
        elif(self.Mapa.objetos[y][x] == 41):
            sound = pygame.mixer.Sound('sounds/beholder.mp3')
            pygame.mixer.Channel(6).play(sound)
            sound = None
            info_mob = "Te acercas poco a poco al beholder que tienes delante, y ves que se remueve ligeramente. Te muestro una imagen."
            if(self.mobsEncontrados.get(str([x,y])) == None):
                # Leer descripción del mob, y lo añadimos a mobs encontrados
                self.mobsEncontrados[str([x,y])] = "beholder"
                # Cogemos la descripción del mob del .json
                self.dir = 'descripciones'
                self.file = 'Monsters.json'
                with open(self.dir+'/'+self.file,'r',encoding='utf-8') as f:
                    try:
                        Monster_descripcion = json.load(f)
                        descripcion = "Delante de ti, ves a un extraño ser. "+Monster_descripcion["beholder"][0]
                        descripcion += " "+info_mob
                    except Exception as e:
                        print(e)
            else:
                descripcion = info_mob
            DM.speak(descripcion)
            a_lista = "El jugador se ha acercado a un beholder, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.setImagePartida("images/monsters/beholder.png")
            self.GLOBAL.setShowImage(True)
        # Troll
        elif(self.Mapa.objetos[y][x] == 42):
            sound = pygame.mixer.Sound('sounds/troll.mp3')
            pygame.mixer.Channel(6).play(sound)
            sound = None
            info_mob = "Te acercas poco a poco al troll que tienes delante, y ves que se remueve ligeramente. Te muestro una imagen."
            if(self.mobsEncontrados.get(str([x,y])) == None):
                # Leer descripción del mob, y lo añadimos a mobs encontrados
                self.mobsEncontrados[str([x,y])] = "troll"
                # Cogemos la descripción del mob del .json
                self.dir = 'descripciones'
                self.file = 'Monsters.json'
                with open(self.dir+'/'+self.file,'r',encoding='utf-8') as f:
                    try:
                        Monster_descripcion = json.load(f)
                        descripcion = "Delante de ti, ves a un extraño ser. "+Monster_descripcion["troll"][0]
                        descripcion += " "+info_mob
                    except Exception as e:
                        print(e)
            else:
                descripcion = info_mob
            DM.speak(descripcion)
            a_lista = "El jugador se ha acercado a un troll, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.setImagePartida("images/monsters/troll.png")
            self.GLOBAL.setShowImage(True)
        # Dragón
        elif(43 <= self.Mapa.objetos[y][x] <= 46):
            sound = pygame.mixer.Sound('sounds/dragon.mp3')
            pygame.mixer.Channel(6).play(sound)
            sound = None
            info_mob = "Te acercas poco a poco al dragón que tienes delante, y ves que se remueve ligeramente. Te muestro una imagen."
            if(self.mobsEncontrados.get(str([x,y])) == None):
                # Leer descripción del mob, y lo añadimos a mobs encontrados
                self.mobsEncontrados[str([x,y])] = "dragón"
                # Cogemos la descripción del mob del .json
                self.dir = 'descripciones'
                self.file = 'Monsters.json'
                with open(self.dir+'/'+self.file,'r',encoding='utf-8') as f:
                    try:
                        Monster_descripcion = json.load(f)
                        descripcion = "Delante de ti, ves a un extraño ser. "+Monster_descripcion["dragón"][0]
                        descripcion += " "+info_mob
                    except Exception as e:
                        print(e)
            else:
                descripcion = info_mob
            DM.speak(descripcion)
            a_lista = "El jugador se ha acercado a un dragón, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.setImagePartida("images/monsters/dragón.png")
            self.GLOBAL.setShowImage(True)
        # Sombra humanoide
        elif(self.Mapa.objetos[y][x] == 47):
            sound = pygame.mixer.Sound('sounds/sombra.mp3')
            pygame.mixer.Channel(6).play(sound)
            sound = None
            info_mob = "Te acercas poco a poco a la sombra humanoide que tienes delante, y ves que se remueve ligeramente. Te muestro una imagen."
            if(self.mobsEncontrados.get(str([x,y])) == None):
                # Leer descripción del mob, y lo añadimos a mobs encontrados
                self.mobsEncontrados[str([x,y])] = "sombra"
                # Cogemos la descripción del mob del .json
                self.dir = 'descripciones'
                self.file = 'Monsters.json'
                with open(self.dir+'/'+self.file,'r',encoding='utf-8') as f:
                    try:
                        Monster_descripcion = json.load(f)
                        descripcion = "Delante de ti, ves a un extraño ser. "+Monster_descripcion["sombra"][0]
                        descripcion += " "+info_mob
                    except Exception as e:
                        print(e)
            else:
                descripcion = info_mob
            DM.speak(descripcion)
            a_lista = "El jugador se ha acercado a una sombra humanoide, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.setImagePartida("images/monsters/sombra.png")
            self.GLOBAL.setShowImage(True)
        # Fénix
        elif(self.Mapa.objetos[y][x] == 48):
            sound = pygame.mixer.Sound('sounds/fenix.mp3')
            pygame.mixer.Channel(6).play(sound)
            sound = None
            info_mob = "Te acercas poco a poco al fénix que tienes delante, y ves que se remueve ligeramente. Te muestro una imagen."
            if(self.mobsEncontrados.get(str([x,y])) == None):
                # Leer descripción del mob, y lo añadimos a mobs encontrados
                self.mobsEncontrados[str([x,y])] = "fénix"
                # Cogemos la descripción del mob del .json
                self.dir = 'descripciones'
                self.file = 'Monsters.json'
                with open(self.dir+'/'+self.file,'r',encoding='utf-8') as f:
                    try:
                        Monster_descripcion = json.load(f)
                        descripcion = "Delante de ti, ves a un extraño ser. "+Monster_descripcion["fénix"][0]
                        descripcion += " "+info_mob
                    except Exception as e:
                        print(e)
            else:
                descripcion = info_mob
            DM.speak(descripcion)
            a_lista = "El jugador se ha acercado a un fénix, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.setImagePartida("images/monsters/fénix.png")
            self.GLOBAL.setShowImage(True)
        # Ankheg
        elif(self.Mapa.objetos[y][x] == 49):
            sound = pygame.mixer.Sound('sounds/ankheg.mp3')
            pygame.mixer.Channel(6).play(sound)
            sound = None
            info_mob = "Te acercas poco a poco al ankheg que tienes delante, y ves que se remueve ligeramente. Te muestro una imagen."
            if(self.mobsEncontrados.get(str([x,y])) == None):
                # Leer descripción del mob, y lo añadimos a mobs encontrados
                self.mobsEncontrados[str([x,y])] = "ankheg"
                # Cogemos la descripción del mob del .json
                self.dir = 'descripciones'
                self.file = 'Monsters.json'
                with open(self.dir+'/'+self.file,'r',encoding='utf-8') as f:
                    try:
                        Monster_descripcion = json.load(f)
                        descripcion = "Delante de ti, ves a un extraño ser. "+Monster_descripcion["ankheg"][0]
                        descripcion += " "+info_mob
                    except Exception as e:
                        print(e)
            else:
                descripcion = info_mob
            DM.speak(descripcion)
            a_lista = "El jugador se ha acercado a un ankheg (que es una mantis religiosa gigante), y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.setImagePartida("images/monsters/ankheg.png")
            self.GLOBAL.setShowImage(True)
        # Basilísco
        elif(50 <= self.Mapa.objetos[y][x] <= 56):
            sound = pygame.mixer.Sound('sounds/basilisco.mp3')
            pygame.mixer.Channel(6).play(sound)
            sound = None
            info_mob = "Te acercas poco a poco al basilisco que tienes delante, y ves que se remueve ligeramente. Te muestro una imagen."
            if(self.mobsEncontrados.get(str([x,y])) == None):
                # Leer descripción del mob, y lo añadimos a mobs encontrados
                self.mobsEncontrados[str([x,y])] = "basilisco"
                # Cogemos la descripción del mob del .json
                self.dir = 'descripciones'
                self.file = 'Monsters.json'
                with open(self.dir+'/'+self.file,'r',encoding='utf-8') as f:
                    try:
                        Monster_descripcion = json.load(f)
                        descripcion = "Delante de ti, ves a un extraño ser. "+Monster_descripcion["basilisco"][0]
                        descripcion += " "+info_mob
                    except Exception as e:
                        print(e)
            else:
                descripcion = info_mob
            DM.speak(descripcion)
            a_lista = "El jugador se ha acercado a un basilisco, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.setImagePartida("images/monsters/basilisco.png")
            self.GLOBAL.setShowImage(True)
        # Murciélago
        elif(self.Mapa.objetos[y][x] == 57):
            sound = pygame.mixer.Sound('sounds/murcielago.mp3')
            pygame.mixer.Channel(6).play(sound)
            sound = None
            info_mob = "Te acercas poco a poco al murciélago que tienes delante, y ves que se remueve ligeramente. Te muestro una imagen."
            if(self.mobsEncontrados.get(str([x,y])) == None):
                # Leer descripción del mob, y lo añadimos a mobs encontrados
                self.mobsEncontrados[str([x,y])] = "murciélago"
                # Cogemos la descripción del mob del .json
                self.dir = 'descripciones'
                self.file = 'Monsters.json'
                with open(self.dir+'/'+self.file,'r',encoding='utf-8') as f:
                    try:
                        Monster_descripcion = json.load(f)
                        descripcion = "Delante de ti, ves a un extraño ser. "+Monster_descripcion["murciélago"][0]
                        descripcion += " "+info_mob
                    except Exception as e:
                        print(e)
            else:
                descripcion = info_mob
            DM.speak(descripcion)
            a_lista = "El jugador se ha acercado a un murciélago, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.setImagePartida("images/monsters/murciélago.png")
            self.GLOBAL.setShowImage(True)
        # Rata
        elif(self.Mapa.objetos[y][x] == 58):
            sound = pygame.mixer.Sound('sounds/rata.mp3')
            pygame.mixer.Channel(6).play(sound)
            sound = None
            info_mob = "Te acercas poco a poco a la rata que tienes delante, y ves que se remueve ligeramente. Te muestro una imagen."
            if(self.mobsEncontrados.get(str([x,y])) == None):
                # Leer descripción del mob, y lo añadimos a mobs encontrados
                self.mobsEncontrados[str([x,y])] = "rata"
                # Cogemos la descripción del mob del .json
                self.dir = 'descripciones'
                self.file = 'Monsters.json'
                with open(self.dir+'/'+self.file,'r',encoding='utf-8') as f:
                    try:
                        Monster_descripcion = json.load(f)
                        descripcion = "Delante de ti, ves a un extraño ser. "+Monster_descripcion["rata"][0]
                        descripcion += " "+info_mob
                    except Exception as e:
                        print(e)
            else:
                descripcion = info_mob
            DM.speak(descripcion)
            a_lista = "El jugador se ha acercado a una rata, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.setImagePartida("images/monsters/rata.png")
            self.GLOBAL.setShowImage(True)
        # Gato
        elif(59 <= self.Mapa.objetos[y][x] <= 66):
            sound = pygame.mixer.Sound('sounds/gato.mp3')
            pygame.mixer.Channel(6).play(sound)
            sound = None
            info_mob = "Te acercas poco a poco al gato que tienes delante, y ves que se remueve ligeramente. Te muestro una imagen."
            if(self.mobsEncontrados.get(str([x,y])) == None):
                # Leer descripción del mob, y lo añadimos a mobs encontrados
                self.mobsEncontrados[str([x,y])] = "gato"
                # Cogemos la descripción del mob del .json
                self.dir = 'descripciones'
                self.file = 'Monsters.json'
                with open(self.dir+'/'+self.file,'r',encoding='utf-8') as f:
                    try:
                        Monster_descripcion = json.load(f)
                        descripcion = "Delante de ti, ves a un extraño ser. "+Monster_descripcion["gato"][0]
                        descripcion += " "+info_mob
                    except Exception as e:
                        print(e)
            else:
                descripcion = info_mob
            DM.speak(descripcion)
            a_lista = "El jugador se ha acercado a un gato, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+texto
            self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
            self.GLOBAL.setImagePartida("images/monsters/gato.png")
            self.GLOBAL.setShowImage(True)

        
        self.GLOBAL.setCanBreak([False,[None,None]])
        self.x = None
        self.y = None
    

class EstadoInteractChest(Estado):
    def __init__(self,isInicial,content,id,obligatorio,personajeDelHost,numJugadores,estado_pred,posicion_cofre,loot,dialogoFull,dialogoEmpty):
        super().__init__(isInicial,content,id)
        self.variableDeCheck["progreso"] = {}
        self.isInicial = isInicial
        self.posicion_cofre = posicion_cofre
        self.personajeDelHost = personajeDelHost
        self.variableDeCheck["progreso"][str(self.personajeDelHost.name)+","+str(self.personajeDelHost.id_jugador)] = -1
        for personaje in self.GLOBAL.getListaPersonajeHost():
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = -1 #-1: No ha abierto el cofre, 0: lo ha abierto pero no ha podido coger el loot, 1: ha cogido el loot
        self.esObligatorio = obligatorio
        self.numJugadores = numJugadores
        self.esPuntoDeRespawn = False
        self.tipo_de_estado = "apertura_cofre"
        self.dialogoDMChestFull = dialogoFull
        self.dialogoDMChestEmpty = dialogoEmpty
        self.estadosSucesores = estado_pred
        self.loot = loot
        self.ids = 0 
        self.ordenEstados = {} #Estados internos de misión
        self.click = {}
        self.click[str(self.personajeDelHost.name)+","+str(self.personajeDelHost.id_jugador)] = False
        for personaje in self.GLOBAL.getListaPersonajeHost():
            self.click[str(personaje.name)+","+str(personaje.id_jugador)] = False 

    def checkIfCanRun(self,DM,personaje):
        canOpen  = self.GLOBAL.getCanOpenChest()
        print("can open = "+str(canOpen))
        isLooking = False
        if(((personaje.playerAction == "WALK_DOWN") or (personaje.playerAction == "IDLE_DOWN")) and ((91 <= self.Mapa.objetos[personaje.coordenadas_actuales_r[1]+1][personaje.coordenadas_actuales_r[0]] <= 94))):  
            isLooking = True
        elif(((personaje.playerAction == "WALK_UP") or (personaje.playerAction == "IDLE_UP")) and ((91 <= self.Mapa.objetos[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] <= 94))):
           isLooking = True
        elif(((personaje.playerAction == "WALK_LEFT") or (personaje.playerAction == "IDLE_LEFT")) and ((91 <= self.Mapa.objetos[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]-1] <= 94))):
            isLooking = True
        elif(((personaje.playerAction == "WALK_RIGHT") or (personaje.playerAction == "IDLE_RIGHT")) and ((91 <= self.Mapa.objetos[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]+1] <= 94))):
            isLooking = True
        if(isLooking and canOpen[0] and canOpen[1][0] == self.posicion_cofre[0] and canOpen[1][1] == self.posicion_cofre[1]):
            self.click[str(personaje.name)+","+str(personaje.id_jugador)] = True
        
        if(self.click[str(personaje.name)+","+str(personaje.id_jugador)]):
            return True
        else:
            return False
        
    def checkIfCompleted(self,personaje):
        return False # Siempre puedes abrir un cofre, aunque esté vacío
        
    def run(self,DM,personaje):
        #TODO: run en función del estado de la misión
        if(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == -1):
            self.OnEnterEstadoByPlayer(DM,personaje)
            print("a False")
            self.GLOBAL.setCanOpenChest([False,[None,None]])
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 0):
            self.DescriptionFullChest(DM,personaje)
            print("a False")
            self.GLOBAL.setCanOpenChest([False,[None,None]])
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 1):
            self.DescriptionEmptyChest(DM,personaje)
            print("a False")
            self.GLOBAL.setCanOpenChest([False,[None,None]])
        

    def ModifyState(self,player,n):
        self.variableDeCheck["progreso"][str(player.name)+","+str(player.id_jugador)] = n

    def OnEnterEstadoByPlayer(self,DM,personaje):
        # Hay que resetar canción, porque con las canciones no es serializable
        cancion =  pygame.mixer.Sound('sounds/open_sarcofago.wav')
        pygame.mixer.Channel(6).play(cancion)
        cancion = None
        print("<DM>: Te acercas con cuidado al sarcófago, y al abrirlo, ves que este no está vacío. "+self.dialogoDMChestFull) #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        string_to_speech = "Te acercas con cuidado al sarcófago, y al abrirlo, ves que este no está vacío. "+self.dialogoDMChestFull
        DM.speak(string_to_speech) 
        res = personaje.equipo.addObjectToInventory(self.loot.inventory[2],self.loot.inventory[0],self.loot.inventory[1])
        if(res == -1):
            print("<DM>: Parece que llevas demasiado peso para cargar con este objeto...")
            string_to_speech = "Parece que llevas demasiado peso para cargar con este objeto..."
            DM.speak(string_to_speech)
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 0
        elif(res == -2):
            print("<DM>: Parece que no puedes llevar más encima, libera algún slot del inventario para poder cargar con este objeto...")
            string_to_speech = "Parece que no puedes llevar más encima, libera algún slot del inventario para poder cargar con este objeto..."
            DM.speak(string_to_speech)
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 0
        else:
            print("<DM>: Sin mayor problema, añades el objeto a tu inventario.")
            string_to_speech = "Sin mayor problema, añades el objeto a tu inventario."
            DM.speak(string_to_speech)
            sala_actual = self.Mapa.getRoomAtPoint(self.posicion_cofre[0],self.posicion_cofre[1],self.Mapa.room_sizes,self.Mapa.room_start_points)
            self.Mapa.salas[sala_actual].cofresSinLoot[str(self.posicion_cofre)] = True
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 1
        a_lista = "El jugador ha abierto un sarcófago, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+string_to_speech
        self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
        self.click[str(personaje.name)+","+str(personaje.id_jugador)] = False
        self.GLOBAL.addOpenedChest()

    def DescriptionFullChest(self,DM,personaje):
        cancion =  pygame.mixer.Sound('sounds/open_sarcofago.wav')
        pygame.mixer.Channel(6).play(cancion)
        cancion = None
        print("<DM>: Abres de nuevo el sarcófago. "+self.dialogoDMChestFull) #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        string_to_speech = "Abres de nuevo el sarcófago. "+self.dialogoDMChestFull
        DM.speak(string_to_speech) 
        # TODO: can take loot
        res = personaje.equipo.addObjectToInventory(self.loot.inventory[2],self.loot.inventory[0],self.loot.inventory[1])
        if(res == -1):
            print("<DM>: Parece que llevas demasiado peso para cargar con este objeto...")
            string_to_speech = "Parece que llevas demasiado peso para cargar con este objeto..."
            DM.speak(string_to_speech)
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 0
        elif(res == -2):
            print("<DM>: Parece que no puedes llevar más encima, libera algún slot del inventario para poder cargar con este objeto...")
            string_to_speech = "Parece que no puedes llevar más encima, libera algún slot del inventario para poder cargar con este objeto..."
            DM.speak(string_to_speech)
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 0
        else:
            print("<DM>: Sin mayor problema, añades el objeto a tu inventario.")
            string_to_speech = "Sin mayor problema, añades el objeto a tu inventario."
            DM.speak(string_to_speech)
            sala_actual = self.Mapa.getRoomAtPoint(self.posicion_cofre[0],self.posicion_cofre[1],self.Mapa.room_sizes,self.Mapa.room_start_points)
            self.Mapa.salas[sala_actual].cofresSinLoot[str(self.posicion_cofre)] = True
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 1
        a_lista = "El jugador ha abierto un sarcófago, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+string_to_speech
        self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
        self.click[str(personaje.name)+","+str(personaje.id_jugador)] = False

    def DescriptionEmptyChest(self,DM,personaje):
        cancion =  pygame.mixer.Sound('sounds/open_sarcofago.wav')
        pygame.mixer.Channel(6).play(cancion)
        cancion = None
        print("<DM>: Abres de nuevo el sarcófago. "+self.dialogoDMChestEmpty) #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        string_to_speech = "Abres de nuevo el sarcófago. "+self.dialogoDMChestEmpty
        DM.speak(string_to_speech) 
        a_lista = "El jugador ha abierto un sarcófago, y esto es lo que dijo el Dungeon Master cuando lo hizo: "+string_to_speech
        self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
        self.click[str(personaje.name)+","+str(personaje.id_jugador)] = False




class EstadoInicial(Estado):
    def __init__(self,isInicial,content,RAG_musica,currentPartida,id):
        super().__init__(isInicial,content,id)
        #extraemos la ubicación desde la bbdd
        conn = sqlite3.connect("simuladordnd.db")
        cur = conn.cursor()
        #cargamos la partida 1, si existe: el orden de las columnas será ese
        cur.execute("SELECT ubicacion_historia FROM partida WHERE numPartida = '"+currentPartida+"'")
        rows = cur.fetchall() #para llegar a esta pantalla, la pantalla tiene que existir sí o sí
        if(rows[0] != None):
            ubicacion = rows[0][0]
        conn.close()

        canciones = RAG_musica.consultar_cancion("¿Cuál es la mejor o mejores canciones para reproducir cuando el DM está dando la introducción para la aventura, y los jugadores empiezan desde "+ubicacion+"?")
        try:
            canciones_list = canciones.split("\n")
            print(canciones_list)
            self.cancion = canciones_list[random.randint(0,(len(canciones_list)-1))] #Tomamos la primera de las canciones -> Mejor coincidencia
        except Exception as e:
            print(e)
            print(canciones)

    def checkIfCanRun(self,player):
        return True

    def checkIfCompleted(self,player):
        if(self.variableDeCheck["progreso"] == True):
            return True
        else:
            return False
    def run(self,DM):
        self.OnEnterEstadoByAllPlayers(DM)

    def OnEnterEstadoByAllPlayers(self,DM):
        #self.GLOBAL.setRefreshScreen() #refrescar la pantalla con el mapa que crearé después
        #TODO: imagen inicial
        #TODO: cambiar a escribir por la pantalla de diálogo del DM

        #Música de inicio
        mixer.music.stop()#para la música
        mixer.music.load('music/'+self.cancion+".mp3") #carga la nueva canción sugerida por la ia
        mixer.music.play(loops=1) # Se va a reproducir 2 veces para que le de tiempo a leer toda la introducción

        print("<DM>: "+self.dialogoDMIntro) #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        DM.speak(self.dialogoDMIntro) 
        #DM.printVoices()
        a_lista = "El Dungeon Master se ha presentado a los jugadores, y esto es lo que dijo: "+self.dialogoDMIntro
        self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
        self.variableDeCheck["progreso"] = True
        self.GLOBAL.setCanStart(True)
        

class EstadoDeMision(Estado):
    def __init__(self,isInicial,content,RAG_musica,currentPartida,estado_pred,numJugadores,descripcionFisicaNPC,motivoUbicacion, trasfondoNPC,id,personajeDelHost,pathImageNPC):
        super().__init__(isInicial,content,id)
        self.variableDeCheck["progreso"] = {}
        self.pathImageNPC = pathImageNPC
        self.personajeDelHost = personajeDelHost
        self.variableDeCheck["progreso"][str(self.personajeDelHost.name)+","+str(self.personajeDelHost.id_jugador)] = -1
        for personaje in self.GLOBAL.getListaPersonajeHost():
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = -1 #-1: No se ha leído la descripción del personaje, 0: se ha leído la descripción del NPC, 1: se ha dado ya la misión, 2:estado normal de búsqueda, 3:se ha desencadenado la misión, 4: se ha completado la misión
        self.esObligatorio = True
        self.numJugadores = numJugadores
        self.esPuntoDeRespawn = False
        self.tipo_de_estado = "mision"
        self.estadosSucesores = estado_pred
        self.ids = 0 
        self.ordenEstados = {} #Estados internos de misión
        self.dialogoDMIntro = "En frente de ti, te parece ver a alguien. "+descripcionFisicaNPC+" Te muestro una imagen."

    def checkIfCanRun(self,DM,player):
        return True #no tiene ningún requisito de acceso
        
    def checkIfCompleted(self,personaje):
        if(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 4):
            return True
        else:
            return False
        
    def run(self,DM,personaje):
        #TODO: run en función del estado de la misión
        if(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == -1):
            self.OnEnterEstadoByPlayer(DM,personaje)
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 0):
            self.runNextInnerEstado(DM,personaje)
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 1):
            self.runNextInnerEstado(DM,personaje)
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 2):
            pass
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 3):
            pass
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 4):
            pass

    def ModifyState(self,personaje,v):
        print("modificando estado de misión a "+str(v))
        self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = v

    def runNextInnerEstado(self,DM,personaje):
        for id,estado in self.ordenEstados.items():
            if(not estado.checkIfCompleted(personaje) and estado.checkIfCanRun(DM,personaje)):
                estado.run(DM,personaje)
                break

    def OnEnterEstadoByPlayer(self,DM,personaje):
        print("<DM>: "+self.dialogoDMIntro) #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        DM.speak(self.dialogoDMIntro) 
        a_lista = "El Dungeon Master ha descrito a un NPC que el jugador ha visto, y esto es lo que dijo: "+self.dialogoDMIntro
        self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
        self.GLOBAL.setImagePartida(self.pathImageNPC)
        self.GLOBAL.setShowImage(True)
        #DM.printVoices()
        #TODO: enviar TCP
        self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 0
        self.GLOBAL.setFinishedStart(True)

class EstadoDeHablaNPC(Estado):
    def __init__(self,isInicial,DMintro,DMMision,id,personajeDelHost,numJugadores,estado_pred,NPC,currentPartida):
        super().__init__(isInicial,DMintro,id)
        self.variableDeCheck["progreso"] = {}
        self.personajeDelHost = personajeDelHost
        self.variableDeCheck["progreso"][str(self.personajeDelHost.name)+","+str(self.personajeDelHost.id_jugador)] = -1
        for personaje in self.GLOBAL.getListaPersonajeHost():
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = -1 #-1: No ha hablado con el NPC, 0: el NPC se ha presentado, 1: le ha dado la misión, 2: ha completado la misión y ha hablado de nuevo con el NPC
        self.esObligatorio = True
        self.numJugadores = numJugadores
        self.esPuntoDeRespawn = False
        self.tipo_de_estado = "mision_especifica"
        self.estadosSucesores = estado_pred
        self.currentPartida = currentPartida
        self.ids = 0 
        self.ordenEstados = {} #Estados internos de misión
        self.click = {}
        self.click[str(self.personajeDelHost.name)+","+str(self.personajeDelHost.id_jugador)] = False
        for personaje in self.GLOBAL.getListaPersonajeHost():
            self.click[str(personaje.name)+","+str(personaje.id_jugador)] = False 
        self.esObligatorio = True
        self.NPC = NPC
        self.dialogoDMIntro = DMintro
        self.dialogoDMMision = DMMision
        self.lastTexto = ""

    def checkIfCanRun(self,DM,personaje):
        print("en el check")
        canTalk  = self.GLOBAL.getCanTalkToNPC()
        isLooking = False
        if(((personaje.playerAction == "WALK_DOWN") or (personaje.playerAction == "IDLE_DOWN")) and ((87 <= self.Mapa.objetos[personaje.coordenadas_actuales_r[1]+1][personaje.coordenadas_actuales_r[0]] <= 90))):  
            isLooking = True
        elif(((personaje.playerAction == "WALK_UP") or (personaje.playerAction == "IDLE_UP")) and ((87 <= self.Mapa.objetos[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] <= 90))):
           isLooking = True
        elif(((personaje.playerAction == "WALK_LEFT") or (personaje.playerAction == "IDLE_LEFT")) and ((87 <= self.Mapa.objetos[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]-1] <= 90))):
            isLooking = True
        elif(((personaje.playerAction == "WALK_RIGHT") or (personaje.playerAction == "IDLE_RIGHT")) and ((87 <= self.Mapa.objetos[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]+1] <= 90))):
            isLooking = True
        if(isLooking and canTalk):
            self.click[str(personaje.name)+","+str(personaje.id_jugador)] = True

        if(self.click[str(personaje.name)+","+str(personaje.id_jugador)]):
            return True
        else:
            return False
        
    def checkIfCompleted(self,personaje):
        if(self.NPC.esta_muerto): #si el personaje ha muerto, ya no puede hablar con él, y habrá concluido este estado
            return True
        else:
            return False
        
    def run(self,DM,personaje):
        #TODO: run en función del estado de la misión
        if(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == -1):
            self.OnEnterEstadoByPlayer(DM,personaje)
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 0):
            self.giveMissionNPC(DM,personaje)
            self.GLOBAL.setCanTalkToNPC(False)
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 1):
            self.talkToNPC(DM,personaje)
            self.GLOBAL.setCanTalkToNPC(False)
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 2):
            self.finishNPCMision(DM,personaje)
            self.GLOBAL.setCanTalkToNPC(False)

    def ModifyState(self,player,n):
        self.variableDeCheck["progreso"][str(player.name)+","+str(player.id_jugador)] = n

    def ModifyToTrueHablaNPC(self,personaje):
        self.click[str(personaje.name)+","+str(personaje.id_jugador)] = True

    def OnEnterEstadoByPlayer(self,DM,personaje):
        if(self.NPC.tipo_raza == "Enano"):
            if(self.NPC.genero == "hombre"):
                msg= "al enano, "
            else:
                msg = "a la enana,"
        else:
            if(self.NPC.genero == "mujer"):
                msg = "a la elfa, "
            else:
                msg = "al elfo, "
        # Hay que resetar canción, porque con las canciones no es serializable
        cancion =  pygame.mixer.Sound('sounds/button_pressed.wav')
        pygame.mixer.Channel(6).play(cancion)
        cancion = None
        self.GLOBAL.setShowNombreNPC(self.NPC.name)
        print("<DM>: Al acercarte "+msg+" ves que te mira fíjamente, y te dice: "+self.dialogoDMIntro) #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        string_to_speech = "Al acercarte "+msg+" ves que te mira fíjamente, y te dice: "+self.dialogoDMIntro
        DM.speak(string_to_speech) 
        a_lista = "El jugador se ha acercado a"+self.NPC.name+", y esto es lo que dijo: "+self.dialogoDMIntro
        self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
        #DM.printVoices()
        self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 0
        self.run(DM,personaje)

    def talkToNPC(self,DM,personaje):
        #TODO: RAG
        # Establecemos el modo habla, pues el jugador ha activado este modo
        self.GLOBAL.setModoHabla(True)
        while(self.GLOBAL.getModoHabla()):
            # Esperar a recibir mensaje
            time.sleep(0.2)
            msg = self.GLOBAL.getTextoMensaje()
            if(msg != ""):
                # RAG
                DM.speak("Espera un momento que piense...")
                rag_historia = RAG_historia.RAG_historia(self.currentPartida)
                resp = rag_historia.consultar_NPC(msg,self.lastTexto)
                DM.speak(resp)
                to_list = "Cuando el NPC le dijo al jugador: '"+self.lastTexto+"'. El jugador le respondió con lo siguiente: '"+msg+"'. A esa respuesta, el Dungeon Master le dijo: "+resp
                self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
                rag_historia.escribirCurrentDialogoNPCYPregunta(msg,resp,self.lastTexto)
                self.lastTexto = resp
                msg = ""
                self.GLOBAL.setTextoMensaje("")
                self.GLOBAL.setModoHabla(True)
            self.click[str(personaje.name)+","+str(personaje.id_jugador)] = False
        


    def finishNPCMision(self,DM,personaje):
        pass

    def giveMissionNPC(self,DM,personaje):
        if(self.NPC.genero == "mujer"):
            pensando = "pensativa"
        else:
            pensando = "pensativo"
        print("<DM>: Tras decirte lo anterior, ves que "+self.NPC.name+" se queda "+pensando+", y continúa diciendote: "+self.dialogoDMMision+" ¿Me ayudarás?") #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        DM.speak("Tras decirte lo anterior, ves que "+self.NPC.name+" se queda "+pensando+", y continúa diciendote: "+self.dialogoDMMision+" ¿Me ayudarás? Si estás interesado, voy a deshacer el conjuro que bloquea la puerta que da acceso al resto de galerías, aunque no te garantizo que puedas abrirla.") 
        magic =  pygame.mixer.Sound('sounds/magic.wav')
        self.lastTexto = self.dialogoDMMision+" ¿Me ayudarás? Si estás interesado, voy a deshacer el conjuro que bloquea la puerta que da acceso al resto de galerías, aunque no te garantizo que puedas abrirla."
        pygame.mixer.Channel(6).play(magic)
        a_lista = "El jugador está hablando con "+self.NPC.name+", y esto es lo que dijo: "+self.dialogoDMIntro
        self.GLOBAL.addElementToListaAndRemoveFirst(a_lista)
        magic = None
        self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 1
        print(type(self.estadosSucesores),self.estadosSucesores)
        self.estadosSucesores.ModifyState(personaje,1) #1 quiere decir que ya le ha dado la misión
        self.click[str(personaje.name)+","+str(personaje.id_jugador)] = False
        # Activo el modo de habla, para que el jugador conteste si quiere
        self.run(DM,personaje)

class EstadoDeMisionConcreta(Estado):
    def __init__(self,isInicial,content,estado_pred,numJugadores,id,tipo_mision,variableDeCheck,mision,Mapa,textoDM):
        super().__init__(isInicial,content,id)
        self.variableDeCheck["progreso"] = variableDeCheck
        self.esObligatorio = True
        self.numJugadores = numJugadores
        self.esPuntoDeRespawn = False
        self.mision = mision
        self.tipo_de_estado = tipo_mision
        self.textoDM = textoDM
        self.estadosSucesores = estado_pred
        self.ids = 0 
        self.currentState = 0 #0 no la tiene aún, 1: la tiene, 2: la ha completado
        self.event_trigged = False
        self.ordenEstados = {} #Estados internos de misión
        self.given = False
        self.Mapa = Mapa

    def checkIfCanRun(self,DM,player):
        if(self.given):
            return True
        else:
            return False
        
    def checkIfCompleted(self,personaje):
        if(self.tipo_de_estado == "combate"):
            for mob,value in self.variableDeCheck["progreso"].items():
                if(value[0] != value[1]):
                    return False
        elif(self.tipo_de_estado == "búsqueda"):
            for objeto,value in self.variableDeCheck["progreso"].items():
                if(not value):
                    return False
        return True
    
    def giveMision(self):
        self.given = True
        
    def run(self,DM,personaje):
        #TODO: run en función del estado de la misión
        if(self.currentState == 0):
            self.OnEnterEstadoByPlayer(DM,personaje)
        elif(self.currentState == 1):
            self.checkCompletedMission(DM,personaje)
        elif(self.currentState == 2):
            self.OnExitEstadoByPlayer(DM,personaje)
        
    def checkCompletedMission(self,DM,personaje):
        self.variableDeCheck["progreso"] = self.Mapa.salas[self.Mapa.main_path[-1]].variableDeCheck
        if(self.checkIfCompleted(personaje)):
            self.CompleteMision()
            self.run(DM,personaje)


    def CompleteMision(self):
        self.currentState = 2

    def OnEnterEstadoByPlayer(self,DM,personaje):
        print("Misión a realizar: "+self.mision)
        self.currentState = 1

    def OnExitEstadoByPlayer(self, player, DM):
        DM.speak(self.textoDM)


class EstadoDeSalaFinal(Estado):
    def __init__(self,isInicial,content,RAG_musica,currentPartida,estado_pred,numJugadores,id,personajeDelHost,id_sala,es_obligatoria,esInicial,daASalas,tienePortales,contieneLlaves,esFinal,orden,tipo_mision, size, pos_x, pos_y,Mapa,frase_puerta,descripcion_sala,idSala_idOrder):
        super().__init__(isInicial,content,id)
        self.personajeDelHost = personajeDelHost
        self.variableDeCheck["progreso"] = {}
        self.variableDeCheck["progreso"][str(self.personajeDelHost.name)+","+str(self.personajeDelHost.id_jugador)] = 1
        for personaje in self.GLOBAL.getListaPersonajeHost():
            personaje = personaje[1]
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 1 #1: ha entrado y está por primera vez en la sala, 2: continúa en la sala normal, 3: Está en uno de los pasillos de la sala, el de la variable self.pasillo_from_puerta, 4: ya no está en la sala, pero entró
        self.numJugadores = numJugadores
        self.tipo_de_estado = "sala_grande"
        self.estadosSucesores = estado_pred
        self.ids = 0
        self.ordenEstados = {} #Estados contenidos por la sala # contiene todos los estados de "self.daASalas = {}"
        self.numAccepts = 0 
        self.dialogoDMIntro = "Tras abrir la puerta, ves que te encuentras en otra galería, también oscura y amplia. "+descripcion_sala
        self.id = id_sala
        self.es_obligatorio = es_obligatoria #por defecto se marcan como opcionales. Luego, las obligatorias se marcarán como obligatorias
        self.esInicial = esInicial
        self.tienePortales = tienePortales
        self.contieneLlaves = contieneLlaves #Lista de posiciones de las puertas que abre cada llave de aquí
        self.esFinal = esFinal
        self.orden = orden
        self.tipo_mision = tipo_mision
        self.size = size
        self.daASalas = daASalas
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pasilloFromPuerta = None
        self.Mapa = Mapa
        self.pasilloToPuerta = None
        self.frases_puerta = frase_puerta
        self.idSala_idOrder = idSala_idOrder
        self.read = False
        self.read2 = False
        self.read4 = False

    def checkIfCanRun(self,DM,personaje):
        return self.checkIfCanRunByPlayer(DM,personaje)
    
    def checkIfCanRunByPlayer(self,DM,personaje):
        return True
        

    def checkIfCanExit(self,DM,personaje,currentEstado):
        if(((personaje.playerAction == "WALK_DOWN") or (personaje.playerAction == "IDLE_DOWN")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]+1][personaje.coordenadas_actuales_r[0]] == 13) or (self.Mapa.matrix[personaje.coordenadas_actuales_r[1]+1][personaje.coordenadas_actuales_r[0]] == 23))):  
            pos_x = personaje.coordenadas_actuales_r[0]
            pos_y = personaje.coordenadas_actuales_r[1]+1
        elif(((personaje.playerAction == "WALK_UP") or (personaje.playerAction == "IDLE_UP")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] == 12) or (self.Mapa.matrix[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] == 23))):
            pos_x = personaje.coordenadas_actuales_r[0]
            pos_y = personaje.coordenadas_actuales_r[1]-1
        elif(((personaje.playerAction == "WALK_LEFT") or (personaje.playerAction == "IDLE_LEFT")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]-1] == 10) or (self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]-1] == 23))):
            pos_x = personaje.coordenadas_actuales_r[0]-1
            pos_y = personaje.coordenadas_actuales_r[1]
        elif(((personaje.playerAction == "WALK_RIGHT") or (personaje.playerAction == "IDLE_RIGHT")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]+1] == 11) or (self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]+1] == 23))):
            pos_x = personaje.coordenadas_actuales_r[0]+1
            pos_y = personaje.coordenadas_actuales_r[1]
        else:
            pos_x = None
            pos_y = None
        print(pos_x,pos_y)
        if(pos_x != None and pos_y != None):
            for sala in self.Mapa.salas[self.id].daASalas:
                if(self.Mapa.salas[self.id].daASalas[sala][0] == [pos_x,pos_y]):
                    print("En sala "+str(self.id)+" da a salas hacia sala "+str(sala)+" está "+self.Mapa.salas[self.id].daASalas[sala][1])
                    if(self.Mapa.salas[self.id].daASalas[sala][1] == "abierto"):
                        #La puerta existe y da a la sala "sala", y está abierta para pasar
                        print("puerta")
                        self.read2 = False
                        if(self.Mapa.matrix[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] == 23):
                            self.GLOBAL.setActionDoor([2,[pos_x,pos_y]])
                            self.pasilloFromPuerta = [[pos_x,pos_y], sala]
                        else:
                            if(self.Mapa.adyacencias[self.id][sala] == 1):
                                #Es adyacente
                                self.GLOBAL.setActionDoor([3,[pos_x,pos_y]]) #podría abrirla
                            else:
                                self.GLOBAL.setActionDoor([1,[pos_x,pos_y]]) #podría abrirla
                            self.pasilloFromPuerta = [[pos_x,pos_y], sala]
                        return False
                    else:
                        # Comprobamos si lleva alguna llave equipada en una de las manos:
                        canPass = [False,None]
                        item_left = personaje.equipo.objeto_equipado_mano_izquierda
                        if((item_left != None) and (item_left[1] == "Llave") and (item_left[2].puerta == self.id) and (item_left[2].enlace == sala)):
                            canPass = [True,"left"]
                        item_right = personaje.equipo.objeto_equipado_mano_derecha
                        if((item_right != None) and (item_right[1] == "Llave") and (item_right[2].puerta == self.id) and (item_right[2].enlace == sala)):
                            canPass = [True,"right"]

                        if(canPass[0]):
                            # Elimino la llave del inventario
                            if(canPass[1] == "left"):
                                personaje.equipo.objeto_equipado_mano_izquierda = None
                            elif(canPass[1] == "right"):
                                personaje.equipo.objeto_equipado_mano_derecha = None

                            # Abro la puerta
                            self.Mapa.salas[self.id].daASalas[sala][1] = "abierto"
                            cancion = pygame.mixer.Sound('sounds/abrir_llave.wav')
                            pygame.mixer.Channel(7).play(cancion) #reproduzco el sonido de poner la llave
                            cancion = None
                            text_abrir = "Intentas usar una llave en el pomo de la puerta, y ves que esta cede."
                            DM.speak(text_abrir) 
                            to_list = "El jugador acaba de poner una llave en la cerradura de una puerta que se encontraba bloqueada, y la ha girado, y esta se ha abierto"
                            self.GLOBAL.addElementToListaAndRemoveFirst(to_list)

                            #Ejecuto la apertura
                            self.read2 = False
                            if(self.Mapa.adyacencias[self.id][sala] == 1):
                            #Es adyacente
                                self.GLOBAL.setActionDoor([3,[pos_x,pos_y]]) #podría abrirla
                                self.pasilloFromPuerta = [[pos_x,pos_y],sala]

                            else:
                                self.GLOBAL.setActionDoor([1,[pos_x,pos_y]]) #podría abrirla
                                self.pasilloFromPuerta = [[pos_x,pos_y],sala]
                            return False

                        else:
                            if(not self.read2):
                                #La puerta está  cerrada
                                self.read2 = True
                                print("puerta cerrada")
                                pygame.mixer.Channel(1).play(self.soundDoor)
                                text_closed = self.frases_puerta[self.id][sala][0]
                                DM.speak(text_closed) 
                                to_list = "El jugador ha intentado abrir una puerta, pero estaba cerrada. Esto fue lo que le dijo el Dungeon Master: "+text_closed
                                self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
                            self.GLOBAL.setActionDoor([0,[None,None]]) 
                            return False
                
        else:
            self.read2 = False
                    # Si ya ha hablado con el NPC y el personaje ha dado click para cruzar la puerta
        print(self.GLOBAL.canGoOutFirst(), self.pasilloFromPuerta, self.GLOBAL.getCrossedDoor())
        if(self.GLOBAL.canGoOutFirst() and (self.pasilloFromPuerta != None) and (self.GLOBAL.getCrossedDoor()[1] == self.pasilloFromPuerta[0])):
            #Ha decidido cruzarla
            self.GLOBAL.setActionDoor([0,[None,None]])
            self.GLOBAL.setCrossedDoor([[False],[None,None]])
            pygame.mixer.Channel(1).play(self.soundDoor)
            text_open_door = self.frases_puerta[self.id][self.pasilloFromPuerta[1]][1]
            DM.speak(text_open_door) 
            to_list = "El jugador acaba de abrir una puerta, y esto es lo que le ha dicho el Dungeon Master: "+text_open_door
            self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
            #reseteo las variables
            #Si la puerta estaba originalmente cerrada, o si está abierta, pero desde el otro lado estaba cerrada, se va a abrir:
            # Es un puntero, así que se cambiará en su correspondiente estado
            self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[self.id][1] = "abierto"
            print("Sala "+str(self.pasilloFromPuerta[1])+", modificado da a salas de sala "+str(self.id))
            if(self.Mapa.adyacencias[self.id][self.pasilloFromPuerta[1]] == 1):
                self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2
                currentEstado[str(personaje.name)+","+str(personaje.id_jugador)] = self.idSala_idOrder[self.pasilloFromPuerta[1]]
            else:
                self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 3 #está en un pasillo
                self.pasilloFromPuerta = [self.pasilloFromPuerta[0],self.pasilloFromPuerta[1]] #guardo cuál es la puerta desde la que entró, y la sala a la que se dirige, para simplificar después las comprobaciones
            
            return True
        else:
            self.GLOBAL.setActionDoor([0,[None,None]])
            self.pasilloFromPuerta = None
            return False
        
    def checkIfItIsInCurrentRoom(self,pos_x,pos_y):
        start_x = self.pos_x
        start_y = self.pos_y
        dif = pos_x - start_x
        dif2 = pos_y - start_y
        if((dif >= 0) and (dif <self.size[0]) and (dif2 >= 0) and (dif2 < self.size[1])):
            #Está en algún punto de esa sala
            return True
        return False

    def checkIfCanEnterAgain(self,DM,personaje):
        if(((personaje.playerAction == "WALK_DOWN") or (personaje.playerAction == "IDLE_DOWN")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]+1][personaje.coordenadas_actuales_r[0]] == 12))):  
            pos_x = personaje.coordenadas_actuales_r[0]
            pos_y = personaje.coordenadas_actuales_r[1]+1
        elif(((personaje.playerAction == "WALK_UP") or (personaje.playerAction == "IDLE_UP")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] == 13))):
            pos_x = personaje.coordenadas_actuales_r[0]
            pos_y = personaje.coordenadas_actuales_r[1]-1
        elif(((personaje.playerAction == "WALK_LEFT") or (personaje.playerAction == "IDLE_LEFT")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]-1] == 11))):
            pos_x = personaje.coordenadas_actuales_r[0]-1
            pos_y = personaje.coordenadas_actuales_r[1]
        elif(((personaje.playerAction == "WALK_RIGHT") or (personaje.playerAction == "IDLE_RIGHT")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]+1] == 10))):
            pos_x = personaje.coordenadas_actuales_r[0]+1
            pos_y = personaje.coordenadas_actuales_r[1]
        else:
            pos_x = None
            pos_y = None
        print(pos_x,pos_y)
        if(pos_x != None and pos_y != None):
            if((self.pasilloFromPuerta[0] == [pos_x,pos_y]) and (self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[self.id][1] == "abierto")):
                #La puerta existe y da a la sala "sala", y está abierta para pasar
                if(self.Mapa.adyacencias[self.id][self.pasilloFromPuerta[1]] == 1):
                    self.GLOBAL.setActionDoor([3,[pos_x,pos_y]]) #podría abrirla
                else:
                    self.GLOBAL.setActionDoor([1,[pos_x,pos_y]]) #podría abrirla
                return True
                
                    # Si ya ha hablado con el NPC y el personaje ha dado click para cruzar la puerta
        if(self.GLOBAL.canGoOutFirst() and (self.pasilloFromPuerta != None) and (self.GLOBAL.getCrossedDoor()[1] == self.pasilloFromPuerta[0]) and self.checkIfItIsInCurrentRoom(personaje.coordenadas_actuales_r[0],personaje.coordenadas_actuales_r[1])):
            #Ha decidido cruzarla
            self.GLOBAL.setActionDoor([0,[None,None]])
            self.GLOBAL.setCrossedDoor([[False],[None,None]])
            pygame.mixer.Channel(1).play(self.soundDoor)
            text_open_door = self.frases_puerta[self.pasilloFromPuerta[1]][self.id][2]
            self.pasilloFromPuerta = None
            DM.speak(text_open_door)
            to_list = "El jugador acaba de abrir una puerta, y esto es lo que le ha dicho el Dungeon Master: "+text_open_door
            self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
            #reseteo las variables
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2 #está en la sala de nuevo
             #guardo cuál es la puerta desde la que entró, y la sala a la que se dirige, para simplificar después las comprobaciones
            # Si trata de entrar después a otra puerta de otro camino que se haya anexado, le dirá que una magia oscura impide que la abra jeje
            return True
        else:
            self.GLOBAL.setActionDoor([0,[None,None]])
            return False
                    


    def checkIfCanPassToAnotherRoom(self,DM,personaje,currentEstadoByPlayers):
        if(((personaje.playerAction == "WALK_DOWN") or (personaje.playerAction == "IDLE_DOWN")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]+1][personaje.coordenadas_actuales_r[0]] == 12))):  
            pos_x = personaje.coordenadas_actuales_r[0]
            pos_y = personaje.coordenadas_actuales_r[1]+1
        elif(((personaje.playerAction == "WALK_UP") or (personaje.playerAction == "IDLE_UP")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] == 13))):
            pos_x = personaje.coordenadas_actuales_r[0]
            pos_y = personaje.coordenadas_actuales_r[1]-1
        elif(((personaje.playerAction == "WALK_LEFT") or (personaje.playerAction == "IDLE_LEFT")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]-1] == 11))):
            pos_x = personaje.coordenadas_actuales_r[0]-1
            pos_y = personaje.coordenadas_actuales_r[1]
        elif(((personaje.playerAction == "WALK_RIGHT") or (personaje.playerAction == "IDLE_RIGHT")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]+1] == 10))):
            pos_x = personaje.coordenadas_actuales_r[0]+1
            pos_y = personaje.coordenadas_actuales_r[1]
        else:
            pos_x = None
            pos_y = None
        print(pos_x,pos_y)
        if(pos_x != None and pos_y != None):
            for sala in self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas:
                if(self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[sala][0] == [pos_x,pos_y]):
                    if(self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[sala][1] == "abierto"):
                        #La puerta existe y da a la sala "sala", y está abierta para pasar
                        if(self.Mapa.adyacencias[self.id][sala] == 1):
                            #Es adyacente
                            self.read = False
                            self.read4 = False
                            self.GLOBAL.setActionDoor([3,[pos_x,pos_y]]) #podría abrirla
                            self.pasilloToPuerta = [[pos_x,pos_y],sala]
                        else:
                            self.read = False
                            self.read4 = False
                            self.GLOBAL.setActionDoor([1,[pos_x,pos_y]]) #podría abrirla
                            self.pasilloToPuerta = [[pos_x,pos_y],sala]
                        return False
                    else:
                        # Comprobamos si lleva alguna llave equipada en una de las manos:
                        canPass = [False,None]
                        item_left = personaje.equipo.objeto_equipado_mano_izquierda
                        if((item_left != None) and (item_left[1] == "Llave") and (item_left[2].puerta == self.id) and (item_left[2].enlace == sala)):
                            canPass = [True,"left"]
                        item_right = personaje.equipo.objeto_equipado_mano_derecha
                        if((item_right != None) and (item_right[1] == "Llave") and (item_right[2].puerta == self.id) and (item_right[2].enlace == sala)):
                            canPass = [True,"right"]

                        if(canPass[0]):
                            # Elimino la llave del inventario
                            if(canPass[1] == "left"):
                                personaje.equipo.objeto_equipado_mano_izquierda = None
                            elif(canPass[1] == "right"):
                                personaje.equipo.objeto_equipado_mano_derecha = None

                            # Abro la puerta
                            self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[sala][1] = "abierto"
                            cancion = pygame.mixer.Sound('sounds/abrir_llave.wav')
                            pygame.mixer.Channel(7).play(cancion) #reproduzco el sonido de poner la llave
                            cancion = None
                            text_abrir = "Intentas usar una llave en el pomo de la puerta, y ves que esta cede."
                            DM.speak(text_abrir) 
                            to_list = "El jugador acaba de poner una llave en la cerradura de una puerta que se encontraba bloqueada, y la ha girado, y esta se ha abierto"
                            self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
                            #Ejecuto la apertura
                            if(self.Mapa.adyacencias[self.id][sala] == 1):
                            #Es adyacente
                                self.GLOBAL.setActionDoor([3,[pos_x,pos_y]]) #podría abrirla
                                self.pasilloToPuerta = [[pos_x,pos_y],sala]
                                self.read = False
                                self.read4 = False
                            else:
                                self.GLOBAL.setActionDoor([1,[pos_x,pos_y]]) #podría abrirla
                                self.pasilloToPuerta = [[pos_x,pos_y],sala]
                                self.read = False
                                self.read4 = False
                            return False

                        else:
                            #La puerta está cerrada
                            if(not self.read):
                                print("puerta cerrada")
                                pygame.mixer.Channel(1).play(self.soundDoor)
                                text_closed = self.frases_puerta[self.pasilloFromPuerta[1]][sala][0]
                                DM.speak(text_closed) 
                                to_list = "El jugador ha intentado abrir una puerta, pero estaba cerrada. Esto fue lo que le dijo el Dungeon Master: "+text_closed
                                self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
                                self.read = False
                                self.read4 = True
                                self.GLOBAL.setActionDoor([0,[None,None]]) 
                            return False
                
            if((not self.read) and (10 <= self.Mapa.matrix[pos_y][pos_x] <= 13) and not((self.pasilloToPuerta != None) and (self.GLOBAL.getCrossedDoor()[1] == self.pasilloToPuerta[0]))):
                #Es otra puerta distinta, pero no se puede pasar porque no es del enlace
                pygame.mixer.Channel(1).play(self.soundDoor)
                text = "Parece que algún tipo de magia impide que puedas abrir esta puerta."
                DM.speak(text) 
                to_list = "El jugador ha intentado abrir una puerta, pero parece que algún tipo de magia impidió que la abriera"
                self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
                self.GLOBAL.setActionDoor([0,[None,None]]) 
                self.read = True
                self.read4 = False
                return False
        else:
            self.read = False
            self.read4 = False
                    # Si ya ha hablado con el NPC y el personaje ha dado click para cruzar la puerta
        if(self.GLOBAL.canGoOutFirst() and (self.pasilloToPuerta != None) and (self.GLOBAL.getCrossedDoor()[1] == self.pasilloToPuerta[0])):
            #Ha decidido cruzarla
            self.GLOBAL.setActionDoor([0,[None,None]])
            self.GLOBAL.setCrossedDoor([[False],[None,None]])
            pygame.mixer.Channel(1).play(self.soundDoor)
            # El texto de la puerta se reproducirá en el estado de destino
            #reseteo las variables
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2 
            #Si la puerta estaba originalmente cerrada, o si está abierta, pero desde el otro lado estaba cerrada, se va a abrir:
            # Es un puntero, así que se cambiará en su correspondiente estado
            self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[self.id][1] = "abierto" #guardo cuál es la puerta desde la que entró, y la sala a la que se dirige, para simplificar después las comprobaciones
            currentEstadoByPlayers[str(personaje.name)+","+str(personaje.id_jugador)] = self.idSala_idOrder[self.pasilloFromPuerta[1]]
            self.pasilloFromPuerta = None
            self.pasilloToPuerta = None
            
            return True
        else:
            self.GLOBAL.setActionDoor([0,[None,None]])
            return False
        
        
    def checkIfCompleted(self,personaje):
        #print("check if completed de sala inicial: False")
        return False #Una sala nunca se puede completar. Siempre puedes entrar a ella, si el check del run se cumple
        
    def run(self,DM,personaje,currentEstadoByPlayers):
        #TODO: run en función del estado de la misión
        # print("run:")
        print(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)])
        if(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 1):
            self.OnEnterEstadoByPlayer(DM,personaje,currentEstadoByPlayers)
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 2):
            if(self.checkIfCanExit(DM,personaje,currentEstadoByPlayers)):
                pass
            else:
                self.runNextInnerEstado(DM,personaje)
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 3):
            print("en el pasillo")
            if(self.checkIfCanEnterAgain(DM,personaje)):
                pass
            else:
                self.checkIfCanPassToAnotherRoom(DM,personaje,currentEstadoByPlayers)
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 4):
            pass
        else:
            pass #si están en 0 no hace nada, hay que esperar a que todos acepten 

    def runNextInnerEstado(self,DM,personaje):
        for id,estado in self.ordenEstados.items(): #quiero que el último estado en ser comprobado sea el de la misión
            if(not estado.checkIfCompleted(personaje) and estado.checkIfCanRun(DM,personaje)):
                estado.run(DM,personaje)

    def OnEnterEstadoByPlayer(self,DM,personaje,currentEstadoByPlayers):
        #El mensaje de introducción a la sala, se le reproduce a cada uno de forma individual (por si alguno muriera, y se tuviera que crear otro, que esto ya sea independiente)
        # print("<DM>: "+self.dialogoDMIntro) #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        # DM.speak(self.dialogoDMIntro) 
        print("Sala "+str(self.id))
        #DM.printVoices()
        #TODO: Enviar mensaje TCP
        self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2 #está en la sala normal
        self.GLOBAL.addRoomVisited()
        self.run(DM,personaje,currentEstadoByPlayers)

    def addChest(self,dmf1,dme1,cofre):
        if(cofre[1].inventory[1] == "Llave"):
            obligatorio = True
        else:
            obligatorio = False
        self.ordenEstados[self.ids] = EstadoInteractChest(False,None,'cofre',obligatorio,self.personajeDelHost,self.numJugadores,self,cofre[0],cofre[1],dmf1,dme1)
        self.ids +=1

class EstadoDeSalaIntermedia(Estado):
    def __init__(self,isInicial,content,RAG_musica,currentPartida,estado_pred,numJugadores,id,personajeDelHost,id_sala,es_obligatoria,esInicial,daASalas,tienePortales,contieneLlaves,esFinal,orden,tipo_mision, size, pos_x, pos_y,Mapa,frase_puerta,descripcion_sala,idSala_idOrder):
        super().__init__(isInicial,content,id)
        self.personajeDelHost = personajeDelHost
        self.variableDeCheck["progreso"] = {}
        self.variableDeCheck["progreso"][str(self.personajeDelHost.name)+","+str(self.personajeDelHost.id_jugador)] = 1
        for personaje in self.GLOBAL.getListaPersonajeHost():
            personaje = personaje[1]
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 1 #1: ha entrado y está por primera vez en la sala, 2: continúa en la sala normal, 3: Está en uno de los pasillos de la sala, el de la variable self.pasillo_from_puerta, 4: ya no está en la sala, pero entró
        self.numJugadores = numJugadores
        self.tipo_de_estado = "sala_grande"
        self.estadosSucesores = estado_pred
        self.ids = 0
        self.ordenEstados = {} #Estados contenidos por la sala # contiene todos los estados de "self.daASalas = {}"
        self.numAccepts = 0 
        self.dialogoDMIntro = "Tras abrir la puerta, ves que te encuentras en otra galería, también oscura y amplia. "+descripcion_sala
        self.id = id_sala
        self.es_obligatorio = es_obligatoria #por defecto se marcan como opcionales. Luego, las obligatorias se marcarán como obligatorias
        self.esInicial = esInicial
        self.tienePortales = tienePortales
        self.contieneLlaves = contieneLlaves #Lista de posiciones de las puertas que abre cada llave de aquí
        self.esFinal = esFinal
        self.orden = orden
        self.tipo_mision = tipo_mision
        self.size = size
        self.daASalas = daASalas
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pasilloToPuerta = None
        self.pasilloFromPuerta = None
        self.Mapa = Mapa
        self.frases_puerta = frase_puerta
        self.idSala_idOrder = idSala_idOrder
        self.read = False
        self.read2 = False
        self.read4 = False


    def checkIfCanRun(self,DM,personaje):
        return self.checkIfCanRunByPlayer(DM,personaje)

    
    def checkIfCanRunByPlayer(self,DM,personaje):
        return True
    
    
    def checkIfCanExit(self,DM,personaje,currentEstado):
        if(((personaje.playerAction == "WALK_DOWN") or (personaje.playerAction == "IDLE_DOWN")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]+1][personaje.coordenadas_actuales_r[0]] == 13) or (self.Mapa.matrix[personaje.coordenadas_actuales_r[1]+1][personaje.coordenadas_actuales_r[0]] == 23))):  
            pos_x = personaje.coordenadas_actuales_r[0]
            pos_y = personaje.coordenadas_actuales_r[1]+1
        elif(((personaje.playerAction == "WALK_UP") or (personaje.playerAction == "IDLE_UP")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] == 12) or (self.Mapa.matrix[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] == 23))):
            pos_x = personaje.coordenadas_actuales_r[0]
            pos_y = personaje.coordenadas_actuales_r[1]-1
        elif(((personaje.playerAction == "WALK_LEFT") or (personaje.playerAction == "IDLE_LEFT")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]-1] == 10) or (self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]-1] == 23))):
            pos_x = personaje.coordenadas_actuales_r[0]-1
            pos_y = personaje.coordenadas_actuales_r[1]
        elif(((personaje.playerAction == "WALK_RIGHT") or (personaje.playerAction == "IDLE_RIGHT")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]+1] == 11) or (self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]+1] == 23))):
            pos_x = personaje.coordenadas_actuales_r[0]+1
            pos_y = personaje.coordenadas_actuales_r[1]
        else:
            pos_x = None
            pos_y = None
        print(pos_x,pos_y)
        if(pos_x != None and pos_y != None):
            for sala in self.Mapa.salas[self.id].daASalas:
                if(self.Mapa.salas[self.id].daASalas[sala][0] == [pos_x,pos_y]):
                    print("En sala "+str(self.id)+" da a salas hacia sala "+str(sala)+" está "+self.Mapa.salas[self.id].daASalas[sala][1])
                    if(self.Mapa.salas[self.id].daASalas[sala][1] == "abierto"):
                        #La puerta existe y da a la sala "sala", y está abierta para pasar
                        print("puerta")
                        self.read2 = False
                        if(self.Mapa.matrix[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] == 23):
                            self.GLOBAL.setActionDoor([2,[pos_x,pos_y]])
                            self.pasilloFromPuerta = [[pos_x,pos_y], sala]
                        else:
                            if(self.Mapa.adyacencias[self.id][sala] == 1):
                                #Es adyacente
                                self.GLOBAL.setActionDoor([3,[pos_x,pos_y]]) #podría abrirla
                            else:
                                self.GLOBAL.setActionDoor([1,[pos_x,pos_y]]) #podría abrirla
                            self.pasilloFromPuerta = [[pos_x,pos_y], sala]
                        return False
                    else:
                        # Comprobamos si lleva alguna llave equipada en una de las manos:
                        canPass = [False,None]
                        item_left = personaje.equipo.objeto_equipado_mano_izquierda
                        if((item_left != None) and (item_left[1] == "Llave") and (item_left[2].puerta == self.id) and (item_left[2].enlace == sala)):
                            canPass = [True,"left"]
                        item_right = personaje.equipo.objeto_equipado_mano_derecha
                        if((item_right != None) and (item_right[1] == "Llave") and (item_right[2].puerta == self.id) and (item_right[2].enlace == sala)):
                            canPass = [True,"right"]

                        if(canPass[0]):
                            # Elimino la llave del inventario
                            if(canPass[1] == "left"):
                                personaje.equipo.objeto_equipado_mano_izquierda = None
                            elif(canPass[1] == "right"):
                                personaje.equipo.objeto_equipado_mano_derecha = None

                            # Abro la puerta
                            self.Mapa.salas[self.id].daASalas[sala][1] = "abierto"
                            cancion = pygame.mixer.Sound('sounds/abrir_llave.wav')
                            pygame.mixer.Channel(7).play(cancion) #reproduzco el sonido de poner la llave
                            cancion = None
                            text_abrir = "Intentas usar una llave en el pomo de la puerta, y ves que esta cede."
                            DM.speak(text_abrir) 
                            to_list = "El jugador acaba de poner una llave en la cerradura de una puerta que se encontraba bloqueada, y la ha girado, y esta se ha abierto"
                            self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
                            #Ejecuto la apertura
                            self.read2 = False
                            if(self.Mapa.adyacencias[self.id][sala] == 1):
                            #Es adyacente
                                self.GLOBAL.setActionDoor([3,[pos_x,pos_y]]) #podría abrirla
                                self.pasilloFromPuerta = [[pos_x,pos_y],sala]

                            else:
                                self.GLOBAL.setActionDoor([1,[pos_x,pos_y]]) #podría abrirla
                                self.pasilloFromPuerta = [[pos_x,pos_y],sala]
                            return False

                        else:
                            if(not self.read2):
                                #La puerta está  cerrada
                                self.read2 = True
                                print("puerta cerrada")
                                pygame.mixer.Channel(1).play(self.soundDoor)
                                text_closed = self.frases_puerta[self.id][sala][0]
                                DM.speak(text_closed) 
                                to_list = "El jugador ha intentado abrir una puerta, pero estaba cerrada. Esto fue lo que le dijo el Dungeon Master: "+text_closed
                                self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
                            self.GLOBAL.setActionDoor([0,[None,None]]) 
                            return False
                
        else:
            self.read2 = False
                    # Si ya ha hablado con el NPC y el personaje ha dado click para cruzar la puerta
        print(self.GLOBAL.canGoOutFirst(), self.pasilloFromPuerta, self.GLOBAL.getCrossedDoor())
        if(self.GLOBAL.canGoOutFirst() and (self.pasilloFromPuerta != None) and (self.GLOBAL.getCrossedDoor()[1] == self.pasilloFromPuerta[0])):
            #Ha decidido cruzarla
            self.GLOBAL.setActionDoor([0,[None,None]])
            self.GLOBAL.setCrossedDoor([[False],[None,None]])
            pygame.mixer.Channel(1).play(self.soundDoor)
            text_open_door = self.frases_puerta[self.id][self.pasilloFromPuerta[1]][1]
            DM.speak(text_open_door) 
            to_list = "El jugador acaba de abrir una puerta, y esto es lo que le ha dicho el Dungeon Master: "+text_open_door
            self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
            #reseteo las variables
            #Si la puerta estaba originalmente cerrada, o si está abierta, pero desde el otro lado estaba cerrada, se va a abrir:
            # Es un puntero, así que se cambiará en su correspondiente estado
            self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[self.id][1] = "abierto"
            print("Sala "+str(self.pasilloFromPuerta[1])+", modificado da a salas de sala "+str(self.id))
            if(self.Mapa.adyacencias[self.id][self.pasilloFromPuerta[1]] == 1):
                self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2
                currentEstado[str(personaje.name)+","+str(personaje.id_jugador)] = self.idSala_idOrder[self.pasilloFromPuerta[1]]
            else:
                self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 3 #está en un pasillo
                self.pasilloFromPuerta = [self.pasilloFromPuerta[0],self.pasilloFromPuerta[1]] #guardo cuál es la puerta desde la que entró, y la sala a la que se dirige, para simplificar después las comprobaciones
            
            return True
        else:
            self.GLOBAL.setActionDoor([0,[None,None]])
            self.pasilloFromPuerta = None
            return False
        
    def checkIfItIsInCurrentRoom(self,pos_x,pos_y):
        start_x = self.pos_x
        start_y = self.pos_y
        dif = pos_x - start_x
        dif2 = pos_y - start_y
        if((dif >= 0) and (dif <self.size[0]) and (dif2 >= 0) and (dif2 < self.size[1])):
            #Está en algún punto de esa sala
            return True
        return False

    def checkIfCanEnterAgain(self,DM,personaje):
        if(((personaje.playerAction == "WALK_DOWN") or (personaje.playerAction == "IDLE_DOWN")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]+1][personaje.coordenadas_actuales_r[0]] == 12))):  
            pos_x = personaje.coordenadas_actuales_r[0]
            pos_y = personaje.coordenadas_actuales_r[1]+1
        elif(((personaje.playerAction == "WALK_UP") or (personaje.playerAction == "IDLE_UP")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] == 13))):
            pos_x = personaje.coordenadas_actuales_r[0]
            pos_y = personaje.coordenadas_actuales_r[1]-1
        elif(((personaje.playerAction == "WALK_LEFT") or (personaje.playerAction == "IDLE_LEFT")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]-1] == 11))):
            pos_x = personaje.coordenadas_actuales_r[0]-1
            pos_y = personaje.coordenadas_actuales_r[1]
        elif(((personaje.playerAction == "WALK_RIGHT") or (personaje.playerAction == "IDLE_RIGHT")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]+1] == 10))):
            pos_x = personaje.coordenadas_actuales_r[0]+1
            pos_y = personaje.coordenadas_actuales_r[1]
        else:
            pos_x = None
            pos_y = None
        print(pos_x,pos_y)
        if(pos_x != None and pos_y != None):
            if((self.pasilloFromPuerta[0] == [pos_x,pos_y]) and (self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[self.id][1] == "abierto")):
                #La puerta existe y da a la sala "sala", y está abierta para pasar
                if(self.Mapa.adyacencias[self.id][self.pasilloFromPuerta[1]] == 1):
                    self.GLOBAL.setActionDoor([3,[pos_x,pos_y]]) #podría abrirla
                else:
                    self.GLOBAL.setActionDoor([1,[pos_x,pos_y]]) #podría abrirla
                return True
                
                    # Si ya ha hablado con el NPC y el personaje ha dado click para cruzar la puerta
        if(self.GLOBAL.canGoOutFirst() and (self.pasilloFromPuerta != None) and (self.GLOBAL.getCrossedDoor()[1] == self.pasilloFromPuerta[0]) and self.checkIfItIsInCurrentRoom(personaje.coordenadas_actuales_r[0],personaje.coordenadas_actuales_r[1])):
            #Ha decidido cruzarla
            self.GLOBAL.setActionDoor([0,[None,None]])
            self.GLOBAL.setCrossedDoor([[False],[None,None]])
            pygame.mixer.Channel(1).play(self.soundDoor)
            text_open_door = self.frases_puerta[self.pasilloFromPuerta[1]][self.id][2]
            self.pasilloFromPuerta = None
            DM.speak(text_open_door) 
            to_list = "El jugador acaba de abrir una puerta, y esto es lo que le ha dicho el Dungeon Master: "+text_open_door
            self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
            #reseteo las variables
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2 #está en la sala de nuevo
             #guardo cuál es la puerta desde la que entró, y la sala a la que se dirige, para simplificar después las comprobaciones
            # Si trata de entrar después a otra puerta de otro camino que se haya anexado, le dirá que una magia oscura impide que la abra jeje
            return True
        else:
            self.GLOBAL.setActionDoor([0,[None,None]])
            return False
                    


    def checkIfCanPassToAnotherRoom(self,DM,personaje,currentEstadoByPlayers):
        if(((personaje.playerAction == "WALK_DOWN") or (personaje.playerAction == "IDLE_DOWN")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]+1][personaje.coordenadas_actuales_r[0]] == 12))):  
            pos_x = personaje.coordenadas_actuales_r[0]
            pos_y = personaje.coordenadas_actuales_r[1]+1
        elif(((personaje.playerAction == "WALK_UP") or (personaje.playerAction == "IDLE_UP")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] == 13))):
            pos_x = personaje.coordenadas_actuales_r[0]
            pos_y = personaje.coordenadas_actuales_r[1]-1
        elif(((personaje.playerAction == "WALK_LEFT") or (personaje.playerAction == "IDLE_LEFT")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]-1] == 11))):
            pos_x = personaje.coordenadas_actuales_r[0]-1
            pos_y = personaje.coordenadas_actuales_r[1]
        elif(((personaje.playerAction == "WALK_RIGHT") or (personaje.playerAction == "IDLE_RIGHT")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]+1] == 10))):
            pos_x = personaje.coordenadas_actuales_r[0]+1
            pos_y = personaje.coordenadas_actuales_r[1]
        else:
            pos_x = None
            pos_y = None
        print(pos_x,pos_y)
        if(pos_x != None and pos_y != None):
            for sala in self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas:
                if(self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[sala][0] == [pos_x,pos_y]):
                    if(self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[sala][1] == "abierto"):
                        #La puerta existe y da a la sala "sala", y está abierta para pasar
                        if(self.Mapa.adyacencias[self.id][sala] == 1):
                            #Es adyacente
                            self.read = False
                            self.read4 = False
                            self.GLOBAL.setActionDoor([3,[pos_x,pos_y]]) #podría abrirla
                            self.pasilloToPuerta = [[pos_x,pos_y],sala]
                        else:
                            self.read = False
                            self.read4 = False
                            self.GLOBAL.setActionDoor([1,[pos_x,pos_y]]) #podría abrirla
                            self.pasilloToPuerta = [[pos_x,pos_y],sala]
                        return False
                    else:
                        # Comprobamos si lleva alguna llave equipada en una de las manos:
                        canPass = [False,None]
                        item_left = personaje.equipo.objeto_equipado_mano_izquierda
                        if((item_left != None) and (item_left[1] == "Llave") and (item_left[2].puerta == self.id) and (item_left[2].enlace == sala)):
                            canPass = [True,"left"]
                        item_right = personaje.equipo.objeto_equipado_mano_derecha
                        if((item_right != None) and (item_right[1] == "Llave") and (item_right[2].puerta == self.id) and (item_right[2].enlace == sala)):
                            canPass = [True,"right"]

                        if(canPass[0]):
                            # Elimino la llave del inventario
                            if(canPass[1] == "left"):
                                personaje.equipo.objeto_equipado_mano_izquierda = None
                            elif(canPass[1] == "right"):
                                personaje.equipo.objeto_equipado_mano_derecha = None

                            # Abro la puerta
                            self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[sala][1] = "abierto"
                            cancion = pygame.mixer.Sound('sounds/abrir_llave.wav')
                            pygame.mixer.Channel(7).play(cancion) #reproduzco el sonido de poner la llave
                            cancion = None
                            text_abrir = "Intentas usar una llave en el pomo de la puerta, y ves que esta cede."
                            DM.speak(text_abrir) 
                            to_list = "El jugador acaba de poner una llave en la cerradura de una puerta que se encontraba bloqueada, y la ha girado, y esta se ha abierto"
                            self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
                            #Ejecuto la apertura
                            if(self.Mapa.adyacencias[self.id][sala] == 1):
                            #Es adyacente
                                self.GLOBAL.setActionDoor([3,[pos_x,pos_y]]) #podría abrirla
                                self.pasilloToPuerta = [[pos_x,pos_y],sala]
                                self.read = False
                                self.read4 = False
                            else:
                                self.GLOBAL.setActionDoor([1,[pos_x,pos_y]]) #podría abrirla
                                self.pasilloToPuerta = [[pos_x,pos_y],sala]
                                self.read = False
                                self.read4 = False
                            return False

                        else:
                            #La puerta está cerrada
                            if(not self.read4):
                                print("puerta cerrada")
                                pygame.mixer.Channel(1).play(self.soundDoor)
                                text_closed = self.frases_puerta[self.pasilloFromPuerta[1]][sala][0]
                                DM.speak(text_closed) 
                                to_list = "El jugador ha intentado abrir una puerta, pero estaba cerrada. Esto fue lo que le dijo el Dungeon Master: "+text_closed
                                self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
                                self.read = False
                                self.read4 = True
                                self.GLOBAL.setActionDoor([0,[None,None]]) 
                            return False
                
            if((not self.read) and (10 <= self.Mapa.matrix[pos_y][pos_x] <= 13) and not((self.pasilloToPuerta != None) and (self.GLOBAL.getCrossedDoor()[1] == self.pasilloToPuerta[0]))):
                #Es otra puerta distinta, pero no se puede pasar porque no es del enlace
                pygame.mixer.Channel(1).play(self.soundDoor)
                text = "Parece que algún tipo de magia impide que puedas abrir esta puerta."
                DM.speak(text)
                to_list = "El jugador ha intentado abrir una puerta, pero parece que algún tipo de magia impidió que la abriera"
                self.GLOBAL.addElementToListaAndRemoveFirst(to_list) 
                self.GLOBAL.setActionDoor([0,[None,None]]) 
                self.read = True
                self.read4 = False
                return False
        else:
            self.read = False
            self.read4 = False
                    # Si ya ha hablado con el NPC y el personaje ha dado click para cruzar la puerta
        if(self.GLOBAL.canGoOutFirst() and (self.pasilloToPuerta != None) and (self.GLOBAL.getCrossedDoor()[1] == self.pasilloToPuerta[0])):
            #Ha decidido cruzarla
            self.GLOBAL.setActionDoor([0,[None,None]])
            self.GLOBAL.setCrossedDoor([[False],[None,None]])
            pygame.mixer.Channel(1).play(self.soundDoor)
            # El texto de la puerta se reproducirá en el estado de destino
            #reseteo las variables
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2 
            #Si la puerta estaba originalmente cerrada, o si está abierta, pero desde el otro lado estaba cerrada, se va a abrir:
            # Es un puntero, así que se cambiará en su correspondiente estado
            self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[self.id][1] = "abierto" #guardo cuál es la puerta desde la que entró, y la sala a la que se dirige, para simplificar después las comprobaciones
            currentEstadoByPlayers[str(personaje.name)+","+str(personaje.id_jugador)] = self.idSala_idOrder[self.pasilloFromPuerta[1]]
            self.pasilloFromPuerta = None
            self.pasilloToPuerta = None
            
            return True
        else:
            self.GLOBAL.setActionDoor([0,[None,None]])
            return False
        
        
    def checkIfCompleted(self,personaje):
        #print("check if completed de sala inicial: False")
        return False #Una sala nunca se puede completar. Siempre puedes entrar a ella, si el check del run se cumple
        
    def run(self,DM,personaje,currentEstadoByPlayers):
        #TODO: run en función del estado de la misión
        # print("run:")
        print(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)])
        if(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 1):
            self.OnEnterEstadoByPlayer(DM,personaje,currentEstadoByPlayers)
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 2):
            if(self.checkIfCanExit(DM,personaje,currentEstadoByPlayers)):
                pass
            else:
                self.runNextInnerEstado(DM,personaje)
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 3):
            print("en el pasillo")
            if(self.checkIfCanEnterAgain(DM,personaje)):
                pass
            else:
                self.checkIfCanPassToAnotherRoom(DM,personaje,currentEstadoByPlayers)
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 4):
            pass
        else:
            pass #si están en 0 no hace nada, hay que esperar a que todos acepten 

    def runNextInnerEstado(self,DM,personaje):
        for id,estado in self.ordenEstados.items():
            if(not estado.checkIfCompleted(personaje) and estado.checkIfCanRun(DM,personaje)):
                estado.run(DM,personaje)


    def OnEnterEstadoByPlayer(self,DM,personaje,currentEstadoByPlayers):
        #El mensaje de introducción a la sala, se le reproduce a cada uno de forma individual (por si alguno muriera, y se tuviera que crear otro, que esto ya sea independiente)
        print("<DM>: "+self.dialogoDMIntro) #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        DM.speak(self.dialogoDMIntro) 
        to_list = "El jugador acaba de entrar a una nueva galería, y esto es lo que le ha dicho el Dungeon Master sobre esa galería: "+self.dialogoDMIntro
        self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
        print("Sala "+str(self.id))
        #DM.printVoices()
        self.GLOBAL.addRoomVisited()
        self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2 #está en la sala normal
        self.run(DM,personaje,currentEstadoByPlayers)

    def addChest(self,dmf1,dme1,cofre):
        if(cofre[1].inventory[1] == "Llave"):
            obligatorio = True
        else:
            obligatorio = False
        self.ordenEstados[self.ids] = EstadoInteractChest(False,None,'cofre',obligatorio,self.personajeDelHost,self.numJugadores,self,cofre[0],cofre[1],dmf1,dme1)
        self.ids +=1



class EstadoDeSalaInicial(Estado):
    def __init__(self,isInicial,content,RAG_musica,currentPartida,estado_pred,numJugadores,id,personajeDelHost,id_sala,es_obligatoria,esInicial,daASalas,tienePortales,contieneLlaves,esFinal,orden,tipo_mision, size, pos_x, pos_y,Mapa,frase_puerta,descripcion_sala,idSala_idOrder):
        super().__init__(isInicial,content,id)
        self.personajeDelHost = personajeDelHost
        self.variableDeCheck["progreso"] = {}
        self.variableDeCheck["progreso"][str(self.personajeDelHost.name)+","+str(self.personajeDelHost.id_jugador)] = -1
        for personaje in self.GLOBAL.getListaPersonajeHost():
            personaje = personaje[1]
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = -1 #-1: No ha aceptado entrar aún, 0: No ha entrado ese personaje en la sala, 1: ha entrado y está por primera vez en la sala, 2: continúa en la sala normal, 3: Está en uno de los pasillos de la sala, el de la variable self.pasillo_from_puerta, 4: ya no está en la sala, pero entró
        self.numJugadores = numJugadores
        self.tipo_de_estado = "sala_grande"
        self.estadosSucesores = estado_pred
        self.ids = 0
        self.ordenEstados = {} #Estados contenidos por la sala
        self.numAccepts = 0 
        #TODO: incluir la descripción del mapa
        self.dialogoDMIntro = "¡Bien! Te encuentras en una amplia galería dentro de una mazmorra subterránea. "+descripcion_sala
        self.id = id_sala
        self.es_obligatorio = es_obligatoria #por defecto se marcan como opcionales. Luego, las obligatorias se marcarán como obligatorias
        self.esInicial = esInicial
        self.tienePortales = tienePortales
        self.contieneLlaves = contieneLlaves #Lista de posiciones de las puertas que abre cada llave de aquí
        self.esFinal = esFinal
        self.orden = orden
        self.tipo_mision = tipo_mision
        self.size = size
        self.daASalas = daASalas
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pasilloFromPuerta = None
        self.read = False
        self.Mapa = Mapa
        self.frases_puerta = frase_puerta
        self.read2 = False
        self.read3 = False
        self.pasilloToPuerta = None
        self.read4 = False
        self.idSala_idOrder = idSala_idOrder

    def addChest(self,dmf1,dme1,cofre):
        if(cofre[1].inventory[1] == "Llave"):
            obligatorio = True
        else:
            obligatorio = False
        self.ordenEstados[self.ids] = EstadoInteractChest(False,None,'cofre',obligatorio,self.personajeDelHost,self.numJugadores,self,cofre[0],cofre[1],dmf1,dme1)
        self.ids +=1


    def checkIfCanRun(self,DM,personaje):
        # print(self.numAccepts)
        # print(self.numJugadores)
        # print("------------------------")
        if self.numAccepts != self.numJugadores:
            return self.checkIfCanRunFirst(personaje)
        else:
            return self.checkIfCanRunByPlayer(DM,personaje)

    def checkIfCanRunFirst(self,personaje):
        if(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 0):
            self.numAccepts +=1
        
        #Si todos han aceptado
        # print("check if can run first sala inicial:")
        # print(self.numAccepts)
        # print(self.numJugadores)
        if self.numAccepts == self.numJugadores:
            self.variableDeCheck["progreso"][str(self.personajeDelHost.name)+","+str(self.personajeDelHost.id_jugador)] = 1 
            for personaje in self.GLOBAL.getListaPersonajeHost():
                self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 1 #los llevo a la sala de inicio
            #print("variable de check a 1")
            return True
        else:
            return False
        
    def checkIfCanExit(self,DM,personaje,currentEstado):
        if(((personaje.playerAction == "WALK_DOWN") or (personaje.playerAction == "IDLE_DOWN")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]+1][personaje.coordenadas_actuales_r[0]] == 13) or (self.Mapa.matrix[personaje.coordenadas_actuales_r[1]+1][personaje.coordenadas_actuales_r[0]] == 23))):  
            pos_x = personaje.coordenadas_actuales_r[0]
            pos_y = personaje.coordenadas_actuales_r[1]+1
        elif(((personaje.playerAction == "WALK_UP") or (personaje.playerAction == "IDLE_UP")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] == 12) or (self.Mapa.matrix[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] == 23))):
            pos_x = personaje.coordenadas_actuales_r[0]
            pos_y = personaje.coordenadas_actuales_r[1]-1
        elif(((personaje.playerAction == "WALK_LEFT") or (personaje.playerAction == "IDLE_LEFT")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]-1] == 10) or (self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]-1] == 23))):
            pos_x = personaje.coordenadas_actuales_r[0]-1
            pos_y = personaje.coordenadas_actuales_r[1]
        elif(((personaje.playerAction == "WALK_RIGHT") or (personaje.playerAction == "IDLE_RIGHT")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]+1] == 11) or (self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]+1] == 23))):
            pos_x = personaje.coordenadas_actuales_r[0]+1
            pos_y = personaje.coordenadas_actuales_r[1]
        else:
            pos_x = None
            pos_y = None
        print(pos_x,pos_y)
        if(pos_x != None and pos_y != None):
            for sala in self.Mapa.salas[self.id].daASalas:
                print(self.Mapa.salas[self.id].daASalas[sala][0])
                
                if(self.Mapa.salas[self.id].daASalas[sala][0] == [pos_x,pos_y]):
                    if(self.Mapa.salas[self.id].daASalas[sala][1] == "abierto"):
                        #La puerta existe y da a la sala "sala", y está abierta para pasar
                        # Comprobamos el estado de la misión: es el último
                        ultimo_id, ultimo_estado = list(self.ordenEstados.items())[-1]
                        if (self.ordenEstados[ultimo_id].variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 1):
                            print("puerta")
                            self.read2 = False
                            self.read3 = False
                            if(self.Mapa.matrix[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] == 23):
                                self.GLOBAL.setActionDoor([2,[pos_x,pos_y]])
                                self.pasilloFromPuerta = [[pos_x,pos_y], sala]
                            else:
                                if(self.Mapa.adyacencias[self.id][sala] == 1):
                                    #Es adyacente
                                    print("sala adyacente")
                                    self.GLOBAL.setActionDoor([3,[pos_x,pos_y]]) #podría abrirla
                                else:
                                    print("sala normal")
                                    self.GLOBAL.setActionDoor([1,[pos_x,pos_y]]) #podría abrirla
                                self.pasilloFromPuerta = [[pos_x,pos_y], sala]
                            return False
                        else:
                            if(not self.read3):
                                self.read3 = True
                                text = "Vaya, parece que algo impide que puedas abrir esta puerta..."
                                pygame.mixer.Channel(1).play(self.soundDoor)
                                DM.speak(text) 
                                to_list = "El jugador ha intentado abrir una puerta, pero parece que algo impide que la pueda abrir, quizás algún conjuro"
                                self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
                            return False
                    else:
                        # Comprobamos si lleva alguna llave equipada en una de las manos:
                        canPass = [False,None]
                        item_left = personaje.equipo.objeto_equipado_mano_izquierda
                        if((item_left != None) and (item_left[1] == "Llave") and (item_left[2].puerta == self.id) and (item_left[2].enlace == sala)):
                            canPass = [True,"left"]
                        item_right = personaje.equipo.objeto_equipado_mano_derecha
                        if((item_right != None) and (item_right[1] == "Llave") and (item_right[2].puerta == self.id) and (item_right[2].enlace == sala)):
                            canPass = [True,"right"]

                        if(canPass[0]):
                            # Elimino la llave del inventario
                            if(canPass[1] == "left"):
                                personaje.equipo.objeto_equipado_mano_izquierda = None
                            elif(canPass[1] == "right"):
                                personaje.equipo.objeto_equipado_mano_derecha = None

                            # Abro la puerta
                            self.Mapa.salas[self.id].daASalas[sala][1] = "abierto"
                            cancion = pygame.mixer.Sound('sounds/abrir_llave.wav')
                            pygame.mixer.Channel(7).play(cancion) #reproduzco el sonido de poner la llave
                            cancion = None
                            text_abrir = "Intentas usar una llave en el pomo de la puerta, y ves que esta cede."
                            DM.speak(text_abrir) 
                            to_list = "El jugador acaba de poner una llave en la cerradura de una puerta que se encontraba bloqueada, y la ha girado, y esta se ha abierto"
                            self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
                            #Ejecuto la apertura
                            self.read2 = False
                            self.read3 = False
                            if(self.Mapa.adyacencias[self.id][sala] == 1):
                            #Es adyacente
                                self.GLOBAL.setActionDoor([3,[pos_x,pos_y]]) #podría abrirla
                                self.pasilloFromPuerta = [[pos_x,pos_y],sala]

                            else:
                                self.GLOBAL.setActionDoor([1,[pos_x,pos_y]]) #podría abrirla
                                self.pasilloFromPuerta = [[pos_x,pos_y],sala]
                            return False

                        else:
                            if(not self.read2):
                                #La puerta está  cerrada
                                self.read2 = True
                                self.read3 = False
                                print("puerta cerrada")
                                pygame.mixer.Channel(1).play(self.soundDoor)
                                text_closed = self.frases_puerta[self.id][sala][0]
                                DM.speak(text_closed) 
                                to_list = "El jugador ha intentado abrir una puerta, pero estaba cerrada. Esto fue lo que le dijo el Dungeon Master: "+text_closed
                                self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
                            self.GLOBAL.setActionDoor([0,[None,None]]) 
                            return False
                
        else:
            self.read2 = False
            self.read3 = False
                    # Si ya ha hablado con el NPC y el personaje ha dado click para cruzar la puerta
        print(self.GLOBAL.canGoOutFirst())
        print(self.GLOBAL.getCrossedDoor())
        if(self.GLOBAL.canGoOutFirst() and (self.pasilloFromPuerta != None) and(self.GLOBAL.getCrossedDoor()[1] == self.pasilloFromPuerta[0])):
            #Ha decidido cruzarla
            print("aquí")
            self.GLOBAL.setActionDoor([0,[None,None]])
            pygame.mixer.Channel(1).play(self.soundDoor)
            self.GLOBAL.setCrossedDoor([[False],[None,None]])
            text_open_door = self.frases_puerta[self.id][self.pasilloFromPuerta[1]][1]
            DM.speak(text_open_door) 
            to_list = "El jugador acaba de abrir una puerta, y esto es lo que le ha dicho el Dungeon Master: "+text_open_door
            self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
            #reseteo las variables
            #Si la puerta estaba originalmente cerrada, o si está abierta, pero desde el otro lado estaba cerrada, se va a abrir:
            # Es un puntero, así que se cambiará en su correspondiente estado
            self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[self.id][1] = "abierto"
            if(self.Mapa.adyacencias[self.id][self.pasilloFromPuerta[1]] == 1):
                print(self.pasilloFromPuerta[1])
                print(self.idSala_idOrder)
                print(self.ordenEstados)
                self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2 
                currentEstado[str(personaje.name)+","+str(personaje.id_jugador)] = self.idSala_idOrder[self.pasilloFromPuerta[1]]
            else:
                self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 3 #está en un pasillo
                self.pasilloFromPuerta = [self.pasilloFromPuerta[0],self.pasilloFromPuerta[1]] #guardo cuál es la puerta desde la que entró, y la sala a la que se dirige, para simplificar después las comprobaciones
            
            return True
        else:
            self.GLOBAL.setActionDoor([0,[None,None]])
            self.pasilloFromPuerta = None
            return False
                    
    def checkIfCanRunByPlayer(self,DM,personaje):
        #print("en run by player")
        if(2 <= self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] <= 3):
            #Si está ya en la sala, y ha ejecutado la descripción inicial
            return True
        

    def checkIfItIsInCurrentRoom(self,pos_x,pos_y):
        start_x = self.pos_x
        start_y = self.pos_y
        dif = pos_x - start_x
        dif2 = pos_y - start_y
        if((dif >= 0) and (dif <self.size[0]) and (dif2 >= 0) and (dif2 < self.size[1])):
            #Está en algún punto de esa sala
            return True
        return False
        
    def checkIfCanEnterAgain(self,DM,personaje):
        if(((personaje.playerAction == "WALK_DOWN") or (personaje.playerAction == "IDLE_DOWN")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]+1][personaje.coordenadas_actuales_r[0]] == 12))):  
            pos_x = personaje.coordenadas_actuales_r[0]
            pos_y = personaje.coordenadas_actuales_r[1]+1
        elif(((personaje.playerAction == "WALK_UP") or (personaje.playerAction == "IDLE_UP")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] == 13))):
            pos_x = personaje.coordenadas_actuales_r[0]
            pos_y = personaje.coordenadas_actuales_r[1]-1
        elif(((personaje.playerAction == "WALK_LEFT") or (personaje.playerAction == "IDLE_LEFT")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]-1] == 11))):
            pos_x = personaje.coordenadas_actuales_r[0]-1
            pos_y = personaje.coordenadas_actuales_r[1]
        elif(((personaje.playerAction == "WALK_RIGHT") or (personaje.playerAction == "IDLE_RIGHT")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]+1] == 10))):
            pos_x = personaje.coordenadas_actuales_r[0]+1
            pos_y = personaje.coordenadas_actuales_r[1]
        else:
            pos_x = None
            pos_y = None
        print(pos_x,pos_y)
        print(self.pasilloFromPuerta)
        if(pos_x != None and pos_y != None):
            if((self.pasilloFromPuerta[0] == [pos_x,pos_y]) and (self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[self.id][1] == "abierto")):
                #La puerta existe y da a la sala "sala", y está abierta para pasar
                if(self.Mapa.adyacencias[self.id][self.pasilloFromPuerta[1]] == 1):
                    self.GLOBAL.setActionDoor([3,[pos_x,pos_y]]) #podría abrirla
                else:
                    self.GLOBAL.setActionDoor([1,[pos_x,pos_y]]) #podría abrirla
                return True
                
                    # Si ya ha hablado con el NPC y el personaje ha dado click para cruzar la puerta
        print("aquí 1")
        if(self.GLOBAL.canGoOutFirst() and (self.pasilloFromPuerta != None) and(self.GLOBAL.getCrossedDoor()[1] == self.pasilloFromPuerta[0]) and self.checkIfItIsInCurrentRoom(personaje.coordenadas_actuales_r[0],personaje.coordenadas_actuales_r[1])):
            #Ha decidido cruzarla
            self.GLOBAL.setActionDoor([0,[None,None]])
            self.GLOBAL.setCrossedDoor([[False],[None,None]])
            pygame.mixer.Channel(1).play(self.soundDoor)
            text_open_door = self.frases_puerta[self.pasilloFromPuerta[1]][self.id][2]
            self.pasilloFromPuerta = None
            DM.speak(text_open_door) 
            to_list = "El jugador acaba de abrir una puerta, y esto es lo que le ha dicho el Dungeon Master: "+text_open_door
            self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
            #reseteo las variables
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2 #está en la sala de nuevo
             #guardo cuál es la puerta desde la que entró, y la sala a la que se dirige, para simplificar después las comprobaciones
            # Si trata de entrar después a otra puerta de otro camino que se haya anexado, le dirá que una magia oscura impide que la abra jeje
            print("True")
            return True
        else:
            self.GLOBAL.setActionDoor([0,[None,None]])
            print("False")
            return False
                    


    def checkIfCanPassToAnotherRoom(self,DM,personaje,currentEstadoByPlayers):
        if(((personaje.playerAction == "WALK_DOWN") or (personaje.playerAction == "IDLE_DOWN")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]+1][personaje.coordenadas_actuales_r[0]] == 12))):  
            pos_x = personaje.coordenadas_actuales_r[0]
            pos_y = personaje.coordenadas_actuales_r[1]+1
        elif(((personaje.playerAction == "WALK_UP") or (personaje.playerAction == "IDLE_UP")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] == 13))):
            pos_x = personaje.coordenadas_actuales_r[0]
            pos_y = personaje.coordenadas_actuales_r[1]-1
        elif(((personaje.playerAction == "WALK_LEFT") or (personaje.playerAction == "IDLE_LEFT")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]-1] == 11))):
            pos_x = personaje.coordenadas_actuales_r[0]-1
            pos_y = personaje.coordenadas_actuales_r[1]
        elif(((personaje.playerAction == "WALK_RIGHT") or (personaje.playerAction == "IDLE_RIGHT")) and ((self.Mapa.matrix[personaje.coordenadas_actuales_r[1]][personaje.coordenadas_actuales_r[0]+1] == 10))):
            pos_x = personaje.coordenadas_actuales_r[0]+1
            pos_y = personaje.coordenadas_actuales_r[1]
        else:
            pos_x = None
            pos_y = None
        print(pos_x,pos_y)
        if(pos_x != None and pos_y != None):
            for sala in self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas:
                if(self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[sala][0] == [pos_x,pos_y]):
                    if(self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[sala][1] == "abierto"):
                        #La puerta existe y da a la sala "sala", y está abierta para pasar
                        if(self.Mapa.adyacencias[self.id][sala] == 1):
                            #Es adyacente
                            self.GLOBAL.setActionDoor([3,[pos_x,pos_y]]) #podría abrirla
                            self.pasilloToPuerta = [[pos_x,pos_y],sala]
                            self.read = False
                            self.read4 = False
                        else:
                            self.GLOBAL.setActionDoor([1,[pos_x,pos_y]]) #podría abrirla
                            self.pasilloToPuerta = [[pos_x,pos_y],sala]
                            self.read = False
                            self.read4 = False
                        return False
                    else:
                        # Comprobamos si lleva alguna llave equipada en una de las manos:
                        canPass = [False,None]
                        item_left = personaje.equipo.objeto_equipado_mano_izquierda
                        if((item_left != None) and (item_left[1] == "Llave") and (item_left[2].puerta == self.id) and (item_left[2].enlace == sala)):
                            canPass = [True,"left"]
                        item_right = personaje.equipo.objeto_equipado_mano_derecha
                        if((item_right != None) and (item_right[1] == "Llave") and (item_right[2].puerta == self.id) and (item_right[2].enlace == sala)):
                            canPass = [True,"right"]

                        if(canPass[0]):
                            # Elimino la llave del inventario
                            if(canPass[1] == "left"):
                                personaje.equipo.objeto_equipado_mano_izquierda = None
                            elif(canPass[1] == "right"):
                                personaje.equipo.objeto_equipado_mano_derecha = None

                            # Abro la puerta
                            self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[sala][1] = "abierto"
                            cancion = pygame.mixer.Sound('sounds/abrir_llave.wav')
                            pygame.mixer.Channel(7).play(cancion) #reproduzco el sonido de poner la llave
                            cancion = None
                            text_abrir = "Intentas usar una llave en el pomo de la puerta, y ves que esta cede."
                            DM.speak(text_abrir) 
                            to_list = "El jugador acaba de poner una llave en la cerradura de una puerta que se encontraba bloqueada, y la ha girado, y esta se ha abierto"
                            self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
                            #Ejecuto la apertura
                            if(self.Mapa.adyacencias[self.id][sala] == 1):
                            #Es adyacente
                                self.GLOBAL.setActionDoor([3,[pos_x,pos_y]]) #podría abrirla
                                self.pasilloToPuerta = [[pos_x,pos_y],sala]
                                self.read = False
                                self.read4 = False
                            else:
                                self.GLOBAL.setActionDoor([1,[pos_x,pos_y]]) #podría abrirla
                                self.pasilloToPuerta = [[pos_x,pos_y],sala]
                                self.read = False
                                self.read4 = False
                            return False

                        else:
                            #La puerta está cerrada
                            if(not self.read4):
                                print("puerta cerrada")
                                pygame.mixer.Channel(1).play(self.soundDoor)
                                text_closed = self.frases_puerta[self.pasilloFromPuerta[1]][sala][0]
                                DM.speak(text_closed) 
                                to_list = "El jugador ha intentado abrir una puerta, pero estaba cerrada. Esto fue lo que le dijo el Dungeon Master: "+text_closed
                                self.GLOBAL.addElementToListaAndRemoveFirst(to_list)
                                self.read4 = True
                                self.read = False
                                self.GLOBAL.setActionDoor([0,[None,None]]) 
                            return False
                
            if((not self.read) and (10 <= self.Mapa.matrix[pos_y][pos_x] <= 13) and not((self.pasilloToPuerta != None) and (self.GLOBAL.getCrossedDoor()[1] == self.pasilloToPuerta[0]))):
                #Es otra puerta distinta, pero no se puede pasar porque no es del enlace
                pygame.mixer.Channel(1).play(self.soundDoor)
                text = "Parece que algún tipo de magia impide que puedas abrir esta puerta."
                DM.speak(text) 
                to_list = "El jugador ha intentado abrir una puerta, pero parece que algún tipo de magia impidió que la abriera"
                self.GLOBAL.addElementToListaAndRemoveFirst(to_list) 
                self.GLOBAL.setActionDoor([0,[None,None]]) 
                self.read = True
                self.read4 = False
                return False
        else:
            self.read = False
            self.read4 = False

                    # Si ya ha hablado con el NPC y el personaje ha dado click para cruzar la puerta
        if(self.GLOBAL.canGoOutFirst() and (self.pasilloToPuerta != None) and(self.GLOBAL.getCrossedDoor()[1] == self.pasilloToPuerta[0])):
            #Ha decidido cruzarla
            self.GLOBAL.setActionDoor([0,[None,None]])
            self.GLOBAL.setCrossedDoor([[False],[None,None]])
            pygame.mixer.Channel(1).play(self.soundDoor)
            # El texto de la puerta se reproducirá en el estado de destino
            #reseteo las variables
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2 #está en un pasillo
            #Si la puerta estaba originalmente cerrada, o si está abierta, pero desde el otro lado estaba cerrada, se va a abrir:
            # Es un puntero, así que se cambiará en su correspondiente estado
            self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[self.id][1] = "abierto" #guardo cuál es la puerta desde la que entró, y la sala a la que se dirige, para simplificar después las comprobaciones
            currentEstadoByPlayers[str(personaje.name)+","+str(personaje.id_jugador)] = self.idSala_idOrder[self.pasilloFromPuerta[1]]
            self.pasilloFromPuerta = None
            self.pasilloToPuerta = None
            
            return True
        else:
            self.GLOBAL.setActionDoor([0,[None,None]])
            return False
        
        
    def checkIfCompleted(self,personaje):
        #print("check if completed de sala inicial: False")
        return False #Una sala nunca se puede completar. Siempre puedes entrar a ella, si el check del run se cumple
        
    def run(self,DM,personaje,currentEstadoByPlayers):
        #TODO: run en función del estado de la misión
        # print("run:")
        #print(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)])
        if(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 1):
            self.OnEnterEstadoByPlayer(DM,personaje,currentEstadoByPlayers)
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 2):
            if(self.checkIfCanExit(DM,personaje,currentEstadoByPlayers)):
                pass
            else:
                self.runNextInnerEstado(DM,personaje)
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 3):
            print("en el pasillo")
            if(self.checkIfCanEnterAgain(DM,personaje)):
                print("no debería printearse esto")
            else:
                print("otra sala?")
                self.checkIfCanPassToAnotherRoom(DM,personaje,currentEstadoByPlayers)
            print("fuera")
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 4):
            pass
        else:
            pass #si están en 0 no hace nada, hay que esperar a que todos acepten


    def ModifyState(self,player,n):
        self.variableDeCheck["progreso"][str(player.name)+","+str(player.id_jugador)] = n
        #print("modificado a 0 en sala inicial")

    def runNextInnerEstado(self,DM,personaje):
        for id,estado in self.ordenEstados.items(): 
            if(not estado.checkIfCompleted(personaje) and estado.checkIfCanRun(DM,personaje)):
                estado.run(DM,personaje)

    def OnEnterEstadoByPlayer(self,DM,personaje,currentEstadoByPlayers):
        #El mensaje de introducción a la sala, se le reproduce a cada uno de forma individual (por si alguno muriera, y se tuviera que crear otro, que esto ya sea independiente)
        print("<DM>: "+self.dialogoDMIntro) #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        self.GLOBAL.setViewMap(True)
        DM.speak(self.dialogoDMIntro) 
        to_list = "El jugador acaba de llegar a una mazmorra subterránea, y la galería en la que se encuentra, es descrita por el Dungeon Master así: "+self.dialogoDMIntro
        self.GLOBAL.addElementToListaAndRemoveFirst(to_list) 
        #DM.printVoices()
        #TODO: Enviar mensaje TCP
        self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2 #está en la sala normal
        self.GLOBAL.addRoomVisited()
        self.run(DM,personaje,currentEstadoByPlayers)

            
class DM:
    def __init__(self,enabledDMVoice):
        self.enabledDMVoice = enabledDMVoice
        self.engine = pyttsx3.init() #inicializamos el text-to-speech por si estuviera habilitado
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', 150) #velocidad de lectura 
        self.engine.setProperty('volume',1) #para que la ia se escuche por encima de todo
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id) #voz en español
        self.engine.setProperty('language',"es-ES")
        self.GLOBAL = Global()

    def changeEnabledDMVoice(self,enabled):
        self.enabledDMVoice = enabled
    def speak(self,text):
        #cambio de la variable de texto a mostrar en la interfaz
        frases = text.split('.') #dividimos el texo por frases
        words = {}
        index_frase = 0
        l = len(frases)
        for frase in frases:
            words[index_frase] = frase.split(' ')
            if (l != index_frase+1):
                if(words[index_frase][-1] != '?' or words[index_frase][-1] != '!'):
                    words[index_frase] += ['.']
                index_frase+=1
            else:
                break
        printearTextos = {}
        cont = 0
        i = 0
        # 100 palabras a printear como mucho por fragmento
        for frase_index,wordList in words.items():
            if(cont +len(wordList) <= 100):
                cont+= len(wordList)
                for word in wordList:
                    if(printearTextos.get(i) == None):
                        printearTextos[i] = word+" "
                    else:
                        printearTextos[i] += word+" "
            else:
                cont= len(wordList)
                i+=1
                for word in wordList:
                    if(printearTextos.get(i) == None):
                        printearTextos[i] = word+" "
                    else:
                        printearTextos[i] += word+" "

        # Va a empezar a hablar 
        self.GLOBAL.setDMTalking(True)
        for id,printText in printearTextos.items():
            self.GLOBAL.setTextoDM(printText)
            print("establecido texto global DM")
            if(self.enabledDMVoice):
                self.engine.say(printText)
                self.engine.runAndWait()
        self.GLOBAL.setDMTalking(False)
    def printVoices(self):
        voices = self.engine.getProperty('voices')
        for voice in voices:
            print(voice, voice.id)
    def reset(self):
        self.engine = None
    def load(self):
        self.engine = pyttsx3.init()
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', 150) #velocidad de lectura 
        self.engine.setProperty('volume',1) #para que la ia se escuche por encima de todo
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id) #voz en español
        self.engine.setProperty('language',"es-ES")

class Maquina_de_estados:
    def __init__(self,enabledDMVoice,currentPartida,personaje):
        self.enabledDMVoice = enabledDMVoice
        self.ordenEstados = {}
        self.currentEstadoByPlayers = {}
        self.personajeDelHost = personaje
        self.ids = 0
        self.estadosDeMision = {}
        self.numMisionID = 0
        self.idSala_idOrder = {}
        self.salaInicialID = None
        self.GLOBAL = Global()
        self.estadoInicial = None #podríamos querer cargarlo de una bbdd
        self.DM = DM(self.enabledDMVoice) #creo la voz del DM, que se pasará como parámetro al ejecutar los métodos
        self.RAG_musica = Consulta_RAG_musica()
        self.currentPartida = currentPartida
        self.output = Queue()
        #TODO: Cargar estados de un fichero (al terminar)

    def crearEstadoInicial(self,mensajeInicial):
        self.estadoInicial = EstadoInicial(True, mensajeInicial,self.RAG_musica,self.currentPartida,self.ids)
        self.ordenEstados[self.ids] = self.estadoInicial
        self.ids +=1

    def initExecution(self):
        self.currentEstadoByPlayers[str(self.personajeDelHost.name)+","+str(self.personajeDelHost.id_jugador)] = 0
        self.runNextEstado(self.personajeDelHost)
        for personaje in self.GLOBAL.getListaPersonajeHost():
            #TODO:Check si ya estaban en otro estado (partida a medias), si no:
            personaje = personaje[1]
            self.currentEstadoByPlayers[str(personaje.name)+","+str(personaje.id_jugador)] = 0
            #para cada jugador, ejecuta su siguiente estado
            self.runNextEstado(personaje)

    def crearEstadoDeMision(self,numJ,descripcion_fisicaNPC,motivoUbicacion,trasfondoNPC,pathImageNPC):
        self.estadosDeMision[self.numMisionID] = EstadoDeMision(False,None,self.RAG_musica,self.currentPartida,self.estadoInicial,numJ,descripcion_fisicaNPC,motivoUbicacion,trasfondoNPC,self.ids,self.personajeDelHost,pathImageNPC)
        for sala in range(1,len(self.ordenEstados)):
            self.ordenEstados[sala].ordenEstados[self.ordenEstados[sala].ids] = self.estadosDeMision[self.numMisionID] #es la misma referencia de objeto para todas las salas
            self.ordenEstados[sala].ids +=1
        self.numMisionID +=1

    def crearEstadoSala(self,numJ,id_sala,es_obligatoria,esInicial,daASalas,tienePortales,contieneLlaves,esFinal,orden,tipo_mision, size, pos_x, pos_y,Mapa,frase_puerta,descripcion_sala):
        if(esInicial): 
            self.ordenEstados[self.ids] = EstadoDeSalaInicial(False,None,self.RAG_musica,self.currentPartida,self.estadoInicial,numJ,self.ids,self.personajeDelHost,id_sala,es_obligatoria,esInicial,daASalas,tienePortales,contieneLlaves,esFinal,orden,tipo_mision, size, pos_x, pos_y,Mapa,frase_puerta,descripcion_sala,self.idSala_idOrder)
            self.salaInicialID = self.ids
            self.idSala_idOrder[id_sala] = self.ids
            self.ids +=1
        elif(esFinal):
            self.ordenEstados[self.ids] = EstadoDeSalaFinal(False,None,self.RAG_musica,self.currentPartida,self.estadoInicial,numJ,self.ids,self.personajeDelHost,id_sala,es_obligatoria,esInicial,daASalas,tienePortales,contieneLlaves,esFinal,orden,tipo_mision, size, pos_x, pos_y,Mapa,frase_puerta,descripcion_sala,self.idSala_idOrder)
            self.idSala_idOrder[id_sala] = self.ids
            self.ids +=1
        else:
            self.ordenEstados[self.ids] = EstadoDeSalaIntermedia(False,None,self.RAG_musica,self.currentPartida,self.estadoInicial,numJ,self.ids,self.personajeDelHost,id_sala,es_obligatoria,esInicial,daASalas,tienePortales,contieneLlaves,esFinal,orden,tipo_mision, size, pos_x, pos_y,Mapa,frase_puerta,descripcion_sala,self.idSala_idOrder)
            self.idSala_idOrder[id_sala] = self.ids
            self.ids +=1

    def addEstadoRecoleccion(self,id_sala,numJ):
        id = self.idSala_idOrder[id_sala]
        self.ordenEstados[id].ordenEstados[self.ordenEstados[id].ids] = EstadoRecolectAndBreak(False,None,'Recoleccion',False,self.personajeDelHost,numJ,self.ordenEstados[id])
        self.ordenEstados[id].ids +=1
        #Mision 0, Estado 1: Misión específica
    def crearEstadoDeMisionConcreta(self,variableDeCheck,num_mision,dialogo_bienvenida,propuesta_mision,numJ,NPC,tipo_mision,mision,Mapa,textoDM):
        self.estadosDeMision[num_mision].ordenEstados[self.estadosDeMision[num_mision].ids] = EstadoDeHablaNPC(False,dialogo_bienvenida,propuesta_mision,self.estadosDeMision[num_mision].ids,self.personajeDelHost,numJ,self.estadosDeMision[num_mision],NPC,self.currentPartida)
        self.estadosDeMision[num_mision].ids +=1

        #Misión concreta
        self.estadosDeMision[num_mision].ordenEstados[self.estadosDeMision[num_mision].ids] = EstadoDeMisionConcreta(False,None,self.estadosDeMision[num_mision],numJ,self.estadosDeMision[num_mision].ids,tipo_mision,variableDeCheck,mision,Mapa,textoDM)
        self.estadosDeMision[num_mision].ids +=1

    def addCofreToSala(self,sala,desFull,desEmpty,cofre):
        id = self.idSala_idOrder[sala]
        self.ordenEstados[id].addChest(desFull,desEmpty,cofre)


    def runNextEstado(self,personaje):
        inicial = self.ordenEstados[0]
        if(self.ordenEstados[self.currentEstadoByPlayers[str(personaje.name)+","+str(personaje.id_jugador)]] == inicial):
            #si hay un jugador, quiere decir que todos están en ese estado inicial
            if((not inicial.checkIfCompleted(personaje)) and inicial.checkIfCanRun(personaje)):
                inicial.run(self.DM)
                self.currentEstadoByPlayers[str(self.personajeDelHost.name)+","+str(self.personajeDelHost.id_jugador)] = self.salaInicialID
                for player in self.GLOBAL.getListaPersonajeHost():
                    player = player[1]
                    self.currentEstadoByPlayers[str(player.name)+","+str(player.id_jugador)] = 1 #paso a todos al segundo estado
        else:
            if(not mixer.music.get_busy() and not self.GLOBAL.getSearchingSong()):
                # La  música ha parado, y hay que elegir una nueva canción
                texto = "Escogiendo una canción apropiada..."
                self.DM.speak(texto)
                self.GLOBAL.setSearchingSong(True)
                self.RAG_musica.establecerCancionHilo(str(self.GLOBAL.getLista()),self.output)
            elif(self.GLOBAL.getSearchingSong()):
                if not self.output.empty():
                    resultado = self.output.get()
                    if(resultado != False):
                        try:
                            mixer.music.stop()#para la música
                            mixer.music.load('music/'+resultado+".mp3") #carga la nueva canción sugerida por la ia
                            mixer.music.play(0)
                        except:
                            pass
                        finally:
                            self.GLOBAL.setSearchingSong(False)
            estado = self.ordenEstados[self.currentEstadoByPlayers[str(personaje.name)+","+str(personaje.id_jugador)]]
            #print("antes :)")
            if((not estado.checkIfCompleted(personaje)) and estado.checkIfCanRun(self.DM,personaje)):
                #print("running estado de sala")
                estado.run(self.DM,personaje,self.currentEstadoByPlayers) #se hará run del estado de sala en el que esté ese jugador

        #de momento solo hay 1 posible opción, con 1 estado
        # for linea_temporal in self.ordenEstados:
        #     for estado in self.ordenEstados[linea_temporal]:
        #         print(estado)
        #         print(estado.checkIfCompleted())
        #         print(estado.checkIfCanRun())
        #         if(not estado.checkIfCompleted() and estado.checkIfCanRun()): 
        #             #Si el estado no ha sido completado, y se puede ejecutar
        #             #estado.
        #             estado.run(self.DM)
        #             return #para salirte
    def resetGlobalsForPickle(self):
        self.GLOBAL = None
        self.DM.GLOBAL = None
        self.output = None
        self.personajeDelHost = None
        for id,estado in self.ordenEstados.items():
            estado.resetForPickle()
        self.DM.reset()
        for id,estado in self.estadosDeMision.items():
            estado.resetForPickle()
            estado.ordenEstados[0].resetForPickle()
            estado.ordenEstados[1].resetForPickle()
            estado.ordenEstados[0].NPC.GLOBAL = None
            estado.ordenEstados[1].GLOBAL = None
        
    def setForLoad(self,mapa,jugadorHost):
        self.GLOBAL = Global()
        self.DM.GLOBAL = Global()
        self.DM.load()
        self.output = Queue()
        self.enabledDMVoice = self.enabledDMVoice
        self.personajeDelHost = jugadorHost

        #cargo el mapa
        mapa = mapa

        for id,estado in self.ordenEstados.items():
            estado.setForLoad(mapa,jugadorHost)
        for id,estado in self.estadosDeMision.items():
            estado.setForLoad(mapa,jugadorHost)
            estado.ordenEstados[0].setForLoad(mapa,jugadorHost)
            estado.ordenEstados[1].setForLoad(mapa,jugadorHost)
            estado.ordenEstados[0].NPC.GLOBAL = Global()
            estado.ordenEstados[1].GLOBAL = Global()


        
        
    
