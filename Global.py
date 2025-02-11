class Global:
    def __init__(self):
        pass
    def initialize(self):
        global otherPlayers 
        otherPlayers = {}
        global currentPlayers
        currentPlayers = 1
        global refreshScreen
        refreshScreen = None
        global timeout
        timeout = None

    def setOtherPlayers(self,list):
        global otherPlayers
        #print('antes',otherPlayers)
        otherPlayers = list
        #print('despues',otherPlayers)

    def getTimeout(self):
        global timeout
        return timeout
    
    def setTimeout(self,v):
        global timeout
        timeout = v

    def decreaseTimeout(self):
        global timeout
        timeout = timeout - 1

    def getTimeoutIndex(self,i):
        global timeout
        return timeout[i]
    
    def decreaseTimeoutIndex(self,i):
        global timeout
        timeout[i] = timeout[i] - 1

    def setTimeoutIndex(self,i,v):
        global timeout
        timeout[i] = v

    def setRefreshScreen(self,screenToRefresh):
        global refreshScreen
        refreshScreen = screenToRefresh

    def getRefreshScreen(self):
        global refreshScreen
        return refreshScreen

    def setOtherPlayersIndex(self,i,v):
        global otherPlayers
        otherPlayers[i] = v
        #print(otherPlayers)

    def setCurrentPlayers(self,i):
        global currentPlayers
        currentPlayers = i

    def getOtherPlayers(self):
        global otherPlayers
        return otherPlayers
    
    def getOtherPlayersIndex(self,i):
        global otherPlayers
        return otherPlayers[i]
    
    def getCurrentPlayers(self):
        global currentPlayers
        return currentPlayers
