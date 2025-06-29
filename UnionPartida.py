import pygame
from pygame.locals import *
from pygame import mixer
from EscuchaTCPClient import EscuchaTCPClient
import socket
import threading
import pickle
import base64
from Personaje import Personaje
import Lista_Inventario

class UnionPartida:
    #sound

    def __init__(self,width,height,screen,ch1,ch2,ch3,ch4,font,id):
        #screen
        self.screen = screen
        self.font = font
        self.id = id
        self.numJugadores = None
        self.jugadores = None
        self.portUDP_server = None
        self.portUDP = None
        self.ip_dest = None
        self.port_dest = None
        self.escuchaTCPClient = None
        self.personaje = None
        self.socket_c = None

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
        self.activeI = True
        self.activeI2 = True
        self.first_timeC = True #Aún no has pulsado el botón de buscar partida
        self.name = None
        self.avatarPicPerfil = None

        #cargamos las imágenes del menú
        self.backgroundPic = pygame.image.load("images/background.png")
        self.titlePic = pygame.image.load("images/title.png")
        self.buttonPic = pygame.image.load("images/button.png")
        self.buttonSelectedPic = pygame.image.load("images/button_selected.png")
        self.buttonPressedPic = pygame.image.load("images/button_pressed.png")
        self.capa = pygame.image.load("images/capa.png")
        self.bCreate = pygame.image.load("images/button_createPartida.png")
        self.bCreate_selected = pygame.image.load("images/button_createPartida_selected.png")
        self.bCreate_pressed = pygame.image.load("images/button_createPartida_pressed.png")
        self.buttonUnavailablePic = pygame.image.load("images/button_unavailable.png")

        #fuentes y colores
        self.fuente = pygame.font.SysFont(font, 70)
        self.color_white = (255,255,255)
        self.color_dark_grey = pygame.Color((119,119,119))
        self.color_light_pink = pygame.Color((234,135,255))
        self.color_black = (0,0,0)
        self.color_grey = pygame.Color((208,208,208))
        self.color_dark_red = pygame.Color((146,0,0))
        self.color_dark_red_sat = pygame.Color((121,58,58))
        self.back = self.fuente.render('Volver atrás', True, self.color_white)
        self.crearT = self.fuente.render('Buscar partida',True,self.color_white)
        self.codeT = self.fuente.render('Código de partida',True,self.color_white)
        self.passwordT = self.fuente.render('Contraseña de acceso',True,self.color_white)
    

        self.introduceTextLen = 37
        self.max_lenght_name = 37
        self.introduceTextLen2 = 37
        self.max_lenght_name2 = 25

    def setScreen(self,screen):
        self.screen = screen
        #self.width,self.height= (self.screen.get_width(), self.screen.get_height())
    def getScreen(self):
        return self.screen
    
    def getIpANDPortDest(self):
        return (self.ip_dest,self.port_dest,self.password)
    
    def getPersonaje(self):
        return self.personaje
    
    def reload(self):
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/4.0956, self.height/12.2807)), (self.width/4.1379, self.height/1.1667))#293 57 290 600
        self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/3.3333, self.height/1.1570)) #150 40 360 605
        self.screen.blit(pygame.transform.scale(self.passwordT, (self.width/4.0000, self.height/17.5000)), (self.width/2.6667, self.height/12.2807)) #300 40 450 57
        self.screen.blit(pygame.transform.scale(self.codeT, (self.width/5.3333, self.height/17.5000)), (self.width/2.4490, self.height/3.3333)) #225 40 490 210
        if(self.password != None and self.password != ' ' and self.code != None and self.code != ' '):
            self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667)) #293 57 620 600
        else:
            self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667))
        self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.7884, self.height/1.1570)) #190 40 671 605 
        pygame.draw.rect(self.screen, self.color_grey, self.inputBox, 2)
        self.screen.blit(self.passwordText, (self.width/4.5455, self.height/5.6000)) #264 x 125
        #password
        pygame.draw.rect(self.screen, self.color_grey, self.inputBox2, 2)
        self.screen.blit(self.codeText, (self.width/4.5455, self.height/2.5180)) #264 x 278


    def refresh(self):
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/4.0956, self.height/12.2807)), (self.width/4.1379, self.height/1.1667))#293 57 290 600
        self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/3.3333, self.height/1.1570)) #150 40 360 605
        self.screen.blit(pygame.transform.scale(self.passwordT, (self.width/4.0000, self.height/17.5000)), (self.width/2.6667, self.height/12.2807)) #300 40 450 57
        self.screen.blit(pygame.transform.scale(self.codeT, (self.width/5.3333, self.height/17.5000)), (self.width/2.4490, self.height/3.3333)) #225 40 490 210
        if(self.password != None and self.password != ' ' and self.code != None and self.code != ' '):
            self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667)) #293 57 620 600
        else:
            self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667))
        self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.7884, self.height/1.1570)) #190 40 671 605 

    def setNameYAvatar(self,name,a):
        self.name = name
        self.avatarPicPerfil = a

    def getPassword(self):
        return self.password

    def render(self):
        #render screen
        self.password = None
        self.code = None
        self.letterwidth = (self.width/3.4286)/14 #cálculo de la base en píxeles 
        self.lettersize = self.letterwidth + 0.5 * self.letterwidth #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuenteText = pygame.font.SysFont(self.font, int(self.lettersize))
        self.emptyText = self.fuenteText.render(' ', True, self.color_dark_grey)
        self.introduceText2 = self.fuenteText.render('--> Introduce el código de la partida' , True, self.color_dark_grey)
        self.emptyText2 = self.fuenteText.render(' ', True, self.color_dark_grey)
        self.introduceText = self.fuenteText.render('--> Introduce la contraseña de acceso' , True, self.color_dark_grey)
        self.introduceText3 = self.fuenteText.render('<!> Puerto o IP no existentes o accesibles' , True, self.color_dark_red_sat)
        if(self.password == None):
            self.password = ' '
            self.passwordText = self.introduceText
        else:
            self.passwordText = self.fuenteText.render(self.password, True, self.color_dark_grey)
        #Input de la contraseña
        if(self.code == None):
            self.code = ' '
            self.codeText = self.introduceText2
        else:
            self.codeText = self.fuenteText.render(self.code, True, self.color_dark_grey)

        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))

        self.screen.blit(pygame.transform.scale(self.passwordT, (self.width/4.0000, self.height/17.5000)), (self.width/2.6667, self.height/12.2807)) #300 40 450 57
        self.inputBox = pygame.Rect(self.width/4.8000, self.height/5.8333, self.width/1.7143, self.height/11.6667) #250 120 700 60 
        pygame.draw.rect(self.screen, self.color_grey, self.inputBox, 2)
        self.screen.blit(self.introduceText, (self.width/4.5455, self.height/5.6000)) #264 x 125


        self.screen.blit(pygame.transform.scale(self.codeT, (self.width/5.3333, self.height/17.5000)), (self.width/2.4490, self.height/3.3333)) #225 40 490 210
        self.inputBox2 = pygame.Rect(self.width/4.8000, self.height/2.5641, self.width/1.7143, self.height/11.6667) #250 273 700 60
        pygame.draw.rect(self.screen, self.color_grey, self.inputBox2, 2)
        self.screen.blit(self.introduceText2, (self.width/4.5455, self.height/2.5180)) #264 x 278
        
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/4.0956, self.height/12.2807)), (self.width/4.1379, self.height/1.1667))#293 57 290 600
        self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/3.3333, self.height/1.1570)) #150 40 360 605
        if(self.password != None and self.password != ' ' and self.code != None and self.code != ' '):
            self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667)) #293 57 620 600
        else:
            self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667))
        self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.7884, self.height/1.1570)) #190 40 671 605 
        pygame.display.update() 

    # size_x, size_y: tamaño del botón en x y en y
    # x_start y y_start: posición de la esquina izquierda del botón
    # pos_x y pos_y: posición actual del ratón
    def checkIfMouseIsInButton(self,size_x,size_y,x_start,y_start,pos_x,pos_y):
        if((pos_x >= x_start and pos_x <= size_x+x_start) and (pos_y >= y_start and pos_y <= size_y + y_start)):
            return True
        else:
            return False
    def isNumber(self, n):
        if (ord(n)>=48 and ord(n)<=57):
            return True
        else:
            return False
        
    def getNumJugadoresAndJugadoresAndPort(self):
        return (self.numJugadores,self.jugadores,self.portUDP_server,self.ip_dest)
        
    def isProperFormat(self,code,it): #comprueba el formato 111.111.111:[49152-65535] -> puede haber de 1 a 3 números en la ip
        #no puede ser 012.304.000:64444 (que empieze por cero)
        if((code != None or it>0)and it<=3): #si es 4, entonces estamos ya donde el puerto
            if(self.isNumber(code[0]) and ord(self.code[0]) != 48):
                if(len(code)>=2 and self.isNumber(code[1])):
                    if(len(code)>=3 and self.isNumber(code[2])):
                        if((it < 3 and (len(code)>=4 and code[3] == '.')) or (it == 3 and code[3] == ':')):
                            if(len(code)>=5):
                                code = code[4:]
                                return self.isProperFormat(code,it+1)
                            else:
                                return (False,None)
                        else:
                            return (False,None)
                    elif((it < 3 and (len(code)>=3 and code[2] == '.')) or (it == 3 and code[2] == ':')):
                        if(len(code)>=4):
                            code = code[3:]
                            return self.isProperFormat(code,it+1)
                        else:
                            return (False,None)
                    else:
                        return (False,None)
                elif((it < 3 and (len(code)>=2 and code[1] == '.')) or (it == 3 and code[1] == ':')):
                    if(len(code)>=3):
                        code = code[2:]
                        return self.isProperFormat(code,it+1)
                    else:
                        return (False,None)
                else:
                    return (False,None)
            else:
                return (False,None)
        elif(it != 4):
            return (False,None)
        else: #estamos donde el puerto
            if(len(code) == 5):
                for i in range(0,5):
                    if(self.isNumber(code[i])):
                        pass
                    else:
                        return (False,None)
                n = int(code)
                if(n>=49152 and n <=65535):
                    (ip,port) = self.code.split(':')
                    return (True,(ip,port))
                else:
                    return (False,None)
            else:
                return (False,None)
            
    def checkformat(self,msg):
        try:
            #ok:4:53456:id1;pepe;1;True:id2;juan;4;True
                                  #  0  1   2       3                  4
            resp = msg.split(':') # ok  4  54634 id1;pepe;1;True   id2;juan;4;True
            if(resp[0] == "ok"):
                if(resp[1] != None and int(resp[1])>=0 and int(resp[1])<=6 and resp[2] != None and int(resp[2])>=10000 and int(resp[2]) <=99999): # si numjugadores recibido está entre 0 y 6 y el puerto es real
                    jugadores = {}
                    for i in range(0,len(resp)-3):
                        [id_j,name,pic,isActive] = resp[i+3].split(';')
                        if isActive == 'False':
                            isActive = False
                        else:
                            isActive = True
                        jugadores[i] = (id_j,(name,int(pic),isActive)) 
                    return (0,int(resp[1]),jugadores,int(resp[2])) #pantalla 0: sala espera
                else:
                    return (-1,None,None)
            elif(resp[0] == "ok_ve_salaEspera2"):
                if(resp[3] != None and int(resp[3])>=0 and int(resp[3])<=6 and resp[4] != None and int(resp[4])>=10000 and int(resp[4]) <=99999): # si numjugadores recibido está entre 0 y 6 y el puerto es real
                    jugadores = {}
                    for i in range(0,len(resp)-5):
                        [id_j,name,pic,isActive] = resp[i+5].split(';')
                        if isActive == 'False':
                            isActive = False
                        else:
                            isActive = True
                        jugadores[i] = (id_j,(name,int(pic),isActive)) 

                    # resp_final = []
                    # total_recibido = len(resp[1])
                    # resp_final.append(bytes(resp[1], encoding='utf8'))
                    # while (total_recibido < int(resp[1])):
                    #     #no hemos recibido todo el mensaje
                    #     print("fragmento 1 recibido del personaje")
                    #     resp_fragment = self.socket_c.recv(4096)
                    #     if not resp_fragment:
                    #         break
                    #     resp_final.append(resp_fragment)
                    #     total_recibido += len(resp_fragment)
                    # respuesta = b''.join(resp_final)
                    datos_personaje_decoded = base64.b64decode(resp[2])
                    personaje = pickle.loads(datos_personaje_decoded)
                    return (1,int(resp[3]),jugadores,int(resp[4]),personaje) #pantalla 1: salaEspera2
                else:
                    return (-1,None,None)
            elif(resp[0] == "ok_ve_seleccionPersonaje"):
                if(resp[1] != None and int(resp[1])>=0 and int(resp[1])<=6 and resp[2] != None and int(resp[2])>=10000 and int(resp[2]) <=99999): # si numjugadores recibido está entre 0 y 6 y el puerto es real
                    jugadores = {}
                    for i in range(0,len(resp)-3):
                        [id_j,name,pic,isActive] = resp[i+3].split(';')
                        if isActive == 'False':
                            isActive = False
                        else:
                            isActive = True
                        jugadores[i] = (id_j,(name,int(pic),isActive)) 
                    return (2,int(resp[1]),jugadores,int(resp[2])) #pantalla 2: seleccionPersonaje
                else:
                    return (-1,None,None)
            elif(resp[0] == "ok_ve_partida"):
                if(resp[3] != None and int(resp[3])>=0 and int(resp[3])<=6 and resp[4] != None and int(resp[4])>=10000 and int(resp[4]) <=99999): # si numjugadores recibido está entre 0 y 6 y el puerto es real
                    jugadores = {}
                    for i in range(0,len(resp)-5):
                        [id_j,name,pic,isActive] = resp[i+5].split(';')
                        if isActive == 'False':
                            isActive = False
                        else:
                            isActive = True
                        jugadores[i] = (id_j,(name,int(pic),isActive)) 
                    # resp_final = []
                    # total_recibido = len(resp[1])
                    # resp_final.append(bytes(resp[2], encoding='utf8'))
                    # while (total_recibido < int(resp[3])):
                    #     #no hemos recibido todo el mensaje
                    #     #print("fragmento 1 recibido del personaje")
                    #     resp_fragment = self.socket_c.recv(4096)
                    #     if not resp_fragment:
                    #         break
                    #     resp_final.append(resp_fragment)
                    #     total_recibido += len(resp_fragment)
                    # respuesta = b''.join(resp_final)
                    datos_personaje_decoded = base64.b64decode(resp[2])
                    personaje = pickle.loads(datos_personaje_decoded)
                    return (3,int(resp[3]),jugadores,int(resp[4]),personaje) #pantalla 3: partida
                else:
                    return (-1,None,None)
            else:
                return (-1,None,None)
        except:
            return (-1,None,None)
        
    def getPortUDPYSocket(self):
        return (self.portUDP,self.socketUDP)

    def clickedMouse(self):
        #click del ratón
        #calculo del tamaño del botón y su posición -> Empezar Simulación
        x_size = self.width/4.0956
        y_size = self.height/12.2807
        x_start = self.width/4.1379
        y_start = self.height/1.1667
        x_startC = self.width/1.9355
        (x,y) = pygame.mouse.get_pos()

        #Botón volver al menú
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/4.0956, self.height/12.2807)), (self.width/4.1379, self.height/1.1667))#293 57 290 600
            self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/3.3333, self.height/1.1570)) #150 40 360 605
            self.ch1.play(self.pressed)
            self.activeI = False
            self.activeI2 = False
            pygame.display.update() 
            return 'seleccionPartidas'

        #Unirse a una partida
        elif(self.checkIfMouseIsInButton(x_size,y_size,x_startC,y_start,x,y)):
            pantalla = 'salaEspera'
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/4.0956, self.height/12.2807)), (self.width/4.1379, self.height/1.1667))#293 57 290 600
            self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/3.3333, self.height/1.1570)) #150 40 360 605
            if(self.password != None and self.password != ' ' and self.code != None and self.code != ' '):
                result = self.isProperFormat(self.code,0)
                if(result[0]):
                    ip_dest = result[1][0]
                    port_dest = result[1][1]
                # ----- conexión TCP  -----
                    self.socket_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_socket_tcp.bind(('', 0)) #encuentra un puerto libre
                    self.socketUDP = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                    self.socketUDP.bind(('', 0)) #encuentra un puerto libre
                    self.portUDP = self.socketUDP.getsockname()[1] #devuelve el nombre del puerto encontrado
                    puertoTCP = server_socket_tcp.getsockname()[1]
                    resp = None
                    try:
                        #print(ip_dest,port_dest)
                        self.ip_dest = ip_dest
                        self.port_dest = port_dest
                        self.socket_c.connect((ip_dest, int(port_dest)))
                        msg_client = str(self.password) + ":"+str(self.name)+":"+str(self.avatarPicPerfil)+":"+str(self.id)+":"+str(self.portUDP)+":"+str(puertoTCP)
                        #patata:pepe:3:id:56384:49234 <- ejemplo mensaje
                        self.socket_c.sendall(msg_client.encode('utf-8'))
                        respuesta = self.socket_c.recv(65555).decode('utf-8') #tiene timeout de unos segundos
                        print('Datos recibidos: ',respuesta)
                        resp = self.checkformat(respuesta)
                        print(resp)
                        if(resp[0] == -1):
                            self.code = ' ' 
                            self.refresh()
                            pygame.draw.rect(self.screen, self.color_dark_red, self.inputBox2, 2)
                            self.screen.blit(self.introduceText3, (self.width/4.5455, self.height/2.5180)) #264 x 278
                            pygame.draw.rect(self.screen, self.color_grey, self.inputBox, 2)
                            if(self.password == ' '):
                                self.passwordText = self.introduceText
                            else:
                                self.passwordText = self.fuenteText.render(self.password, True, self.color_grey)
                            self.screen.blit(self.passwordText, (self.width/4.5455, self.height/5.6000)) #264 x 125
                            pantalla = "joinPartida"
                            self.ch1.play(self.error)
                        else:
                            self.numJugadores = resp[1]
                            self.jugadores = resp[2]
                            self.portUDP_server = resp[3]
                            print('jugadores: ',self.jugadores)
                            self.screen.blit(pygame.transform.scale(self.bCreate_pressed, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667)) #293 57 620 600
                            self.ch1.play(self.pressed)
                            if(resp[0] == 1):
                                pantalla = "partida_load_wait"
                                self.personaje = resp[4]
                            elif(resp[0] == 2):
                                pantalla = "seleccionPersonaje"
                            elif(resp[0] == 3):
                                pantalla = "partida"
                                self.personaje = resp[4]
                    except:
                        #mostrar en rojo el recuadro + texto de no es correcto + reseteo del valor de self.code
                        self.code = ' ' 
                        self.refresh()
                        pygame.draw.rect(self.screen, self.color_dark_red, self.inputBox2, 2)
                        self.screen.blit(self.introduceText3, (self.width/4.5455, self.height/2.5180)) #264 x 278
                        pygame.draw.rect(self.screen, self.color_grey, self.inputBox, 2)
                        if(self.password == ' '):
                            self.passwordText = self.introduceText
                        else:
                            self.passwordText = self.fuenteText.render(self.password, True, self.color_grey)
                        self.screen.blit(self.passwordText, (self.width/4.5455, self.height/5.6000)) #264 x 125
                        pantalla = "joinPartida"
                        self.ch1.play(self.error)
                    finally:
                        ip = self.socket_c.getsockname()[0]
                        port = self.socket_c.getsockname()[1]
                        self.socket_c.close()
                        print(ip,port)
                        if(resp != None and resp[0] != -1): #solo pondremos las conexiones si nos ha dicho que sí el servidor
                            self.escuchaTCPClient = EscuchaTCPClient(server_socket_tcp,ip,puertoTCP,ip_dest,port_dest,self.id,self.password) #creamos un servidor para recibir mensajes TCP del host
                            hiloEscuchaTCPClient = threading.Thread(target=self.escuchaTCPClient.escuchaTCPClient)
                            hiloEscuchaTCPClient.start()
                # --------------------------
                else:
                    #mostrar en rojo el recuadro + texto de no es correcto + reseteo del valor de self.code
                    self.code = ' '
                    self.refresh()
                    pygame.draw.rect(self.screen, self.color_dark_red, self.inputBox2, 2)
                    self.screen.blit(self.introduceText3, (self.width/4.5455, self.height/2.5180)) #264 x 278
                    pygame.draw.rect(self.screen, self.color_grey, self.inputBox, 2)
                    if(self.password == ' '):
                        self.passwordText = self.introduceText
                    else:
                        self.passwordText = self.fuenteText.render(self.password, True, self.color_grey)
                    self.screen.blit(self.passwordText, (self.width/4.5455, self.height/5.6000)) #264 x 125
                    pantalla = "joinPartida"
                    self.ch1.play(self.error)
            
            else:
                pantalla = 'joinPartida'
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667))
                self.ch1.play(self.error)
            self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.7884, self.height/1.1570)) #190 40 671 605 
            self.activeI = False
            self.activeI2 = False
            pygame.display.update() 
            return pantalla    

        #Input code
        elif self.inputBox2.collidepoint((x,y)):
            self.refresh()
            pygame.draw.rect(self.screen, self.color_light_pink, self.inputBox2, 2)
            if(self.code == ' '):
                self.codeText = self.emptyText
                self.screen.blit(self.codeText, (self.width/4.5455, self.height/2.5180)) #264 x 278)
            else:
                self.screen.blit(self.codeText, (self.width/4.5455, self.height/2.5180)) #264 x 278

            if(self.password == ' '):
                self.passwordText = self.introduceText
            else:
                self.passwordText = self.fuenteText.render(self.password, True, self.color_grey)
            pygame.draw.rect(self.screen, self.color_grey, self.inputBox, 2)
            self.screen.blit(self.passwordText, (self.width/4.5455, self.height/5.6000)) #264 x 125
            pygame.display.update() 
            self.activeI = True
            self.activeI2 = False
            return 'joinPartida'

        #Input password
        elif self.inputBox.collidepoint((x,y)):
            self.refresh()
            pygame.draw.rect(self.screen, self.color_light_pink, self.inputBox, 2)
            if(self.password == ' '):
                self.passwordText = self.emptyText
                self.screen.blit(self.passwordText, (self.width/4.5455, self.height/5.6000)) #264 x 125
            else:
                self.screen.blit(self.passwordText, (self.width/4.5455, self.height/5.6000)) #264 x 125

            if(self.code == ' '):
                self.codeText = self.introduceText2
            else:
                self.codeText = self.fuenteText.render(self.code, True, self.color_grey)
            pygame.draw.rect(self.screen, self.color_grey, self.inputBox2, 2)
            self.screen.blit(self.codeText, (self.width/4.5455, self.height/2.5180)) #264 x 278
            pygame.display.update() 
            self.activeI = False
            self.activeI2 = True
            return 'joinPartida'

        else:
            self.activeI = False
            self.activeI2 = False
            if(self.password == ' '):
                self.passwordText = self.introduceText
            else:
                self.passwordText = self.fuenteText.render(self.password, True, self.color_grey)

            if(self.code == ' '):
                self.codeText = self.introduceText2
            else:
                self.codeText = self.fuenteText.render(self.code, True, self.color_grey)
            self.refresh()
            pygame.draw.rect(self.screen, self.color_grey, self.inputBox, 2)
            self.screen.blit(self.passwordText, (self.width/4.5455, self.height/5.6000)) #264 x 125
            #password
            pygame.draw.rect(self.screen, self.color_grey, self.inputBox2, 2)
            self.screen.blit(self.codeText, (self.width/4.5455, self.height/2.5180)) #264 x 278
            pygame.display.update() 
            return 'joinPartida'

    def manageInputBox(self, key, unicode):
        if(self.activeI):
            self.activeI2 = False
            if key == pygame.K_RETURN:
                self.code = ' '
            elif key == pygame.K_BACKSPACE:
                self.code = self.code[:-1]
                if(len(self.code) == 0):
                    self.code = ' '
            else:
                if(len(self.code)<self.max_lenght_name):
                    if(self.code == ' '):
                        self.code = unicode
                    else:
                        self.code += unicode
                    #self.widthText = self.letterwidth*len(self.name)
                else:
                    self.ch2.play(self.error)
            self.refresh()
            pygame.draw.rect(self.screen, self.color_light_pink, self.inputBox2, 2)
            self.codeText = self.fuenteText.render(self.code, True, self.color_light_pink)
            self.screen.blit(self.codeText, (self.width/4.5455, self.height/2.5180)) #264 x 278

            if(self.password == ' '):
                self.passwordText = self.introduceText
            else:
                self.passwordText = self.fuenteText.render(self.password, True, self.color_grey)
            #password
            pygame.draw.rect(self.screen, self.color_grey, self.inputBox, 2)
            self.screen.blit(self.passwordText, (self.width/4.5455, self.height/5.6000)) #264 x 125
            pygame.display.update() 

        elif(self.activeI2):
            self.activeI = False
            if key == pygame.K_RETURN:
                self.password = ' '
            elif key == pygame.K_BACKSPACE:
                self.password = self.password[:-1]
                if(len(self.password) == 0):
                    self.password = ' '
            else:
                if(len(self.password)<self.max_lenght_name2):
                    if(unicode != ':' and unicode != ';'):
                        if(self.password == ' '):
                            self.password = unicode
                        else:
                            self.password += unicode
                    else:
                        self.ch2.play(self.error)
                else:
                    self.ch2.play(self.error)
            self.refresh()
            pygame.draw.rect(self.screen, self.color_light_pink, self.inputBox, 2)
            self.passwordText = self.fuenteText.render(self.password, True, self.color_light_pink)
            self.screen.blit(self.passwordText, (self.width/4.5455, self.height/5.6000)) #264 x 125

            if(self.code == ' '):
                self.codeText = self.introduceText2
            else:
                self.codeText = self.fuenteText.render(self.code, True, self.color_grey)
            #password
            pygame.draw.rect(self.screen, self.color_grey, self.inputBox2, 2)
            self.screen.blit(self.codeText, (self.width/4.5455, self.height/2.5180)) #264 x 278
            pygame.display.update() 
        else:
            pass

    def movedMouse(self):
        # Calculo las dimensiones y el tamaño del botón de volver al menú
        x_size = self.width/4.0956
        y_size = self.height/12.2807
        x_start = self.width/4.1379
        y_start = self.height/1.1667
        x_startC = self.width/1.9355
        (x,y) = pygame.mouse.get_pos()

        # Botón volver al menú
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/4.0956, self.height/12.2807)), (self.width/4.1379, self.height/1.1667))#293 57 290 600
            self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/3.3333, self.height/1.1570)) #150 40 360 605
            # Si se cumplen todas las condiciones, el botón estará disponible y tendrá un color morado
            if(self.password != None and self.password != ' ' and self.code != None and self.code != ' '):
                self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667)) #293 57 620 600
            else:
                # Si no se cumplen las condiciones, el botón no estará disponible y se verá en gris
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.7884, self.height/1.1570)) #190 40 671 605 
            # Si el cursor acaba de acceder al botón, se establecerá a False su variable, y a True la de los demás botones
            # Esto es debido a que queremos que el sonido solo se reproduzca la primera vez que se entra, no constantemente
            if(self.first_timeB):
                self.first_timeB = False
                self.first_timeC = True
                self.ch2.play(self.selected)   
            # Refrescamos la pantalla  
            pygame.display.update() 

        #Boton unirse a partida
        elif(self.checkIfMouseIsInButton(x_size,y_size,x_startC,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/4.0956, self.height/12.2807)), (self.width/4.1379, self.height/1.1667))#293 57 290 600
            self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/3.3333, self.height/1.1570)) #150 40 360 605
            if(self.password != None and self.password != ' ' and self.code != None and self.code != ' '):
                self.screen.blit(pygame.transform.scale(self.bCreate_selected, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667)) #293 57 620 600
                if(self.first_timeC):
                    self.first_timeC = False
                    self.first_timeB = True
                    self.ch1.play(self.selected)
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.9355, self.height/1.1667))
                if(self.first_timeC):
                    self.first_timeC = False
                    self.first_timeB = True
            self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.7884, self.height/1.1570)) #190 40 671 605 
            pygame.display.update() 


        else:
            self.first_timeB = True
            self.first_timeC = True
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/4.0956, self.height/12.2807)), (self.width/4.1379, self.height/1.1667))#293 57 290 600
            self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/3.3333, self.height/1.1570)) #150 40 360 605
            pygame.display.update() 

        
    
