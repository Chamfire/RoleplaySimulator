import threading
class Global:
    def __init__(self):
        self.lock_op = threading.Lock() #para gestionar la concurrencia en otherPlayers
        self.lock_cp = threading.Lock() #para currentPlayers
        self.lock_rs = threading.Lock() #para refreshScreen
        self.lock_to = threading.Lock() #para timeout
        self.lock_np = threading.Lock() #para gestionar las salidas de la partida
        self.lock_cs = threading.Lock() #para gestionar la currentScreen
        self.lock_lph = threading.Lock() #para gestionar la lista de personajes en el host
        self.lock_text = threading.Lock() #para gestionar el texto que va a mostrar el DM
        self.lock_image = threading.Lock() #para gestionar la imagen que va a mostrar el DM
        self.lock_openChest = threading.Lock()
        self.lock_canTalk = threading.Lock()
        self.lock_canBreak = threading.Lock()

    def initialize(self):
        global otherPlayers 
        otherPlayers = {}
        global currentPlayers
        currentPlayers = 1
        global refreshScreen
        refreshScreen = None
        global timeout
        timeout = None
        global noEnPartida
        noEnPartida = True
        global currentScreen
        currentScreen = "menu"
        global listaPersonajesHost
        listaPersonajesHost = {}
        global actualPartidaState 
        actualPartidaState = None #por defecto es none
        global tokenDePalabra 
        tokenDePalabra = None
        global texto_DM 
        texto_DM = ""
        global imagenPartida
        imagenPartida = ""
        global canStart
        canStart = False
        global showImage 
        showImage = False
        global imagenPartidaBkg
        imagenPartidaBkg = ""
        global viewMap
        viewMap = False
        global m
        m = None
        global actionDoor
        actionDoor = [0,[None,None]]
        global crossedDoor
        crossedDoor = [[False],[None,None]]
        global canGoOutFirst 
        canGoOutFirst = True #cambiar cuando se haga la parte de diálogo con el NPC
        global DMTalking
        DMTalking = False
        global canTalk
        canTalk = False
        global finishedStart
        finishedStart = False
        global canOpenChest
        canOpenChest = [False,[None,None]]
        global canBreak 
        canBreak = [False,[None,None]]
        global showNombreNPC
        showNombreNPC = ""
        global modoHabla
        modoHabla = False
        global textoMensaje
        textoMensaje = ""
        global lista 
        lista = list()

    def addElementToListaAndRemoveFirst(self,i):
        global lista
        lista.append(i)
        if(len(lista) > 10):
            lista.pop(0)
    
    def getLista(self):
        global lista
        return lista

    def setTextoMensaje(self,v):
        global textoMensaje
        textoMensaje = v

    def getTextoMensaje(self):
        global textoMensaje
        return textoMensaje

    def setModoHabla(self,v):
        global modoHabla
        modoHabla = v

    def getModoHabla(self):
        global modoHabla
        return modoHabla

    def setShowNombreNPC(self,v):
        global showNombreNPC
        showNombreNPC = v

    def getShowNombreNPC(self):
        global showNombreNPC
        return showNombreNPC
    
    def setCanBreak(self,v):
        global canBreak
        self.lock_canBreak.acquire()
        canBreak = v
        self.lock_canBreak.release()

    def getCanBreak(self):
        global canBreak
        return canBreak
    
    def setCanOpenChest(self,v):
        global canOpenChest
        self.lock_openChest.acquire()
        canOpenChest = v
        self.lock_openChest.release()

    def getCanOpenChest(self):
        global canOpenChest
        return canOpenChest

    def setFinishedStart(self,v):
        global finishedStart
        finishedStart = v

    def getFinishedStart(self):
        global finishedStart
        return finishedStart

    def setCanTalkToNPC(self,v):
        global canTalk
        self.lock_canTalk.acquire()
        canTalk = v
        self.lock_canTalk.release()

    def getCanTalkToNPC(self):
        global canTalk
        return canTalk

    def setDMTalking(self,v):
        global DMTalking 
        DMTalking = v

    def getDMTalking(self):
        global DMTalking
        return DMTalking

    
    def canGoOutFirst(self):
        global canGoOutFirst
        return canGoOutFirst
    
    def setCanGoOutFirst(self,v):
        global canGoOutFirst
        canGoOutFirst = v

    def getCrossedDoor(self):
        global crossedDoor
        return crossedDoor
    
    def setCrossedDoor(self,v):
        global crossedDoor
        crossedDoor = v
    
    def getActionDoor(self):
        global actionDoor
        return actionDoor
    
    def setActionDoor(self,v):
        global actionDoor
        actionDoor = v

    def getViewMap(self):
        global viewMap
        return viewMap
    
    def setMAPA(self, m):
        global mapa
        mapa = m
        
    def getMapa(self):
        global mapa
        return mapa
    
    def setViewMap(self,v):
        global viewMap
        viewMap = v

    def getImagePartidaBkg(self):
        global imagenPartidaBkg
        return imagenPartidaBkg
    
    def setImagePartidaBkg(self,v):
        global imagenPartidaBkg 
        imagenPartidaBkg = v

    def setShowImage(self,v):
        global showImage
        showImage = v

    def getShowImage(self):
        global showImage
        return showImage

    def setCanStart(self,v):
        global canStart
        canStart = v

    def getCanStart(self):
        global canStart
        return canStart

    def setImagePartida(self,path):
        global imagenPartida
        self.lock_image.acquire()
        imagenPartida = path
        self.lock_image.release()

    def getImagePartida(self):
        global imagenPartida
        self.lock_image.acquire()
        img = imagenPartida
        imagenPartida = ""
        self.lock_image.release()
        return img

    def setTextoDM(self,texto):
        global texto_DM
        self.lock_text.acquire()
        texto_DM = texto
        self.lock_text.release()
    
    def extractAndRemoveTextoDM(self):
        global texto_DM
        self.lock_text.acquire()
        aux = texto_DM
        texto_DM = "" 
        self.lock_text.release()
        return aux

    def setTokenDePalabra(self,id_usuario):
        global tokenDePalabra
        tokenDePalabra = id_usuario

    def getTokenDePalabra(self):
        global tokenDePalabra
        return tokenDePalabra

    def setActualPartidaState(self,state):
        global actualPartidaState
        actualPartidaState = state

    def getActualPartidaState(self):
        global actualPartidaState
        return actualPartidaState

    def setCurrentScreen(self,s):
        global currentScreen
        self.lock_cs.acquire()
        currentScreen = s
        self.lock_cs.release()

    def setListaPersonajesHost(self,l):
        global listaPersonajesHost
        self.lock_lph.acquire()
        listaPersonajesHost = l
        self.lock_lph.release()

    def getListaPersonajeHost(self):
        global listaPersonajesHost
        return listaPersonajesHost
    
    def setListaPersonajeHostIndex(self,index,personaje):
        global listaPersonajesHost
        self.lock_lph.acquire()
        listaPersonajesHost[index] = personaje
        self.lock_lph.release()

    def getListaPersonajeHostIndex(self,index):
        global listaPersonajesHost
        personaje = listaPersonajesHost.get(index)
        if(personaje != None):
            return personaje
        else:
            return -1

    def getCurrentScreen(self):
        global currentScreen
        return currentScreen
    
    def setOtherPlayers(self,list):
        global otherPlayers
        #print('antes',otherPlayers)
        self.lock_op.acquire()
        otherPlayers = list
        #print('despues',otherPlayers)
        self.lock_op.release()

    def getOtherPlayersTotalRegistered(self):
        global otherPlayers
        cont = 0
        if (otherPlayers != {}):
            for i,player in otherPlayers.items():
                if player != None:
                    cont +=1
        return cont


    def getTimeout(self):
        global timeout
        return timeout
    
    def setEnPartida(self):
        global noEnPartida
        self.lock_np.acquire()
        noEnPartida = False
        self.lock_np.release()

    def getNoEnPartida(self):
        global noEnPartida
        return noEnPartida
    
    def setNoEnPartida(self):
        global noEnPartida
        self.lock_np.acquire()
        noEnPartida = True
        self.lock_np.release()
    
    def setTimeout(self,v):
        global timeout
        self.lock_to.acquire()
        timeout = v
        self.lock_to.release()

    def decreaseTimeout(self):
        global timeout
        self.lock_to.acquire()
        timeout = timeout - 1
        self.lock_to.release()

    def getTimeoutIndex(self,i):
        global timeout
        return timeout[i]
    
    def decreaseTimeoutIndex(self,i):
        global timeout
        self.lock_to.acquire()
        timeout[i] = timeout[i] - 1
        self.lock_to.release()

    def setTimeoutIndex(self,i,v):
        global timeout
        self.lock_to.acquire()
        timeout[i] = v
        self.lock_to.release()

    def setRefreshScreen(self,screenToRefresh):
        global refreshScreen
        self.lock_rs.acquire()
        refreshScreen = screenToRefresh
        self.lock_rs.release()

    def getRefreshScreen(self):
        global refreshScreen
        return refreshScreen

    def setOtherPlayersIndex(self,i,v):
        global otherPlayers
        self.lock_op.acquire()
        otherPlayers[i] = v
        self.lock_op.release()
        #print(otherPlayers)

    def setCurrentPlayers(self,i):
        global currentPlayers
        self.lock_cp.acquire()
        currentPlayers = i
        self.lock_cp.release()

    def getOtherPlayers(self):
        global otherPlayers
        return otherPlayers
    
    def getOtherPlayersIndex(self,i):
        global otherPlayers
        return otherPlayers[i]
    
    def getCurrentPlayers(self):
        global currentPlayers
        return currentPlayers
