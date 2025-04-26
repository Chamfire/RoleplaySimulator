import pygame
from pygame.locals import *
from pygame import mixer
from EscuchaUDP import EscuchaUDP
from EnviarEstadoUDP import EnviarEstadoUDP
import threading
import socket
import ctypes
from Global import Global
import queue
from ProcesamientoPartida import ProcesamientoPartida


class PartidaScreen:
    #sound

    def __init__(self,width,height,screen,ch1,ch2,ch3,ch4,font,id,seed):
        #screen
        self.screen = screen
        self.justAfterSala = False
        self.isOnline = False
        self.id = id
        self.password = None
        self.font = font
        self.currentFrame = 0
        self.seed_random = seed
        self.hiloProcesamientoPartida = None
        self.currentPartida = None

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
        self.ProcesamientoPartida = None
        self.GLOBAL = Global()
        self.GLOBAL.setActualPartidaState("loading") #por defecto será loading
        self.first_timeScreen = True

        #canales
        self.ch1 = ch1
        self.ch2 = ch2
        self.ch3 = ch3
        self.ch4 = ch4
        
        self.personaje = None
        self.numJugadores = None
        self.DMVoice = None
        self.volEffects = None

        #variables
        self.first_timeB = True # Aún no has pulsado el botón volver al menú
        self.first_timeM = True #Aún no has pulsado el botón de enviar mensaje
        self.first_timeP = True # Aún no has pulsado el botón de pedir/liberar turno de palabra

        #cargamos las imágenes del menú
        self.backgroundPic = pygame.image.load("images/background.png")
        self.capa = pygame.image.load("images/capa.png")
        self.buttonPic = pygame.image.load("images/button.png")
        self.buttonSelectedPic = pygame.image.load("images/button_selected.png")
        self.buttonPressedPic = pygame.image.load("images/button_pressed.png")
        self.backgroundPartidaPic = pygame.image.load("images/background_partida.png")
        self.changePhoto = False
        self.currentImageToShow = ""
        self.imagePhoto = ""

        #fuentes y colores
        self.fuente = pygame.font.SysFont(font, 70)
        self.color_white = (255,255,255)
        self.color_black = (0,0,0)
        self.back = self.fuente.render('Volver al menú', True, self.color_white)
        self.enviar_msg = self.fuente.render('Enviar mensaje', True, self.color_white)
        self.pedir_turno_palabra = self.fuente.render('Pedir la palabra', True, self.color_white)
        self.liberar_turno_palabra = self.fuente.render('Ceder la palabra', True, self.color_white)
        self.msg = None
        self.msg1 = None
        self.msg2 = None
        self.msg3 = None
        self.textoDM = queue.Queue()
        self.image = queue.Queue()
        self.currentTextToShow = ""

        #estado variable
        self.contMsg = 0 #por defecto empieza en 0

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

    def setNumJugadores(self,j):
        self.numJugadores = j

    def setDMVoice(self,dmv):
        self.DMVoice = dmv

    def setIpANDPortDest(self,ip_y_port_y_pswd):
        self.ip_dest = ip_y_port_y_pswd[0]
        self.port_dest = ip_y_port_y_pswd[1]
        self.password =ip_y_port_y_pswd[2]
        self.isOnline = True

    def changeScreen(self,pantalla):
        self.GLOBAL.setActualPartidaState(pantalla)
        if(pantalla == "loading"):
            self.first_timeScreen = True
            self.GLOBAL.setTokenDePalabra(None)
        
    def setPassword(self,v):
        self.password = v

    def setCurrentPartida(self,p):
        self.currentPartida = p

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

    def reload(self):
        x_size = self.width/3.8339
        y_size = self.height/12.2807
        x_start = self.width/1.3873
        y_start = self.height/1.1290
        y_start2 = self.height/1.2658
        y_start3 = self.height/1.4403
        (x,y) = pygame.mouse.get_pos()

        if(self.GLOBAL.getActualPartidaState() == "loading"):
            self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
            self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
            self.screen.blit(self.msg3, (self.width/4.0000, self.height/4.0000)) #300 175 
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
        elif(self.GLOBAL.getActualPartidaState() == "partida"):
            self.screen.blit(pygame.transform.scale(self.backgroundPartidaPic, (self.width,self.height)), (0, 0))
            if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
            else:
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
            
            if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start2,x,y)):
                self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
            else:
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
            self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
            if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start3,x,y)):
                self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
            else:
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
            self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
            self.inputBoxDescripcion = pygame.Rect(self.width/48.0000, self.height/1.4894, self.width/1.4815, self.height/5.6452) #25 470 810 124
            pygame.draw.rect(self.screen, self.color_white, self.inputBoxDescripcion, 2)
            img = self.GLOBAL.getImagePartida() 
            if(img != ""):
                self.image.put(img)

            try:
                if(self.changePhoto):
                    self.currentImageToShow = self.image.get()
                    self.changePhoto = False
                    self.imagePhoto = pygame.image.load(img)
            except:
                self.currentImageToShow = ""

            if(self.currentImageToShow != ""):
                self.screen.blit(pygame.transform.scale(self.imagePhoto, (self.width/4.7059, self.height/2.6415)), (self.width/1.3378, self.height/14.0000)) #255 265 897 50

        pygame.display.update() 


    def cerrarHilo(self):
        #si está activo, que lo detenga
        if self.hiloProcesamientoPartida != None and self.hiloProcesamientoPartida.is_alive():
            ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(self.hiloProcesamientoPartida.ident), ctypes.py_object(SystemExit)
            )


    def render(self):
        #render screen
        self.letterwidth = (self.width/3.4286)/6 #cálculo de la base en píxeles 
        self.lettersize = int(self.letterwidth + 0.5 * self.letterwidth) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente2 = pygame.font.SysFont(self.font,self.lettersize)

        self.letterwidth3 = (self.width/3.4286)/32 #cálculo de la base en píxeles 
        self.lettersize3 = int(self.letterwidth3 + 0.5 * self.letterwidth3) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente4 = pygame.font.SysFont(self.font,self.lettersize3)

        if(self.GLOBAL.getActualPartidaState() == "loading"):
            self.ProcesamientoPartida = ProcesamientoPartida(self.seed_random,self.currentPartida)
            self.msg = self.fuente2.render('Preparando Partida', True, self.color_white)
            self.msg1 = self.fuente2.render('Preparando Partida.', True, self.color_white)
            self.msg2 = self.fuente2.render('Preparando Partida..', True, self.color_white)
            self.msg3 = self.fuente2.render('Preparando Partida...', True, self.color_white)
            self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
            self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
            self.screen.blit(self.msg3, (self.width/4.0000, self.height/4.0000)) #300 175 
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(not self.isOnline):
                print(self.GLOBAL.getOtherPlayers())
                print(self.password,self.id)
                for i in range(0,len(self.GLOBAL.getOtherPlayers())):
                    if(self.GLOBAL.getOtherPlayersIndex(i) != None and self.GLOBAL.getOtherPlayersIndex(i)[1][2]): 
                        socket_temporal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        try:
                            socket_temporal.connect((self.GLOBAL.getOtherPlayersIndex(i)[1][4],self.GLOBAL.getOtherPlayersIndex(i)[1][5]))
                            msg = f"{self.password};{self.id};ve_partida_fromSalaEspera"
                            socket_temporal.sendall(msg.encode('utf-8'))
                        except Exception as e:
                            print('e1: ',e)
                            pass
                        finally:
                            socket_temporal.close() #se cierra el socket al terminar
                #inicio del hilo de carga de partida
                self.ProcesamientoPartida.initialize(self.numJugadores,self.DMVoice,self.currentPartida,self.personaje,self)
                self.hiloProcesamientoPartida = threading.Thread(target=self.ProcesamientoPartida.prepararPartida)
                self.hiloProcesamientoPartida.start()
            else:
                #TODO: esperar a recibir maquina de estados para la partida, y crearla con la configuración de voz y efectos
                pass
        elif(self.GLOBAL.getActualPartidaState() == "partida"):
            self.screen.blit(pygame.transform.scale(self.backgroundPartidaPic, (self.width,self.height)), (0, 0))
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
            self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
            self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491

            self.inputBoxDescripcion = pygame.Rect(self.width/48.0000, self.height/1.4894, self.width/1.4815, self.height/5.6452) #25 470 810 124
            pygame.draw.rect(self.screen, self.color_white, self.inputBoxDescripcion, 2)
        pygame.display.update() 

    def renderTextBlock(self,text,position):
        x_size = self.width/3.8339
        y_size = self.height/12.2807
        x_start = self.width/1.3873
        y_start = self.height/1.1290
        y_start2 = self.height/1.2658
        y_start3 = self.height/1.4403
        (x,y) = pygame.mouse.get_pos()
        self.screen.blit(pygame.transform.scale(self.backgroundPartidaPic, (self.width,self.height)), (0, 0))
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
        else:
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
        self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
            
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start2,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
        else:
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
        self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start3,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
        else:
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
        self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
        self.inputBoxDescripcion = pygame.Rect(self.width/48.0000, self.height/1.4894, self.width/1.4815, self.height/5.6452) #25 470 810 124
        pygame.draw.rect(self.screen, self.color_white, self.inputBoxDescripcion, 2)

        img = self.GLOBAL.getImagePartida() 
        if(img != "" and self.changePhoto):
            self.image = pygame.image.load(img)
            self.changePhoto = False
        if(img != ""):
            self.screen.blit(pygame.transform.scale(self.image, (self.width/4.7059, self.height/2.6415)), (self.width/1.3378, self.height/14.0000)) #255 265 897 50



        currentWordsPrinted = 0
        lineSpacing = -2
        spaceWidth, fontHeight = self.fuente4.size(" ")[0], self.fuente4.size("Tg")[1]

        listOfWords = text.split(" ")
        imageList = [self.fuente4.render(word, True, self.color_black) for word in listOfWords]

        maxLen = self.inputBoxDescripcion[2]-20 #10 de cada lado de margen
        lineLenList = [0]
        lineList = [[]]
        for image in imageList:
            width = image.get_width()
            lineLen = lineLenList[-1] + len(lineList[-1]) * spaceWidth + width
            if len(lineList[-1]) == 0 or lineLen <= maxLen:
                lineLenList[-1] += width
                lineList[-1].append(image)
            else:
                lineLenList.append(width)
                lineList.append([image])

        lineBottom = self.inputBoxDescripcion[1] 
        lastLine = 0
        for lineLen, lineImages in zip(lineLenList, lineList):
            lineLeft = self.inputBoxDescripcion[0] +10
            #if len(lineImages) > 1:
            #   spaceWidth = (self.inputBoxDescripcion[2] - lineLen -20) // (len(lineImages)-1)
            if lineBottom + fontHeight > self.inputBoxDescripcion[1] + self.inputBoxDescripcion[3]:
                break
            lastLine += 1
            for i, image in enumerate(lineImages):
                x, y = lineLeft + i*spaceWidth, lineBottom
                if(position >= currentWordsPrinted):
                    self.screen.blit(image, (round(x), y))
                    lineLeft += image.get_width() 
                    currentWordsPrinted += 1
                else:
                    return #así termina el método
            lineBottom += fontHeight + lineSpacing

    def animateScreen(self,maxFPS):
        if(self.GLOBAL.getActualPartidaState() == "loading"):
            x_size = self.width/3.8339
            y_size = self.height/12.2807
            x_start = self.width/2.7907
            y_start = self.height/1.1667
            (x,y) = pygame.mouse.get_pos()

            #frames del contador para cambiar la animación -> por si hubiera cambiado los FPS máximos
            change_frame = maxFPS // 4 
            #Calculamos el frame actual
            self.currentFrame +=1 

            #Cargamos la animación
            if(self.currentFrame >= change_frame):
                #Reseteamos a 0 el contador para esperar a la siguiente animación
                #Cargamos la base de la pantalla
                self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
                self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))

                if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                    self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            
                self.currentFrame = 0
                if(self.contMsg == 0):
                    self.screen.blit(self.msg, (self.width/4.0000, self.height/4.0000)) #300 175 
                    self.contMsg +=1
                elif(self.contMsg == 1):
                    self.screen.blit(self.msg1, (self.width/4.0000, self.height/4.0000)) #300 175 
                    self.contMsg +=1
                elif(self.contMsg == 2):
                    self.screen.blit(self.msg2, (self.width/4.0000, self.height/4.0000)) #300 175 
                    self.contMsg +=1
                elif(self.contMsg == 3):
                    self.screen.blit(self.msg3, (self.width/4.0000, self.height/4.0000)) #300 175 
                    self.contMsg = 0
                pygame.display.update()
        elif(self.GLOBAL.getActualPartidaState() == "partida"):
            x_size = self.width/3.8339
            y_size = self.height/12.2807
            x_start = self.width/1.3873
            y_start = self.height/1.1290
            y_start2 = self.height/1.2658
            y_start3 = self.height/1.4403
            (x,y) = pygame.mouse.get_pos()
            if(self.first_timeScreen == True):
                if(not self.isOnline):
                    self.GLOBAL.setTokenDePalabra(None)
                    self.reload()
                    self.first_timeScreen = False
                    self.currentFrame = 0
                else:
                    #TODO: establecer turno de palabra en función de lo que te haya dicho el mensaje UDP
                    pass
                
            else:
                change_frame = maxFPS//8
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625

                if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                    self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
                
                if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start2,x,y)):
                    self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start3,x,y)):
                    self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491

                img = self.GLOBAL.getImagePartida() 
                if(img != "" and self.changePhoto):
                    self.image = pygame.image.load(img)
                    self.changePhoto = False
                if(img != ""):
                    self.screen.blit(pygame.transform.scale(self.image, (self.width/4.7059, self.height/2.6415)), (self.width/1.3378, self.height/14.0000)) #255 265 897 50

                aux = self.GLOBAL.extractAndRemoveTextoDM()
                if(aux != ""):
                    self.textoDM.put(aux)
                try:
                    if(self.currentTextToShow == ""):
                        self.currentTextToShow = ["<DM>: "+self.textoDM.get(block = False),0,None]
                        self.currentTextToShow = [self.currentTextToShow[0],0,len(self.currentTextToShow[0].split(" "))] #texto,palabras_printeadas,total_palabras_a_printear
                except:
                    self.currentTextToShow = ""
                if(self.currentTextToShow != "" and self.currentTextToShow[0] != "" and (self.currentTextToShow[2]+5) >= (self.currentTextToShow[1])):
                    #hay que printear animado el texto    
                    #Cargamos la animación
                    self.currentFrame +=1 
                    if(self.currentFrame >= change_frame):
                        if(self.currentTextToShow[2] > self.currentTextToShow[1]):
                            #printar texto con una letra más
                            self.renderTextBlock(self.currentTextToShow[0],self.currentTextToShow[1])
                            self.currentTextToShow[1] +=1
                            self.currentFrame = 0
                        elif(self.currentTextToShow[2] == self.currentTextToShow[1]):
                            self.currentTextToShow = ""
                        else:
                            self.currentTextToShow = ""
                        
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
        if(self.GLOBAL.getActualPartidaState() == "loading"):
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
                mixer.music.stop()#para la música
                mixer.music.load("sounds/background.wav") #carga de nuevo la canción normal de fondo
                mixer.music.play(-1)
                try:
                    self.cerrarHilo()
                except:
                    pass
                return 'menu'    
            else:
                return 'partida'
        elif(self.GLOBAL.getActualPartidaState() == "partida"):
            x_size = self.width/3.8339
            y_size = self.height/12.2807
            x_start = self.width/1.3873
            y_start = self.height/1.1290
            y_start2 = self.height/1.2658
            y_start3 = self.height/1.4403
            (x,y) = pygame.mouse.get_pos()

            #Botón volver al menú
            if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                self.ch1.play(self.pressed)
                pygame.display.update() 
                mixer.music.stop()#para la música
                mixer.music.load("sounds/background.wav") #carga de nuevo la canción normal de fondo
                mixer.music.play(-1)
                try:
                    self.cerrarHilo()
                except:
                    pass
                return 'menu'
            #Botón de enviar mensaje
            elif(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start2,x,y)):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
                self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                self.ch1.play(self.pressed)
                pygame.display.update() 
                return 'partida'
            #Botón de pedir turno de palabra
            elif(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start3,x,y)):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                self.ch1.play(self.pressed)
                pygame.display.update() 
                return 'partida'
                
            else:
                return 'partida'
        

    def movedMouse(self):
        if(self.GLOBAL.getActualPartidaState() == "loading"):
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
                    self.first_timeM = True
                    self.first_timeP = True
                    self.ch2.play(self.selected)     
                pygame.display.update() 

            else:
                self.first_timeB = True
                self.first_timeM = True
                self.first_timeP = True
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
                pygame.display.update() 

        elif(self.GLOBAL.getActualPartidaState() == "partida"):
            x_size = self.width/3.8339
            y_size = self.height/12.2807
            x_start = self.width/1.3873
            y_start = self.height/1.1290
            y_start2 = self.height/1.2658
            y_start3 = self.height/1.4403
            (x,y) = pygame.mouse.get_pos()

            #Botón volver al menú
            if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                if(self.first_timeB):
                    self.first_timeB = False
                    self.first_timeM = True
                    self.first_timeP = True
                    self.ch2.play(self.selected)     
                pygame.display.update() 
            
            #Botón enviar mensaje
            elif(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start2,x,y)):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
                self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                if(self.first_timeM):
                    self.first_timeM = False
                    self.first_timeB = True
                    self.first_timeP = True
                    self.ch2.play(self.selected)     
                pygame.display.update() 
            
            #Botón pedir turno
            elif(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start3,x,y)):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                if(self.first_timeP):
                    self.first_timeP = False
                    self.first_timeB = True
                    self.first_timeM = True
                    self.ch2.play(self.selected)     
                pygame.display.update() 

            else:
                self.first_timeB = True
                self.first_timeM = True
                self.first_timeP = True
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                pygame.display.update() 
            
