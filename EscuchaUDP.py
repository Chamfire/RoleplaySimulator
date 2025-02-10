import socket
from Global import Global

class EscuchaUDP:
    def __init__(self):
        self.GLOBAL = Global()
        self.server_socketUDP = None
        self.ip = None
        self.puertoUDP = None

    def initialize(self,ip,puertoUDP,socket,isOnline):
        self.ip = ip
        self.puertoUDP = puertoUDP
        self.server_socketUDP = socket
        self.isOnline = isOnline


    def escuchaUDP(self):
        #para asegurarnos de que siguen activos
        #crear socket con puerto para UDP. Cada 3 segundos se va a comprobar si alguien no está. 
        #Si uno no responde en 2 intentos, se le quitará de la lista de jugadores activos. 
        #self.server_socketUDP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server_socketUDP.bind((self.ip, self.puertoUDP))
        #self.server_socketUDP.listen() 
        
        if(self.isOnline):
            cont = 0 #veces sin recibir mensajes de "estoy" del servidor
            recv_server = False
            while True:
                print("activo en UDP: ",self.server_socketUDP.getsockname())
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
                except Exception as e:
                    print(e)
                    break
        else:
            cont = {}
            recv_server = False
            for i in range(0,len(self.GLOBAL.getOtherPlayers())):
                if(self.GLOBAL.getOtherPlayersIndex(i) != None):
                    cont[i] = 0 #veces sin recibir mensajes de "estoy" del jugador i
                else:
                    cont[i] = None

            while True:
                print("activo en UDP: ",self.server_socketUDP.getsockname())
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
                except Exception as e:
                    print(e)
                    break
                
        
        try:
            self.server_socketUDP.close()
        except:
            pass
        print("fin hilo UDP")
    
    def closeSocketUDPServer(self):
        if(self.server_socketUDP != None):
            self.server_socketUDP.close()
            self.server_socketUDP = None
            #print("UDP closed in server")
    
    def checkformatUDP(self,msg):
        try:
            pass
        except:
            return (False,None)