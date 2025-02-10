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

    def initialize(self,ip,puerto,password,numJugadores,idPropia,nombrePropio,miIcono,puertoUDP,socket):
        self.ip = ip
        self.puerto = puerto
        self.puertoUDP = puertoUDP
        self.password = password
        self.numJugadores = numJugadores
        self.idPropia = idPropia
        self.nombrePropio = nombrePropio
        self.miIcono = miIcono
        self.server_socket = socket

    def escuchaTCP(self):
        #Es multijugador
        #self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server_socket.bind((self.ip, self.puerto))
        self.server_socket.listen() 
        while True:
            #print("activo en TCP escucha")
            #print(self.GLOBAL.getOtherPlayers())
            try:
                socket_c, ip_port_client = self.server_socket.accept()
                #print("msg received in server")
                msg_client = socket_c.recv(1024).decode('utf-8')
                resp = self.checkformat(msg_client)
                print('msg received: ',msg_client)
                msg_to_OtherPlayers = None
                id_new_player = None
                print(resp)
                #print(resp[0])
                #print(resp[1][0])
                #print(self.password)
                #print(self.currentPlayers)
                #print(self.numJugadores)
                #print(resp[1][3])
                #print(self.existsPlayer(resp[1][3]))
                #print(self.GLOBAL.getOtherPlayers())
                #print(self.idPropia)
                #print(self.isNotCurrentlyActive(resp[1][3]))
                #si el que se conecta tiene tu mismo id (es tu misma cuenta), lo va a echar
                if(resp[0] == 2):
                    #quitamos al jugador de la lista de jugadores activos
                    self.GLOBAL.setCurrentPlayers(self.GLOBAL.getCurrentPlayers()-1)
                    for posicion,jugador in self.GLOBAL.getOtherPlayers().items():
                        if(jugador != None and jugador[0] == resp[1]):
                            jugador_modificado = (jugador[0],(jugador[1][0],jugador[1][1],False,jugador[1][3],jugador[1][4],jugador[1][5]))
                            self.GLOBAL.setOtherPlayersIndex(posicion,jugador_modificado) #modificamos el jugador, y lo ponemos como inactivo
                    self.GLOBAL.setRefreshScreen("salaEspera") #le damos un aviso a GAME para actualizar esta pantalla

                    #enviamos la actualizacón que deben hacer los jugadores conectados actualmente
                    msg_to_OtherPlayers = self.password+";"+str(self.idPropia)+";usuario_desconectado:"+resp[1]
                    
                    #TODO: modificar cuando esté en partida (coger currentScreen)
                elif(resp[0] == -1):
                    pass
                elif(resp[0] == 1 and (resp[1][0] == self.password) and ((self.GLOBAL.getCurrentPlayers() < self.numJugadores) or self.existsPlayer(resp[1][3])) and self.idPropia != resp[1][3] and self.isNotCurrentlyActive(resp[1][3])): #existsPlayer también comprueba que no esté activo actualmente
                    msg_ok = "ok:"+str(self.numJugadores)+":"+str(self.puertoUDP)+":"+str(self.idPropia)+";"+str(self.nombrePropio)+";"+str(self.miIcono)+";True"#te pasas a ti mismo como jugador, para que te añada -> True porque estás activo
                    for i in range(0,len(self.GLOBAL.getOtherPlayers())):
                        if(self.GLOBAL.getOtherPlayersIndex(i) != None): #le pasamos la lista de jugadores tanto activos como inactivos
                            print('aquí' ,self.GLOBAL.getOtherPlayersIndex(i))
                            msg_ok = msg_ok+":"+str(self.GLOBAL.getOtherPlayersIndex(i)[0])+";"+self.GLOBAL.getOtherPlayersIndex(i)[1][0]+";"+str(self.GLOBAL.getOtherPlayersIndex(i)[1][1])+";"+str(self.GLOBAL.getOtherPlayersIndex(i)[1][2])
                            #el mensaje tendrá este formato -> ok:4:56382:id1;pepe;1:id2;juan;4
                    free_pos = -1
                    for i in range(0,len(self.GLOBAL.getOtherPlayers())):
                        if(self.GLOBAL.getOtherPlayersIndex(i) == None): #si no se ha conectado nunca, lo añadimos
                            free_pos = i
                            break
                    for j in range(0,len(self.GLOBAL.getOtherPlayers())):
                        if(self.GLOBAL.getOtherPlayersIndex(j) != None and self.GLOBAL.getOtherPlayersIndex(j)[0] == resp[1][3]):
                            free_pos = j
                            break #así nos quedamos con esa j -> si el jugador existe, actualizamos su nombre y pic
        
                    self.GLOBAL.setOtherPlayersIndex(free_pos, (resp[1][3],(resp[1][1],int(resp[1][2]),True,int(resp[1][4]),ip_port_client[0],resp[1][5]))) #(id,(nombre,avatarPicPerfil,True,54823,ip,puertoTCP) <- añado al jugador (True es porque está activo)
                    self.GLOBAL.setCurrentPlayers(self.GLOBAL.getCurrentPlayers()+1)
                    msg_to_OtherPlayers = str(self.password)+";"+str(self.idPropia)+";"+"usuario_nuevo:"+str(resp[1][3])+":"+str(resp[1][1])+":"+str(resp[1][2])+":True" #patata;idPropia;usuario_nuevo:id:nombre:avatarPicPerfil:True
                    id_new_player = resp[1][3]
                    self.GLOBAL.setRefreshScreen("salaEspera") #le damos un aviso a GAME para actualizar esta pantalla
                    #es posible que se haya desconectado y se haya vuelto a conectar
                            
                    #print("self.otherPlayers = ",self.otherPlayers)
                    socket_c.sendall(msg_ok.encode('utf-8'))
                else:
                    msg_no = "no"
                    socket_c.sendall(msg_no.encode('utf-8'))
                socket_c.close()

                if(msg_to_OtherPlayers != None):
                    #hemos recibido un mensaje que implica la modificación de la lista de jugadores activos, y hay que
                    #enviarles el cambio a los otros jugadores ACTIVOS 
                    for i in range(0,len(self.GLOBAL.getOtherPlayers())):
                        if(self.GLOBAL.getOtherPlayersIndex(i) != None and self.GLOBAL.getOtherPlayersIndex(i)[1][2]): 
                            if((id_new_player == None) or (id_new_player != self.GLOBAL.getOtherPlayersIndex(i)[0])):
                                socket_temporal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                try:
                                    socket_temporal.connect((self.GLOBAL.getOtherPlayersIndex(i)[1][4],self.GLOBAL.getOtherPlayersIndex(i)[1][5]))
                                    socket_temporal.sendall(msg_to_OtherPlayers.encode('utf-8'))
                                except:
                                    pass
                                finally:
                                    socket_temporal.close() #se cierra el socket al terminar
                    id_new_player = None

            except:
                try:
                    socket_c.close()
                except:
                    pass
                break
        #print("fin hilo TCP escucha")

    def closeSocketTCPServer(self):
        if(self.server_socket != None):
            for id,jugador in self.GLOBAL.getOtherPlayers().items():
                if(jugador != None and jugador[1][2]): #si el jugador está activo, le mandamos un mensaje de que el servidor se va a desconectar
                    msg = str(self.password)+";"+str(self.idPropia)+";servidor_desconectado"
                    socket_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        ip_dest = jugador[1][4]
                        print(self.GLOBAL.getOtherPlayers())
                        print(id,jugador)
                        print(msg,ip_dest,jugador[1][5])
                        socket_c.connect((ip_dest, int(jugador[1][5])))
                        socket_c.sendall(msg.encode('utf-8')) #mensaje de meMuero, para que los jugadores se salgan del servidor
                        #Si el mensaje de me muero no se pudiera enviar, se detectaría a través del timeout de UDP
                    except:
                        pass
                    finally:
                        try:
                            socket_c.close()
                        except:
                            pass
            self.server_socket.close()
            self.server_socket = None
            #print("TCP closed in server")
    
    def checkformat(self,msg):
        try:
            #0: Mensaje erróneo
            #1: Mensaje correcto de solicitud de acceso
            #2: Mensaje correcto de desconexión
            resp = msg.split(':')
            if(len(resp) == 6):
                #MENSAJE TIPO 1 -> solicitud de acceso
                [password,nombre,pic,id,puerto,puertoTCP] = resp
                #print(password,nombre,pic,id)
                if(password != None and len(password) <= 16): #es la longitud de la password máxima
                    if(nombre != None and len(nombre) <= 13):
                        if(pic != None and int(pic) >=0 and int(pic) <=6): #solo hay 6 iconos
                            if(id != None and id != ' '):
                                if(puerto != None and puertoTCP != None and int(puerto)>=10000 and int(puertoTCP)>= 10000 and int(puerto) <=99999 and int(puertoTCP)<=99999):
                                    return (1,(password,nombre,pic,id,puerto,puertoTCP))
                                else:
                                    return (0,None)
                            else:
                                return (0,None)
                        else:
                            return (0,None)
                    else:
                        return (0,None)
                else:
                    return (0,None)
                
            elif(len(resp) == 3):
                #MENSAJE TIPO 2 -> DESCONEXIÓN
                [pswd,id_user,contenido] = resp
                if (pswd != None and pswd == self.password and self.existsPlayer(id_user) and not self.isNotCurrentlyActive(id_user)):
                    if(contenido != None and contenido == "usuario_desconectado"):
                        return (2,id_user)
                    else:
                        return (-1,None)
                else:
                    return (-1,None)
            else:
                return (0,None)
        except:
            return (0,None)
        
    def existsPlayer(self,id):
        for i in range(0,len(self.GLOBAL.getOtherPlayers())):
            if(self.GLOBAL.getOtherPlayersIndex(i) != None and id == self.GLOBAL.getOtherPlayersIndex(i)[0]):
                #print(self.GLOBAL.getOtherPlayersIndex(i)[0])
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