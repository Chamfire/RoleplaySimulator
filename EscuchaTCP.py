import socket
from Global import Global
import sqlite3
import pygame
from pygame import mixer
import pickle
from Personaje import Personaje
import Lista_Inventario
import base64


class EscuchaTCP:

    def __init__(self,ch5,max_msg_delay):
        self.GLOBAL = Global()
        self.server_socket = None
        self.ip = None
        self.puerto = None
        self.password = None
        self.numJugadores = None
        self.idPropia = None
        self.nombrePropio = None
        self.miIcono = None
        self.ch5 = ch5
        self.join = pygame.mixer.Sound('sounds/joinPartida.wav')
        self.max_msg_delay = max_msg_delay

    def initialize(self,ip,puerto,password,numJugadores,idPropia,nombrePropio,miIcono,puertoUDP,socket,currentPartida):
        self.ip = ip
        self.puerto = puerto
        self.puertoUDP = puertoUDP
        self.password = password
        self.numJugadores = numJugadores
        self.idPropia = idPropia
        self.nombrePropio = nombrePropio
        self.miIcono = miIcono
        self.server_socket = socket
        self.currentPartida = currentPartida

    def escuchaTCP(self):
        #Es multijugador
        #self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server_socket.bind((self.ip, self.puerto))
        self.server_socket.listen() 
        while True:
            #print("activo en TCP escucha: ",self.server_socket.getsockname())
            #print(self.GLOBAL.getOtherPlayers())
            try:
                #print("esperando TCP")
                socket_c, ip_port_client = self.server_socket.accept()
                #print("msg received in server")
                msg_client = socket_c.recv(9999999).decode('utf-8')
                resp = self.checkformat(msg_client)
                print('msg received: ',msg_client)
                msg_to_OtherPlayers = None
                id_new_player = None
                #print(resp)
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
                    for posicion,jugador in self.GLOBAL.getOtherPlayers().items():
                        if(jugador != None and jugador[0] == resp[1]):
                            self.GLOBAL.setCurrentPlayers(self.GLOBAL.getCurrentPlayers()-1)
                            jugador_modificado = (jugador[0],(jugador[1][0],jugador[1][1],False,jugador[1][3],jugador[1][4],jugador[1][5]))
                            self.GLOBAL.setOtherPlayersIndex(posicion,jugador_modificado) #modificamos el jugador, y lo ponemos como inactivo
                            self.GLOBAL.setTimeoutIndex(posicion,None)
                            break
                    #quitamos su contador el timeout
                    if(self.GLOBAL.getCurrentScreen() == "salaEspera"):
                        self.GLOBAL.setRefreshScreen("salaEspera") #le damos un aviso a GAME para actualizar esta pantalla
                    else:
                        #en otro caso la desconexión de un jugador se limitará a la reproducción de un sonido
                        self.ch5.play(self.join)

                    #enviamos la actualizacón que deben hacer los jugadores conectados actualmente
                    msg_to_OtherPlayers = self.password+";"+str(self.idPropia)+";usuario_desconectado:"+resp[1]
                elif(resp[0] == 3):
                    #check del nombre
                    conn = sqlite3.connect("simuladordnd.db")
                    cursor = conn.cursor()
                    query_check_same_name = "SELECT name FROM personaje WHERE name = '"+resp[1]+"' AND partida_id = '"+self.currentPartida+"' AND id_jugador = '"+resp[2]+"'"
                    cursor.execute(query_check_same_name)
                    rows = cursor.fetchall() 
                    conn.close()
                    if rows != []:
                        #ese personaje ya existió, y está muerto
                        msg_no_usar_nombre = str(self.password)+":"+self.idPropia+":no_usar"
                        socket_c.sendall(msg_no_usar_nombre.encode('utf-8'))
                    else:
                        #puede usar ese nombre sin problemas
                        msg_usar = str(self.password)+":"+self.idPropia+":usar"
                        socket_c.sendall(msg_usar.encode('utf-8'))

                elif(resp[0] == 4):
                    try:
                        datos_personaje_decoded = base64.b64decode(resp[1])
                        personaje_temp = pickle.loads(datos_personaje_decoded)   #extraer los datos
                        personaje_temp.partida_id = self.currentPartida
                        self.GLOBAL.setListaPersonajeHostIndex(resp[2],personaje_temp) #añadimos el personaje a la lista de usuarios activos
                        
                        #guardamos en la bbdd el personaje que se ha creado
                        conn = sqlite3.connect("simuladordnd.db")
                        cursor = conn.cursor()

                        #trasfondo: num_trasfondo es la pk, que se autoincrementa sola
                        query_save_trasfondo = """INSERT INTO trasfondo (tipo_trasfondo, vinculo, defecto, ideal, rasgo_personalidad, num_trasfondo) 
                                                    VALUES (?,?,?,?,?,?)"""
                        id_t = personaje_temp.id_trasfondo[1]
                        id_trasfondo = str(personaje_temp.id_trasfondo[0])+"_"+str((personaje_temp.vinculo[1]+id_t*6))+"_"+str((personaje_temp.defecto[1]+ id_t*6))+"_"+str((personaje_temp.ideal[1]+id_t*6))+"_"+str((personaje_temp.rasgo_personalidad[1]+id_t*8))
                        data_trasfondo = (personaje_temp.id_trasfondo[0],(personaje_temp.vinculo[1]+id_t*6) ,(personaje_temp.defecto[1]+ id_t*6),(personaje_temp.ideal[1]+id_t*6),(personaje_temp.rasgo_personalidad[1]+id_t*8),id_trasfondo)
                        #print(data_trasfondo)
                        query_check_same_trasfondo = "SELECT num_trasfondo FROM trasfondo WHERE num_trasfondo = '"+id_trasfondo+"'"
                        cursor.execute(query_check_same_trasfondo)
                        rows = cursor.fetchall() 
                        #print(rows)
                        if rows != []:
                            #existe esa combinación en la bbdd
                            pass
                        else:
                            #si no existe esa combinación aún en la bbdd
                            cursor.execute(query_save_trasfondo, data_trasfondo)

                        #personaje
                        query_save_personaje = """INSERT INTO personaje (name, sm1, sm2, sm3, nivel, inspiracion,esta_muerto,bpc,cons,fu,des,sab,car,int,coordenadas_actuales,vida_temp,max_vida,ca,edad,peso,pc,pp,pe,po,ppt,velocidad,descripcion_fisica,tipo_raza,tipo_clase,tipo_alineamiento,id_trasfondo,tipo_size,partida_id,id_jugador,num_npc_partida) 
                                                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
                            
                        data_personaje = (personaje_temp.name, personaje_temp.sm1,personaje_temp.sm2,personaje_temp.sm3,personaje_temp.nivel,personaje_temp.inspiracion,personaje_temp.esta_muerto,personaje_temp.bpc,personaje_temp.cons,personaje_temp.fu,personaje_temp.des,personaje_temp.sab,personaje_temp.car,personaje_temp.int,personaje_temp.coordenadas_actuales,personaje_temp.vida_temp,personaje_temp.max_vida,personaje_temp.ca,personaje_temp.edad,personaje_temp.peso,personaje_temp.pc,personaje_temp.pp,personaje_temp.pe,personaje_temp.po,personaje_temp.ppt,personaje_temp.velocidad,personaje_temp.descripcion_fisica,personaje_temp.tipo_raza,personaje_temp.tipo_clase,personaje_temp.tipo_alineamiento[0],id_trasfondo,personaje_temp.tipo_size,personaje_temp.partida_id,resp[2],None) 
                        conn.execute(query_save_personaje,data_personaje)

                        #competencias de idioma
                        data_idiomas_comp = []
                        query_save_comp_idioma = """INSERT INTO comp_idioma (tipo_language,name,partida_id,id_jugador,num_npc_partida)
                                                    VALUES (?,?,?,?,?)"""
                        for idioma,isCompetent in personaje_temp.idiomas_competencia.items():
                            if(isCompetent):
                                data_idiomas_comp += [(idioma,personaje_temp.name,personaje_temp.partida_id,resp[2],None)]
                        conn.executemany(query_save_comp_idioma,data_idiomas_comp)
                        
                        #salvaciones de competencia
                        data_salvaciones_comp = []
                        query_save_salvaciones_comp = """INSERT INTO salvaciones_comp (tipo_caracteristica,name,partida_id,id_jugador,num_npc_partida)
                                                        VALUES(?,?,?,?,?)"""
                        for salvacion, isCompetent in personaje_temp.salvaciones_comp.items():
                            if(isCompetent):
                                data_salvaciones_comp += [(salvacion,personaje_temp.name,personaje_temp.partida_id,resp[2],None)]
                        conn.executemany(query_save_salvaciones_comp,data_salvaciones_comp)

                        #habilidades de competencia
                        data_habilidades_comp = []
                        query_save_habilidades_comp = """INSERT INTO habilidades_comp (tipo_habilidad,name,partida_id,id_jugador,num_npc_partida)
                                                        VALUES(?,?,?,?,?)"""
                        for habilidad, isCompetent in personaje_temp.habilidades_comp.items():
                            if(isCompetent):
                                data_habilidades_comp += [(habilidad,personaje_temp.name,personaje_temp.partida_id,resp[2],None)]
                        conn.executemany(query_save_habilidades_comp,data_habilidades_comp)

                        #inventario
                        data_inventario = []
                        query_save_inventario = """INSERT INTO inventario (cantidad,name_obj,categoria_obj,name,partida_id,id_jugador,num_npc_partida,procedencia,lista_nombre,slot)
                                                    VALUES(?,?,?,?,?,?,?,?,?,?)"""
                        for slot_name, objeto in personaje_temp.equipo.objetos.items():
                            if(objeto != None):
                                tipo = str(type(objeto[2]))
                                tipo_nombre = tipo[25:-2]
                                data_inventario += [(objeto[3],objeto[1],objeto[0],personaje_temp.name,personaje_temp.partida_id,resp[2],None,'Equipo',tipo_nombre,slot_name)]
                        conn.executemany(query_save_inventario,data_inventario)


                        #como no tiene armadura equipada, ni objetos al empezar, no se almacenarán aquí, pero si se extraerán de la base de datos en la sala de espera
                        conn.commit()
                        conn.close()
                        
                        if(self.numJugadores == (len(self.GLOBAL.getListaPersonajeHost()) + 1)):
                            msg_ve_partida = str(self.password)+":"+self.idPropia+":ve_partida"
                            socket_c.sendall(msg_ve_partida.encode('utf-8'))
                            #TODO: Mandar a todos a la partida
                            for i in range(0,len(self.GLOBAL.getCurrentPlayers())):
                                if(self.GLOBAL.getCurrentPlayers(i) != None and self.GLOBAL.getCurrentPlayers(i)[0] != resp[2]):
                                    #enviamos un mensaje a todos para que vayan a la partida
                                    #TODO: pass
                                    pass
                            
                            if(self.GLOBAL.getCurrentScreen != "partida"):
                                self.GLOBAL.setRefreshScreen("partida") #para que vaya a partida

                        else:
                            msg_ve_sala_espera = str(self.password)+":"+self.idPropia+":ve_salaEspera2"
                            socket_c.sendall(msg_ve_sala_espera.encode('utf-8'))

                    except Exception as e:
                        print(e)
                        msg_mal_personaje = str(self.password)+":"+self.idPropia+":mal_personaje"
                        socket_c.sendall(msg_mal_personaje.encode('utf-8'))


                elif(resp[0] == -1):
                    pass
                elif(resp[0] == 1 and (resp[1][0] == self.password) and (((self.GLOBAL.getCurrentPlayers() < self.numJugadores) and (self.numJugadores > self.GLOBAL.getOtherPlayersTotalRegistered()+1)) or self.existsPlayer(resp[1][3])) and self.idPropia != resp[1][3] and self.isNotCurrentlyActive(resp[1][3])): #existsPlayer también comprueba que no esté activo actualmente
                    currentScreen = self.GLOBAL.getCurrentScreen()
                    print(currentScreen)
                    if(currentScreen == "salaEspera"):
                        msg_ok = "ok:"+str(self.numJugadores)+":"+str(self.puertoUDP)+":"+str(self.idPropia)+";"+str(self.nombrePropio)+";"+str(self.miIcono)+";True"#te pasas a ti mismo como jugador, para que te añada -> True porque estás activo
                    elif(currentScreen == "seleccionPersonaje" or currentScreen == "seleccionPersonaje2" or "salaEspera2"):
                        personaje_temp = self.GLOBAL.getListaPersonajeHostIndex(resp[1][3])
                        if(personaje_temp != -1):
                            datos_personaje_serialized = pickle.dumps(personaje_temp)
                            datos_personaje_encoded = base64.b64encode(datos_personaje_serialized).decode('utf-8')
                            msg_ok = f"ok_ve_salaEspera2:{datos_personaje_encoded}:{self.numJugadores}:{self.puertoUDP}:{self.idPropia};{self.nombrePropio};{self.miIcono};True"#te pasas a ti mismo como jugador, para que te añada -> True porque estás activo
                        else:
                            msg_ok = "ok_ve_seleccionPersonaje:"+str(self.numJugadores)+":"+str(self.puertoUDP)+":"+str(self.idPropia)+";"+str(self.nombrePropio)+";"+str(self.miIcono)+";True"#te pasas a ti mismo como jugador, para que te añada -> True porque estás activo
                    elif(currentScreen == "partida"):
                        personaje_temp = self.GLOBAL.getListaPersonajeHostIndex(resp[1][3])
                        datos_personaje_serialized = pickle.dumps(personaje_temp)
                        datos_personaje_encoded = base64.b64encode(datos_personaje_serialized).decode('utf-8')
                        msg_ok = f"ok_ve_partida:{datos_personaje_encoded}:{self.numJugadores}:{self.puertoUDP}:{self.idPropia};{self.nombrePropio};{self.miIcono};True"#te pasas a ti mismo como jugador, para que te añada -> True porque estás activo
                    for i in range(0,len(self.GLOBAL.getOtherPlayers())):
                        if(self.GLOBAL.getOtherPlayersIndex(i) != None): #le pasamos la lista de jugadores tanto activos como inactivos
                            #print('aquí' ,self.GLOBAL.getOtherPlayersIndex(i))
                            msg_ok = msg_ok+":"+str(self.GLOBAL.getOtherPlayersIndex(i)[0])+";"+self.GLOBAL.getOtherPlayersIndex(i)[1][0]+";"+str(self.GLOBAL.getOtherPlayersIndex(i)[1][1])+";"+str(self.GLOBAL.getOtherPlayersIndex(i)[1][2])
                            #el mensaje tendrá este formato -> ok:4:56382:id1;pepe;1:id2;juan;4
                
                    free_pos = -1
                    existing_player = False
                    for i in range(0,len(self.GLOBAL.getOtherPlayers())):
                        if(self.GLOBAL.getOtherPlayersIndex(i) == None): #si no se ha conectado nunca, lo añadimos
                            free_pos = i
                            break
                    for j in range(0,len(self.GLOBAL.getOtherPlayers())):
                        if(self.GLOBAL.getOtherPlayersIndex(j) != None and self.GLOBAL.getOtherPlayersIndex(j)[0] == resp[1][3]):
                            free_pos = j
                            existing_player = True
                            break #así nos quedamos con esa j -> si el jugador existe, actualizamos su nombre y pic
        
                    self.GLOBAL.setOtherPlayersIndex(free_pos, (resp[1][3],(resp[1][1],int(resp[1][2]),True,int(resp[1][4]),ip_port_client[0],int(resp[1][5])))) #(id,(nombre,avatarPicPerfil,True,54823,ip,puertoTCP) <- añado al jugador (True es porque está activo)
                    self.GLOBAL.setCurrentPlayers(self.GLOBAL.getCurrentPlayers()+1)
                    msg_to_OtherPlayers = str(self.password)+";"+str(self.idPropia)+";"+"usuario_nuevo:"+str(resp[1][3])+":"+str(resp[1][1])+":"+str(resp[1][2])+":True" #patata;idPropia;usuario_nuevo:id:nombre:avatarPicPerfil:True
                    id_new_player = resp[1][3]
                    #hay que crear un nuevo index para ese jugador en cont de timeout
                    self.GLOBAL.setTimeoutIndex(free_pos,self.max_msg_delay) #la id en cont es la misma que en otherPlayers
                    if(self.GLOBAL.getCurrentScreen() == "salaEspera"):
                        self.GLOBAL.setRefreshScreen("salaEspera") #le damos un aviso a GAME para actualizar esta pantalla
                    else:
                        #en otro caso la desconexión de un jugador se limitará a la reproducción de un sonido
                        self.ch5.play(self.join)
                    #es posible que se haya desconectado y se haya vuelto a conectar
                            
                    #print("self.otherPlayers = ",self.otherPlayers)
                    socket_c.sendall(msg_ok.encode('utf-8'))
                    #lo guardamos en la bbdd como jugador y lo metemos en partida-jugador
                    if(existing_player):
                        print("ya existía")
                        #si el jugador ya existía, modificamos nombre y pic en la bbdd (pueden haber cambiado)
                        conn = sqlite3.connect("simuladordnd.db")
                        cursor = conn.cursor()
                        query_update_pic = "UPDATE jugador SET pic = "+resp[1][2]+" WHERE id_jugador = '"+resp[1][3]+"';"
                        cursor.execute(query_update_pic)  
                        query_update_name = "UPDATE jugador SET name = '"+resp[1][1]+"' WHERE id_jugador = '"+resp[1][3]+"';"
                        cursor.execute(query_update_name)  
                        conn.commit() 
                        conn.close()
                    else:
                        #hay que comprobar si el jugador es un jugador que ya existía en otra partida
                        conn = sqlite3.connect("simuladordnd.db")
                        query_find_player = "SELECT id_jugador FROM jugador WHERE id_jugador = '"+resp[1][3]+"';"
                        cursor = conn.cursor()
                        cursor.execute(query_find_player)
                        rows = cursor.fetchall() 
                        if(rows != [] and rows[0] == resp[1][3]): #si existe la id 
                            #actualizamos pic y name
                            query_update_pic = "UPDATE jugador SET pic = "+str(resp[1][2])+" WHERE id_jugador = '"+resp[1][3]+"';"
                            cursor.execute(query_update_pic)  
                            query_update_name = "UPDATE jugador SET name = '"+resp[1][1]+"' WHERE id_jugador = '"+resp[1][3]+"';"
                            cursor.execute(query_update_name)  
                            conn.commit() 
                            conn.close()
                        else: #no existe el jugador -> lo añadimos
                            conn = sqlite3.connect("simuladordnd.db")
                            cursor = conn.cursor()
                            data_jugador_yo = (resp[1][3],False,resp[1][2],resp[1][1])
                            query_save_jugador = """INSERT INTO jugador
                                                (id_jugador,is_my_id,pic,name) 
                                                VALUES (?,?,?,?)"""
                            cursor.execute(query_save_jugador,data_jugador_yo)  
                            conn.commit() 
                        print("adding to partida-jugador")
                        data_jugador_partida = (0,self.currentPartida,resp[1][3]) #nMuertes_partida,partida_id,id_jugador
                        query_save_partida_jugador = """INSERT INTO partida_jugador
                                                        (nMuertes_partida,partida_id,id_jugador) 
                                                        VALUES (?,?,?)"""
                        cursor.execute(query_save_partida_jugador,data_jugador_partida)  
                        conn.commit() 
                        conn.close()
                    
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
                                #print("dentro de envío a otros jugadores")
                                socket_temporal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                try:
                                    socket_temporal.connect((self.GLOBAL.getOtherPlayersIndex(i)[1][4],self.GLOBAL.getOtherPlayersIndex(i)[1][5]))
                                    socket_temporal.sendall(msg_to_OtherPlayers.encode('utf-8'))
                                except:
                                    pass
                                finally:
                                    socket_temporal.close() #se cierra el socket al terminar
                    id_new_player = None


            except Exception as e:
                #print(e)
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
                        #print(self.GLOBAL.getOtherPlayers())
                        #print(id,jugador)
                        #print(msg,ip_dest,jugador[1][5])
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
            #MENSAJE TIPO 3 -> CHECK NOMBRE o personaje
            elif(len(resp) == 4):
                [pswd,id_user,contenido,objeto] = resp
                if (pswd != None and pswd == self.password and self.existsPlayer(id_user) and not self.isNotCurrentlyActive(id_user)):
                    if(contenido != None and contenido == "check_nombre"):
                        if(objeto != None):
                            return(3,objeto,id_user)
                        else:
                            return(-1,None)
                    else:
                        #toca deserializar a ver si funciona
                        try:
                            return(4,objeto,id_user)
                            #TODO: Comprobar dónde está cada usuario, y mandarles un mensaje de hacia donde tienen que ir
                        except:
                            return(-1,None)
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