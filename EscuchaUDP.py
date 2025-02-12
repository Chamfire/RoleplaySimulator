import socket
from Global import Global

class EscuchaUDP:
    def __init__(self):
        self.GLOBAL = Global()
        self.server_socketUDP = None
        self.ip = None
        self.puertoUDP = None

    def initialize(self,ip,puertoUDP,socket,isOnline,password,id):
        self.ip = ip
        self.puertoUDP = puertoUDP
        self.server_socketUDP = socket
        self.isOnline = isOnline
        self.password = password
        self.id = id


    def escuchaUDP(self):
        #para asegurarnos de que siguen activos
        #crear socket con puerto para UDP. Cada 3 segundos se va a comprobar si alguien no está. 
        #Si uno no responde en 2 intentos, se le quitará de la lista de jugadores activos. 
        #self.server_socketUDP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server_socketUDP.bind((self.ip, self.puertoUDP))
        #self.server_socketUDP.listen() 

        if(self.isOnline):
            while True:
                #print("activo en UDP: ",self.server_socketUDP.getsockname())
                try:
                    data,addr = self.server_socketUDP.recvfrom(1024)
                    #print("msg received in server")
                    msg_clientUDP = data.decode('utf-8')
                    respUDP = self.checkformatUDP(msg_clientUDP)
                    print('msg received UDP: ',msg_clientUDP)
                    #print(resp[0])
                    #print(resp[1][0])
                    #print(self.password)
                    #print(self.currentPlayers)
                    #print(self.numJugadores)
                    #print(resp[1][3])
                    #print(self.existsPlayer(resp[1][3]))
                    #si el que se conecta tiene tu mismo id (es tu misma cuenta), lo va a echar
                    if(respUDP[0] and respUDP[1][0] == self.password and respUDP[1][1] == self.GLOBAL.getOtherPlayersIndex(0)[0]):
                        if(respUDP[1][2] == "estoy"):
                            self.GLOBAL.setTimeout(15) #reiniciamos el contador, pues hemos recibido un mensaje suyo
                            #print("reinicio contador servidor a 15")
                    else:
                        #print("mensaje con mal formato")
                        pass
                except:
                    #print('Exception en escuchaUDP jugador', e) 
                    break
                    
        else:

            while True:
                #print("activo en UDP: ",self.server_socketUDP.getsockname())
                try:
                    data,addr = self.server_socketUDP.recvfrom(1024)
                    #print("msg received in server")
                    msg_clientUDP = data.decode('utf-8')
                    respUDP = self.checkformatUDP(msg_clientUDP)
                    print('msg received UDP: ',msg_clientUDP)
                    if(respUDP[0] and respUDP[1][0] == self.password and respUDP[1][1] != self.id):
                        if(respUDP[1][2] == "estoy"):
                            for posicion,jugador in self.GLOBAL.getOtherPlayers().items():
                                if(jugador != None and jugador[0] == respUDP[1][1]): #es el id de un jugador existente
                                    self.GLOBAL.setTimeoutIndex(posicion,15) #reiniciamos su contador
                                    #print("reinicio contador jugador a 15")
                                    break 
                    #print(resp[0])
                    #print(resp[1][0])
                    #print(self.password)
                    #print(self.currentPlayers)
                    #print(self.numJugadores)
                    #print(resp[1][3])
                    #print(self.existsPlayer(resp[1][3]))
                    #si el que se conecta tiene tu mismo id (es tu misma cuenta), lo va a echar

                except:
                    break
                
        
        try:
            self.server_socketUDP.close()
        except:
            pass
        #print("fin hilo UDP")
    
    def closeSocketUDPServer(self):
        if(self.server_socketUDP != None):
            self.server_socketUDP.close()
            self.server_socketUDP = None
            #print("UDP closed in server")
    
    def checkformatUDP(self,msg):
        try:
            [password,id,content] = msg.split(":")
            if(password != None and password != ' ' and id != None and id != ' ' and content != None and content != ' '):
                return (True,(password,id,content))
            else:
                return (False,None)
        except:
            return (False,None)