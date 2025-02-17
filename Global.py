import threading
class Global:
    def __init__(self):
        self.lock_op = threading.Lock() #para gestionar la concurrencia en otherPlayers
        self.lock_cp = threading.Lock() #para currentPlayers
        self.lock_rs = threading.Lock() #para refreshScreen
        self.lock_to = threading.Lock() #para timeout
        self.lock_np = threading.Lock() #para gestionar las salidas de la partida
        self.lock_cs = threading.Lock() #para gestionar la currentScreen

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

    def setCurrentScreen(self,s):
        global currentScreen
        currentScreen = s

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
