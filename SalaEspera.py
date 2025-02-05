import pygame
from pygame.locals import *
from pygame import mixer
import sqlite3
import socket
import threading
from EscuchaTCP import EscuchaTCP
from EscuchaUDP import EscuchaUDP
from EnviarEstadoUDP import EnviarEstadoUDP
from Global import Global

class SalaEspera:
    #sound

    def __init__(self,width,height,screen,ch1,ch2,ch3,ch4,icono,name,ml,ip,puertoTCP,puertoUDP,font,id):
        #screen
        self.screen = screen
        self.font = font
        self.escuchaTCP = EscuchaTCP()
        self.escuchaUDP = EscuchaUDP()
        self.GLOBAL = Global() 
        self.enviarEstadoUDP = None #tenemos que esperarnos a recibir la variable isOnline para saber qué tipo de envío se hará

        #musica
        self.pressed =  pygame.mixer.Sound('sounds/button_pressed.wav')
        self.pressed_exit = pygame.mixer.Sound('sounds/button_pressed_ogg.ogg')
        self.selected = pygame.mixer.Sound('sounds/selected_button.wav')
        self.join = pygame.mixer.Sound('sounds/joinPartida.wav')

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
        self.isOnline = None
        self.activeOtherPlayers = {} #jugadores actualmente conectados -> lo emplean host y clientes
        self.ip = ip
        self.puerto = puertoTCP
        self.puertoUDP = puertoUDP
        self.ip_dest = None
        self.puertoUDP_server = None
        self.password = None
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
        self.avatarJugadorDefault = {}
        for i in range(0,6):
            self.avatarJugador[i] = pygame.image.load("images/iconos/icon_"+str(i)+".png")
            self.avatarJugadorDefault[i] = pygame.image.load("images/iconos/icon_"+str(i)+"_default.png")
        self.default = pygame.image.load("images/iconos/icon_default.png")
        self.default_red = pygame.image.load("images/iconos/icon_default_red.png")

        #fuentes y colores
        self.fuente = pygame.font.SysFont(font, 70)
        self.fuente2 = pygame.font.SysFont(font,600)
        self.color_white = (255,255,255)
        self.color_black = (0,0,0)
        self.color_light_pink = pygame.Color((234,135,255))
        self.color_grey = pygame.Color((208,208,208))
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
        #Other players en el cliente va a tener los jugadores activos que haya en ese momento
        #en el servidor es un registro de jugadores activos, donde se incluye una variable de actividad/no actividad
        self.numJugadores = no[0] #la lista otherPlayers nunca va a estar vacía, porque siempre se envía como mínimo el otro jugador
        self.puertoUDP_server = no[2]
        self.ip_dest = no[3]
        cont = 0
        for i in range(0,(self.numJugadores-1)):
            if((i in no[1]) and (no[1][i][0] != self.id)):
                self.GLOBAL.setOtherPlayersIndex(cont,no[1][i]) #jugadores que hay activos cuando te conectas al servidor
            else:
                self.GLOBAL.setOtherPlayersIndex(cont,None)
            cont = cont+1
        

    def refresh(self):
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
        if(self.isOnline):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            #el número de jugadores y la lista de otros jugadores se la pasa por parámetro en game
        else:
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/4.0956, self.height/12.2807)), (self.width/4.1379, self.height/1.1667))#293 57 290 600
            self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/3.3333, self.height/1.1570)) #150 40 360 605
            self.letterwidth3 = (self.width/3.4286)/18 #cálculo de la base en píxeles 
            self.lettersize3 = int(self.letterwidth3 + 0.5 * self.letterwidth3)
            self.fuente4 = pygame.font.SysFont(self.font,self.lettersize3)
            
            if(self.numJugadores == self.GLOBAL.getCurrentPlayers):
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
                    if(self.GLOBAL.getOtherPlayersIndex((i-1)) != None):
                        #i: (id,(nombre,pic))
                        temp = self.GLOBAL.getOtherPlayersIndex((i-1))[1][0] # el nombre
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
                        if(self.GLOBAL.getOtherPlayersIndex((i-1))[1][2]):
                            self.textName = self.fuente.render(text_to_show, True, self.color_white)
                            self.screen.blit(pygame.transform.scale(self.avatarJugador[self.GLOBAL.getOtherPlayersIndex((i-1))[1][1]], (x_size, y_size)), (x_start, y_start))#imagenes
                            self.screen.blit(pygame.transform.scale(self.textName, (self.widthText2, self.height/17.5000)), (x_start, y_start2)) # x x 300 300
                        else:
                            self.textName = self.fuente.render(text_to_show, True, self.color_grey)
                            self.screen.blit(pygame.transform.scale(self.avatarJugadorDefault[self.GLOBAL.getOtherPlayersIndex((i-1))[1][1]], (x_size, y_size)), (x_start, y_start))#imagenes
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
        self.ch1.play(self.join)
        pygame.display.update() 


    def render(self,isOnline):
        #render screen
        self.enviarEstadoUDP = EnviarEstadoUDP(isOnline,self.puertoUDP_server,self.ip_dest)
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
            self.GLOBAL.setOtherPlayers({}) #reiniciamos la lista de otherPlayers
            self.GLOBAL.setCurrentPlayers(1) #reiniciamos el número de jugadores actuales en partida
            print(self.GLOBAL.getOtherPlayers())
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
                    for i in range(0,self.numJugadores-1):
                        self.GLOBAL.setOtherPlayersIndex(i,None) #TODO: incluir actividad/no actividad cuando se extraiga de la bbdd
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
                    for i in range(0,self.numJugadores-1):
                        self.GLOBAL.setOtherPlayersIndex(i,None)
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
                    for i in range(0,self.numJugadores-1):
                        self.GLOBAL.setOtherPlayersIndex(i,None)
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
            if(self.numJugadores == self.GLOBAL.getCurrentPlayers):
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
                    if(self.GLOBAL.getOtherPlayersIndex((i-1)) != None):
                        #i: (id,(nombre,pic))
                        temp = self.GLOBAL.getOtherPlayersIndex((i-1))[1][0] # el nombre
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
                        self.screen.blit(pygame.transform.scale(self.avatarJugador[self.GLOBAL.getOtherPlayersIndex((i-1))[1][1]], (x_size, y_size)), (x_start, y_start))#imagenes
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
            # ------ servidor UDP y TCP ---------
            self.escuchaTCP.initialize(self.ip,self.puerto,self.password,self.numJugadores,self.id,self.name,self.currentIcono,self.puertoUDP)
            hiloEscuchaTCP = threading.Thread(target=self.escuchaTCP.escuchaTCP)
            hiloEscuchaTCP.start()
            # -----------------------------
        if(self.numJugadores >1): #tanto en cliente como en servidor vamos a usar UDP
            self.escuchaUDP.initialize(self.ip,self.puertoUDP)
            hiloMantenerConexionUDP = threading.Thread(target = self.escuchaUDP.escuchaUDP)
            hiloMantenerConexionUDP.start()
            hiloEnviarEstadoUDP = threading.Thread(target = self.enviarEstadoUDP.enviarEstadoUDP)
            hiloEnviarEstadoUDP.start()
    

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
            if(self.numJugadores == self.GLOBAL.getCurrentPlayers()):
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
            if(self.numJugadores == self.GLOBAL.getCurrentPlayers):
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
            if(self.numJugadores == self.GLOBAL.getCurrentPlayers):
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
            if(self.numJugadores == self.GLOBAL.getCurrentPlayers):
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
                if(self.numJugadores == self.GLOBAL.getCurrentPlayers):
                    self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667)) #293 57 620 600
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667))
                self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.7884, self.height/1.1570)) #190 40 671 605 
            pygame.display.update() 

        
    
