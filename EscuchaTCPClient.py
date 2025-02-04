import socket
from Global import Global
class EscuchaTCPClient:
    def __init__(self,server_socket,ip,puerto):
        self.server_socket = server_socket
        self.ip = ip
        self.puerto = puerto
        self.GLOBAL = Global()
        
    def escuchaTCPClient(self):
        self.server_socket.bind((self.ip, self.puerto))
        self.server_socket.listen() 

        while True:
            try:
                socket_c, ip_port_client = self.server_socket.accept()
                #print("msg received in server")
                msg_client = socket_c.recv(1024).decode('utf-8')
                print('msg received: ',msg_client)
                if(msg_client == "servidor_desconectado"):
                    self.GLOBAL.setOtherPlayersIndex({}) #se reestablece a lista vacía
                    self.GLOBAL.setRefreshScreen("server_disc") #le decimos que se ha desactivado el servidor
                #si no es eso, lo ignoramos
                socket_c.close()
            except:
                try:
                    socket_c.close()
                except:
                    pass
                break

    def closeSocketTCPServer(self):
        if(self.server_socket != None):
            self.server_socket.close()