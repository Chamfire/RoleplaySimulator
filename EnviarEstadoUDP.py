import socket
from Global import Global
import threading

class EnviarEstadoUDP:
    def __init__(self,isOnline,serverPort,ipDest,id,password,t,max_msgs_udp):
        self.id = id
        self.max_msgs_udp = max_msgs_udp
        self.GLOBAL = Global()
        self.isOnline = isOnline
        if(self.isOnline):
            self.serverPortUDP = serverPort #en caso de ser cliente, solo tendrá eel puerto y la ip del server
            self.ipDest = ipDest
        self.conected = True
        self.password = password
        self.t = t
        
    def enviarEstadoUDP(self):
        if(self.isOnline):
            self.GLOBAL.setTimeout(15)
            while self.conected:
                #print("activo en enviarUDP usuario a ip y puerto: ", self.ipDest,self.serverPortUDP)
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    message = str(self.password)+":"+self.id+":estoy"
                    client_socket.sendto(message.encode('utf-8'), (self.ipDest, int(self.serverPortUDP)))
                    client_socket.close()
                    self.GLOBAL.decreaseTimeout() 
                    if(self.GLOBAL.getTimeout() == 0): #no hemos recibido ningún mensaje del servidor en 15 envíos de mensaje
                        self.GLOBAL.setOtherPlayers({})  #se reestablece a lista vacía
                        self.GLOBAL.setNoEnPartida() #se sale de la partida
                        self.GLOBAL.setRefreshScreen("server_disc") #le decimos que se ha desactivado el servidor
                        self.GLOBAL.setTimeout(None) #reiniciamos el contador para posibles nuevas partidas
            
                except:
                    #print('Excepción en enviarEstadoUDP ',e)
                    threading.Event().wait(self.t) #0.2 segundos
                threading.Event().wait(self.t) #0.2 segundos
        else:
            cont = {}
            for i in range(0,len(self.GLOBAL.getOtherPlayers())):
                if(self.GLOBAL.getOtherPlayersIndex(i) != None):
                    cont[i] = self.max_msgs_udp #veces sin recibir mensajes de "estoy" del jugador i
                else:
                    cont[i] = None
            self.GLOBAL.setTimeout(cont)

            while self.conected:
                #print("activo en enviarUDP servidor")
                try:
                    for posicion,jugador in self.GLOBAL.getOtherPlayers().items():
                        if(jugador != None and jugador[1][2] and self.GLOBAL.getTimeoutIndex(posicion) != None):
                            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            message = str(self.password)+":"+self.id+":estoy"
                            client_socket.sendto(message.encode('utf-8'), (jugador[1][4], int(jugador[1][3])))
                            #print("enviado msg ",message," a ",jugador[1][4], int(jugador[1][3]))
                            client_socket.close()
                            self.GLOBAL.decreaseTimeoutIndex(posicion)
                            if(self.GLOBAL.getTimeoutIndex(posicion) == 0):
                                #consideramos que el jugador se ha desconectado
                                self.GLOBAL.setCurrentPlayers(self.GLOBAL.getCurrentPlayers()-1)
                                jugador_modificado = (jugador[0],(jugador[1][0],jugador[1][1],False,jugador[1][3],jugador[1][4],jugador[1][5]))
                                self.GLOBAL.setOtherPlayersIndex(posicion,jugador_modificado) #modificamos el jugador, y lo ponemos como inactivo
                                self.GLOBAL.setTimeoutIndex(posicion,None)
                                print('otherPlayers: ', self.GLOBAL.getOtherPlayers())
                                if(self.GLOBAL.getCurrentScreen() == "salaEspera"):
                                    self.GLOBAL.setRefreshScreen("salaEspera") #le damos un aviso a GAME para actualizar esta pantalla
                                else:
                                    self.GLOBAL.setRefreshScreen("joinSound")
                                #enviamos la actualizacón que deben hacer los jugadores conectados actualmente
                                msg_to_OtherPlayers = str(self.password)+";"+str(self.id)+";usuario_desconectado:"+str(jugador[0])
                                for i in range(0,len(self.GLOBAL.getOtherPlayers())):
                                    if(self.GLOBAL.getOtherPlayersIndex(i) != None and self.GLOBAL.getOtherPlayersIndex(i)[1][2]):
                                        socket_temporal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                        try:
                                            socket_temporal.connect((self.GLOBAL.getOtherPlayersIndex(i)[1][4],self.GLOBAL.getOtherPlayersIndex(i)[1][5]))
                                            socket_temporal.sendall(msg_to_OtherPlayers.encode('utf-8'))
                                        except:
                                            pass
                                        finally:
                                            socket_temporal.close() #se cierra el socket al terminar
                    threading.Event().wait(self.t) #0.2 segundos
                except:
                    #print(e)
                    threading.Event().wait(self.t) #0.2 segundos
        try:
            client_socket.close()
        except:
            pass
        #print("fin hilo enviarUDP")

    def desconectar(self):
        self.conected = False
    


