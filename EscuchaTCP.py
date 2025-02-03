import socket
from Global import Global
class EscuchaTCP:

    def __init__(self):
        self.GLOBAL = Global()
        self.server_socket = None
        self.ip = None
        self.puerto = None
        self.password = None
        self.numJugadores = None
        self.idPropia = None
        self.nombrePropio = None
        self.miIcono = None

    def initialize(self,ip,puerto,password,numJugadores,idPropia,nombrePropio,miIcono,puertoUDP):
        self.ip = ip
        self.puerto = puerto
        self.puertoUDP = puertoUDP
        self.password = password
        self.numJugadores = numJugadores
        self.idPropia = idPropia
        self.nombrePropio = nombrePropio
        self.miIcono = miIcono

    def escuchaTCP(self):
        #Es multijugador
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.puerto))
        self.server_socket.listen() 
        while True:
            try:
                socket_c, ip_port_client = self.server_socket.accept()
                #print("msg received in server")
                msg_client = socket_c.recv(1024).decode('utf-8')
                resp = self.checkformat(msg_client)
                print('msg received: ',msg_client)
                #print(resp[0])
                #print(resp[1][0])
                #print(self.password)
                #print(self.currentPlayers)
                #print(self.numJugadores)
                #print(resp[1][3])
                #print(self.existsPlayer(resp[1][3]))
                #si el que se conecta tiene tu mismo id (es tu misma cuenta), lo va a echar
                if(resp[0] and (resp[1][0] == self.password) and ((self.GLOBAL.getCurrentPlayers() < self.numJugadores) or self.existsPlayer(resp[1][3])) and id != resp[1][3] and self.isNotCurrentlyActive(resp[1][3])): #existsPlayer también comprueba que no esté activo actualmente
                    msg_ok = "ok:"+str(self.numJugadores)+":"+str(self.puertoUDP)+":"+str(self.idPropia)+";"+str(self.nombrePropio)+";"+str(self.miIcono) #te pasas a ti mismo como jugador, para que te añada
                    for i in range(0,len(self.GLOBAL.getOtherPlayers())):
                        if(self.GLOBAL.getOtherPlayersIndex(i) != None and self.GLOBAL.getOtherPlayersIndex(i)[1][2] == True): #True es que está activo el jugador en ese momento
                            print('aquí' ,self.GLOBAL.getOtherPlayersIndex(i))
                            msg_ok = msg_ok+":"+str(self.GLOBAL.getOtherPlayersIndex(i)[0])+";"+self.GLOBAL.getOtherPlayersIndex(i)[1][0]+";"+str(self.GLOBAL.getOtherPlayersIndex(i)[1][1])
                            #el mensaje tendrá este formato -> ok:4:56382:id1;pepe;1:id2;juan;4
                    free_pos = -1
                    for i in range(0,len(self.GLOBAL.getOtherPlayers())):
                        if(self.GLOBAL.getOtherPlayersIndex(i) == None): #si no se ha conectado nunca, lo añadimos
                            free_pos = i
                            for j in range(0,len(self.GLOBAL.getOtherPlayers())):
                                if(self.GLOBAL.getOtherPlayersIndex(j) != None and self.GLOBAL.getOtherPlayersIndex(j)[0] == resp[1][3]):
                                   free_pos = j
                                   break #así nos quedamos con esa j -> si el jugador existe, actualizamos su nombre y pic
                            break
                    self.GLOBAL.setOtherPlayersIndex(free_pos, (resp[1][3],(resp[1][1],int(resp[1][2]),True,int(resp[1][4])))) #(id,(nombre,avatarPicPerfil,True,54823) <- añado al jugador (True es porque está activo)
                    self.GLOBAL.setCurrentPlayers(self.GLOBAL.getCurrentPlayers()+1)
                    self.GLOBAL.setRefreshScreen("salaEspera") #le damos un aviso a GAME para actualizar esta pantalla
                    #es posible que se haya desconectado y se haya vuelto a conectar
                            
                    #print("self.otherPlayers = ",self.otherPlayers)
                    socket_c.sendall(msg_ok.encode('utf-8'))
                else:
                    msg_no = "no"
                    socket_c.sendall(msg_no.encode('utf-8'))
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
    
    def checkformat(self,msg):
        try:
            [password,nombre,pic,id,puerto] = msg.split(':')
            #print(password,nombre,pic,id)
            if(password != None and len(password) <= 16): #es la longitud de la password máxima
                if(nombre != None and len(nombre) <= 13):
                    if(pic != None and int(pic) >=0 and int(pic) <=6): #solo hay 6 iconos
                        if(id != None and id != ' '):
                            if(puerto != None and int(puerto)>=49152 and int(puerto) <=65535):
                                return (True,(password,nombre,pic,id,puerto))
                            else:
                                return (False,None)
                        else:
                            return (False,None)
                    else:
                        return (False,None)
                else:
                    return (False,None)
            else:
                return (False,None)
        except:
            return (False,None)
        
    def existsPlayer(self,id):
        for i in range(0,len(self.GLOBAL.getOtherPlayers())):
            if(self.GLOBAL.getOtherPlayersIndex(i) != None and id == self.GLOBAL.getOtherPlayersIndex(i)[0]):
                print(self.GLOBAL.getOtherPlayersIndex(i)[0])
                return True
            #print(self.otherPlayers[i])
        return False
    
    def isNotCurrentlyActive(self,id):
        for i in range(0,len(self.GLOBAL.getOtherPlayers())):
            if(self.GLOBAL.getOtherPlayersIndex(i) != None and id == self.GLOBAL.getOtherPlayersIndex(i)[0]):
                if(self.GLOBAL.getOtherPlayersIndex(i)[1][2] == False):
                    return True
                else:
                    return False #ya está conectado supuestamente -> posible hacker
            #print(self.otherPlayers[i])
        return True