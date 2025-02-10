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
        print('escuchando en ',self.ip,self.puerto)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.puerto))
        self.server_socket.listen() 

        while True:
            print("activo en TCPClient")
            try:
                socket_c, ip_port_client = self.server_socket.accept()
                #print("msg received in server")
                msg_client = socket_c.recv(1024).decode('utf-8')
                print('msg received: ',msg_client)
                try:
                    [password,id_server,content] = msg_client.split(";")
                    #el primero siempre es el servidor -> posición 0
                    #Comprobamos la contraseña de la partida, y si la id que me está pasando == la id del servidor -> comprobamos que el mensaje es de desconexión
                    print(self.password,id_server,content)
                    if(password == self.password and id_server == self.GLOBAL.getOtherPlayersIndex(0)[0]):
                        resp = content.split(":")
                        if(len(resp) == 1 and resp[0] == "servidor_desconectado"):
                            self.GLOBAL.setOtherPlayersIndex(0,{}) #se reestablece a lista vacía
                            self.GLOBAL.setRefreshScreen("server_disc") #le decimos que se ha desactivado el servidor
                        elif(len(resp) == 5 and resp[0] == "usuario_nuevo"):
                            #añadimos a jugador en la lista, y hacer refresh
                            for i in range(0,len(self.GLOBAL.getOtherPlayers())):
                                if(self.GLOBAL.getOtherPlayersIndex(i) == None): #si no se ha conectado nunca, lo añadimos
                                    free_pos = i
                                    for j in range(0,len(self.GLOBAL.getOtherPlayers())):
                                        if(self.GLOBAL.getOtherPlayersIndex(j) != None and self.GLOBAL.getOtherPlayersIndex(j)[0] == resp[1][3]):
                                            free_pos = j
                                            break #así nos quedamos con esa j -> si el jugador existe, actualizamos su nombre y pic
                                    break
                            self.GLOBAL.setOtherPlayersIndex(free_pos, (resp[1],(resp[2],int(resp[3]),True))) #(id,(nombre,avatarPicPerfil,True) <- añado al jugador (True es porque está activo)
                            self.GLOBAL.setCurrentPlayers(self.GLOBAL.getCurrentPlayers()+1)
                            self.GLOBAL.setRefreshScreen("salaEspera")
                        elif(len(resp) == 2 and resp[0] == "usuario_desconectado"):
                            #ponemos el jugador como inactivo en la lista
                            for posicion,jugador in self.GLOBAL.getOtherPlayers().items():
                                if(jugador != None and jugador[0] == resp[1]):
                                    jugador_modificado = (jugador[0],(jugador[1][0],jugador[1][1],False))
                                    self.GLOBAL.setOtherPlayersIndex(posicion,jugador_modificado) #modificamos el jugador, y lo ponemos como inactivo
                                    break
                            self.GLOBAL.setCurrentPlayers(self.GLOBAL.getCurrentPlayers()-1)
                            self.GLOBAL.setRefreshScreen("salaEspera")
                    
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
            #print("Fin hilo EscuchaTCPClient")

    def closeSocketTCPServer(self):
        if(self.server_socket != None):
            msg = str(self.password)+":"+str(self.id)+":"+"usuario_desconectado"
            socket_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                socket_c.connect((self.ip_server, int(self.puerto_server)))
                socket_c.sendall(msg.encode('utf-8')) #mensaje de meMuero, para que los jugadores se salgan del servidor
                #Si el mensaje de me muero no se pudiera enviar, se detectaría a través del timeout de UDP
            except:
                pass
            self.server_socket.close()
            self.server_socket = None
            #print("TCP closed in client")

    def closeSocketTCPServerSinMSG(self):
        if(self.server_socket != None):
            self.server_socket.close()
            self.server_socket = None