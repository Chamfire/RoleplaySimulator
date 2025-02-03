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

    def setOtherPlayers(self,list):
        global otherPlayers
        print('antes',otherPlayers)
        otherPlayers = list
        print('despues',otherPlayers)

    def setRefreshScreen(self,screenToRefresh):
        global refreshScreen
        refreshScreen = screenToRefresh

    def getRefreshScreen(self):
        global refreshScreen
        return refreshScreen

    def setOtherPlayersIndex(self,i,v):
        global otherPlayers
        print(otherPlayers)
        otherPlayers[i] = v

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
