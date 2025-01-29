import pygame
from pygame.locals import *
from pygame import mixer
import sqlite3
import socket
import threading

class SalaEspera:
    #sound

    def __init__(self,width,height,screen,ch1,ch2,ch3,ch4,icono,name,ml,ip,puerto,font,id):
        #screen
        self.screen = screen
        self.font = font

        #musica
        self.pressed =  pygame.mixer.Sound('sounds/button_pressed.wav')
        self.pressed_exit = pygame.mixer.Sound('sounds/button_pressed_ogg.ogg')
        self.selected = pygame.mixer.Sound('sounds/selected_button.wav')
        self.error = pygame.mixer.Sound('sounds/error.wav')

        #widht y height
        self.width = width
        self.height = height

        #canales
        self.ch1 = ch1
        self.ch2 = ch2
        self.ch3 = ch3
        self.ch4 = ch4

        #variables
        self.first_timeB = True # Aún no has pulsado el botón volver al menú
        self.first_timeC = True # Aún no has pulsado el botón cargar partida
        self.numJugadores = None
        self.currentPlayers = 1 #Por defecto siempre habrá 1 (tú mismo)
        self.isOnline = None
        self.otherPlayers = {}
        self.ip = ip
        self.puerto = puerto
        self.password = None
        self.server_socket = None 
        self.id = id
        

        #cargamos las imágenes del menú
        self.backgroundPic = pygame.image.load("images/background.png")
        self.buttonPic = pygame.image.load("images/button.png")
        self.buttonSelectedPic = pygame.image.load("images/button_selected.png")
        self.buttonPressedPic = pygame.image.load("images/button_pressed.png")
        self.capa = pygame.image.load("images/capa.png")
        self.bCreate = pygame.image.load("images/button_createPartida.png")
        self.bCreate_selected = pygame.image.load("images/button_createPartida_selected.png")
        self.bCreate_pressed = pygame.image.load("images/button_createPartida_pressed.png")
        self.buttonUnavailablePic = pygame.image.load("images/button_unavailable.png")
        self.avatarJugador = {}
        for i in range(0,6):
            self.avatarJugador[i] = pygame.image.load("images/iconos/icon_"+str(i)+".png")
        self.default = pygame.image.load("images/iconos/icon_default.png")
        self.default_red = pygame.image.load("images/iconos/icon_default_red.png")

        #fuentes y colores
        self.fuente = pygame.font.SysFont(font, 70)
        self.fuente2 = pygame.font.SysFont(font,600)
        self.color_white = (255,255,255)
        self.color_black = (0,0,0)
        self.color_light_pink = pygame.Color((234,135,255))
        self.back = self.fuente.render('Volver al menú', True, self.color_white)
        self.crearT = self.fuente.render('Cargar partida', True, self.color_white)
        self.labelTitle = None
        self.currentIcono = icono
        self.name = name
        self.max_lenght_name = ml

    def setScreen(self,screen):
        self.screen = screen
        #self.width,self.height= (self.screen.get_width(), self.screen.get_height())
    def getScreen(self):
        return self.screen
    def setCurrentPartida(self,p):
        self.currentPartida = p
    def setSelfIcono(self,icono):
        self.currentIcono = icono
    def setSelfName(self,name):
        self.name = name
    def setPassword(self,password):
        self.password = password

    def setNumJugadoresYOtherPlayers(self,no):
        self.numJugadores = no[0] #la lista otherPlayers nunca va a estar vacía, porque siempre se envía como mínimo el otro jugador
        cont = 0
        for i in range(0,(self.numJugadores-1)):
            if((i in no[1]) and (no[1][i][0] != self.id)):
                self.otherPlayers[cont] = no[1][i] 
            else:
                self.otherPlayers[cont] = None
            cont = cont+1

            


    def render(self,isOnline):
        #render screen
        self.letterwidth = (self.width/3.4286)/10 #cálculo de la base en píxeles 
        self.lettersize = int(self.letterwidth + 0.5 * self.letterwidth) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente3 = pygame.font.SysFont(self.font,self.lettersize)
        self.labelTitle = self.fuente3.render('-------- [ Jugadores ] --------',True, self.color_white)
        self.isOnline = isOnline
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
        if(isOnline):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            #el número de jugadores y la lista de otros jugadores se la pasa por parámetro en game
        else:
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/4.0956, self.height/12.2807)), (self.width/4.1379, self.height/1.1667))#293 57 290 600
            self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/3.3333, self.height/1.1570)) #150 40 360 605
            self.letterwidth3 = (self.width/3.4286)/18 #cálculo de la base en píxeles 
            self.lettersize3 = int(self.letterwidth3 + 0.5 * self.letterwidth3)
            self.fuente4 = pygame.font.SysFont(self.font,self.lettersize3)
            #--Cargar el número de jugadores de la partida--

            conn = sqlite3.connect("simuladordnd.db")
            cur = conn.cursor()
            if(self.currentPartida == "p1"):
                #cargamos la partida 1, si existe: el orden de las columnas será ese
                cur.execute("SELECT num_jugadores,server_code FROM partida WHERE numPartida = 'p1'")
                rows = cur.fetchall() #para llegar a esta pantalla, la pantalla tiene que existir sí o sí
                if(rows[0] != None and len(rows[0]) == 2):
                    self.numJugadores = rows[0][0]
                    self.password = rows[0][1]
                    for i in range(0,self.numJugadores):
                        self.otherPlayers[i] = None
                else:
                    print("Error: El atributo num_jugadores o server_code de la partida 1 está corrupto. Estableciendo valores por defecto...")
                    self.numJugadores = 1 #valor por defecto
                    query_update_numj = """UPDATE partida SET num_jugadores = 1 WHERE numPartida = 'p1';"""
                    self.password = "password"
                    query_update_psw = """UPDATE partida SET server_code = 'password' WHERE numPartida = 'p1';"""
                    cur.execute(query_update_numj)
                    cur.execute(query_update_psw)
                    conn.commit() 
            
            elif(self.currentPartida == "p2"):
                cur.execute("SELECT num_jugadores,server_code FROM partida WHERE numPartida = 'p2'")
                rows = cur.fetchall() #para llegar a esta pantalla, la pantalla tiene que existir sí o sí
                if(rows[0] != None):
                    self.numJugadores = rows[0][0]
                    self.password = rows[0][1]
                    for i in range(0,self.numJugadores):
                        self.otherPlayers[i] = None
                else:
                    print("Error: El atributo num_jugadores o server_code de la partida 2 está corrupto. Estableciendo valor por defecto...")
                    self.numJugadores = 1 #valor por defecto
                    query_update_numj = """UPDATE partida SET num_jugadores = 1 WHERE numPartida = 'p2';"""
                    self.password = "password"
                    query_update_psw = """UPDATE partida SET server_code = 'password' WHERE numPartida = 'p2';"""
                    cur.execute(query_update_numj)
                    cur.execute(query_update_psw)
                    conn.commit()
            elif(self.currentPartida == "p3"):
                cur.execute("SELECT num_jugadores,server_code FROM partida WHERE numPartida = 'p3'")
                rows = cur.fetchall() #para llegar a esta pantalla, la pantalla tiene que existir sí o sí
                if(rows[0] != None):
                    self.numJugadores = rows[0][0]
                    self.password = rows[0][1]
                    for i in range(0,self.numJugadores):
                        self.otherPlayers[i] = None
                else:
                    print("Error: El atributo num_jugadores o server_code de la partida 3 está corrupto. Estableciendo valor por defecto...")
                    self.numJugadores = 1 #valor por defecto
                    query_update_numj = """UPDATE partida SET num_jugadores = 1 WHERE numPartida = 'p3';"""
                    self.password = "password"
                    query_update_psw = """UPDATE partida SET server_code = 'password' WHERE numPartida = 'p2';"""
                    cur.execute(query_update_numj)
                    cur.execute(query_update_psw)
                    conn.commit()

            cur.close()
            conn.close() #cerramos la conexión con la bbdd
            if(self.numJugadores == self.currentPlayers):
                self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667)) #293 57 620 600
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.7884, self.height/1.1570)) #190 40 671 605 
            textPwd = "Contraseña de partida: "+self.password+" <-> Código: "+self.ip+":"+str(self.puerto)
            self.textPassword = self.fuente4.render(textPwd, True, self.color_light_pink)
            self.screen.blit(self.textPassword,(self.width/4.0000, self.height/7.0000)) #300 100
        #Título
        self.screen.blit(self.labelTitle, (self.width/3.4783, self.height/17.5000)) #345 40
        #Iconos de los jugadores

        for i in range(0,6):
            x_size = self.width/8.0000 #150
            y_size = self.width/8.0000
            x_start = (self.width/4.0000) +  ((self.width/5.2863)*(i%3)) #300 + 227*(i%3)
            y_start = (self.height/5.0000) +((self.height/3.0837)*(i//3)) #140 +227*(i//3)
            if(i//3 <1):
                y_start2 = self.height/2.3333  #300
            else:
                y_start2 = self.height/1.3283  #527 (140+227+150+10)

            self.letterwidth2 = (self.width/8.0000)/(self.max_lenght_name+1) #the width for 1 letter
            self.widthText2 = self.letterwidth2*self.max_lenght_name
    
            if(i == 0): #tú mismo
                spaces = self.max_lenght_name - len(self.name)
                one_side = spaces//2
                other_side = self.max_lenght_name - one_side - len(self.name)
                text_to_show = ' '
                inside = False
                for i in range(0,one_side):
                    if(i == 0):
                        text_to_show = ' '
                    text_to_show += ' '
                    inside = True
                if (inside):
                    text_to_show +=self.name
                else:
                    text_to_show = self.name
                    inside = False
                for i in range(0,other_side):
                    text_to_show += ' '
                self.textName = self.fuente.render(text_to_show, True, self.color_white)
                #self.screen.blit(pygame.transform.scale(self.avatarJugador[i], (114,114)), (173+154*(i%3),140+154*(i//3)))
                self.screen.blit(pygame.transform.scale(self.avatarJugador[self.currentIcono], (x_size, y_size)), (x_start, y_start))
                self.screen.blit(pygame.transform.scale(self.textName, (self.widthText2, self.height/17.5000)), (x_start, y_start2)) # x x 300 300
            else:
                #self.screen.blit(pygame.transform.scale(self.avatarJugador[i], (114,114)), (173+154*(i%3),140+154*(i//3)))
                if(i < self.numJugadores):
                    if(self.otherPlayers[i-1] != None):
                        #i: (id,(nombre,pic))
                        temp = self.otherPlayers[i-1][1][0] # el nombre
                        spaces = self.max_lenght_name - len(temp)
                        one_side = spaces//2
                        other_side = self.max_lenght_name - one_side - len(temp)
                        text_to_show = ' '
                        inside = False
                        for j in range(0,one_side):
                            if(j == 0):
                                text_to_show = ' '
                            text_to_show += ' '
                            inside = True
                        if (inside):
                            text_to_show +=temp
                        else:
                            text_to_show = temp
                            inside = False
                        for j in range(0,other_side):
                            text_to_show += ' '
                        self.textName = self.fuente.render(text_to_show, True, self.color_white)
                        self.screen.blit(pygame.transform.scale(self.avatarJugador[self.otherPlayers[i-1][1][1]], (x_size, y_size)), (x_start, y_start))#imagenes
                        self.screen.blit(pygame.transform.scale(self.textName, (self.widthText2, self.height/17.5000)), (x_start, y_start2)) # x x 300 300
                    else:
                        temp = "<?>"
                        spaces = self.max_lenght_name - len(temp)
                        one_side = spaces//2
                        other_side = self.max_lenght_name - one_side - len(temp)
                        text_to_show = ' '
                        inside = False
                        for j in range(0,one_side):
                            if(j == 0):
                                text_to_show = ' '
                            text_to_show += ' '
                            inside = True
                        if (inside):
                            text_to_show +=temp
                        else:
                            text_to_show = temp
                            inside = False
                        for j in range(0,other_side):
                            text_to_show += ' '
                        self.textName = self.fuente.render(text_to_show, True, self.color_white)
                        self.screen.blit(pygame.transform.scale(self.default, (x_size, y_size)), (x_start, y_start))#imagenes
                        self.screen.blit(pygame.transform.scale(self.textName, (self.widthText2, self.height/17.5000)), (x_start, y_start2)) # x x 300 300
                else:
                    self.screen.blit(pygame.transform.scale(self.default_red, (x_size, y_size)), (x_start, y_start))#imagenes
        pygame.display.update() 
        if(not self.isOnline and self.numJugadores > 1): #si vamos a permitir varios jugadores, iniciamos una conexión TCP
            # ------ servidor TCP ---------
            hiloEscuchaTCP = threading.Thread(target=self.escuchaTCP)
            hiloEscuchaTCP.start()
            # -----------------------------
    
    def existsPlayer(self,id):
        for i in range(0,len(self.otherPlayers)):
            if(self.otherPlayers[i] != None and id == self.otherPlayers[i][0]):
                print(self.otherPlayers[i][0])
                return True
            print(self.otherPlayers[i])
        return False

    def escuchaTCP(self):
        #Es multijugador
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.puerto))
        self.server_socket.listen() 
        while True:
            try:
                socket_c, ip_port_client = self.server_socket.accept()
                #print("msg received in server")
                msg_client = socket_c.recv(1024).decode('ascii')
                resp = self.checkformat(msg_client)
                print('msg received: ',msg_client)
                print(resp[0])
                print(resp[1][0])
                print(self.password)
                print(self.currentPlayers)
                print(self.numJugadores)
                print(resp[1][3])
                print(self.existsPlayer(resp[1][3]))
                if(resp[0] and (resp[1][0] == self.password) and ((self.currentPlayers < self.numJugadores) or self.existsPlayer(resp[1][3]))):
                    msg_ok = "ok:"+str(self.numJugadores)+":"+str(self.id)+";"+self.name+";"+str(self.currentIcono) #te pasas a ti mismo como jugador, para que te añada
                    for i in range(0,len(self.otherPlayers)):
                        if(self.otherPlayers[i] != None):
                            print(self.otherPlayers[i])
                            msg_ok = msg_ok+":"+str(self.otherPlayers[i][0])+";"+self.otherPlayers[i][1][0]+";"+str(self.otherPlayers[i][1][1])
                            #el mensaje tendrá este formato -> ok:4:id1;pepe;1:id2;juan;4
                    free_pos = -1
                    for i in range(0,len(self.otherPlayers)):
                        if(self.otherPlayers[i] == None): #si no se ha conectado nunca, lo añadimos
                            free_pos = i
                            for j in range(0,len(self.otherPlayers)):
                                if(self.otherPlayers[j] != None and self.otherPlayers[j][0] == resp[1][3]):
                                   break #así nos quedamos con esa i -> si el jugador existe, actualizamos su nombre y pic
                            break
                    self.otherPlayers[free_pos] = (resp[1][3],(resp[1][1],int(resp[1][2]))) #(id,(nombre,avatarPicPerfil) <- añado al jugador
                    self.currentPlayers = self.currentPlayers + 1
                    #es posible que se haya desconectado y se haya vuelto a conectar
                            
                    #print("self.otherPlayers = ",self.otherPlayers)
                    socket_c.sendall(msg_ok.encode('ascii'))
                else:
                    msg_no = "no"
                    socket_c.sendall(msg_no.encode('ascii'))
                socket_c.close()
            except:
                break

    def closeSocketTCPServer(self):
        if(self.server_socket != None):
            self.server_socket.close()

    def checkformat(self,msg):
        try:
            [password,nombre,pic,id] = msg.split(':')
            #print(password,nombre,pic,id)
            if(password != None and len(password) <= 16): #es la longitud de la password máxima
                if(nombre != None and len(nombre) <= 13):
                    if(pic != None and int(pic) >=0 and int(pic) <=6): #solo hay 6 iconos
                        if(id != None and id != ' '):
                            return (True,(password,nombre,pic,id))
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



    # size_x, size_y: tamaño del botón en x y en y
    # x_start y y_start: posición de la esquina izquierda del botón
    # pos_x y pos_y: posición actual del ratón
    def checkIfMouseIsInButton(self,size_x,size_y,x_start,y_start,pos_x,pos_y):
        if((pos_x >= x_start and pos_x <= size_x+x_start) and (pos_y >= y_start and pos_y <= size_y + y_start)):
            return True
        else:
            return False

    def clickedMouse(self):
        #click del ratón
        #calculo del tamaño del botón y su posición -> Empezar Simulación
        x_size = self.width/3.8339
        y_size = self.height/12.2807
        x_start = self.width/2.7907
        y_start = self.height/1.1667
        x_size2 = self.width/4.0956
        x_start2 = self.width/4.1379
        x_startC = self.width/1.9355
        (x,y) = pygame.mouse.get_pos()

        #Botón volver al menú en modo online
        if(self.isOnline and self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            self.ch1.play(self.pressed)
            pygame.display.update() 
            return 'menu'
        
        #Volver al menú siendo el líder de la partida
        elif(not self.isOnline and self.checkIfMouseIsInButton(x_size2,y_size,x_start2,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/4.0956, self.height/12.2807)), (self.width/4.1379, self.height/1.1667))#293 57 290 600
            self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/3.3333, self.height/1.1570)) #150 40 360 605
            if(self.numJugadores == self.currentPlayers):
                self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667)) #293 57 620 600
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.7884, self.height/1.1570)) #190 40 671 605 
            self.ch1.play(self.pressed)
            pygame.display.update() 
            return 'menu'
        
        #Botón cargar partida si eres el líder de la partida
        elif(not self.isOnline and self.checkIfMouseIsInButton(x_size2,y_size,x_startC,y_start,x,y)):
            pantalla = "partida"
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/4.0956, self.height/12.2807)), (self.width/4.1379, self.height/1.1667))#293 57 290 600
            self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/3.3333, self.height/1.1570)) #150 40 360 605
            if(self.numJugadores == self.currentPlayers):
                self.screen.blit(pygame.transform.scale(self.bCreate_pressed, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667)) #293 57 620 600
                self.ch1.play(self.pressed) 
                      
            else:
                pantalla = "salaEspera"
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667))
                self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.7884, self.height/1.1570)) #190 40 671 605 
                self.ch1.play(self.error)
            pygame.display.update() 
            return pantalla

        else:
            return 'salaEspera'
        

        

    def movedMouse(self):
        x_size = self.width/3.8339
        y_size = self.height/12.2807
        x_start = self.width/2.7907
        y_start = self.height/1.1667
        x_size2 = self.width/4.0956
        x_start2 = self.width/4.1379
        x_startC = self.width/1.9355
        (x,y) = pygame.mouse.get_pos()

        #Botón volver al menú si es online
        if(self.isOnline and self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(self.first_timeB):
                self.first_timeB = False
                self.first_timeC = True
                self.ch2.play(self.selected)     
            pygame.display.update() 

        #Botón voler al menú si eres el líder
        elif(not self.isOnline and self.checkIfMouseIsInButton(x_size2,y_size,x_start2,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/4.0956, self.height/12.2807)), (self.width/4.1379, self.height/1.1667))#293 57 290 600
            self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/3.3333, self.height/1.1570)) #150 40 360 605
            if(self.numJugadores == self.currentPlayers):
                self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667)) #293 57 620 600
                if(self.first_timeB):
                    self.first_timeB = False
                    self.first_timeC = True
                    self.ch2.play(self.selected)  
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667))
                if(self.first_timeB):
                    self.first_timeB = False
                    self.first_timeC = True
                    self.ch2.play(self.selected)  
            self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.7884, self.height/1.1570)) #190 40 671 605    
            pygame.display.update() 

        #Cargar partida si eres el líder
        elif(not self.isOnline and self.checkIfMouseIsInButton(x_size2,y_size,x_startC,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/4.0956, self.height/12.2807)), (self.width/4.1379, self.height/1.1667))#293 57 290 600
            self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/3.3333, self.height/1.1570)) #150 40 360 605
            if(self.numJugadores == self.currentPlayers):
                self.screen.blit(pygame.transform.scale(self.bCreate_selected, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667)) #293 57 620 600
                if(self.first_timeC):
                    self.first_timeC = False
                    self.first_timeB = True
                    self.ch2.play(self.selected) 
                      
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667))
                if(self.first_timeC):
                    self.first_timeC = False
                    self.first_timeB = True
            self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.7884, self.height/1.1570))
            pygame.display.update() 

        else:
            self.first_timeB = True
            self.first_timeC = True
            if(self.isOnline):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            else:
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/4.0956, self.height/12.2807)), (self.width/4.1379, self.height/1.1667))#293 57 290 600
                self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/3.3333, self.height/1.1570)) #150 40 360 605
                if(self.numJugadores == self.currentPlayers):
                    self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667)) #293 57 620 600
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667))
                self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.7884, self.height/1.1570)) #190 40 671 605 
            pygame.display.update() 
        
    
