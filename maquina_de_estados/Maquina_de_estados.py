import pyttsx3
from RAG_music.Consulta_RAG_musica import Consulta_RAG_musica
import sqlite3
import pygame
import random
from pygame import mixer
from Global import Global
import time

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
    def setForLoad(self,mapa):
        self.GLOBAL = Global()
        self.Mapa = mapa

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
        #TODO: incluir la descripción del mapa
        self.dialogoDMIntro = "En frente de ti, te parece ver a alguien. "+descripcionFisicaNPC+" Te muestro una imagen."
        #TODO: Printear su imagen
        #TODO: Registrarlos en el mapa
        #self.NPCs = #TODO
        #self.mobs = #TODO
        #self.objetos = #TODO

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
            pass
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 2):
            pass
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 3):
            pass
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 4):
            pass

    def ModifyState(self,personaje):
        pass

    def runNextInnerEstado(self,DM,personaje):
        for id,estado in self.ordenEstados.items():
            if(not estado.checkIfCompleted(personaje) and estado.checkIfCanRun(DM,personaje)):
                estado.run(DM,personaje)
                break

    def OnEnterEstadoByPlayer(self,DM,personaje):
        print("<DM>: "+self.dialogoDMIntro) #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        DM.speak(self.dialogoDMIntro) 
        self.GLOBAL.setImagePartida(self.pathImageNPC)
        self.GLOBAL.setShowImage(True)
        #DM.printVoices()
        #TODO: enviar TCP
        self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 0

class EstadoDeHablaNPC(Estado):
    def __init__(self,isInicial,DMintro,DMMision,id,personajeDelHost,numJugadores,estado_pred,NPC):
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

    def checkIfCanRun(self,DM,personaje):
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
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 1):
            self.talkToNPC(DM,personaje)
        elif(self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] == 2):
            self.finishNPCMision(DM,personaje)

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
        print("<DM>: Al acercarte "+msg+" ves que te mira fíjamente, y te dice: "+self.dialogoDMIntro) #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        string_to_speech = "Al acercarte "+msg+" ves que te mira fíjamente, y te dice: "+self.dialogoDMIntro
        DM.speak(string_to_speech) 
        #DM.printVoices()
        #TODO: enviar TCP
        self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 0
        self.run(DM,personaje)

    def talkToNPC(self,DM,personaje):
        #TODO: RAG
        pass

    def finishNPCMision(self,DM,personaje):
        pass

    def giveMissionNPC(self,DM,personaje):
        if(self.NPC.genero == "mujer"):
            pensando = "pensativa"
        else:
            pensando = "pensativo"
        print("<DM>: Tras decirte lo anterior, ves que "+self.NPC.name+" se queda "+pensando+", y continúa diciendote: "+self.dialogoDMMision+" ¿Me ayudarás?") #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        DM.speak("Tras decirte lo anterior, ves que "+self.NPC.name+" se queda "+pensando+", y continúa diciendote: "+self.dialogoDMMision+" ¿Me ayudarás?") 
        #DM.printVoices()
        #TODO: enviar TCP
        self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 1
        self.click[str(personaje.name)+","+str(personaje.id_jugador)] = False

class EstadoDeMisionConcreta(Estado):
    def __init__(self,isInicial,content,estado_pred,numJugadores,id,tipo_mision,variableDeCheck,mision):
        super().__init__(isInicial,content,id)
        self.variableDeCheck["progreso"] = variableDeCheck
        self.esObligatorio = True
        self.numJugadores = numJugadores
        self.esPuntoDeRespawn = False
        self.mision = mision
        self.tipo_de_estado = tipo_mision
        self.estadosSucesores = estado_pred
        self.ids = 0 
        self.currentState = 0 #0 no la tiene aún, 1: la tiene, 2: la ha completado
        self.event_trigged = False
        self.ordenEstados = {} #Estados internos de misión
        self.given = False
        #self.NPCs = #TODO
        #self.mobs = #TODO
        #self.objetos = #TODO

    def checkIfCanRun(self,DM,player):
        if(self.given):
            return True
        else:
            return False
        
    def checkIfCompleted(self,personaje):
        for mob in self.variableDeCheck:
            if(mob[0] != mob[1]):
                return False
        return True
    
    def giveMision(self):
        self.given = True
        
    def run(self,DM,personaje):
        #TODO: run en función del estado de la misión
        if(self.currentState == 0):
            self.OnEnterEstadoByPlayer(DM,personaje)
        elif(self.currentState == 1):
            pass
        elif(self.currentState == 2):
            pass

    def ModifyState(self,personaje,mob_o_lugar = None):
        if(self.tipo_de_estado == "combate"):
            self.variableDeCheck[mob_o_lugar][1] +=1 
        elif(self.tipo_de_estado == "búsqueda"):
            self.variableDeCheck[mob_o_lugar] = True

    def CompleteMision(self):
        self.currentState = 2

    def OnEnterEstadoByPlayer(self,DM,personaje):
        print("Misión a realizar: "+self.mision)
        self.currentState = 1


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
        self.soundDoor = pygame.mixer.Sound('sounds/door.wav')
        self.frases_puerta = frase_puerta
        self.idSala_idOrder = idSala_idOrder

    def checkIfCanRun(self,DM,personaje):
        return self.checkIfCanRunByPlayer(DM,personaje)
    
    def checkIfCanRunByPlayer(self,DM,personaje):
        return True
        

    def checkIfCanExit(self,DM,personaje):
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
            for sala in self.daASalas:
                if(self.daASalas[sala][0] == [pos_x,pos_y]):
                    if(self.daASalas[sala][1] == "abierto"):
                        #La puerta existe y da a la sala "sala", y está abierta para pasar
                        print("puerta")
                        if(self.Mapa.matrix[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] == 23):
                            self.GLOBAL.setActionDoor(2)
                            self.pasilloFromPuerta = [[pos_x,pos_y], sala]
                        else:
                            if(self.Mapa.adyacencias[self.id][sala] == 1):
                                #Es adyacente
                                self.GLOBAL.setActionDoor(3) #podría abrirla
                            else:
                                self.GLOBAL.setActionDoor(1) #podría abrirla
                            self.pasilloFromPuerta = [[pos_x,pos_y], sala]
                        return False
                    else:
                        #La puerta está  cerrada
                        print("puerta cerrada")
                        pygame.mixer.Channel(1).play(self.soundDoor)
                        text_closed = self.frases_puerta[self.id][sala][0]
                        DM.speak(text_closed) 
                        self.GLOBAL.setActionDoor(0) 
                        return False
                
                
                    # Si ya ha hablado con el NPC y el personaje ha dado click para cruzar la puerta
        if(self.GLOBAL.canGoOutFirst() and (self.pasilloFromPuerta != None) and (self.GLOBAL.getCrossedDoor()[1] == self.pasilloFromPuerta[0])):
            #Ha decidido cruzarla
            self.GLOBAL.setActionDoor(0)
            self.GLOBAL.setCrossedDoor([[False],[None,None]])
            pygame.mixer.Channel(1).play(self.soundDoor)
            text_open_door = self.frases_puerta[self.id][self.pasilloFromPuerta[1]][1]
            DM.speak(text_open_door) 
            #reseteo las variables
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 3 #está en un pasillo
            #Si la puerta estaba originalmente cerrada, o si está abierta, pero desde el otro lado estaba cerrada, se va a abrir:
            # Es un puntero, así que se cambiará en su correspondiente estado
            self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[self.id][1] = "abierto"
            self.pasilloFromPuerta = [self.pasilloFromPuerta[0],self.pasilloFromPuerta[1]] #guardo cuál es la puerta desde la que entró, y la sala a la que se dirige, para simplificar después las comprobaciones
            
            return True
        else:
            self.GLOBAL.setActionDoor(0)
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
                    self.GLOBAL.setActionDoor(3) #podría abrirla
                else:
                    self.GLOBAL.setActionDoor(1) #podría abrirla
                return True
                
                    # Si ya ha hablado con el NPC y el personaje ha dado click para cruzar la puerta
        if(self.GLOBAL.canGoOutFirst() and (self.pasilloFromPuerta != None) and (self.GLOBAL.getCrossedDoor()[1] == self.pasilloFromPuerta[0]) and self.checkIfItIsInCurrentRoom(personaje.coordenadas_actuales_r[0],personaje.coordenadas_actuales_r[1])):
            #Ha decidido cruzarla
            self.GLOBAL.setActionDoor(0)
            self.GLOBAL.setCrossedDoor([[False],[None,None]])
            pygame.mixer.Channel(1).play(self.soundDoor)
            text_open_door = self.frases_puerta[self.pasilloFromPuerta[1]][self.id][2]
            self.pasilloFromPuerta = None
            DM.speak(text_open_door) 
            #reseteo las variables
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2 #está en la sala de nuevo
             #guardo cuál es la puerta desde la que entró, y la sala a la que se dirige, para simplificar después las comprobaciones
            # Si trata de entrar después a otra puerta de otro camino que se haya anexado, le dirá que una magia oscura impide que la abra jeje
            return True
        else:
            self.GLOBAL.setActionDoor(0)
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
                            self.GLOBAL.setActionDoor(3) #podría abrirla
                            self.pasilloToPuerta = [[pos_x,pos_y],sala]
                        else:
                            self.GLOBAL.setActionDoor(1) #podría abrirla
                            self.pasilloToPuerta = [[pos_x,pos_y],sala]
                        return False
                    else:
                        #La puerta está cerrada
                        print("puerta cerrada")
                        pygame.mixer.Channel(1).play(self.soundDoor)
                        text_closed = self.frases_puerta[sala][self.id][0]
                        DM.speak(text_closed) 
                        self.GLOBAL.setActionDoor(0) 
                        return False
                
                
                    # Si ya ha hablado con el NPC y el personaje ha dado click para cruzar la puerta
        if(self.GLOBAL.canGoOutFirst() and (self.pasilloToPuerta != None) and (self.GLOBAL.getCrossedDoor()[1] == self.pasilloToPuerta[0])):
            #Ha decidido cruzarla
            self.GLOBAL.setActionDoor(0)
            self.GLOBAL.setCrossedDoor([[False],[None,None]])
            pygame.mixer.Channel(1).play(self.soundDoor)
            # El texto de la puerta se reproducirá en el estado de destino
            #reseteo las variables
            #Si la puerta estaba originalmente cerrada, o si está abierta, pero desde el otro lado estaba cerrada, se va a abrir:
            # Es un puntero, así que se cambiará en su correspondiente estado
            self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[self.id][1] = "abierto" #guardo cuál es la puerta desde la que entró, y la sala a la que se dirige, para simplificar después las comprobaciones
            if(self.Mapa.adyacencias[self.id][self.pasilloFromPuerta[1]] == 1):
                self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2
                currentEstadoByPlayers[str(personaje.name)+","+str(personaje.id_jugador)] = self.idSala_idOrder[self.pasilloFromPuerta[1]]
            else:
                self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 3 #está en un pasillo
                self.pasilloFromPuerta = [self.pasilloFromPuerta[0],self.pasilloFromPuerta[1]] #guardo cuál es la puerta desde la que entró, y la sala a la que se dirige, para simplificar después las comprobaciones
            self.pasilloFromPuerta = None
            self.pasilloToPuerta = None
            
            return True
        else:
            self.GLOBAL.setActionDoor(0)
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
                break

    def OnEnterEstadoByPlayer(self,DM,personaje,currentEstadoByPlayers):
        #El mensaje de introducción a la sala, se le reproduce a cada uno de forma individual (por si alguno muriera, y se tuviera que crear otro, que esto ya sea independiente)
        # print("<DM>: "+self.dialogoDMIntro) #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        # DM.speak(self.dialogoDMIntro) 
        print("Sala "+str(self.id))
        #DM.printVoices()
        #TODO: Enviar mensaje TCP
        self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2 #está en la sala normal
        self.run(DM,personaje,currentEstadoByPlayers)

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
        self.soundDoor = pygame.mixer.Sound('sounds/door.wav')
        self.frases_puerta = frase_puerta
        self.idSala_idOrder = idSala_idOrder


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
            for sala in self.daASalas:
                if(self.daASalas[sala][0] == [pos_x,pos_y]):
                    if(self.daASalas[sala][1] == "abierto"):
                        #La puerta existe y da a la sala "sala", y está abierta para pasar
                        print("puerta")
                        if(self.Mapa.matrix[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] == 23):
                            self.GLOBAL.setActionDoor(2)
                            self.pasilloFromPuerta = [[pos_x,pos_y], sala]
                        else:
                            if(self.Mapa.adyacencias[self.id][sala] == 1):
                                #Es adyacente
                                self.GLOBAL.setActionDoor(3) #podría abrirla
                            else:
                                self.GLOBAL.setActionDoor(1) #podría abrirla
                            self.pasilloFromPuerta = [[pos_x,pos_y], sala]
                        return False
                    else:
                        #La puerta está  cerrada
                        print("puerta cerrada")
                        pygame.mixer.Channel(1).play(self.soundDoor)
                        text_closed = self.frases_puerta[self.id][sala][0]
                        DM.speak(text_closed) 
                        self.GLOBAL.setActionDoor(0) 
                        return False
                
                
                    # Si ya ha hablado con el NPC y el personaje ha dado click para cruzar la puerta
        if(self.GLOBAL.canGoOutFirst() and (self.pasilloFromPuerta != None) and (self.GLOBAL.getCrossedDoor()[1] == self.pasilloFromPuerta[0])):
            #Ha decidido cruzarla
            self.GLOBAL.setActionDoor(0)
            self.GLOBAL.setCrossedDoor([[False],[None,None]])
            pygame.mixer.Channel(1).play(self.soundDoor)
            text_open_door = self.frases_puerta[self.id][self.pasilloFromPuerta[1]][1]
            DM.speak(text_open_door) 
            #reseteo las variables
            #Si la puerta estaba originalmente cerrada, o si está abierta, pero desde el otro lado estaba cerrada, se va a abrir:
            # Es un puntero, así que se cambiará en su correspondiente estado
            self.Mapa.salas[self.pasilloFromPuerta[1]].daASalas[self.id][1] = "abierto"
            if(self.Mapa.adyacencias[self.id][self.pasilloFromPuerta[1]] == 1):
                self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2
                currentEstado[str(personaje.name)+","+str(personaje.id_jugador)] = self.idSala_idOrder[self.pasilloFromPuerta[1]]
            else:
                self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 3 #está en un pasillo
                self.pasilloFromPuerta = [self.pasilloFromPuerta[0],self.pasilloFromPuerta[1]] #guardo cuál es la puerta desde la que entró, y la sala a la que se dirige, para simplificar después las comprobaciones
            
            return True
        else:
            self.GLOBAL.setActionDoor(0)
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
                    self.GLOBAL.setActionDoor(3) #podría abrirla
                else:
                    self.GLOBAL.setActionDoor(1) #podría abrirla
                return True
                
                    # Si ya ha hablado con el NPC y el personaje ha dado click para cruzar la puerta
        if(self.GLOBAL.canGoOutFirst() and (self.pasilloFromPuerta != None) and (self.GLOBAL.getCrossedDoor()[1] == self.pasilloFromPuerta[0]) and self.checkIfItIsInCurrentRoom(personaje.coordenadas_actuales_r[0],personaje.coordenadas_actuales_r[1])):
            #Ha decidido cruzarla
            self.GLOBAL.setActionDoor(0)
            self.GLOBAL.setCrossedDoor([[False],[None,None]])
            pygame.mixer.Channel(1).play(self.soundDoor)
            text_open_door = self.frases_puerta[self.pasilloFromPuerta[1]][self.id][2]
            self.pasilloFromPuerta = None
            DM.speak(text_open_door) 
            #reseteo las variables
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2 #está en la sala de nuevo
             #guardo cuál es la puerta desde la que entró, y la sala a la que se dirige, para simplificar después las comprobaciones
            # Si trata de entrar después a otra puerta de otro camino que se haya anexado, le dirá que una magia oscura impide que la abra jeje
            return True
        else:
            self.GLOBAL.setActionDoor(0)
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
                            self.GLOBAL.setActionDoor(3) #podría abrirla
                            self.pasilloToPuerta = [[pos_x,pos_y],sala]
                        else:
                            self.GLOBAL.setActionDoor(1) #podría abrirla
                            self.pasilloToPuerta = [[pos_x,pos_y],sala]
                        return False
                    else:
                        #La puerta está cerrada
                        print("puerta cerrada")
                        pygame.mixer.Channel(1).play(self.soundDoor)
                        text_closed = self.frases_puerta[sala][self.id][0]
                        DM.speak(text_closed) 
                        self.GLOBAL.setActionDoor(0) 
                        return False
                
                
                    # Si ya ha hablado con el NPC y el personaje ha dado click para cruzar la puerta
        if(self.GLOBAL.canGoOutFirst() and (self.pasilloToPuerta != None) and (self.GLOBAL.getCrossedDoor()[1] == self.pasilloToPuerta[0])):
            #Ha decidido cruzarla
            self.GLOBAL.setActionDoor(0)
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
            self.GLOBAL.setActionDoor(0)
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
                break

    def OnEnterEstadoByPlayer(self,DM,personaje,currentEstadoByPlayers):
        #El mensaje de introducción a la sala, se le reproduce a cada uno de forma individual (por si alguno muriera, y se tuviera que crear otro, que esto ya sea independiente)
        print("<DM>: "+self.dialogoDMIntro) #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        DM.speak(self.dialogoDMIntro) 
        print("Sala "+str(self.id))
        #DM.printVoices()

        self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2 #está en la sala normal
        self.run(DM,personaje,currentEstadoByPlayers)



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
        self.Mapa = Mapa
        self.soundDoor = pygame.mixer.Sound('sounds/door.wav')
        self.frases_puerta = frase_puerta
        self.pasilloToPuerta = None
        self.idSala_idOrder = idSala_idOrder


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
            for sala in self.daASalas:
                print(self.daASalas[sala][0])
                
                if(self.daASalas[sala][0] == [pos_x,pos_y]):
                    if(self.daASalas[sala][1] == "abierto"):
                        #La puerta existe y da a la sala "sala", y está abierta para pasar
                        print("puerta")
                        if(self.Mapa.matrix[personaje.coordenadas_actuales_r[1]-1][personaje.coordenadas_actuales_r[0]] == 23):
                            self.GLOBAL.setActionDoor(2)
                            self.pasilloFromPuerta = [[pos_x,pos_y], sala]
                        else:
                            if(self.Mapa.adyacencias[self.id][sala] == 1):
                                #Es adyacente
                                print("sala adyacente")
                                self.GLOBAL.setActionDoor(3) #podría abrirla
                            else:
                                print("sala normal")
                                self.GLOBAL.setActionDoor(1) #podría abrirla
                            self.pasilloFromPuerta = [[pos_x,pos_y], sala]
                        return False
                    else:
                        #La puerta está  cerrada
                        print("puerta cerrada")
                        pygame.mixer.Channel(1).play(self.soundDoor)
                        text_closed = self.frases_puerta[self.id][sala][0]
                        DM.speak(text_closed) 
                        self.GLOBAL.setActionDoor(0) 
                        return False
                
                
                    # Si ya ha hablado con el NPC y el personaje ha dado click para cruzar la puerta
        print(self.GLOBAL.canGoOutFirst())
        print(self.GLOBAL.getCrossedDoor())
        if(self.GLOBAL.canGoOutFirst() and (self.pasilloFromPuerta != None) and(self.GLOBAL.getCrossedDoor()[1] == self.pasilloFromPuerta[0])):
            #Ha decidido cruzarla
            print("aquí")
            self.GLOBAL.setActionDoor(0)
            pygame.mixer.Channel(1).play(self.soundDoor)
            self.GLOBAL.setCrossedDoor([[False],[None,None]])
            text_open_door = self.frases_puerta[self.id][self.pasilloFromPuerta[1]][1]
            DM.speak(text_open_door) 
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
            self.GLOBAL.setActionDoor(0)
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
                    self.GLOBAL.setActionDoor(3) #podría abrirla
                else:
                    self.GLOBAL.setActionDoor(1) #podría abrirla
                return True
                
                    # Si ya ha hablado con el NPC y el personaje ha dado click para cruzar la puerta
        print("aquí 1")
        if(self.GLOBAL.canGoOutFirst() and (self.pasilloFromPuerta != None) and(self.GLOBAL.getCrossedDoor()[1] == self.pasilloFromPuerta[0]) and self.checkIfItIsInCurrentRoom(personaje.coordenadas_actuales_r[0],personaje.coordenadas_actuales_r[1])):
            #Ha decidido cruzarla
            self.GLOBAL.setActionDoor(0)
            self.GLOBAL.setCrossedDoor([[False],[None,None]])
            pygame.mixer.Channel(1).play(self.soundDoor)
            text_open_door = self.frases_puerta[self.pasilloFromPuerta[1]][self.id][2]
            self.pasilloFromPuerta = None
            DM.speak(text_open_door) 
            #reseteo las variables
            self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2 #está en la sala de nuevo
             #guardo cuál es la puerta desde la que entró, y la sala a la que se dirige, para simplificar después las comprobaciones
            # Si trata de entrar después a otra puerta de otro camino que se haya anexado, le dirá que una magia oscura impide que la abra jeje
            print("True")
            return True
        else:
            self.GLOBAL.setActionDoor(0)
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
                            self.GLOBAL.setActionDoor(3) #podría abrirla
                            self.pasilloToPuerta = [[pos_x,pos_y],sala]
                        else:
                            self.GLOBAL.setActionDoor(1) #podría abrirla
                            self.pasilloToPuerta = [[pos_x,pos_y],sala]
                        return False
                    else:
                        #La puerta está cerrada
                        print("puerta cerrada")
                        pygame.mixer.Channel(1).play(self.soundDoor)
                        text_closed = self.frases_puerta[sala][self.id][0]
                        DM.speak(text_closed) 
                        self.GLOBAL.setActionDoor(0) 
                        return False
                
                
                    # Si ya ha hablado con el NPC y el personaje ha dado click para cruzar la puerta
        if(self.GLOBAL.canGoOutFirst() and (self.pasilloToPuerta != None) and(self.GLOBAL.getCrossedDoor()[1] == self.pasilloToPuerta[0])):
            #Ha decidido cruzarla
            self.GLOBAL.setActionDoor(0)
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
            self.GLOBAL.setActionDoor(0)
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
                break

    def OnEnterEstadoByPlayer(self,DM,personaje,currentEstadoByPlayers):
        #El mensaje de introducción a la sala, se le reproduce a cada uno de forma individual (por si alguno muriera, y se tuviera que crear otro, que esto ya sea independiente)
        print("<DM>: "+self.dialogoDMIntro) #al mostrarlo por pantalla se añade DM para que no aparezca en el diálogo del text-to-speech
        self.GLOBAL.setViewMap(True)
        DM.speak(self.dialogoDMIntro) 
        #DM.printVoices()
        #TODO: Enviar mensaje TCP
        self.variableDeCheck["progreso"][str(personaje.name)+","+str(personaje.id_jugador)] = 2 #está en la sala normal
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
        self.GLOBAL.setTextoDM(text)
        print("establecido texto global DM")
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
        self.estadosDeMision = {}
        self.numMisionID = 0
        self.idSala_idOrder = {}
        self.salaInicialID = None
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

        #Mision 0, Estado 1: Misión específica
    def crearEstadoDeMisionConcreta(self,variableDeCheck,num_mision,dialogo_bienvenida,propuesta_mision,numJ,NPC,tipo_mision,mision):
        self.estadosDeMision[num_mision].ordenEstados[self.estadosDeMision[num_mision].ids] = EstadoDeHablaNPC(False,dialogo_bienvenida,propuesta_mision,self.estadosDeMision[num_mision].ids,self.personajeDelHost,numJ,self.estadosDeMision[num_mision],NPC)
        self.estadosDeMision[num_mision].ids +=1

        #Misión concreta
        self.estadosDeMision[num_mision].ordenEstados[self.estadosDeMision[num_mision].ids] = EstadoDeMisionConcreta(False,None,self.estadosDeMision[num_mision],numJ,self.estadosDeMision[num_mision].ids,tipo_mision,variableDeCheck,mision)
        self.estadosDeMision[num_mision].ids +=1


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
        for id,estado in self.ordenEstados.items():
            estado.resetForPickle()
        
        
    def setForLoad(self,mapa):
        self.GLOBAL = Global()
        self.DM.GLOBAL = Global()

        #cargo el mapa
        mapa = mapa

        for id,estado in self.ordenEstados.items():
            estado.setForLoad(mapa)


        
        
    
