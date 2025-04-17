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

    def checkIfCanRun(self):
        pass

    def checkIfCompleted(self):
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

    def checkIfCanRun(self):
        return True

    def checkIfCompleted(self):
        if(self.variableDeCheck["progreso"] == True):
            return True
        else:
            return False
    def run(self,DM):
        self.OnEnterEstadoByAllPlayers(DM)

    def OnEnterEstadoByAllPlayers(self,DM):
        #self.GLOBAL.setRefreshScreen() #refrescar la pantalla con el mapa que crearé después
        #TODO: mapa inicial e interfaz gráfica
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
    def __init__(self,isInicial,content,RAG_musica,currentPartida,estado_pred,numJugadores,descripcionFisicaNPC,motivoUbicacion, trasfondoNPC,id):
        super().__init__(isInicial,content,id)
        self.variableDeCheck["progreso"] = 0 #0: No se ha leído la introducción al mundo, 1: se ha leído la introducción y la descripción del NPC, 2: se ha dado ya la misión, 3:se ha desencadenado la misión, 4: se ha completado la misión
        self.esObligatorio = True
        self.numJugadores = numJugadores
        self.esPuntoDeRespawn = False
        self.estadosSucesores = estado_pred
        self.numInt = 0
        self.ordenEstados = {} #Estados internos de misión
        self.numAccepts = 0 
        #TODO: incluir la descripción del mapa
        self.dialogoDMIntro = "¡Bien! Os encontráis en ... y frente a vosotros, os parece ver a alguien. "+descripcionFisicaNPC+". Os muestro una imagen."
        #TODO: Printear su imagen
        #TODO: Registrarlos en el mapa
        #self.NPCs = #TODO
        #self.mobs = #TODO
        #self.objetos = #TODO

    def checkIfCanRun(self):
        if(self.numAccepts == self.numJugadores):
            return True
        else:
            return False
        
    def checkIfCompleted(self):
        if(self.variableDeCheck["progreso"] == 4):
            return True
        else:
            return False
        
    def run(self,DM):
        #TODO: run en función del estado de la misión
        if(self.variableDeCheck["progreso"] == 0):
            self.OnEnterEstadoByAllPlayers(DM)
        elif(self.variableDeCheck["progreso"] == 1):
            pass
        elif(self.variableDeCheck["progreso"] == 2):
            pass
        elif(self.variableDeCheck["progreso"] == 3):
            pass
        elif(self.variableDeCheck["progreso"] == 4):
            pass

    def ModifyVarEnter(self,n):
        self.numAccepts = n

    def ModifyState(self):
        if(self.variableDeCheck == 3):
            self.variableDeCheck = 4
            #TODO: diálogos de fin
            #self.OnExitEstadoByPlayers()
        self.variableDeCheck  +=1

    def runNextEstado(self):
        pass

    def OnEnterEstadoByAllPlayers(self,DM):
        print("<DM>: "+self.dialogoDMIntro) #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        DM.speak(self.dialogoDMIntro) 
        #DM.printVoices()
        self.variableDeCheck["progreso"] = 1

            
class DM:
    def __init__(self,enabledDMVoice):
        self.enabledDMVoice = enabledDMVoice
        self.engine = pyttsx3.init() #inicializamos el text-to-speech por si estuviera habilitado
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', 150) #velocidad de lectura x1
        self.engine.setProperty('volume',1.5) #para que la ia se escuche por encima de todo
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
    def __init__(self,enabledDMVoice,currentPartida):
        self.enabledDMVoice = enabledDMVoice
        self.ordenEstados = {}
        self.ids = 0
        self.estadoInicial = None #podríamos querer cargarlo de una bbdd
        self.DM = DM(self.enabledDMVoice) #creo la voz del DM, que se pasará como parámetro al ejecutar los métodos
        self.RAG_musica = Consulta_RAG_musica()
        self.currentPartida = currentPartida
        #TODO: Cargar estados de un fichero (al terminar)

    def crearEstadoInicial(self,mensajeInicial):
        self.estadoInicial = EstadoInicial(True, mensajeInicial,self.RAG_musica,self.currentPartida,self.ids)
        self.ids +=1
        self.ordenEstados[0] = [self.estadoInicial]
    def initExecution(self):
        self.runNextEstado()
    def crearEstadoDeMision(self,numJ,descripcion_fisicaNPC,motivoUbicacion,trasfondoNPC):
        #TODO: Cambiar None, por la descripción del mapa donde se encuentran los jugadores, la temperatura, etc
        self.ordenEstados[0] += [EstadoDeMision(False,None,self.RAG_musica,self.currentPartida,self.estadoInicial,numJ,descripcion_fisicaNPC,motivoUbicacion,trasfondoNPC,self.ids)]
        self.ids +=1
        self.estadoInicial.estadosSucesores[0] = self.ordenEstados[0][1] #añado el estado de misión

    def runNextEstado(self):
        #de momento solo hay 1 posible opción, con 1 estado
        for linea_temporal in self.ordenEstados:
            for estado in self.ordenEstados[linea_temporal]:
                print(estado)
                print(estado.checkIfCompleted())
                print(estado.checkIfCanRun())
                if(not estado.checkIfCompleted() and estado.checkIfCanRun()): 
                    #Si el estado no ha sido completado, y se puede ejecutar
                    #estado.
                    estado.run(self.DM)
                    return #para salirte
        
        
    
