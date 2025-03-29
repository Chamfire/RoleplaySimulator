import pygame
from pygame.locals import *
from pygame import mixer
from EscuchaUDP import EscuchaUDP
from EnviarEstadoUDP import EnviarEstadoUDP
import threading
import socket
from Global import Global

class PartidaScreen:
    #sound

    def __init__(self,width,height,screen,ch1,ch2,ch3,ch4,font):
        #screen
        self.screen = screen
        self.justAfterSala = False

        #musica
        self.pressed =  pygame.mixer.Sound('sounds/button_pressed.wav')
        self.pressed_exit = pygame.mixer.Sound('sounds/button_pressed_ogg.ogg')
        self.selected = pygame.mixer.Sound('sounds/selected_button.wav')
        self.error = pygame.mixer.Sound('sounds/error.wav')

        #widht y height
        self.width = width
        self.height = height

        #si ya se había conectado antes (se establecen desde Game)
        self.puertoUDP = None
        self.ip_dest = None
        self.port_dest = None
        self.puertoUDP_server = None
        self.socketUDP = None
        self.escuchaUDP = None
        self.enviarEstadoUDP = None
        self.GLOBAL = Global()

        #canales
        self.ch1 = ch1
        self.ch2 = ch2
        self.ch3 = ch3
        self.ch4 = ch4
        
        self.personaje = None

        #variables
        self.first_timeB = True # Aún no has pulsado el botón volver al menú

        #cargamos las imágenes del menú
        self.backgroundPic = pygame.image.load("images/background.png")
        self.capa = pygame.image.load("images/capa.png")
        self.buttonPic = pygame.image.load("images/button.png")
        self.buttonSelectedPic = pygame.image.load("images/button_selected.png")
        self.buttonPressedPic = pygame.image.load("images/button_pressed.png")

        #fuentes y colores
        self.fuente = pygame.font.SysFont(font, 70)
        self.color_white = (255,255,255)
        self.color_black = (0,0,0)
        self.back = self.fuente.render('Volver al menú', True, self.color_white)
        self.msg = self.fuente.render('Partida', True, self.color_white)

    def setScreen(self,screen):
        self.screen = screen
        #self.width,self.height= (self.screen.get_width(), self.screen.get_height())
    def getScreen(self):
        return self.screen
    def setPersonajeMio(self,personaje):
        self.personaje = personaje

    def getPersonajeMio(self):
        return self.personaje
    def setJustAfterSala(self,v):
        self.justAfterSala = v

    def setIpANDPortDest(self,ip_y_port_y_pswd):
        self.ip_dest = ip_y_port_y_pswd[0]
        self.port_dest = ip_y_port_y_pswd[1]
        self.password =ip_y_port_y_pswd[2]
        self.isOnline = True

    def initUDPServerAndClient(self, puertoYSocket,puertoUDPServer,t,msg_delay,ip):
        self.puertoUDP = puertoYSocket[0]
        self.socketUDP = puertoYSocket[1]
        self.escuchaUDP = EscuchaUDP()
        self.puertoUDP_server = puertoUDPServer
        self.enviarEstadoUDP = EnviarEstadoUDP(True,self.puertoUDP_server,self.ip_dest,self.id,self.password,t,msg_delay)
        self.escuchaUDP.initialize(ip,self.puertoUDP,self.socketUDP,True,self.password,self.id)
        hiloMantenerConexionUDP = threading.Thread(target = self.escuchaUDP.escuchaUDP)
        hiloMantenerConexionUDP.start()
        hiloEnviarEstadoUDP = threading.Thread(target = self.enviarEstadoUDP.enviarEstadoUDP)
        hiloEnviarEstadoUDP.start()

    def render(self):
        #render screen
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
        self.screen.blit(pygame.transform.scale(self.msg, (self.width/1.8462, self.height/8.7500)), (self.width/4.0000, self.height/4.0000)) #650 80 300 175 
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
        self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
        if(self.justAfterSala):
            if(not self.isOnline):
                for i in range(0,len(self.GLOBAL.getOtherPlayers())):
                    if(self.GLOBAL.getOtherPlayersIndex(i) != None and self.GLOBAL.getOtherPlayersIndex(i)[1][2]): 
                        socket_temporal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        try:
                            socket_temporal.connect((self.GLOBAL.getOtherPlayersIndex(i)[1][4],self.GLOBAL.getOtherPlayersIndex(i)[1][5]))
                            msg = f"{self.password};{self.id};ve_partida_fromSalaEspera"
                            socket_temporal.sendall(msg.encode('utf-8'))
                        except:
                            pass
                        finally:
                            socket_temporal.close() #se cierra el socket al terminar
                self.justAfterSala = False #ya ha enviado los mensajes con los personajes existentes
        pygame.display.update() 

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
        (x,y) = pygame.mouse.get_pos()

        #Botón volver al menú
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            self.ch1.play(self.pressed)
            pygame.display.update() 
            return 'menu'
        else:
            return 'partida'
        

    def movedMouse(self):
        x_size = self.width/3.8339
        y_size = self.height/12.2807
        x_start = self.width/2.7907
        y_start = self.height/1.1667
        (x,y) = pygame.mouse.get_pos()

        #Botón volver al menú
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(self.first_timeB):
                self.first_timeB = False
                self.ch2.play(self.selected)     
            pygame.display.update() 

        else:
            self.first_timeB = True
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            pygame.display.update() 