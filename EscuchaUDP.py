import socket
from Global import Global

class EscuchaUDP:
    def __init__(self):
        self.GLOBAL = Global()
        self.server_socketUDP = None
        self.ip = None
        self.puertoUDP = None

    def initialize(self,ip,puertoUDP):
        self.ip = ip
        self.puertoUDP = puertoUDP


    def escuchaUDP(self):
        #para asegurarnos de que siguen activos
        #crear socket con puerto para UDP. Cada 3 segundos se va a comprobar si alguien no está. 
        #Si uno no responde en 2 intentos, se le quitará de la lista de jugadores activos. 
        self.server_socketUDP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socketUDP.bind((self.ip, self.puertoUDP))
        self.server_socketUDP.listen() 
        while True:
            try:
                socket_c_udp, ip_port_client = self.server_socketUDP.accept()
                #print("msg received in server")
                msg_clientUDP = socket_c_udp.recv(1024).decode('utf-8')
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
                socket_c_udp.close()
            except:
                try:
                    socket_c_udp.close()
                except:
                    pass
                break
    
    def closeSocketUDPServer(self):
        if(self.server_socketUDP != None):
            self.server_socketUDP.close()
    
    def checkformatUDP(self,msg):
        try:
            pass
        except:
            return (False,None)