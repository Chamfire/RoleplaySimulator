import socket
from Global import Global
import pickle
from Personaje import Personaje
import Lista_Inventario
import base64

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
        self.personaje_received = None
        self.GLOBAL = Global()
        
    def escuchaTCPClient(self):
        #print('escuchando en ',self.ip,self.puerto)
        self.server_socket.listen() 

        while True:
            #print("activo en TCPClient")
            try:
                socket_c, ip_port_client = self.server_socket.accept()
                #print("msg received in server")
                msg_client = socket_c.recv(65555).decode('utf-8')
                print('msg received: ',msg_client)
                try:
                    [password,id_server,content] = msg_client.split(";")
                    #el primero siempre es el servidor -> posición 0
                    #Comprobamos la contraseña de la partida, y si la id que me está pasando == la id del servidor -> comprobamos que el mensaje es de desconexión
                    #print(self.password,id_server,content)
                    if(password == self.password and id_server == self.GLOBAL.getOtherPlayersIndex(0)[0]):
                        resp = content.split(":")
                        #print(resp)
                        if(len(resp) == 1 and resp[0] == "servidor_desconectado"):
                            self.GLOBAL.setOtherPlayers({}) #se reestablece a lista vacía
                            self.GLOBAL.setRefreshScreen("server_disc") #le decimos que se ha desactivado el servidor
                            self.GLOBAL.setTimeout(None)
                        elif(len(resp) == 5 and resp[0] == "usuario_nuevo"):
                            #añadimos a jugador en la lista, y hacer refresh
                            for i in range(0,len(self.GLOBAL.getOtherPlayers())):
                                if(self.GLOBAL.getOtherPlayersIndex(i) == None): #si no se ha conectado nunca, lo añadimos
                                    free_pos = i
                                    break
                            for j in range(0,len(self.GLOBAL.getOtherPlayers())):
                                if(self.GLOBAL.getOtherPlayersIndex(j) != None and self.GLOBAL.getOtherPlayersIndex(j)[0] == resp[1]):
                                    free_pos = j
                                    break #así nos quedamos con esa j -> si el jugador existe, actualizamos su nombre y pic
                            self.GLOBAL.setOtherPlayersIndex(free_pos, (resp[1],(resp[2],int(resp[3]),True))) #(id,(nombre,avatarPicPerfil,True) <- añado al jugador (True es porque está activo)
                            #print(self.GLOBAL.getOtherPlayers())
                            currentScreen = self.GLOBAL.getCurrentScreen()
                            if(currentScreen == "salaEspera"):
                                self.GLOBAL.setRefreshScreen("salaEspera")
                            elif(currentScreen == "seleccionPersonaje" or currentScreen == "seleccionPersonaje2" or currentScreen == "salaEspera2"):
                                self.GLOBAL.setRefreshScreen("joinSound")
                        elif(len(resp) == 2 and resp[0] == "usuario_desconectado"):
                            #ponemos el jugador como inactivo en la lista
                            for posicion,jugador in self.GLOBAL.getOtherPlayers().items():
                                if(jugador != None and jugador[0] == resp[1]):
                                    jugador_modificado = (jugador[0],(jugador[1][0],jugador[1][1],False))
                                    self.GLOBAL.setOtherPlayersIndex(posicion,jugador_modificado) #modificamos el jugador, y lo ponemos como inactivo
                                    break
                            currentScreen = self.GLOBAL.getCurrentScreen()
                            if(currentScreen == "salaEspera"):
                                self.GLOBAL.setRefreshScreen("salaEspera")
                            elif(currentScreen == "seleccionPersonaje" or currentScreen == "seleccionPersonaje2" or currentScreen == "salaEspera2"):
                                self.GLOBAL.setRefreshScreen("joinSound")
                        elif(len(resp) == 1 and resp[0] == "seleccion_personaje"):
                            #que cambie de pantalla a selección de personaje
                            self.GLOBAL.setRefreshScreen("seleccionPersonaje")

                        elif(resp[0] == "ve_salaEspera2"):
                            #que cambie de pantalla a selección de personaje
                            #usaremos content, porque aquí el split no tiene sentido (es un json)
                            resp_final = []
                            total_recibido = len(resp[2])
                            resp_final.append(bytes(resp[2], encoding='utf8'))
                            while (total_recibido < int(resp[1])):
                                #no hemos recibido todo el mensaje
                                #print("fragmento 1 recibido del personaje")
                                resp_fragment = socket_c.recv(4096)
                                if not resp_fragment:
                                    break
                                resp_final.append(resp_fragment)
                                total_recibido += len(resp_fragment)
                            respuesta = b''.join(resp_final)
                            datos_personaje_decoded = base64.b64decode(respuesta)
                            personaje = pickle.loads(datos_personaje_decoded)   #extraer los datos
                            print(personaje.name)
                            print(personaje.equipo.printEquipoConsolaDebugSuperficial())
                            self.personaje_received = personaje
                            self.GLOBAL.setRefreshScreen("partida_load_wait_1") #cuando el usuario estaba en la sala de espera y le manda a partida_load_wait
                        elif(resp[0] == "ve_partida"):
                            #que cambie de pantalla a selección de personaje
                            #usaremos content, porque aquí el split no tiene sentido (es un json)
                            resp_final = []
                            total_recibido = len(resp[2])
                            resp_final.append(bytes(resp[2], encoding='utf8'))
                            while (total_recibido < int(resp[1])):
                                #no hemos recibido todo el mensaje
                                #print("fragmento 1 recibido del personaje")
                                resp_fragment = socket_c.recv(4096)
                                if not resp_fragment:
                                    break
                                resp_final.append(resp_fragment)
                                total_recibido += len(resp_fragment)
                            respuesta = b''.join(resp_final)
                            datos_personaje_decoded = base64.b64decode(respuesta)
                            personaje = pickle.loads(datos_personaje_decoded)   #extraer los datos
                            print(personaje.name)
                            print(personaje.equipo.printEquipoConsolaDebugSuperficial())
                            self.personaje_received = personaje
                            self.GLOBAL.setRefreshScreen("partida") #te manda a partida
                        elif(resp[0] == "ve_partida_fromSalaEspera"):
                            self.GLOBAL.setRefreshScreen("partida") #te manda a partida
                    #si no es el id del servidor, o la contraseña no es correcta, lo ignoramos
                except:
                    pass #si no es el id del servidor, lo ignoramos
                finally:
                    try:
                        socket_c.close()
                    except:
                        pass
                #si no es eso, lo ignoramos
            except:
                try:
                    self.server_socket.close()
                except:
                    pass
                break
            #print("Fin hilo EscuchaTCPClient")
        try:
            self.server_socket.close()
        except:
            pass

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

    def getPersonajeReceived(self):
        return self.personaje_received
    
    def setPersonajeReceived(self):
        self.personaje_received = None
    