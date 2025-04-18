from Global import Global
import pyttsx3
from RAG_music.Consulta_RAG_musica import Consulta_RAG_musica
import sqlite3
import pygame
import random
from pygame import mixer

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
        mixer.music.play(-1)

        print("<DM>: "+self.dialogoDMIntro) #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        DM.speak(self.dialogoDMIntro) 
        #DM.printVoices()
        self.variableDeCheck["progreso"] = True
        

class EstadoDeMision(Estado):
    def __init__(self,isInicial,content,RAG_musica,currentPartida,estado_pred,numJugadores,descripcionFisicaNPC,motivoUbicacion, trasfondoNPC,id,personajeDelHost):
        super().__init__(isInicial,content,id)
        self.variableDeCheck["progreso"] = {}
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
        #TODO: incluir la descripción del mapa
        self.dialogoDMIntro = "En frente de ti, te parece ver a alguien. "+descripcionFisicaNPC+". Te muestro una imagen."
        #TODO: Printear su imagen
        #TODO: Registrarlos en el mapa
        #self.NPCs = #TODO
        #self.mobs = #TODO
        #self.objetos = #TODO

    def checkIfCanRun(self,player):
        return True #no tiene ningún requisito de acceso
        
    def checkIfCompleted(self,personaje):
        if(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 4):
            return True
        else:
            return False
        
    def run(self,DM,personaje):
        #TODO: run en función del estado de la misión
        if(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == -1):
            self.OnEnterEstadoByPlayer(DM)
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 0):
            pass
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 1):
            pass
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 2):
            pass
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 3):
            pass
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 4):
            pass

    def ModifyState(self,personaje):
        pass

    def runNextInnerEstado(self):
        pass

    def OnEnterEstadoByPlayer(self,DM,personaje):
        print("<DM>: "+self.dialogoDMIntro) #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        DM.speak(self.dialogoDMIntro) 
        #DM.printVoices()
        #TODO: enviar TCP
        self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 0

class EstadoDeSalaInicial(Estado):
    def __init__(self,isInicial,content,RAG_musica,currentPartida,estado_pred,numJugadores,id,personajeDelHost):
        super().__init__(isInicial,content,id)
        self.personajeDelHost = personajeDelHost
        self.variableDeCheck["progreso"] = {}
        self.variableDeCheck["progreso"][str(self.personajeDelHost.name)+","+str(self.personajeDelHost.id_jugador)] = -1
        for personaje in self.GLOBAL.getListaPersonajeHost():
            personaje = personaje[1]
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = -1 #-1: No ha aceptado entrar aún, 0: No ha entrado ese personaje en la sala, 1: ha entrado y está por primera vez en la sala, 2: continúa en la sala normal, 3: ya no está en la sala, pero entró


        self.esObligatorio = True
        self.numJugadores = numJugadores
        self.tipo_de_estado = "sala_grande"
        self.esPuntoDeRespawn = True
        self.estadosSucesores = estado_pred
        self.ids = 0
        self.ordenEstados = {} #Estados contenidos por la sala
        self.numAccepts = 0 
        #TODO: incluir la descripción del mapa
        self.dialogoDMIntro = "¡Bien! Te encuentras en ..."
        #TODO: Printear su imagen
        #TODO: Registrarlos en el mapa
        #self.NPCs = #TODO
        #self.mobs = #TODO
        #self.objetos = #TODO

    def checkIfCanRun(self,personaje):
        print(self.numAccepts)
        print(self.numJugadores)
        print("------------------------")
        if self.numAccepts != self.numJugadores:
            return self.checkIfCanRunFirst(personaje)
        else:
            return self.checkIfCanRunByPlayer(personaje)

    def checkIfCanRunFirst(self,personaje):
        if(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 0):
            self.numAccepts +=1
        
        #Si todos han aceptado
        print("check if can run first sala inicial:")
        print(self.numAccepts)
        print(self.numJugadores)
        if self.numAccepts == self.numJugadores:
            self.variableDeCheck["progreso"][str(self.personajeDelHost.name)+","+str(self.personajeDelHost.id_jugador)] = 1 
            for personaje in self.GLOBAL.getListaPersonajeHost():
                self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 1 #los llevo a la sala de inicio
            print("variable de check a 1")
            return True
        else:
            return False
    
    def checkIfCanRunByPlayer(self,personaje):
        print("en run by player")
        if(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 2):
            #Si está ya en la sala, y ha ejecutado la descripción inicial
            return True
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 3):
            return self.checkIfCanEnterAgain(personaje)
        
        
    def checkIfCanEnterAgain(self,personaje):
        pass
        
    def checkIfCompleted(self,personaje):
        print("check if completed de sala inicial: False")
        return False #Una sala nunca se puede completar. Siempre puedes entrar a ella, si el check del run se cumple
        
    def run(self,DM,personaje):
        #TODO: run en función del estado de la misión
        print("run:")
        print(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)])
        if(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 1):
            self.OnEnterEstadoByPlayer(DM,personaje)
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 2):
            self.runNextInnerEstado(DM,personaje)
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 3):
            pass
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 4):
            pass
        else:
            pass #si están en 0 no hace nada, hay que esperar a que todos acepten


    def ModifyState(self,player,n):
        self.variableDeCheck["progreso"][str(player.name)+","+str(player.id_jugador)] = n
        print("modificado a 0 en sala inicial")

    def runNextInnerEstado(self,DM,personaje):
        for id,estado in self.ordenEstados.items():
            if(not estado.checkIfCompleted(personaje) and estado.checkIfCanRun(personaje)):
                estado.run(self.DM,personaje)
                #que se ejecuten todos los que se puedan ejecutar

    def OnEnterEstadoByPlayer(self,DM,personaje):
        #El mensaje de introducción a la sala, se le reproduce a cada uno de forma individual (por si alguno muriera, y se tuviera que crear otro, que esto ya sea independiente)
        print("<DM>: "+self.dialogoDMIntro) #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        DM.speak(self.dialogoDMIntro) 
        #DM.printVoices()
        #TODO: Enviar mensaje TCP
        self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2 #está en la sala normal

            
class DM:
    def __init__(self,enabledDMVoice):
        self.enabledDMVoice = enabledDMVoice
        self.engine = pyttsx3.init() #inicializamos el text-to-speech por si estuviera habilitado
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', 150) #velocidad de lectura x1
        self.engine.setProperty('volume',1) #para que la ia se escuche por encima de todo
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id) #voz en español
        self.engine.setProperty('language',"es-ES")

    def changeEnabledDMVoice(self,enabled):
        self.enabledDMVoice = enabled
    def speak(self,text):
        if(self.enabledDMVoice):
            self.engine.say(text)
            self.engine.runAndWait()
    def printVoices(self):
        voices = self.engine.getProperty('voices')
        for voice in voices:
            print(voice, voice.id)

class Maquina_de_estados:
    def __init__(self,enabledDMVoice,currentPartida,personaje):
        self.enabledDMVoice = enabledDMVoice
        self.ordenEstados = {}
        self.currentEstadoByPlayers = {}
        self.personajeDelHost = personaje
        self.ids = 0
        self.GLOBAL = Global()
        self.estadoInicial = None #podríamos querer cargarlo de una bbdd
        self.DM = DM(self.enabledDMVoice) #creo la voz del DM, que se pasará como parámetro al ejecutar los métodos
        self.RAG_musica = Consulta_RAG_musica()
        self.currentPartida = currentPartida
        #TODO: Cargar estados de un fichero (al terminar)

    def crearEstadoInicial(self,mensajeInicial):
        self.estadoInicial = EstadoInicial(True, mensajeInicial,self.RAG_musica,self.currentPartida,self.ids)
        self.ordenEstados[self.ids] = self.estadoInicial
        self.ids +=1

    def initExecution(self):
        self.currentEstadoByPlayers[str(self.personajeDelHost.name)+","+str(self.personajeDelHost.id_jugador)] = self.estadoInicial
        self.runNextEstado(self.personajeDelHost)
        for personaje in self.GLOBAL.getListaPersonajeHost():
            #TODO:Check si ya estaban en otro estado (partida a medias), si no:
            personaje = personaje[1]
            self.currentEstadoByPlayers[str(personaje.name)+","+str(personaje.id_jugador)] = self.estadoInicial
            #para cada jugador, ejecuta su siguiente estado
            self.runNextEstado(personaje)

    def crearEstadoDeMision(self,numJ,descripcion_fisicaNPC,motivoUbicacion,trasfondoNPC):
        estado_mision = EstadoDeMision(False,None,self.RAG_musica,self.currentPartida,self.estadoInicial,numJ,descripcion_fisicaNPC,motivoUbicacion,trasfondoNPC,self.ids,self.personajeDelHost)
        for sala in range(1,len(self.ordenEstados)-1):
            self.ordenEstados[sala].ordenEstados[self.ordenEstados[sala].ids] = estado_mision #es la misma referencia de objeto para todas las salas
            self.ordenEstados[sala].ids +=1

    def crearEstadoSala(self,numJ):
        self.ordenEstados[self.ids] = EstadoDeSalaInicial(False,None,self.RAG_musica,self.currentPartida,self.estadoInicial,numJ,self.ids,self.personajeDelHost)
        self.ids +=1


    def runNextEstado(self,personaje):
        inicial = self.ordenEstados[0]
        if(self.currentEstadoByPlayers[str(personaje.name)+","+str(personaje.id_jugador)] == inicial):
            #si hay un jugador, quiere decir que todos están en ese estado inicial
            if((not inicial.checkIfCompleted(personaje)) and inicial.checkIfCanRun(personaje)):
                inicial.run(self.DM)
                self.currentEstadoByPlayers[str(self.personajeDelHost.name)+","+str(self.personajeDelHost.id_jugador)] = self.ordenEstados[1]
                for player in self.GLOBAL.getListaPersonajeHost():
                    player = player[1]
                    self.currentEstadoByPlayers[str(player.name)+","+str(player.id_jugador)] = self.ordenEstados[1] #paso a todos al segundo estado
        else:
            estado = self.currentEstadoByPlayers[str(personaje.name)+","+str(personaje.id_jugador)]
            print("antes :)")
            if((not estado.checkIfCompleted(personaje)) and estado.checkIfCanRun(personaje)):
                print("running estado de sala")
                estado.run(self.DM,personaje) #se hará run del estado de sala en el que esté ese jugador

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
        
        
    
