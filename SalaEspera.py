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
from Personaje import Personaje

class SalaEspera:
    #sound

    def __init__(self,width,height,screen,ch1,ch2,ch3,ch4,icono,name,ml,ip,font,id,t,ch5,max_msg_delay):
        #screen
        self.screen = screen
        self.font = font
        self.max_msg_delay = max_msg_delay
        self.escuchaTCP = EscuchaTCP(ch5,max_msg_delay)
        self.escuchaUDP = EscuchaUDP()
        self.GLOBAL = Global() 
        self.enviarEstadoUDP = None #tenemos que esperarnos a recibir la variable isOnline para saber qué tipo de envío se hará
        self.socketTCP = None
        self.socketUDP = None
        self.t = t
        self.personaje = None #si lo extrae de la bbdd

        #musica
        self.pressed =  pygame.mixer.Sound('sounds/button_pressed.wav')
        self.pressed_exit = pygame.mixer.Sound('sounds/button_pressed_ogg.ogg')
        self.selected = pygame.mixer.Sound('sounds/selected_button.wav')
        self.join = pygame.mixer.Sound('sounds/joinPartida.wav')
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
        self.isOnline = None
        #self.activeOtherPlayers = {} #jugadores actualmente conectados -> lo emplean host y clientes
        self.ip = ip
        self.puerto = None
        self.puertoUDP = None
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
        self.color_light_red = pygame.Color((228,99,86))
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

    def getPersonaje(self):
        return self.personaje
    def getNumJugadores(self):
        return self.numJugadores

    def setPortUDPYSocketUDP(self,puertoYSocket): #solo la usará un jugador que se vaya a unir a la partida
        self.puertoUDP = puertoYSocket[0]
        self.socketUDP = puertoYSocket[1]

    def setNumJugadoresYOtherPlayers(self,no):
        #Other players en el cliente va a tener los jugadores activos que haya en ese momento
        #en el servidor es un registro de jugadores activos, donde se incluye una variable de actividad/no actividad
        self.numJugadores = no[0] #la lista otherPlayers nunca va a estar vacía, porque siempre se envía como mínimo el otro jugador
        self.puertoUDP_server = no[2]
        self.ip_dest = no[3]
        cont = 0
        #print(no)
        #print('numJugadores: ',self.numJugadores)
        for i in range(0,(self.numJugadores)): #te pueden pasar a ti mismo también
            if((i in no[1]) and (no[1][i][0] != self.id)):
                self.GLOBAL.setOtherPlayersIndex(cont,no[1][i]) #jugadores que hay activos cuando te conectas al servidor
                cont = cont+1
            elif((i in no[1]) and (no[1][i][0] == self.id)):
                pass 
            else:
                if(cont < (self.numJugadores - 1)):
                    self.GLOBAL.setOtherPlayersIndex(cont,None)
                    cont = cont+1
                #si el contador ya está a 2 para una partida de 3 jugadores, paramos
        #print('otherPlayers: ',self.GLOBAL.getOtherPlayers())
        
    def reload(self):
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
            if(self.numJugadores == self.GLOBAL.getCurrentPlayers()):
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
        pygame.display.update() 

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
            if(self.numJugadores == self.GLOBAL.getCurrentPlayers()):
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

    def findFreePort(self,isOnline):
        self.socketTCP.bind(('', 0)) #encuentra un puerto libre
        free_portTCP = self.socketTCP.getsockname()[1] #devuelve el nombre del puerto encontrado
        free_portUDP = None
        if(not isOnline): #si es online, ya se lo han pasado como parámetro el puerto UDP y el socket de UDP
            self.socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socketUDP.bind(('', 0)) #encuentra un puerto libre
            free_portUDP = self.socketUDP.getsockname()[1] #devuelve el nombre del puerto encontrado
        return (free_portTCP,free_portUDP)

    def getPassword(self):
        return self.password
    
    def getCurrentPartida(self):
        return self.currentPartida

    def render(self,isOnline):
        #render screen
        #abro socket TCP y UDP
        self.GLOBAL.setEnPartida()
        self.personaje = None #reiniciamos el personaje
        self.GLOBAL.setListaPersonajesHost({}) #se resetea la lista de personajes
        self.socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        (self.puerto,pudp) = self.findFreePort(isOnline) #pudp será distinto de none si no es online
        if(pudp != None):
            self.puertoUDP = pudp
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
            #print(self.GLOBAL.getOtherPlayers())
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
                    #cargamos los jugadores de esta partida
                    query_find_jugadores = "SELECT id_jugador FROM partida_jugador WHERE partida_id = 'p1' AND id_jugador != '"+self.id+"'"
                    cur.execute(query_find_jugadores)
                    rows2 = cur.fetchall()
                    for i in range(0,self.numJugadores-1):
                        #print(rows2,self.numJugadores)
                        if(rows2 != [] and i < len(rows2)): 
                            query_find_attr_jugador = "SELECT id_jugador,pic,name FROM jugador WHERE id_jugador = '"+rows2[i][0]+"'"
                            cur.execute(query_find_attr_jugador)
                            jugador = cur.fetchall()[0]
                            self.GLOBAL.setOtherPlayersIndex(i,(jugador[0],(jugador[2],jugador[1],False,None,None,None)))
                            #print(jugador)
                            #print(self.GLOBAL.getOtherPlayersIndex(i))
                        else:
                            self.GLOBAL.setOtherPlayersIndex(i,None) 
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
                    query_find_jugadores = "SELECT id_jugador FROM partida_jugador WHERE partida_id = 'p2' AND id_jugador != '"+self.id+"'"
                    cur.execute(query_find_jugadores)
                    rows2 = cur.fetchall()
                    #print(rows2)
                    for i in range(0,self.numJugadores-1):
                        if(rows2 != [] and i < len(rows2)): 
                            query_find_attr_jugador = "SELECT id_jugador,pic,name FROM jugador WHERE id_jugador = '"+rows2[i][0]+"'"
                            cur.execute(query_find_attr_jugador)
                            jugador = cur.fetchall()[0]
                            self.GLOBAL.setOtherPlayersIndex(i,(jugador[0],(jugador[2],jugador[1],False,None,None,None)))
                        else:
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
                    query_find_jugadores = "SELECT id_jugador FROM partida_jugador WHERE partida_id = 'p3' AND id_jugador != '"+self.id+"'"
                    cur.execute(query_find_jugadores)
                    rows2 = cur.fetchall()
                    for i in range(0,self.numJugadores-1):
                        if(rows2 != [] and i < len(rows2)): 
                            query_find_attr_jugador = "SELECT id_jugador,pic,name FROM jugador WHERE id_jugador = '"+rows2[i][0]+"'"
                            cur.execute(query_find_attr_jugador)
                            jugador = cur.fetchall()[0]
                            self.GLOBAL.setOtherPlayersIndex(i,(jugador[0],(jugador[2],jugador[1],False,None,None,None)))
                        else:
                            self.GLOBAL.setOtherPlayersIndex(i,None) 
                else:
                    print("Error: El atributo num_jugadores o server_code de la partida 3 está corrupto. Estableciendo valor por defecto...")
                    self.numJugadores = 1 #valor por defecto
                    query_update_numj = """UPDATE partida SET num_jugadores = 1 WHERE numPartida = 'p3';"""
                    self.password = "password"
                    query_update_psw = """UPDATE partida SET server_code = 'password' WHERE numPartida = 'p3';"""
                    cur.execute(query_update_numj)
                    cur.execute(query_update_psw)
                    conn.commit()

            cur.close()
            conn.close() #cerramos la conexión con la bbdd
            if(self.numJugadores == self.GLOBAL.getCurrentPlayers()):
                self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667)) #293 57 620 600
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.7884, self.height/1.1570)) #190 40 671 605 
            if(self.ip != None):
                textPwd = "Contraseña de partida: "+self.password+" <-> Código: "+self.ip+":"+str(self.puerto)
                self.textPassword = self.fuente4.render(textPwd, True, self.color_light_pink)
            else:
                textPwd = "No estás conectado a una red wifi. Si esperas a más jugadores, conéctate y reinicia el juego."
                self.textPassword = self.fuente4.render(textPwd, True, self.color_light_red)
            self.screen.blit(self.textPassword,(self.width/4.0000, self.height/7.0000)) #300 100
        #Título
        self.screen.blit(self.labelTitle, (self.width/3.4783, self.height/17.5000)) #345 40
        #Iconos de los jugadores
        self.enviarEstadoUDP = EnviarEstadoUDP(isOnline,self.puertoUDP_server,self.ip_dest,self.id,self.password,self.t,self.max_msg_delay)
        #print(self.GLOBAL.getOtherPlayers())
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
        pygame.display.update() 
        if(not self.isOnline and self.numJugadores > 1): #si vamos a permitir varios jugadores, iniciamos una conexión TCP
            # ------ servidor UDP y TCP ---------
            self.escuchaTCP.initialize(self.ip,self.puerto,self.password,self.numJugadores,self.id,self.name,self.currentIcono,self.puertoUDP,self.socketTCP,self.currentPartida)
            hiloEscuchaTCP = threading.Thread(target=self.escuchaTCP.escuchaTCP)
            hiloEscuchaTCP.start()
            # -----------------------------
        if(self.numJugadores >1): #se inicializa UDP en el servidor
            self.escuchaUDP.initialize(self.ip,self.puertoUDP,self.socketUDP,self.isOnline,self.password,self.id)
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
            self.GLOBAL.setNoEnPartida() #establecemos que se ha salido de la partida
            return 'menu'
        
        #Botón cargar partida si eres el líder de la partida
        elif(not self.isOnline and self.checkIfMouseIsInButton(x_size2,y_size,x_startC,y_start,x,y)):
            pantalla = "seleccionPersonaje"
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/4.0956, self.height/12.2807)), (self.width/4.1379, self.height/1.1667))#293 57 290 600
            self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/3.3333, self.height/1.1570)) #150 40 360 605
            if(self.numJugadores == self.GLOBAL.getCurrentPlayers()):
                self.screen.blit(pygame.transform.scale(self.bCreate_pressed, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667)) #293 57 620 600
                self.ch1.play(self.pressed) 
                #TODO:
                # Consulta para obtener todos los personajes VIVOS asociados a la partida.
                # Si todos los jugadores tienen un personaje vivo asociado -> carga directamente la partida, y envía mensaje TCP de cambio de pantalla
                # Si no todos los jugadores tienen un personaje vivo asociado -> envía a los jugadores sin personaje a la sala de seleccion de personaje, y al resto a la sala de espera 2
                # Si solo juega el host, no enviará ningun mensaje TCP, y solo puede ir a la pantalla de selección de personaje, o a la de partida, sin pasar por la sala de espera 2
                if(not self.isOnline):
                    conn = sqlite3.connect("simuladordnd.db")
                    cursor = conn.cursor()
                    query_take_characters = """SELECT name, sm1, sm2, sm3, nivel, inspiracion,esta_muerto,bpc,cons,fu,des,sab,car,int,coordenadas_actuales,vida_temp,max_vida,ca,edad,peso,pc,pp,pe,po,ppt,velocidad,descripcion_fisica,tipo_raza,tipo_clase,tipo_alineamiento,id_trasfondo,tipo_size,partida_id,id_jugador,num_npc_partida FROM personaje WHERE partida_id = '"""+self.currentPartida+"' AND esta_muerto = false"
                    cursor.execute(query_take_characters)
                    rows = cursor.fetchall()
                    if(self.numJugadores != 1):
                        players_for_finding_character = self.GLOBAL.getOtherPlayers()
                        num_personajes_to_find = len(players_for_finding_character) + 1 #+1 por el host
                    
                    if rows != []:
                        for row in rows:
                            if(self.numJugadores != 1):
                                #varios jugadores -> conectados online
                                for i,players in players_for_finding_character.items():
                                    if(row[33] == players[0]):
                                        #ese jugador tiene un personaje vivo asociado (su id coincide con la id de jugador de ese personaje)
                                        personaje_temp = Personaje(False,self.currentPartida,row[33])
                                        personaje_temp.name = row[0]
                                        personaje_temp.sm1 = row[1]
                                        personaje_temp.sm2 = row[2]
                                        personaje_temp.sm3 = row[3]
                                        personaje_temp.nivel = row[4]
                                        personaje_temp.inspiracion = row[5]
                                        personaje_temp.esta_muerto = row[6]
                                        personaje_temp.bpc = row[7]
                                        personaje_temp.cons = row[8]
                                        personaje_temp.fu = row[9]
                                        personaje_temp.initEquipo()
                                        personaje_temp.des = row[10]
                                        personaje_temp.sab = row[11]
                                        personaje_temp.car = row[12]
                                        personaje_temp.int = row[13]
                                        personaje_temp.coordenadas_actuales = row[14]
                                        personaje_temp.vida_temp = row[15]
                                        personaje_temp.max_vida = row[16]
                                        personaje_temp.ca = row[17]
                                        personaje_temp.edad = row[18]
                                        personaje_temp.peso = row[19]
                                        personaje_temp.pc = row[20]
                                        personaje_temp.pp = row[21]
                                        personaje_temp.pe = row[22]
                                        personaje_temp.po = row[23]
                                        personaje_temp.ppt = row[24]
                                        personaje_temp.velocidad = row[25]
                                        personaje_temp.descripcion_fisica = row[26]
                                        personaje_temp.tipo_raza = row[27]
                                        personaje_temp.tipo_clase = row[28]
                                        personaje_temp.tipo_alineamiento = row[29]
                                        personaje_temp.id_trasfondo = row[30]
                                        personaje_temp.tipo_size = row[31]
                                        personaje_temp.partida_id = row[32]
                                        personaje_temp.id_jugador = row[33]
                                        personaje_temp.num_npc_partida = row[34]

                                        #idiomas con competencia
                                        query_get_comp_idioma = """SELECT tipo_language,name,partida_id,id_jugador,num_npc_partida FROM comp_idioma WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"'"
                                        cursor.execute(query_get_comp_idioma)
                                        rows = cursor.fetchall()
                                        for row in rows:
                                            personaje_temp.idiomas_competencia[row[0]] = True
                                        
                                        #salvaciones de competencia
                                        query_get_salvaciones_comp = """SELECT tipo_caracteristica,name,partida_id,id_jugador,num_npc_partida FROM salvaciones_comp WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"'"
                                        cursor.execute(query_get_salvaciones_comp)
                                        rows = cursor.fetchall()
                                        for row in rows:
                                            personaje_temp.salvaciones_comp[row[0]] = True
                                        
                                        #habilidades de competencia
                                        query_get_habilidades_comp = """SELECT tipo_habilidad,name,partida_id,id_jugador,num_npc_partida FROM habilidades_comp WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"'"
                                        cursor.execute(query_get_habilidades_comp)
                                        rows = cursor.fetchall()
                                        for row in rows:
                                            personaje_temp.habilidades_comp[row[0]] = True
                                        
                                        #inventario
                                        query_get_inventario_basico = """SELECT cantidad,name_obj,categoria_obj,name,partida_id,id_jugador,num_npc_partida,procedencia,lista_nombre,slot FROM inventario WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"' AND procedencia = 'Equipo'"
                                        cursor.execute(query_get_inventario_basico)
                                        rows = cursor.fetchall()
                                        slot_name = {}
                                        if(rows != []):
                                            for row in rows:
                                                #cada fila es un objeto del inventario de ese jugador
                                                    if(row[8] == 'Arma'):
                                                        for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                            personaje_temp.equipo.addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getArmasList()[row[2]][row[1]],row[2],row[1])
                                                    elif(row[8] == 'Objeto_de_Espacio'):
                                                        for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                            personaje_temp.equipo.addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]],row[2],row[1])
                                                    elif(row[8] == 'Objeto'):
                                                        for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                            personaje_temp.equipo.addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]],row[2],row[1])
                                                    elif(row[8] == 'Armadura'):
                                                        for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                            personaje_temp.equipo.addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getArmaduraList()[row[2]][row[1]],row[2],row[1])
                                                    elif(row[8] == 'Escudo'):
                                                        for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                            personaje_temp.equipo.addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getEscudosList()[row[2]][row[1]],row[2],row[1])

                                        #coger inventario de la mochila
                                        if(slot_name != {}): #hay mochilas en su inventario
                                            query_get_inventario_mochila = """SELECT cantidad,name_obj,categoria_obj,name,partida_id,id_jugador,num_npc_partida,procedencia,lista_nombre,slot FROM inventario WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"' AND procedencia = 'Mochila'"
                                            cursor.execute(query_get_inventario_mochila)
                                            rows = cursor.fetchall()
                                            if(rows != []):
                                                for row in rows:
                                                    #cada fila es un objeto del inventario de la mochila de ese jugador
                                                    if(row[8] == 'Arma'):
                                                        for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                            personaje_temp.equipo.objetos[row["Almacenaje"][row[7]]].addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getArmasList()[row[2]][row[1]],row[2],row[1])
                                                    elif(row[8] == 'Objeto_de_Espacio'):
                                                        for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                            personaje_temp.equipo.objetos[row["Almacenaje"][row[7]]].addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]],row[2],row[1])
                                                    elif(row[8] == 'Objeto'):
                                                        for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                            personaje_temp.equipo.objetos[row["Almacenaje"][row[7]]].addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]],row[2],row[1])
                                                    elif(row[8] == 'Armadura'):
                                                        for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                            personaje_temp.equipo.objetos[row["Almacenaje"][row[7]]].addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getArmaduraList()[row[2]][row[1]],row[2],row[1])
                                                    elif(row[8] == 'Escudo'):
                                                        for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                            personaje_temp.equipo.objetos[row["Almacenaje"][row[7]]].addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getEscudosList()[row[2]][row[1]],row[2],row[1])

                                        #armadura equipada
                                        query_get_armor_equiped = """SELECT cantidad,name_obj,categoria_obj,name,partida_id,id_jugador,num_npc_partida,procedencia,lista_nombre,slot FROM inventario WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"' AND procedencia = 'Armadura actual'"
                                        cursor.execute(query_get_armor_equiped)
                                        rows = cursor.fetchall()
                                        if(rows != []):
                                            row = rows[0]
                                            personaje_temp.equipo.armadura_actual = [row[2],row[1],personaje_temp.equipo.listaInventario.getArmaduraList()[row[2]][row[1]]]
                                        
                                        #objeto mano derecha equipado
                                        query_get_objeto_mano_derecha = """SELECT cantidad,name_obj,categoria_obj,name,partida_id,id_jugador,num_npc_partida,procedencia,lista_nombre,slot FROM inventario WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"' AND procedencia = 'Mano derecha'"
                                        cursor.execute(query_get_objeto_mano_derecha)
                                        rows = cursor.fetchall()
                                        if(rows != []):
                                            row = rows[0]
                                            if(row[2] == 'Arma'):
                                                personaje_temp.equipo.objeto_equipado_mano_derecha = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getArmasList()[row[2]][row[1]]]
                                            elif(row[2] == 'Objeto_de_Espacio'):
                                                personaje_temp.equipo.objeto_equipado_mano_derecha = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]]]
                                            elif(row[2] == 'Objeto'):
                                                personaje_temp.equipo.objeto_equipado_mano_derecha = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]]]
                                            elif(row[2] == 'Armadura'):
                                                personaje_temp.equipo.objeto_equipado_mano_derecha = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getArmaduraList()[row[2]][row[1]]]
                                            elif(row[2] == 'Escudo'):
                                                personaje_temp.equipo.objeto_equipado_mano_derecha = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getEscudosList()[row[2]][row[1]]]
                                            
                                        #objeto mano izquierda equipado
                                        query_get_objeto_mano_izquierda = """SELECT cantidad,name_obj,categoria_obj,name,partida_id,id_jugador,num_npc_partida,procedencia,lista_nombre,slot FROM inventario WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"' AND procedencia = 'Mano izquierda'"
                                        cursor.execute(query_get_objeto_mano_izquierda)
                                        rows = cursor.fetchall()
                                        if(rows != []):
                                            row = rows[0]
                                            if(row[2] == 'Arma'):
                                                personaje_temp.equipo.objeto_equipado_mano_izquierda = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getArmasList()[row[2]][row[1]]]
                                            elif(row[2] == 'Objeto_de_Espacio'):
                                                personaje_temp.equipo.objeto_equipado_mano_izquierda = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]]]
                                            elif(row[2] == 'Objeto'):
                                                personaje_temp.equipo.objeto_equipado_mano_izquierda = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]]]
                                            elif(row[2] == 'Armadura'):
                                                personaje_temp.equipo.objeto_equipado_mano_izquierda = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getArmaduraList()[row[2]][row[1]]]
                                            elif(row[2] == 'Escudo'):
                                                personaje_temp.equipo.objeto_equipado_mano_izquierda = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getEscudosList()[row[2]][row[1]]]
                                            

                                        self.GLOBAL.setListaPersonajeHostIndex(row[33],personaje_temp)
                                        num_personajes_to_find -=1
                                        break #saltas el bucle, y continúas con el siguiente personaje de la lista
                                        
                                if(row[33] == self.id):
                                    #el host tiene personaje asociado
                                    #ese jugador tiene un personaje vivo asociado (su id coincide con la id de jugador de ese personaje)
                                    personaje_temp = Personaje(False,self.currentPartida,row[33])
                                    personaje_temp.name = row[0]
                                    personaje_temp.sm1 = row[1]
                                    personaje_temp.sm2 = row[2]
                                    personaje_temp.sm3 = row[3]
                                    personaje_temp.nivel = row[4]
                                    personaje_temp.inspiracion = row[5]
                                    personaje_temp.esta_muerto = row[6]
                                    personaje_temp.bpc = row[7]
                                    personaje_temp.cons = row[8]
                                    personaje_temp.fu = row[9]
                                    personaje_temp.initEquipo()
                                    personaje_temp.des = row[10]
                                    personaje_temp.sab = row[11]
                                    personaje_temp.car = row[12]
                                    personaje_temp.int = row[13]
                                    personaje_temp.coordenadas_actuales = row[14]
                                    personaje_temp.vida_temp = row[15]
                                    personaje_temp.max_vida = row[16]
                                    personaje_temp.ca = row[17]
                                    personaje_temp.edad = row[18]
                                    personaje_temp.peso = row[19]
                                    personaje_temp.pc = row[20]
                                    personaje_temp.pp = row[21]
                                    personaje_temp.pe = row[22]
                                    personaje_temp.po = row[23]
                                    personaje_temp.ppt = row[24]
                                    personaje_temp.velocidad = row[25]
                                    personaje_temp.descripcion_fisica = row[26]
                                    personaje_temp.tipo_raza = row[27]
                                    personaje_temp.tipo_clase = row[28]
                                    personaje_temp.tipo_alineamiento = row[29]
                                    personaje_temp.id_trasfondo = row[30]
                                    personaje_temp.tipo_size = row[31]
                                    personaje_temp.partida_id = row[32]
                                    personaje_temp.id_jugador = row[33]
                                    personaje_temp.num_npc_partida = row[34]

                                    #idiomas con competencia
                                    query_get_comp_idioma = """SELECT tipo_language,name,partida_id,id_jugador,num_npc_partida FROM comp_idioma WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"'"
                                    cursor.execute(query_get_comp_idioma)
                                    rows = cursor.fetchall()
                                    for row in rows:
                                        personaje_temp.idiomas_competencia[row[0]] = True
                                        
                                    #salvaciones de competencia
                                    query_get_salvaciones_comp = """SELECT tipo_caracteristica,name,partida_id,id_jugador,num_npc_partida FROM salvaciones_comp WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"'"
                                    cursor.execute(query_get_salvaciones_comp)
                                    rows = cursor.fetchall()
                                    for row in rows:
                                        personaje_temp.salvaciones_comp[row[0]] = True
                                        
                                    #habilidades de competencia
                                    query_get_habilidades_comp = """SELECT tipo_habilidad,name,partida_id,id_jugador,num_npc_partida FROM habilidades_comp WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"'"
                                    cursor.execute(query_get_habilidades_comp)
                                    rows = cursor.fetchall()
                                    for row in rows:
                                        personaje_temp.habilidades_comp[row[0]] = True
                                        
                                    #inventario
                                    query_get_inventario_basico = """SELECT cantidad,name_obj,categoria_obj,name,partida_id,id_jugador,num_npc_partida,procedencia,lista_nombre,slot FROM inventario WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"' AND procedencia = 'Equipo'"
                                    cursor.execute(query_get_inventario_basico)
                                    rows = cursor.fetchall()
                                    slot_name = {}
                                    if(rows != []):
                                        for row in rows:
                                            #cada fila es un objeto del inventario de ese jugador
                                                if(row[8] == 'Arma'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getArmasList()[row[2]][row[1]],row[2],row[1])
                                                elif(row[8] == 'Objeto_de_Espacio'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]],row[2],row[1])
                                                elif(row[8] == 'Objeto'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]],row[2],row[1])
                                                elif(row[8] == 'Armadura'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getArmaduraList()[row[2]][row[1]],row[2],row[1])
                                                elif(row[8] == 'Escudo'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getEscudosList()[row[2]][row[1]],row[2],row[1])

                                    #coger inventario de la mochila
                                    if(slot_name != {}): #hay mochilas en su inventario
                                        query_get_inventario_mochila = """SELECT cantidad,name_obj,categoria_obj,name,partida_id,id_jugador,num_npc_partida,procedencia,lista_nombre,slot FROM inventario WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"' AND procedencia = 'Mochila'"
                                        cursor.execute(query_get_inventario_mochila)
                                        rows = cursor.fetchall()
                                        if(rows != []):
                                            for row in rows:
                                                #cada fila es un objeto del inventario de la mochila de ese jugador
                                                if(row[8] == 'Arma'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.objetos[row["Almacenaje"][row[7]]].addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getArmasList()[row[2]][row[1]],row[2],row[1])
                                                elif(row[8] == 'Objeto_de_Espacio'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.objetos[row["Almacenaje"][row[7]]].addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]],row[2],row[1])
                                                elif(row[8] == 'Objeto'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.objetos[row["Almacenaje"][row[7]]].addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]],row[2],row[1])
                                                elif(row[8] == 'Armadura'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.objetos[row["Almacenaje"][row[7]]].addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getArmaduraList()[row[2]][row[1]],row[2],row[1])
                                                elif(row[8] == 'Escudo'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.objetos[row["Almacenaje"][row[7]]].addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getEscudosList()[row[2]][row[1]],row[2],row[1])
                                    
                                    #armadura equipada
                                    query_get_armor_equiped = """SELECT cantidad,name_obj,categoria_obj,name,partida_id,id_jugador,num_npc_partida,procedencia,lista_nombre,slot FROM inventario WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"' AND procedencia = 'Armadura actual'"
                                    cursor.execute(query_get_armor_equiped)
                                    rows = cursor.fetchall()
                                    if(rows != []):
                                        row = rows[0]
                                        personaje_temp.equipo.armadura_actual = [row[2],row[1],personaje_temp.equipo.listaInventario.getArmaduraList()[row[2]][row[1]]]
                                        
                                    #objeto mano derecha equipado
                                    query_get_objeto_mano_derecha = """SELECT cantidad,name_obj,categoria_obj,name,partida_id,id_jugador,num_npc_partida,procedencia,lista_nombre,slot FROM inventario WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"' AND procedencia = 'Mano derecha'"
                                    cursor.execute(query_get_objeto_mano_derecha)
                                    rows = cursor.fetchall()
                                    if(rows != []):
                                        row = rows[0]
                                        if(row[2] == 'Arma'):
                                            personaje_temp.equipo.objeto_equipado_mano_derecha = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getArmasList()[row[2]][row[1]]]
                                        elif(row[2] == 'Objeto_de_Espacio'):
                                            personaje_temp.equipo.objeto_equipado_mano_derecha = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]]]
                                        elif(row[2] == 'Objeto'):
                                            personaje_temp.equipo.objeto_equipado_mano_derecha = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]]]
                                        elif(row[2] == 'Armadura'):
                                            personaje_temp.equipo.objeto_equipado_mano_derecha = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getArmaduraList()[row[2]][row[1]]]
                                        elif(row[2] == 'Escudo'):
                                            personaje_temp.equipo.objeto_equipado_mano_derecha = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getEscudosList()[row[2]][row[1]]]
                                            
                                    #objeto mano izquierda equipado
                                    query_get_objeto_mano_izquierda = """SELECT cantidad,name_obj,categoria_obj,name,partida_id,id_jugador,num_npc_partida,procedencia,lista_nombre,slot FROM inventario WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"' AND procedencia = 'Mano izquierda'"
                                    cursor.execute(query_get_objeto_mano_izquierda)
                                    rows = cursor.fetchall()
                                    if(rows != []):
                                        row = rows[0]
                                        if(row[2] == 'Arma'):
                                            personaje_temp.equipo.objeto_equipado_mano_izquierda = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getArmasList()[row[2]][row[1]]]
                                        elif(row[2] == 'Objeto_de_Espacio'):
                                            personaje_temp.equipo.objeto_equipado_mano_izquierda = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]]]
                                        elif(row[2] == 'Objeto'):
                                            personaje_temp.equipo.objeto_equipado_mano_izquierda = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]]]
                                        elif(row[2] == 'Armadura'):
                                            personaje_temp.equipo.objeto_equipado_mano_izquierda = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getArmaduraList()[row[2]][row[1]]]
                                        elif(row[2] == 'Escudo'):
                                            personaje_temp.equipo.objeto_equipado_mano_izquierda = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getEscudosList()[row[2]][row[1]]]
                                    self.personaje = personaje_temp      
                                    
                                    num_personajes_to_find -=1
                                    if(num_personajes_to_find >0):
                                        pantalla = 'partida_load_wait' #a alguno le falta, pero el host tiene
                                    else:
                                        pantalla = 'partida' #todos tienen personaje
                                #else: pantalla = seleccionPersonaje
                            #solo 1 jugador
                            else:
                                if(row[33] == self.id):
                                    personaje_temp = Personaje(False,self.currentPartida,row[33])
                                    personaje_temp.name = row[0]
                                    personaje_temp.sm1 = row[1]
                                    personaje_temp.sm2 = row[2]
                                    personaje_temp.sm3 = row[3]
                                    personaje_temp.nivel = row[4]
                                    personaje_temp.inspiracion = row[5]
                                    personaje_temp.esta_muerto = row[6]
                                    personaje_temp.bpc = row[7]
                                    personaje_temp.cons = row[8]
                                    personaje_temp.fu = row[9]
                                    personaje_temp.initEquipo()
                                    personaje_temp.des = row[10]
                                    personaje_temp.sab = row[11]
                                    personaje_temp.car = row[12]
                                    personaje_temp.int = row[13]
                                    personaje_temp.coordenadas_actuales = row[14]
                                    personaje_temp.vida_temp = row[15]
                                    personaje_temp.max_vida = row[16]
                                    personaje_temp.ca = row[17]
                                    personaje_temp.edad = row[18]
                                    personaje_temp.peso = row[19]
                                    personaje_temp.pc = row[20]
                                    personaje_temp.pp = row[21]
                                    personaje_temp.pe = row[22]
                                    personaje_temp.po = row[23]
                                    personaje_temp.ppt = row[24]
                                    personaje_temp.velocidad = row[25]
                                    personaje_temp.descripcion_fisica = row[26]
                                    personaje_temp.tipo_raza = row[27]
                                    personaje_temp.tipo_clase = row[28]
                                    personaje_temp.tipo_alineamiento = row[29]
                                    personaje_temp.id_trasfondo = row[30]
                                    personaje_temp.tipo_size = row[31]
                                    personaje_temp.partida_id = row[32]
                                    personaje_temp.id_jugador = row[33]
                                    personaje_temp.num_npc_partida = row[34]

                                    #idiomas con competencia
                                    query_get_comp_idioma = """SELECT tipo_language,name,partida_id,id_jugador,num_npc_partida FROM comp_idioma WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"'"
                                    cursor.execute(query_get_comp_idioma)
                                    rows = cursor.fetchall()
                                    for row in rows:
                                        personaje_temp.idiomas_competencia[row[0]] = True
                                        
                                    #salvaciones de competencia
                                    query_get_salvaciones_comp = """SELECT tipo_caracteristica,name,partida_id,id_jugador,num_npc_partida FROM salvaciones_comp WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"'"
                                    cursor.execute(query_get_salvaciones_comp)
                                    rows = cursor.fetchall()
                                    for row in rows:
                                        personaje_temp.salvaciones_comp[row[0]] = True
                                        
                                    #habilidades de competencia
                                    query_get_habilidades_comp = """SELECT tipo_habilidad,name,partida_id,id_jugador,num_npc_partida FROM habilidades_comp WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"'"
                                    cursor.execute(query_get_habilidades_comp)
                                    rows = cursor.fetchall()
                                    for row in rows:
                                        personaje_temp.habilidades_comp[row[0]] = True
                                        
                                    #inventario
                                    query_get_inventario_basico = """SELECT cantidad,name_obj,categoria_obj,name,partida_id,id_jugador,num_npc_partida,procedencia,lista_nombre,slot FROM inventario WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"' AND procedencia = 'Equipo'"
                                    cursor.execute(query_get_inventario_basico)
                                    rows = cursor.fetchall()
                                    slot_name = {}
                                    if(rows != []):
                                        for row in rows:
                                            #cada fila es un objeto del inventario de ese jugador
                                                if(row[8] == 'Arma'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getArmasList()[row[2]][row[1]],row[2],row[1])
                                                elif(row[8] == 'Objeto_de_Espacio'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]],row[2],row[1])
                                                elif(row[8] == 'Objeto'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]],row[2],row[1])
                                                elif(row[8] == 'Armadura'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getArmaduraList()[row[2]][row[1]],row[2],row[1])
                                                elif(row[8] == 'Escudo'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getEscudosList()[row[2]][row[1]],row[2],row[1])

                                    #coger inventario de la mochila
                                    if(slot_name != {}): #hay mochilas en su inventario
                                        query_get_inventario_mochila = """SELECT cantidad,name_obj,categoria_obj,name,partida_id,id_jugador,num_npc_partida,procedencia,lista_nombre,slot FROM inventario WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"' AND procedencia = 'Mochila'"
                                        cursor.execute(query_get_inventario_mochila)
                                        rows = cursor.fetchall()
                                        if(rows != []):
                                            for row in rows:
                                                #cada fila es un objeto del inventario de la mochila de ese jugador
                                                if(row[8] == 'Arma'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.objetos[row["Almacenaje"][row[7]]].addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getArmasList()[row[2]][row[1]],row[2],row[1])
                                                elif(row[8] == 'Objeto_de_Espacio'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.objetos[row["Almacenaje"][row[7]]].addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]],row[2],row[1])
                                                elif(row[8] == 'Objeto'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.objetos[row["Almacenaje"][row[7]]].addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]],row[2],row[1])
                                                elif(row[8] == 'Armadura'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.objetos[row["Almacenaje"][row[7]]].addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getArmaduraList()[row[2]][row[1]],row[2],row[1])
                                                elif(row[8] == 'Escudo'):
                                                    for i in range(0,row[0]): #añades tantos objetos como cantidad indique
                                                        personaje_temp.equipo.objetos[row["Almacenaje"][row[7]]].addObjectToSpecificSlotInInventory(row[9],personaje_temp.equipo.listaInventario.getEscudosList()[row[2]][row[1]],row[2],row[1])
                                
                                    #armadura equipada
                                    query_get_armor_equiped = """SELECT cantidad,name_obj,categoria_obj,name,partida_id,id_jugador,num_npc_partida,procedencia,lista_nombre,slot FROM inventario WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"' AND procedencia = 'Armadura actual'"
                                    cursor.execute(query_get_armor_equiped)
                                    rows = cursor.fetchall()
                                    if(rows != []):
                                        row = rows[0]
                                        personaje_temp.equipo.armadura_actual = [row[2],row[1],personaje_temp.equipo.listaInventario.getArmaduraList()[row[2]][row[1]]]
                                        
                                    #objeto mano derecha equipado
                                    query_get_objeto_mano_derecha = """SELECT cantidad,name_obj,categoria_obj,name,partida_id,id_jugador,num_npc_partida,procedencia,lista_nombre,slot FROM inventario WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"' AND procedencia = 'Mano derecha'"
                                    cursor.execute(query_get_objeto_mano_derecha)
                                    rows = cursor.fetchall()
                                    if(rows != []):
                                        row = rows[0]
                                        if(row[2] == 'Arma'):
                                            personaje_temp.equipo.objeto_equipado_mano_derecha = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getArmasList()[row[2]][row[1]]]
                                        elif(row[2] == 'Objeto_de_Espacio'):
                                            personaje_temp.equipo.objeto_equipado_mano_derecha = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]]]
                                        elif(row[2] == 'Objeto'):
                                            personaje_temp.equipo.objeto_equipado_mano_derecha = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]]]
                                        elif(row[2] == 'Armadura'):
                                            personaje_temp.equipo.objeto_equipado_mano_derecha = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getArmaduraList()[row[2]][row[1]]]
                                        elif(row[2] == 'Escudo'):
                                            personaje_temp.equipo.objeto_equipado_mano_derecha = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getEscudosList()[row[2]][row[1]]]
                                            
                                    #objeto mano izquierda equipado
                                    query_get_objeto_mano_izquierda = """SELECT cantidad,name_obj,categoria_obj,name,partida_id,id_jugador,num_npc_partida,procedencia,lista_nombre,slot FROM inventario WHERE partida_id = '"""+self.currentPartida+"' AND name = '"+personaje_temp.name+"' AND id_jugador = '"+personaje_temp.id_jugador+"' AND procedencia = 'Mano izquierda'"
                                    cursor.execute(query_get_objeto_mano_izquierda)
                                    rows = cursor.fetchall()
                                    if(rows != []):
                                        row = rows[0]
                                        if(row[2] == 'Arma'):
                                            personaje_temp.equipo.objeto_equipado_mano_izquierda = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getArmasList()[row[2]][row[1]]]
                                        elif(row[2] == 'Objeto_de_Espacio'):
                                            personaje_temp.equipo.objeto_equipado_mano_izquierda = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]]]
                                        elif(row[2] == 'Objeto'):
                                            personaje_temp.equipo.objeto_equipado_mano_izquierda = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getObjetosList()[row[2]][row[1]]]
                                        elif(row[2] == 'Armadura'):
                                            personaje_temp.equipo.objeto_equipado_mano_izquierda = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getArmaduraList()[row[2]][row[1]]]
                                        elif(row[2] == 'Escudo'):
                                            personaje_temp.equipo.objeto_equipado_mano_izquierda = [row[0],row[2],row[1],personaje_temp.equipo.listaInventario.getEscudosList()[row[2]][row[1]]]

                                    self.personaje = personaje_temp
                                    #self.personaje.equipo.printEquipoConsolaDebugSuperficial()
                                    #el host tiene personaje asociado
                                    pantalla = 'partida' #solo está el host, así que pasa directamente a partida
                                    #else: pantalla = seleccionPersonaje

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
            if(self.numJugadores == self.GLOBAL.getCurrentPlayers()):
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
            if(self.numJugadores == self.GLOBAL.getCurrentPlayers()):
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
                if(self.numJugadores == self.GLOBAL.getCurrentPlayers()):
                    self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667)) #293 57 620 600
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667))
                self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.7884, self.height/1.1570)) #190 40 671 605 
            pygame.display.update() 

        
    
