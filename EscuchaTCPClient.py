import socket
from Global import Global
class EscuchaTCPClient:
    def __init__(self,server_socket,ip,puerto,ip_server,puerto_server,id,password):
        self.imUser = True
        self.server_socket = server_socket
        self.ip = ip
        self.puerto = puerto
        self.ip_server = ip_server
        self.puerto_server = puerto_server
        self.id = id
        self.password = password
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
                try:
                    [password,id_server,content] = msg_client.split(";")
                    #el primero siempre es el servidor -> posición 0
                    #Comprobamos la contraseña de la partida, y si la id que me está pasando == la id del servidor -> comprobamos que el mensaje es de desconexión
                    if(password == self.password and id_server == self.GLOBAL.getOtherPlayersIndex[0][0] and content == "servidor_desconectado"):
                        self.GLOBAL.setOtherPlayersIndex({}) #se reestablece a lista vacía
                        self.GLOBAL.setRefreshScreen("server_disc") #le decimos que se ha desactivado el servidor
                    #si no es el id del servidor, o la contraseña no es correcta, lo ignoramos
                except:
                    pass #si no es el id del servidor, lo ignoramos
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
            msg = str(self.password)+":"+str(self.id)+":"+"usuario_desconectado"
            socket_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                socket_c.connect((self.ip_server, self.puerto_server))
                socket_c.sendall(msg.encode('utf-8')) #mensaje de meMuero, para que los jugadores se salgan del servidor
                #Si el mensaje de me muero no se pudiera enviar, se detectaría a través del timeout de UDP
            except:
                pass
            self.server_socket.close()
            #print("TCP closed in client")