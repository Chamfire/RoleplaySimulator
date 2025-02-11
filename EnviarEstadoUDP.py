import socket
from Global import Global
import threading

class EnviarEstadoUDP:
    def __init__(self,isOnline,serverPort,ipDest,id,password):
        self.id = id
        self.GLOBAL = Global()
        self.isOnline = isOnline
        if(self.isOnline):
            self.serverPortUDP = serverPort #en caso de ser cliente, solo tendrá eel puerto y la ip del server
            self.ipDest = ipDest
        self.conected = True
        self.password = password
        
    def enviarEstadoUDP(self):
        if(self.isOnline):
            self.GLOBAL.setTimeout(15)
            while self.conected:
                print("activo en enviarUDP usuario")
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    message = str(self.password)+":"+self.id+":estoy"
                    client_socket.sendto(message.encode('utf-8'), (self.ipDest, int(self.serverPortUDP)))
                    client_socket.close()
                    self.GLOBAL.decreaseTimeout() 
                    if(self.GLOBAL.getTimeout() == 0): #no hemos recibido ningún mensaje del servidor en 15 envíos de mensaje
                        self.GLOBAL.setOtherPlayers({})  #se reestablece a lista vacía
                        self.GLOBAL.setRefreshScreen("server_disc") #le decimos que se ha desactivado el servidor
                        self.GLOBAL.setTimeout(None) #reiniciamos el contador para posibles nuevas partidas
            
                except:
                    threading.Event().wait(0.2) #0.2 segundos
        else:
            cont = {}
            for i in range(0,len(self.GLOBAL.getOtherPlayers())):
                if(self.GLOBAL.getOtherPlayersIndex(i) != None):
                    cont[i] = 15 #veces sin recibir mensajes de "estoy" del jugador i
                else:
                    cont[i] = None
            self.GLOBAL.setTimeout(cont)

            while self.conected:
                print("activo en enviarUDP servidor")
                try:
                    if(self.GLOBAL.getOtherPlayers() != None):
                        for posicion,jugador in self.GLOBAL.getOtherPlayers().items():
                            if(jugador[1][2] and self.GLOBAL.getTimeoutIndex(posicion) != None):
                                client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                                message = str(self.password)+":"+self.id+":estoy"
                                client_socket.sendto(message.encode('utf-8'), (jugador[1][3], int(jugador[1][4])))
                                client_socket.close()
                                self.GLOBAL.decreaseTimeoutIndex(posicion)
                                if(self.GLOBAL.getTimeoutIndex(posicion) == 0):
                                    #consideramos que el jugador se ha desconectado
                                    self.GLOBAL.setCurrentPlayers(self.GLOBAL.getCurrentPlayers()-1)
                                    jugador_modificado = (jugador[0],(jugador[1][0],jugador[1][1],False,jugador[1][3],jugador[1][4],jugador[1][5]))
                                    self.GLOBAL.setOtherPlayersIndex(posicion,jugador_modificado) #modificamos el jugador, y lo ponemos como inactivo
                                    self.GLOBAL.setTimeoutIndex(posicion,None)
                                    self.GLOBAL.setRefreshScreen("salaEspera") #le damos un aviso a GAME para actualizar esta pantalla

                                    #enviamos la actualizacón que deben hacer los jugadores conectados actualmente
                                    msg_to_OtherPlayers = str(self.password)+";"+str(self.id)+";usuario_desconectado:"+str(jugador[0])
                                    socket_temporal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                    try:
                                        socket_temporal.connect((self.GLOBAL.getOtherPlayersIndex(posicion)[1][4],self.GLOBAL.getOtherPlayersIndex(posicion)[1][5]))
                                        socket_temporal.sendall(msg_to_OtherPlayers.encode('utf-8'))
                                    except:
                                        pass
                                    finally:
                                        socket_temporal.close() #se cierra el socket al terminar
                    threading.Event().wait(0.2) #0.2 segundos
                except:
                    threading.Event().wait(0.2) #0.2 segundos
        try:
            client_socket.close()
        except:
            pass
        print("fin hilo enviarUDP")

    def desconectar(self):
        self.conected = False
    


