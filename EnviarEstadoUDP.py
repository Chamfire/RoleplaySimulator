import socket
from Global import Global
import threading

class EnviarEstadoUDP:
    def __init__(self,isOnline,serverPort,ipDest):
        self.isOnline = isOnline
        if(self.isOnline):
            self.serverPortUDP = serverPort #en caso de ser cliente, solo tendrá eel puerto y la ip del server
            self.ipDest = ipDest
        self.conected = True
        
    def enviarEstadoUDP(self):
        while self.conected:
            #print("activo en enviarUDP")
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                if(self.isOnline):
                    message = b'msg a modificar con el estado'
                    client_socket.sendto(message, (self.ipDest, int(self.serverPortUDP)))
                    client_socket.close()
                else:
                    pass #recorrer lista de usuarios activos y mandarles mensajes de ver si están conectados
                threading.Event().wait(2) #2 segundos
            except:
                threading.Event().wait(2) #2 segundos
        try:
            client_socket.close()
        except:
            pass
        #print("fin hilo enviarUDP")

    def desconectar(self):
        self.conected = False
    


