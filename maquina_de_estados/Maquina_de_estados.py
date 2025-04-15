from Global import Global
import pyttsx3
from RAG_music.Consulta_RAG_musica import Consulta_RAG_musica
import sqlite3
import pygame
from pygame import mixer

class Estado:
    def __init__(self,isInicial,content):
        if(isInicial):
            self.esInicial = True
            self.esPuntoDeRespawn = False
            self.tipo_de_estado = "Introducción"
            self.esObligatorio = True
            self.cancion = None #por definir con el RAG
            self.variableDeCheck = {"leido": False}
            self.dialogoDMIntro = content #mensaje que dirá el DM al iniciar el estado
            self.dialogoDMExit = None
        else:
            self.esInicial = False
            self.esPuntoDeRespawn = None
            self.tipo_de_estado = None
            self.esObligatorio = None
            self.cancion = None
            self.variableDeCheck = {}
        self.GLOBAL = Global()
        self.estadoAlQuePertenezco = None
        self.estadoPredecesor = None
        self.NPCs = {}
        self.jugadores = {}
        self.mobs = {}
        self.objetos = {}

    def OnEnterEstadoByPlayer(self,player,DM):
        pass
    def OnExitEstadoByPlayer(self,player,DM):
        pass
    def OnEnterEstadoByAllPlayers(self,DM):
        pass
    def OnExitEstadoByPlayers(self,DM):
        pass

class EstadoInicial(Estado):
    def __init__(self,isInicial,content,RAG_musica,currentPartida):
        super().__init__(isInicial,content)

        #extraemos la ubicación desde la bbdd
        conn = sqlite3.connect("simuladordnd.db")
        cur = conn.cursor()
        #cargamos la partida 1, si existe: el orden de las columnas será ese
        cur.execute("SELECT ubicacion_historia FROM partida WHERE numPartida = '"+currentPartida+"'")
        rows = cur.fetchall() #para llegar a esta pantalla, la pantalla tiene que existir sí o sí
        if(rows[0] != None):
            ubicacion = rows[0][0]

        canciones = RAG_musica.consultar_cancion("¿Cuál es la mejor o mejores canciones para reproducir cuando el DM está dando la introducción para la aventura, y los jugadores empiezan desde "+ubicacion+"?")
        try:
            canciones_list = canciones.split("\n")
            self.cancion = canciones_list[0] #Tomamos la primera de las canciones -> Mejor coincidencia
        except Exception as e:
            print(e)
            print(canciones)

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
        self.variableDeCheck["leido"] = True

            
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
        self.estadoInicial = None #podríamos querer cargarlo de una bbdd
        self.DM = DM(self.enabledDMVoice) #creo la voz del DM, que se pasará como parámetro al ejecutar los métodos
        self.RAG_musica = Consulta_RAG_musica()
        self.currentPartida = currentPartida
        #TODO: Cargar estados de un fichero (al terminar)


    def crearEstadoInicial(self,mensajeInicial):
        self.estadoInicial = EstadoInicial(True, mensajeInicial,self.RAG_musica,self.currentPartida)
    def initExecution(self):
        self.estadoInicial.OnEnterEstadoByAllPlayers(self.DM)
        
        
    
