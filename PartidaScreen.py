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
import sqlite3
from Lista_Inventario import Escudo,Objeto,Objeto_de_Espacio,Arma,Armadura,Llave


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
        self.joinPartida = pygame.mixer.Sound('sounds/joinPartida.wav')

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
        self.startBoton = True
        self.availableStart = False
        self.textWriten = False
        self.canCheck = True
        self.peso = None
        self.pc = None
        self.pp = None
        self.pe = None
        self.po = None
        self.ppt = None
        self.car = None
        self.sab = None
        self.cons = None
        self.des = None
        self.int = None
        self.fu = None
        self.ca = None
        self.vida = None
        self.bpc = None
        self.clase = None
        self.slot_selected = None

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
        self.first_timeI = True # Aún no has pulsado el botón de abrir el inventario
        self.first_timeF = True # Aún no has pulsado el botón de volver a la partida desde el inventario

        #cargamos las imágenes del menú
        self.backgroundPic = pygame.image.load("images/background.png")
        self.capa = pygame.image.load("images/capa.png")
        self.buttonPic = pygame.image.load("images/button.png")
        self.buttonSelectedPic = pygame.image.load("images/button_selected.png")
        self.buttonPressedPic = pygame.image.load("images/button_pressed.png")
        self.backgroundPartidaPic = pygame.image.load("images/background_partida.png")
        self.buttonUnavailablePic = pygame.image.load("images/button_unavailable.png")
        self.butonInv = pygame.image.load("images/inventario_icono.png")
        self.butonInv_selected = pygame.image.load("images/inventario_icono_selected.png")
        self.butonInv_pressed = pygame.image.load("images/inventario_icono_pressed.png")
        self.invetoryBkg = pygame.image.load("images/pantalla_inventario.png")
        self.flecha = pygame.image.load("images/flecha_atras.png")
        self.flecha_selected = pygame.image.load("images/flecha_atras_selected.png")
        self.flecha_pressed = pygame.image.load("images/flecha_atras_pressed.png")
        self.whitebkg = pygame.image.load("images/white_bkg.png")
        self.selected_slot = pygame.image.load("images/selected_slot.png")
        self.intercambio_slot = pygame.image.load("images/intercambio_slot.png")

        #diccionario de imágenes:
        # ARMADURAS -------
        self.imgs = {"Armaduras ligeras": {},"Armaduras medias": {},"Armaduras pesadas": {}, "Armas c/c simples": {}, "Armas a distancia simples":{},"Armas c/c marciales":{},"Armas a distancia marciales":{},"Comida": {}, "Bebida": {}, "Mecanico": {}, "Refugio": {},"Libro": {}, "Kit": {}, "Iluminación": {}, "Otros": {}, "Almacenaje": {}, "Munición": {}, "Escudo":{}, "Llave": {}, "Recoleccion": {}}
        self.imgs["Armaduras ligeras"]["Acolchada"] = pygame.image.load("images/objetos/Armadura/Armaduras ligeras/Acolchada.png")
        self.imgs["Armaduras ligeras"]["Cuero"] = pygame.image.load("images/objetos/Armadura/Armaduras ligeras/Cuero.png")
        self.imgs["Armaduras ligeras"]["Cuero tachonado"] = pygame.image.load("images/objetos/Armadura/Armaduras ligeras/Cuero tachonado.png")
        self.imgs["Armaduras medias"]["Pieles"] = pygame.image.load("images/objetos/Armadura/Armaduras medias/Pieles.png")
        self.imgs["Armaduras medias"]["Camisote de mallas"] = pygame.image.load("images/objetos/Armadura/Armaduras medias/Camisote de mallas.png")
        self.imgs["Armaduras medias"]["Cota de escamas"] = pygame.image.load("images/objetos/Armadura/Armaduras medias/Cota de escamas.png")
        self.imgs["Armaduras medias"]["Coraza"] = pygame.image.load("images/objetos/Armadura/Armaduras medias/Coraza.png")
        self.imgs["Armaduras medias"]["Semiplacas"] = pygame.image.load("images/objetos/Armadura/Armaduras medias/Semiplacas.png")
        self.imgs["Armaduras pesadas"]["Cota de anillas"] = pygame.image.load("images/objetos/Armadura/Armaduras pesadas/Cota de anillas.png")
        self.imgs["Armaduras pesadas"]["Cota de mallas"] = pygame.image.load("images/objetos/Armadura/Armaduras pesadas/Cota de mallas.png")
        self.imgs["Armaduras pesadas"]["Bandas"] = pygame.image.load("images/objetos/Armadura/Armaduras pesadas/Bandas.png")
        self.imgs["Armaduras pesadas"]["Placas"] = pygame.image.load("images/objetos/Armadura/Armaduras pesadas/Placas.png")

        # Armas
        self.imgs["Armas c/c simples"]["Bastón"] = pygame.image.load("images/objetos/Armas/Armas cc simples/Bastón.png")
        self.imgs["Armas c/c simples"]["Daga"] = pygame.image.load("images/objetos/Armas/Armas cc simples/Daga.png")
        self.imgs["Armas c/c simples"]["Gran clava"] = pygame.image.load("images/objetos/Armas/Armas cc simples/Gran Clava.png")
        self.imgs["Armas c/c simples"]["Hacha de mano"] = pygame.image.load("images/objetos/Armas/Armas cc simples/Hacha de mano.png")
        self.imgs["Armas c/c simples"]["Hoz"] = pygame.image.load("images/objetos/Armas/Armas cc simples/Hoz.png")
        self.imgs["Armas c/c simples"]["Jabalina"] = pygame.image.load("images/objetos/Armas/Armas cc simples/Jabalina.png")
        self.imgs["Armas c/c simples"]["Lanza"] = pygame.image.load("images/objetos/Armas/Armas cc simples/Lanza.png")
        self.imgs["Armas c/c simples"]["Martillo ligero"] = pygame.image.load("images/objetos/Armas/Armas cc simples/Martillo Ligero.png")
        self.imgs["Armas c/c simples"]["Maza"] = pygame.image.load("images/objetos/Armas/Armas cc simples/Maza.png")
        self.imgs["Armas c/c simples"]["Clava"] = pygame.image.load("images/objetos/Armas/Armas cc simples/Clava.png")

        self.imgs["Armas a distancia simples"]["Arco corto"] = pygame.image.load("images/objetos/Armas/Armas a distancia simples/Arco Corto.png")
        self.imgs["Armas a distancia simples"]["Ballesta ligera"] = pygame.image.load("images/objetos/Armas/Armas a distancia simples/Ballesta Ligera.png")
        self.imgs["Armas a distancia simples"]["Dardo"] = pygame.image.load("images/objetos/Armas/Armas a distancia simples/Dardo.png")
        self.imgs["Armas a distancia simples"]["Honda"] = pygame.image.load("images/objetos/Armas/Armas a distancia simples/Honda.png")

        self.imgs["Armas c/c marciales"]["Alabarda"] = pygame.image.load("images/objetos/Armas/Armas cc marciales/Alabarda.png")
        self.imgs["Armas c/c marciales"]["Atarraga"] = pygame.image.load("images/objetos/Armas/Armas cc marciales/Atarraga.png")
        self.imgs["Armas c/c marciales"]["Cimitarra"] = pygame.image.load("images/objetos/Armas/Armas cc marciales/Cimitarra.png")
        self.imgs["Armas c/c marciales"]["Espada corta"] = pygame.image.load("images/objetos/Armas/Armas cc marciales/Espada corta.png")
        self.imgs["Armas c/c marciales"]["Espada larga"] = pygame.image.load("images/objetos/Armas/Armas cc marciales/Espada larga.png")
        self.imgs["Armas c/c marciales"]["Espadón"] = pygame.image.load("images/objetos/Armas/Armas cc marciales/Espadón.png")
        self.imgs["Armas c/c marciales"]["Estoque"] = pygame.image.load("images/objetos/Armas/Armas cc marciales/Estoque.png")
        self.imgs["Armas c/c marciales"]["Hacha de batalla"] = pygame.image.load("images/objetos/Armas/Armas cc marciales/Hacha de batalla.png")
        self.imgs["Armas c/c marciales"]["Gran hacha"] = pygame.image.load("images/objetos/Armas/Armas cc marciales/Gran hacha.png")
        self.imgs["Armas c/c marciales"]["Guja"] = pygame.image.load("images/objetos/Armas/Armas cc marciales/Guja.png")
        self.imgs["Armas c/c marciales"]["Lanza de caballería"] = pygame.image.load("images/objetos/Armas/Armas cc marciales/Lanza de caballería.png")
        self.imgs["Armas c/c marciales"]["Látigo"] = pygame.image.load("images/objetos/Armas/Armas cc marciales/Látigo.png")
        self.imgs["Armas c/c marciales"]["Lucero del alba"] = pygame.image.load("images/objetos/Armas/Armas cc marciales/Lucero del alba.png")
        self.imgs["Armas c/c marciales"]["Martillo de guerra"] = pygame.image.load("images/objetos/Armas/Armas cc marciales/Martillo de guerra.png")
        self.imgs["Armas c/c marciales"]["Mayal"] = pygame.image.load("images/objetos/Armas/Armas cc marciales/Mayal.png")
        self.imgs["Armas c/c marciales"]["Pica"] = pygame.image.load("images/objetos/Armas/Armas cc marciales/Pica.png")
        self.imgs["Armas c/c marciales"]["Pica de guerra"] = pygame.image.load("images/objetos/Armas/Armas cc marciales/Pica de guerra.png")
        self.imgs["Armas c/c marciales"]["Tridente"] = pygame.image.load("images/objetos/Armas/Armas cc marciales/Tridente.png")
        self.imgs["Armas a distancia marciales"]["Arco largo"] = pygame.image.load("images/objetos/Armas/Armas a distancia marciales/Arco largo.png")
        self.imgs["Armas a distancia marciales"]["Ballesta de mano"] = pygame.image.load("images/objetos/Armas/Armas a distancia marciales/Ballesta de mano.png")
        self.imgs["Armas a distancia marciales"]["Ballesta pesada"] = pygame.image.load("images/objetos/Armas/Armas a distancia marciales/Ballesta pesada.png")
        self.imgs["Armas a distancia marciales"]["Cerbatana"] = pygame.image.load("images/objetos/Armas/Armas a distancia marciales/Cerbatana.png")

        # Objetos variados
        self.imgs["Refugio"]["Saco de dormir"] = pygame.image.load("images/objetos/Objeto/Refugio/Saco de dormir.png")
        self.imgs["Mecanico"]["Palanca"] = pygame.image.load("images/objetos/Objeto/Mecanico/Palanca.png")
        self.imgs["Mecanico"]["Martillo"] = pygame.image.load("images/objetos/Objeto/Mecanico/Martillo.png")
        self.imgs["Otros"]["Piton"] = pygame.image.load("images/objetos/Objeto/Otros/Pitón.png")
        self.imgs["Otros"]["Yesquero"] = pygame.image.load("images/objetos/Objeto/Otros/Yesquero.png")
        self.imgs["Otros"]["Cuerda de cáñamo"] = pygame.image.load("images/objetos/Objeto/Otros/Cuerda de cáñamo.png")
        self.imgs["Iluminación"]["Antorcha"] = pygame.image.load("images/objetos/Objeto/Iluminación/Antorcha.png")
        self.imgs["Comida"]["Ración"] = pygame.image.load("images/objetos/Objeto/Comida/Ración.png")
        self.imgs["Bebida"]["Odre de agua"] = pygame.image.load("images/objetos/Objeto/Bebida/Odre de agua.png")
        self.imgs["Munición"]["Flecha"] = pygame.image.load("images/objetos/Objeto/Munición/Flecha.png")
        self.imgs["Almacenaje"]["Mochila"] = pygame.image.load("images/objetos/Objeto/Almacenaje/Mochila.png")
        self.imgs["Kit"]["De cocina"] = pygame.image.load("images/objetos/Objeto/Kit/De cocina.png")

        self.imgs["Escudo"]["Escudo básico"] = pygame.image.load("images/objetos/Armadura/Escudo/Escudo básico.png")

        self.imgs["Llave"]["Llave"] = pygame.image.load("images/objetos/Llave/Llave.png")

        self.imgs["Recoleccion"]["Seta"] = pygame.image.load("images/objetos/items/seta.png")
        self.imgs["Recoleccion"]["Esmeralda"] = pygame.image.load("images/objetos/items/esmeralda.png")
        self.imgs["Recoleccion"]["Rubí"] = pygame.image.load("images/objetos/items/rubi.png")
        self.imgs["Recoleccion"]["Mineral"] = pygame.image.load("images/objetos/items/mineral.png")
        self.imgs["Recoleccion"]["Hongo"] = pygame.image.load("images/objetos/items/hongo.png")

        self.changePhoto = False
        self.currentImageToShow = ""
        self.imagePhoto = ""
        self.currentImageBkgToShow = ""
        self.map = None
        self.ubicacion = ""

        #fuentes y colores
        self.fuente = pygame.font.SysFont(font, 70)
        self.color_white = (255,255,255)
        self.color_black = (0,0,0)
        self.back = self.fuente.render('Volver al menú', True, self.color_white)
        self.enviar_msg = self.fuente.render('Enviar mensaje', True, self.color_white)
        self.pedir_turno_palabra = self.fuente.render('Pedir la palabra', True, self.color_white)
        self.liberar_turno_palabra = self.fuente.render('Ceder la palabra', True, self.color_white)
        self.continuar = self.fuente.render('¡Estoy preparado!', True, self.color_white)
        self.msg = None
        self.msg1 = None
        self.msg2 = None
        self.msg3 = None
        self.textoDM = queue.Queue()
        self.image = queue.Queue()
        self.currentTextToShow = ""
        self.cont = 0
        self.openedInventory = False
        self.intercambio = False

        #estado variable
        self.contMsg = 0 #por defecto empieza en 0

        self.filas = [self.height/6.3063, self.height/6.3063 + self.height/16.2791]
        self.columnas = [self.width/3.1250, self.width/3.1250 + self.width/28.5714, self.width/3.1250 + self.width/28.5714*2, self.width/3.1250 + self.width/28.5714*3, self.width/3.1250 + self.width/28.5714*4, self.width/3.1250 + self.width/28.5714*5, self.width/3.1250 + self.width/28.5714*6, self.width/3.1250 + self.width/28.5714*7, self.width/3.1250 + self.width/28.5714*8, self.width/3.1250 + self.width/28.5714*9]
        self.base_x_size = self.width/30.7692
        self.base_y_size =  self.height/17.5000


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
            if(not self.GLOBAL.getViewMap()):
                self.screen.blit(pygame.transform.scale(self.currentImageBkgToShow, (self.width/1.4252, self.height/1.5837)), (self.width/150.0000, self.height/87.5000)) #842 442 8 8
            else:
                if((not self.openedInventory)):
                    self.screen = self.map.drawMapInGame(self.ubicacion,self.width,self.height,self.screen,self.personaje.coordenadas_actuales_r)
                    self.screen = self.personaje.renderLast(self.map, self.ubicacion, self.width, self.height, self.screen)
                    self.screen.blit(pygame.transform.scale(self.butonInv, (self.width/37.5000, self.height/21.8750)),(self.width/1.4706, self.height/1.7157)) 
                else:
                    # Pantalla del inventario
                    self.screen.blit(pygame.transform.scale(self.invetoryBkg, (self.width/1.4252, self.height/1.5837)), (self.width/150.0000, self.height/87.5000))
                    self.screen.blit(pygame.transform.scale(self.flecha, (self.width/37.5000, self.height/21.8750)), (self.width/120.0000, self.height/70.0000)) #32 32 10 10
                    self.peso = self.fuente3.render(str(self.personaje.equipo.peso_actual), True, self.color_black)
                    self.screen.blit(self.peso, (self.width/14.1176, self.height/2.1472)) #85 326
                    self.pc = self.fuente1.render(str(self.personaje.pc), True, self.color_black)
                    self.pp = self.fuente1.render(str(self.personaje.pp), True, self.color_black)
                    self.pe = self.fuente1.render(str(self.personaje.pe), True, self.color_black)
                    self.po = self.fuente1.render(str(self.personaje.po), True, self.color_black)
                    self.ppt = self.fuente1.render(str(self.personaje.ppt), True, self.color_black)
                    self.screen.blit(self.pc, (self.width/3.4286, self.height/1.7632)) #350 397
                    self.screen.blit(self.pp, (self.width/2.9630, self.height/1.7632)) #405 397
                    self.screen.blit(self.pe, (self.width/2.6030, self.height/1.7632)) #461 397
                    self.screen.blit(self.po, (self.width/2.3256, self.height/1.7632)) #516 397
                    self.screen.blit(self.ppt, (self.width/2.0979, self.height/1.7632)) #572 397
                    #Armadura slot
                    if(self.personaje.equipo.armadura_actual != None):
                        # Cargamos cuál es su armadura
                        img_armadura = self.imgs[self.personaje.equipo.armadura_actual[0]][self.personaje.equipo.armadura_actual[1]]
                        if(self.slot_selected == 'armor_slot'):
                            if(self.intercambio):
                                self.screen.blit(pygame.transform.scale(self.intercambio_slot, (self.width/16.9014, self.height/9.5890)), (self.width/16.2162, self.height/9.7222)) # 71 73 74 72
                            else:
                                self.screen.blit(pygame.transform.scale(self.selected_slot, (self.width/16.9014, self.height/9.5890)), (self.width/16.2162, self.height/9.7222)) # 71 73 74 72
                        self.screen.blit(pygame.transform.scale(img_armadura, (self.width/16.9014, self.height/9.5890)), (self.width/16.2162, self.height/9.7222)) # 71 73 74 72
                            
                    # Mano dcha
                    if(self.personaje.equipo.objeto_equipado_mano_derecha != None):
                        img_armadura = self.imgs[self.personaje.equipo.objeto_equipado_mano_derecha[0]][self.personaje.equipo.objeto_equipado_mano_derecha[1]]
                        if(self.slot_selected == 'mano derecha'):
                            if(self.intercambio):
                                self.screen.blit(pygame.transform.scale(self.intercambio_slot, (self.width/16.2162, self.height/9.2105)), (self.width/48.0000, self.height/3.6842)) # 74 76 25 190
                            else:
                                self.screen.blit(pygame.transform.scale(self.selected_slot, (self.width/16.2162, self.height/9.2105)), (self.width/48.0000, self.height/3.6842)) # 74 76 25 190
                        self.screen.blit(pygame.transform.scale(img_armadura, (self.width/16.2162, self.height/9.2105)), (self.width/48.0000, self.height/3.6842)) # 74 76 25 190

                    # Mano izqda
                    if(self.personaje.equipo.objeto_equipado_mano_izquierda != None): 
                        img_armadura = self.imgs[self.personaje.equipo.objeto_equipado_mano_izquierda[0]][self.personaje.equipo.objeto_equipado_mano_izquierda[1]]
                        if(self.slot_selected == 'mano izquierda'):
                            if(self.intercambio):
                                self.screen.blit(pygame.transform.scale(self.intercambio_slot, (self.width/16.2162, self.height/9.2105)), (self.width/10.1695, self.height/3.6842)) # 74 76 118 190
                            else:
                                self.screen.blit(pygame.transform.scale(self.selected_slot, (self.width/16.2162, self.height/9.2105)), (self.width/10.1695, self.height/3.6842)) # 74 76 118 190
                        self.screen.blit(pygame.transform.scale(img_armadura, (self.width/16.2162, self.height/9.2105)), (self.width/10.1695, self.height/3.6842)) # 74 76 118 190
                                    
                    
                    # Características
                    att = self.personaje.car-10
                    if(att < 0):
                        att -=1
                    puntaje = str(int(att // 2))
                    self.car = self.fuente1.render(str(self.personaje.car)+"("+puntaje+")", True, self.color_black)
                    att = self.personaje.sab-10
                    if(att < 0):
                        att -=1
                    puntaje = str(int(att // 2))
                    self.sab = self.fuente1.render(str(self.personaje.sab)+"("+puntaje+")", True, self.color_black)
                    att = self.personaje.des-10
                    if(att < 0):
                        att -=1
                    puntaje = str(int(att // 2))
                    self.des = self.fuente1.render(str(self.personaje.des)+"("+puntaje+")", True, self.color_black)
                    att = self.personaje.int-10
                    if(att < 0):
                        att -=1
                    puntaje = str(int(att // 2))
                    self.int = self.fuente1.render(str(self.personaje.int)+"("+puntaje+")", True, self.color_black)
                    att = self.personaje.fu-10
                    if(att < 0):
                        att -=1
                    puntaje = str(int(att // 2))
                    self.fu = self.fuente1.render(str(self.personaje.fu)+"("+puntaje+")", True, self.color_black)
                    att = self.personaje.cons-10
                    if(att < 0):
                        att -=1
                    puntaje = str(int(att // 2))
                    self.cons = self.fuente1.render(str(self.personaje.cons)+"("+puntaje+")", True, self.color_black)
                    self.screen.blit(self.car, (self.width/2.2989, self.height/12.0690)) #522 58
                    self.screen.blit(self.sab, (self.width/2.0761, self.height/12.0690)) #578 58
                    self.screen.blit(self.des, (self.width/1.8957, self.height/12.0690)) #633 58
                    self.screen.blit(self.int, (self.width/1.7417, self.height/12.0690)) #689 58
                    self.screen.blit(self.fu, (self.width/1.6129, self.height/12.0690)) #744 58
                    self.screen.blit(self.cons, (self.width/1.5000, self.height/12.0690)) #800 58

                    # BPC
                    self.bpc = self.fuente3.render(str(self.personaje.bpc), True, self.color_black)
                    self.screen.blit(self.bpc, (self.width/4.8980, self.height/4.6358)) #245 151
                    # CA
                    self.ca = self.fuente1.render(str(self.personaje.ca), True, self.color_black)
                    self.screen.blit(self.ca, (self.width/5.1064, self.height/12.0690)) #235 58
                    # Vida
                    self.vida = self.fuente1.render(str(self.personaje.vida_temp), True, self.color_black)
                    self.screen.blit(self.vida, (self.width/4.1237, self.height/12.0690)) #291 58

                    # Clase
                    self.clase = self.fuente1.render(str(self.personaje.tipo_clase), True, self.color_black)
                    self.screen.blit(self.clase, (self.width/3.3241, self.height/12.0690)) #361 58

                    # Objetos de los slot normales
                    base_x_start = self.width/3.1250
                    base_y_start = self.height/6.3063
                    base_x_size = self.width/30.7692
                    base_y_size =  self.height/17.5000
                    dif_x = self.width/35.2941
                    dif_y = self.height/20.5882
                    base_c_x_start = self.width/2.9412
                    base_c_y_start = self.height/4.9296
                    base_c_x_size = self.width/46.1538
                    base_c_y_size = self.height/36.8421
                    dif_l_x = self.width/600.0000
                    dif_l_y = self.height/700.0000
                    for slot_name, objeto in self.personaje.equipo.objetos.items():
                        if(objeto != None):
                            categoria = objeto[0]
                            name = objeto[1]
                            slot_num = int(slot_name[5:])
                            fila = int(slot_num // 10) # Se cuenta a partir de 0 
                            col = int(slot_num % 10)
                            img_slot = self.imgs[categoria][name]
                            if(self.slot_selected == slot_num):
                                if(self.intercambio):
                                    self.screen.blit(pygame.transform.scale(self.intercambio_slot, (base_x_size, base_y_size)), (base_x_start+dif_x*col, base_y_start+dif_y*fila)) #39 40 384 111 
                                else:
                                    self.screen.blit(pygame.transform.scale(self.selected_slot, (base_x_size, base_y_size)), (base_x_start+dif_x*col, base_y_start+dif_y*fila)) #39 40 384 111 
                                self.screen.blit(pygame.transform.scale(img_slot, (self.width/8.6957, self.height/4.9645)), (self.width/1.7143, self.height/2.3973))
                                obj_name = self.fuente3.render(str(name), True, self.color_black)
                                self.screen.blit(obj_name, (self.width/1.7217, self.height/3.0043)) 
                            self.screen.blit(pygame.transform.scale(img_slot, (base_x_size, base_y_size)), (base_x_start+dif_x*col, base_y_start+dif_y*fila)) #39 40 384 111 
                    for slot_name, objeto in self.personaje.equipo.objetos.items():
                        if(objeto != None):
                            cantidad = objeto[3]
                            slot_num = int(slot_name[5:])
                            fila = int(slot_num // 10) # Se cuenta a partir de 0 
                            col = int(slot_num % 10)
                            self.screen.blit(pygame.transform.scale(self.whitebkg, (base_c_x_size, base_c_y_size)), (base_c_x_start+dif_x*col, base_c_y_start+dif_y*fila))
                            cantidadLetra = self.fuente1.render(str(cantidad), True, self.color_black)
                            self.screen.blit(cantidadLetra, (base_c_x_start+dif_x*col+dif_l_x, base_c_y_start+dif_y*fila+dif_l_y))
            if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
            else:
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
            
            if(self.availableStart):
                if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start2,x,y)):
                    self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
            
            if(self.startBoton):
                self.screen.blit(pygame.transform.scale(self.continuar, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
            else:
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
                        self.imagePhoto = pygame.image.load(self.currentImageToShow)
                except:
                    self.currentImageToShow = ""

                if(self.currentImageToShow != ""):
                    self.screen.blit(pygame.transform.scale(self.imagePhoto, (self.width/4.7059, self.height/2.6415)), (self.width/1.3378, self.height/14.0000)) #255 265 897 50
                
                # Para mostrar el nombre del NPC
                nombre_NPC = self.GLOBAL.getShowNombreNPC()
                if(nombre_NPC != ""):
                    textoNPC = self.fuente5.render(nombre_NPC, True, self.color_black)
                    self.screen.blit(textoNPC,(self.width/1.3514, self.height/1.8421)) #888 380

        pygame.display.update() 

    def calculateCurrentSlot(self,pos_x,pos_y):
        for fila in self.filas:
            for col in self.columnas:
                if((pos_x >= col and pos_x <= self.base_x_size+col) and (pos_y >= fila and pos_y <= self.base_y_size + fila)):
                    f_n = self.filas.index(fila)
                    c_n = self.columnas.index(col)
                    slot = c_n + f_n*10
                    return slot
        
        # Comprobamos si lo que ha clickeado es la armadura
        armor_x_size = self.width/16.9014
        armor_y_size = self.height/9.5890
        armor_x_start = self.width/16.2162
        armor_y_start = self.height/9.7222
        if((pos_x >= armor_x_start and pos_x <= armor_x_size+armor_x_start) and (pos_y >= armor_y_start and pos_y <= armor_y_size + armor_y_start)):
            return 'armor_slot'
        
        # Comprobamos si lo que ha clickeado es la mano dcha o la izqda
        mano_dcha_x_size = self.width/16.2162
        mano_dcha_y_size = self.height/9.2105
        mano_dcha_x_start = self.width/48.0000
        mano_dcha_y_start = self.height/3.6842
        mano_izda_x_start = self.width/10.1695
        if((pos_x >= mano_dcha_x_start and pos_x <= mano_dcha_x_size+mano_dcha_x_start) and (pos_y >= mano_dcha_y_start and pos_y <= mano_dcha_y_size + mano_dcha_y_start)):
            return 'mano derecha'
        if((pos_x >= mano_izda_x_start and pos_x <= mano_dcha_x_size+mano_izda_x_start) and (pos_y >= mano_dcha_y_start and pos_y <= mano_dcha_y_size + mano_dcha_y_start)):
            return 'mano izquierda'

        return None

    def cerrarHilo(self):
        #si está activo, que lo detenga
        if self.hiloProcesamientoPartida != None and self.hiloProcesamientoPartida.is_alive():
            try:
                self.ProcesamientoPartida.maquina.DM.engine.stop()
                self.ProcesamientoPartida.maquina.DM.engine.endLoop()
            except:
                pass
            self.ProcesamientoPartida.finished = True
            self.GLOBAL.setTextoDM("")
            ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(self.hiloProcesamientoPartida.ident), ctypes.py_object(SystemExit)
            )


    def render(self):
        #render screen
        self.letterwidth = (self.width/3.4286)/6 #cálculo de la base en píxeles 
        self.lettersize = int(self.letterwidth + 0.5 * self.letterwidth) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente2 = pygame.font.SysFont(self.font,self.lettersize)

        self.letterwidth1 = (self.width/3.4286)/25 #cálculo de la base en píxeles 
        self.lettersize1 = int(self.letterwidth1 + 0.1 * self.letterwidth1) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente1 = pygame.font.SysFont(self.font,self.lettersize1)

        self.letterwidth2 = (self.width/3.4286)/20 #cálculo de la base en píxeles 
        self.lettersize2 = int(self.letterwidth2 + 0.5 * self.letterwidth2) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente3 = pygame.font.SysFont(self.font,self.lettersize2)

        self.letterwidth3 = (self.width/3.4286)/32 #cálculo de la base en píxeles 
        self.lettersize3 = int(self.letterwidth3 + 0.5 * self.letterwidth3) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente4 = pygame.font.SysFont(self.font,self.lettersize3)

        self.letterwidth4 = (self.width/3.4286)/15 #cálculo de la base en píxeles 
        self.lettersize4 = int(self.letterwidth4 + 0.5 * self.letterwidth4) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente5 = pygame.font.SysFont(self.font,self.lettersize4)

        #para extraer qué ubicación se escogió
        conn = sqlite3.connect("simuladordnd.db")
        cur = conn.cursor()
        #cargamos la partida 1, si existe: el orden de las columnas será ese
        cur.execute("SELECT ubicacion_historia FROM partida WHERE numPartida = '"+self.currentPartida+"'")
        rows = cur.fetchall() #para llegar a esta pantalla, la pantalla tiene que existir sí o sí
        if(rows[0] != None):
            ubicacion = rows[0][0]
        conn.close()
        self.currentImageBkgToShow = pygame.image.load("images/background/"+ubicacion+".png")
        self.ubicacion = ubicacion
        self.personaje.loadAnimations(ubicacion)

        if(self.GLOBAL.getActualPartidaState() == "loading"):
            self.startBoton = True

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
                self.ProcesamientoPartida.initialize(self.numJugadores,self.DMVoice,self.currentPartida,self.personaje,self,self.width,self.height)
                self.hiloProcesamientoPartida = threading.Thread(target=self.ProcesamientoPartida.prepararPartida)
                self.hiloProcesamientoPartida.start()
            else:
                #TODO: esperar a recibir maquina de estados para la partida, y crearla con la configuración de voz y efectos
                pass
        elif(self.GLOBAL.getActualPartidaState() == "partida"):
            self.peso = self.fuente3.render(str(self.personaje.equipo.peso_actual), True, self.color_black)
            self.pc = self.fuente1.render(str(self.personaje.pc), True, self.color_black)
            self.pp = self.fuente1.render(str(self.personaje.pp), True, self.color_black)
            self.pe = self.fuente1.render(str(self.personaje.pe), True, self.color_black)
            self.po = self.fuente1.render(str(self.personaje.po), True, self.color_black)
            self.ppt = self.fuente1.render(str(self.personaje.ppt), True, self.color_black)
            self.screen.blit(pygame.transform.scale(self.backgroundPartidaPic, (self.width,self.height)), (0, 0))
            if(not self.GLOBAL.getViewMap()):
                self.screen.blit(pygame.transform.scale(self.currentImageBkgToShow, (self.width/1.4252, self.height/1.5837)), (self.width/150.0000, self.height/87.5000)) #842 442 8 8
            else:
                self.screen = self.map.drawMapInGame(self.ubicacion,self.width,self.height,self.screen,self.personaje.coordenadas_actuales_r)
                self.screen = self.personaje.renderLast(self.map, self.ubicacion, self.width, self.height, self.screen)
                self.screen.blit(pygame.transform.scale(self.butonInv, (self.width/37.5000, self.height/21.8750)),(self.width/1.4706, self.height/1.7157)) 
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
            if(self.availableStart):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
            
            if(self.startBoton):
                self.screen.blit(pygame.transform.scale(self.continuar, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
            else:
                self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491

            self.inputBoxDescripcion = pygame.Rect(self.width/48.0000, self.height/1.4894, self.width/1.4815, self.height/5.6452) #25 470 810 124
            pygame.draw.rect(self.screen, self.color_white, self.inputBoxDescripcion, 2)
        pygame.display.update() 

    def renderTextBlock(self,text,position):

        (x,y) = pygame.mouse.get_pos()

        self.inputBoxDescripcion = pygame.Rect(self.width/48.0000, self.height/1.4894, self.width/1.4815, self.height/5.6452) #25 470 810 124
        pygame.draw.rect(self.screen, self.color_white, self.inputBoxDescripcion, 0)
        # img = self.GLOBAL.getImagePartida() 
        # if(img != ""):
        #     self.image.put(img)

        # try:
        #     if(self.changePhoto):
        #         self.currentImageToShow = self.image.get()
        #         self.changePhoto = False
        #         self.imagePhoto = pygame.image.load(self.currentImageToShow)
        # except:
        #     self.currentImageToShow = ""

        # if(self.currentImageToShow != ""):
        #     self.screen.blit(pygame.transform.scale(self.imagePhoto, (self.width/4.7059, self.height/2.6415)), (self.width/1.3378, self.height/14.0000)) #255 265 897 50



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
            self.GLOBAL.setShowImage(False)

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
            x_start1 = self.width/1.4706
            y_start1 = self.height/1.7157
            x_size1 = self.width/37.5000
            y_size1 = self.height/21.8750
            x_size4 = self.width/37.5000
            y_size4 = self.height/21.8750
            x_start4 = self.width/120.0000
            y_start4 = self.height/70.0000
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
                #Establezco la posición del personaje
                self.map = self.GLOBAL.getMapa()
                self.personaje.mapa = self.map
                self.personaje.setCurrentPos(self.map.playersCurrentPos[self.id],self.map.map_tileSize,self.width,self.height)
                self.personaje.setFPS(maxFPS)
                
            else:
                change_frame = maxFPS//5
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
                
                if(self.canCheck and self.textWriten and self.GLOBAL.getCanStart()):
                    self.availableStart = True
                    self.canCheck = False
                if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                    self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
                
                if(self.availableStart):
                    if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start2,x,y)):
                        self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                    else:
                        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                else: 
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                
                if(self.startBoton):
                    self.screen.blit(pygame.transform.scale(self.continuar, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                else:
                    self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                    if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start3,x,y)):
                        self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                    else:
                        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                    self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                
                img = self.GLOBAL.getImagePartida() 
                if(img != ""):
                    self.image.put(img)

                try:
                    if(self.changePhoto):
                        self.currentImageToShow = self.image.get()
                        self.changePhoto = False
                        self.imagePhoto = pygame.image.load(self.currentImageToShow)
                except Exception as e:
                    print(e)
                    self.currentImageToShow = ""

                if(self.currentImageToShow != ""):
                    self.screen.blit(pygame.transform.scale(self.imagePhoto, (self.width/4.7059, self.height/2.6415)), (self.width/1.3378, self.height/14.0000)) #255 265 897 50
                # Para mostrar el nombre del NPC
                nombre_NPC = self.GLOBAL.getShowNombreNPC()
                if(nombre_NPC != ""):
                    textoNPC = self.fuente5.render(nombre_NPC, True, self.color_black)
                    self.screen.blit(textoNPC,(self.width/1.3514, self.height/1.8421)) #888 380

                aux = self.GLOBAL.extractAndRemoveTextoDM()
                if(aux != ""):
                    self.textoDM.put(aux)
                try:
                    if(self.currentTextToShow == ""):
                        self.currentTextToShow = ["<DM>: "+self.textoDM.get(block = False),0,None]
                        self.currentTextToShow = [self.currentTextToShow[0],0,len(self.currentTextToShow[0].split(" "))] #texto,palabras_printeadas,total_palabras_a_printear
                except:
                    self.currentTextToShow = ""
                self.currentFrame +=1 
                #print(self.currentFrame)
                if(self.currentFrame >= change_frame):
                    self.currentFrame = 0
                    if(self.currentTextToShow != "" and self.currentTextToShow[0] != "" and (self.currentTextToShow[2]) >= (self.currentTextToShow[1])):
                        #hay que printear animado el texto    
                        #Cargamos la animación
                            if(self.currentTextToShow[2] > self.currentTextToShow[1]):
                                #printear texto con una letra más
                                self.renderTextBlock(self.currentTextToShow[0],self.currentTextToShow[1])
                                self.currentTextToShow[1] +=1
                            elif(self.currentTextToShow[2] == self.currentTextToShow[1]):
                                self.textWriten = True
                                yes = self.GLOBAL.getShowImage()
                                if(yes):
                                    self.changePhoto = True
                                    self.GLOBAL.setShowImage(False)
                                self.currentTextToShow = ""
                            else:
                                self.currentTextToShow = ""
                    yes = self.GLOBAL.getShowImage()
                    if(yes):
                        self.changePhoto = True
                        self.GLOBAL.setShowImage(False)

                # Renderizamos al jugador si se ve el mapa
                self.cont +=1
                if(self.cont >= 4):
                    self.cont = 0
                    ma = self.GLOBAL.getViewMap()
                    if(ma):
                        if(not self.openedInventory):
                            self.screen = self.personaje.render(maxFPS,self.map, self.ubicacion, self.width, self.height, self.screen)
                            if(self.checkIfMouseIsInButton(x_size1,y_size1,x_start1,y_start1,x,y)):
                                self.screen.blit(pygame.transform.scale(self.butonInv_selected,(self.width/37.5000, self.height/21.8750)),(self.width/1.4706, self.height/1.7157)) 
                            else:
                                self.screen.blit(pygame.transform.scale(self.butonInv, (self.width/37.5000, self.height/21.8750)),(self.width/1.4706, self.height/1.7157)) 
                        else:
                            # Pantalla de inventario
                            self.screen.blit(pygame.transform.scale(self.invetoryBkg, (self.width/1.4252, self.height/1.5837)), (self.width/150.0000, self.height/87.5000))
                            if(self.checkIfMouseIsInButton(x_size4,y_size4,x_start4,y_start4,x,y)):
                                self.screen.blit(pygame.transform.scale(self.flecha_selected, (self.width/37.5000, self.height/21.8750)), (self.width/120.0000, self.height/70.0000)) #32 32 10 10
                            else:
                                self.screen.blit(pygame.transform.scale(self.flecha, (self.width/37.5000, self.height/21.8750)), (self.width/120.0000, self.height/70.0000)) #32 32 10 10
                            self.peso = self.fuente3.render(str(self.personaje.equipo.peso_actual), True, self.color_black)
                            self.screen.blit(self.peso, (self.width/14.1176, self.height/2.1472)) #85 326
                            self.pc = self.fuente1.render(str(self.personaje.pc), True, self.color_black)
                            self.pp = self.fuente1.render(str(self.personaje.pp), True, self.color_black)
                            self.pe = self.fuente1.render(str(self.personaje.pe), True, self.color_black)
                            self.po = self.fuente1.render(str(self.personaje.po), True, self.color_black)
                            self.ppt = self.fuente1.render(str(self.personaje.ppt), True, self.color_black)
                            self.screen.blit(self.pc, (self.width/3.4286, self.height/1.7632)) #350 397
                            self.screen.blit(self.pp, (self.width/2.9630, self.height/1.7632)) #405 397
                            self.screen.blit(self.pe, (self.width/2.6030, self.height/1.7632)) #461 397
                            self.screen.blit(self.po, (self.width/2.3256, self.height/1.7632)) #516 397
                            self.screen.blit(self.ppt, (self.width/2.0979, self.height/1.7632)) #572 397
                            #Armadura slot
                            if(self.personaje.equipo.armadura_actual != None):
                                # Cargamos cuál es su armadura
                                img_armadura = self.imgs[self.personaje.equipo.armadura_actual[0]][self.personaje.equipo.armadura_actual[1]]
                                if(self.slot_selected == 'armor_slot'):
                                    if(self.intercambio):
                                        self.screen.blit(pygame.transform.scale(self.intercambio_slot, (self.width/16.9014, self.height/9.5890)), (self.width/16.2162, self.height/9.7222)) # 71 73 74 72
                                    else:
                                        self.screen.blit(pygame.transform.scale(self.selected_slot, (self.width/16.9014, self.height/9.5890)), (self.width/16.2162, self.height/9.7222)) # 71 73 74 72
                                self.screen.blit(pygame.transform.scale(img_armadura, (self.width/16.9014, self.height/9.5890)), (self.width/16.2162, self.height/9.7222)) # 71 73 74 72
                            
                            # Mano dcha
                            if(self.personaje.equipo.objeto_equipado_mano_derecha != None):
                                img_armadura = self.imgs[self.personaje.equipo.objeto_equipado_mano_derecha[0]][self.personaje.equipo.objeto_equipado_mano_derecha[1]]
                                if(self.slot_selected == 'mano derecha'):
                                    if(self.intercambio):
                                        self.screen.blit(pygame.transform.scale(self.intercambio_slot, (self.width/16.2162, self.height/9.2105)), (self.width/48.0000, self.height/3.6842)) # 74 76 25 190
                                    else:
                                        self.screen.blit(pygame.transform.scale(self.selected_slot, (self.width/16.2162, self.height/9.2105)), (self.width/48.0000, self.height/3.6842)) # 74 76 25 190
                                self.screen.blit(pygame.transform.scale(img_armadura, (self.width/16.2162, self.height/9.2105)), (self.width/48.0000, self.height/3.6842)) # 74 76 25 190

                            # Mano izqda
                            if(self.personaje.equipo.objeto_equipado_mano_izquierda != None): 
                                img_armadura = self.imgs[self.personaje.equipo.objeto_equipado_mano_izquierda[0]][self.personaje.equipo.objeto_equipado_mano_izquierda[1]]
                                if(self.slot_selected == 'mano izquierda'):
                                    if(self.intercambio):
                                        self.screen.blit(pygame.transform.scale(self.intercambio_slot, (self.width/16.2162, self.height/9.2105)), (self.width/10.1695, self.height/3.6842)) # 74 76 118 190
                                    else:
                                        self.screen.blit(pygame.transform.scale(self.selected_slot, (self.width/16.2162, self.height/9.2105)), (self.width/10.1695, self.height/3.6842)) # 74 76 118 190
                                self.screen.blit(pygame.transform.scale(img_armadura, (self.width/16.2162, self.height/9.2105)), (self.width/10.1695, self.height/3.6842)) # 74 76 118 190
                                    
                            # Características
                            att = self.personaje.car-10
                            if(att < 0):
                                att -=1
                            puntaje = str(int(att // 2))
                            self.car = self.fuente1.render(str(self.personaje.car)+"("+puntaje+")", True, self.color_black)
                            att = self.personaje.sab-10
                            if(att < 0):
                                att -=1
                            puntaje = str(int(att // 2))
                            self.sab = self.fuente1.render(str(self.personaje.sab)+"("+puntaje+")", True, self.color_black)
                            att = self.personaje.des-10
                            if(att < 0):
                                att -=1
                            puntaje = str(int(att // 2))
                            self.des = self.fuente1.render(str(self.personaje.des)+"("+puntaje+")", True, self.color_black)
                            att = self.personaje.int-10
                            if(att < 0):
                                att -=1
                            puntaje = str(int(att // 2))
                            self.int = self.fuente1.render(str(self.personaje.int)+"("+puntaje+")", True, self.color_black)
                            att = self.personaje.fu-10
                            if(att < 0):
                                att -=1
                            puntaje = str(int(att // 2))
                            self.fu = self.fuente1.render(str(self.personaje.fu)+"("+puntaje+")", True, self.color_black)
                            att = self.personaje.cons-10
                            if(att < 0):
                                att -=1
                            puntaje = str(int(att // 2))
                            self.cons = self.fuente1.render(str(self.personaje.cons)+"("+puntaje+")", True, self.color_black)

                            self.screen.blit(self.car, (self.width/2.2989, self.height/12.0690)) #522 58
                            self.screen.blit(self.sab, (self.width/2.0761, self.height/12.0690)) #578 58
                            self.screen.blit(self.des, (self.width/1.8957, self.height/12.0690)) #633 58
                            self.screen.blit(self.int, (self.width/1.7417, self.height/12.0690)) #689 58
                            self.screen.blit(self.fu, (self.width/1.6129, self.height/12.0690)) #744 58
                            self.screen.blit(self.cons, (self.width/1.5000, self.height/12.0690)) #800 58

                            # BPC
                            self.bpc = self.fuente3.render(str(self.personaje.bpc), True, self.color_black)
                            self.screen.blit(self.bpc, (self.width/4.8980, self.height/4.6358)) #245 151
                            # CA
                            self.ca = self.fuente1.render(str(self.personaje.ca), True, self.color_black)
                            self.screen.blit(self.ca, (self.width/5.1064, self.height/12.0690)) #235 58
                            # Vida
                            self.vida = self.fuente1.render(str(self.personaje.vida_temp), True, self.color_black)
                            self.screen.blit(self.vida, (self.width/4.1237, self.height/12.0690)) #291 58

                            # Clase
                            self.clase = self.fuente1.render(str(self.personaje.tipo_clase), True, self.color_black)
                            self.screen.blit(self.clase, (self.width/3.3241, self.height/12.0690)) #361 58

                            # Objetos de los slot normales
                            base_x_start = self.width/3.1250
                            base_y_start = self.height/6.3063
                            base_x_size = self.width/30.7692
                            base_y_size =  self.height/17.5000
                            dif_x = self.width/28.5714
                            dif_y = self.height/16.2791
                            base_c_x_start = self.width/2.9412
                            base_c_y_start = self.height/4.9296
                            base_c_x_size = self.width/46.1538
                            base_c_y_size = self.height/36.8421
                            dif_l_x = self.width/600.0000
                            dif_l_y = self.height/700.0000
                            for slot_name, objeto in self.personaje.equipo.objetos.items():
                                if(objeto != None):
                                    categoria = objeto[0]
                                    name = objeto[1]
                                    slot_num = int(slot_name[5:])
                                    fila = int(slot_num // 10) # Se cuenta a partir de 0 
                                    col = int(slot_num % 10)
                                    img_slot = self.imgs[categoria][name]
                                    if(self.slot_selected == slot_num):
                                        if(self.intercambio):
                                            self.screen.blit(pygame.transform.scale(self.intercambio_slot, (base_x_size, base_y_size)), (base_x_start+dif_x*col, base_y_start+dif_y*fila)) #39 40 384 111 
                                        else:
                                            self.screen.blit(pygame.transform.scale(self.selected_slot, (base_x_size, base_y_size)), (base_x_start+dif_x*col, base_y_start+dif_y*fila)) #39 40 384 111 
                                        self.screen.blit(pygame.transform.scale(img_slot, (self.width/8.6957, self.height/4.9645)), (self.width/1.7143, self.height/2.3973))
                                        obj_name = self.fuente3.render(str(name), True, self.color_black)
                                        self.screen.blit(obj_name, (self.width/1.7217, self.height/3.0043)) 
                                    self.screen.blit(pygame.transform.scale(img_slot, (base_x_size, base_y_size)), (base_x_start+dif_x*col, base_y_start+dif_y*fila)) #39 40 384 111 
                            for slot_name, objeto in self.personaje.equipo.objetos.items():
                                if(objeto != None):
                                    cantidad = objeto[3]
                                    slot_num = int(slot_name[5:])
                                    fila = int(slot_num // 10) # Se cuenta a partir de 0 
                                    col = int(slot_num % 10)
                                    self.screen.blit(pygame.transform.scale(self.whitebkg, (base_c_x_size, base_c_y_size)), (base_c_x_start+dif_x*col, base_c_y_start+dif_y*fila))
                                    cantidadLetra = self.fuente1.render(str(cantidad), True, self.color_black)
                                    self.screen.blit(cantidadLetra, (base_c_x_start+dif_x*col+dif_l_x, base_c_y_start+dif_y*fila+dif_l_y))
                pygame.display.update()
                    
    # size_x, size_y: tamaño del botón en x y en y
    # x_start y y_start: posición de la esquina izquierda del botón
    # pos_x y pos_y: posición actual del ratón
    def checkIfMouseIsInButton(self,size_x,size_y,x_start,y_start,pos_x,pos_y):
        if((pos_x >= x_start and pos_x <= size_x+x_start) and (pos_y >= y_start and pos_y <= size_y + y_start)):
            return True
        else:
            return False
        
    def hasPressedAKey(self,key,unicode):
        if(self.GLOBAL.getViewMap()):
            # Si se puede ver el mapa, podemos movernos
            if(key == pygame.K_DOWN):
                print("down")
                self.personaje.setDown(True)
                self.GLOBAL.setCanTalkToNPC(False)
                self.GLOBAL.setCanOpenChest([False,[None,None]])
            elif(key == pygame.K_UP):
                print("up")
                self.personaje.setUp(True)
                self.GLOBAL.setCanTalkToNPC(False)
                self.GLOBAL.setCanOpenChest([False,[None,None]])
            elif(key == pygame.K_LEFT):
                print("left")
                self.personaje.setLeft(True)
                self.GLOBAL.setCanTalkToNPC(False)
                self.GLOBAL.setCanOpenChest([False,[None,None]])
            elif(key == pygame.K_RIGHT):
                print("right")
                self.personaje.setRight(True)
                self.GLOBAL.setCanTalkToNPC(False)
                self.GLOBAL.setCanOpenChest([False,[None,None]])
            elif(key == pygame.K_t):
                if(self.GLOBAL.getViewMap() and (not self.openedInventory) and self.GLOBAL.getFinishedStart() and (not self.GLOBAL.getDMTalking())):
                    # Si se ve el mapa, no está abierto el inventario, el DM no está hablando y ya se ha leído la descripción -> al darle a la t, si está a 5 pies del NPC puede hablar con él
                    self.GLOBAL.setCanTalkToNPC(True)
                    self.GLOBAL.setCanOpenChest([False,[None,None]])
                    # Así le indico que puede hablar con el NPC
            elif(key == pygame.K_r):
                # Para recoger minerales, hongos, setas, sacos o romper rocas/sarcófagos
                if(self.GLOBAL.getViewMap() and (not self.openedInventory) and self.GLOBAL.getFinishedStart() and (not self.GLOBAL.getDMTalking())):
                    if(((self.personaje.playerAction == "WALK_DOWN") or (self.personaje.playerAction == "IDLE_DOWN"))):  
                        pos_x = self.personaje.coordenadas_actuales_r[0]
                        pos_y = self.personaje.coordenadas_actuales_r[1]+1
                    elif(((self.personaje.playerAction == "WALK_UP") or (self.personaje.playerAction == "IDLE_UP"))):
                        pos_x = self.personaje.coordenadas_actuales_r[0]
                        pos_y = self.personaje.coordenadas_actuales_r[1]-1
                    elif(((self.personaje.playerAction == "WALK_LEFT") or (self.personaje.playerAction == "IDLE_LEFT"))):
                        pos_x = self.personaje.coordenadas_actuales_r[0]-1
                        pos_y = self.personaje.coordenadas_actuales_r[1]
                    elif(((self.personaje.playerAction == "WALK_RIGHT") or (self.personaje.playerAction == "IDLE_RIGHT"))):
                        pos_x = self.personaje.coordenadas_actuales_r[0]+1
                        pos_y = self.personaje.coordenadas_actuales_r[1]
                    else:
                        pos_x = None
                        pos_y = None
                    self.GLOBAL.setCanBreak([True,[pos_x,pos_y]])
                    self.GLOBAL.setCanTalkToNPC(False)
                    self.GLOBAL.setCanOpenChest([False,[None,None]])

            elif(key == pygame.K_a):
                if(self.GLOBAL.getViewMap() and (not self.openedInventory) and self.GLOBAL.getFinishedStart() and (not self.GLOBAL.getDMTalking())):
                    # Si se ve el mapa, no está abierto el inventario, el DM no está hablando y ya se ha leído la descripción -> al darle a la t, si está a 5 pies del NPC puede hablar con él
                    if(((self.personaje.playerAction == "WALK_DOWN") or (self.personaje.playerAction == "IDLE_DOWN"))):  
                        pos_x = self.personaje.coordenadas_actuales_r[0]
                        pos_y = self.personaje.coordenadas_actuales_r[1]+1
                    elif(((self.personaje.playerAction == "WALK_UP") or (self.personaje.playerAction == "IDLE_UP"))):
                        pos_x = self.personaje.coordenadas_actuales_r[0]
                        pos_y = self.personaje.coordenadas_actuales_r[1]-1
                    elif(((self.personaje.playerAction == "WALK_LEFT") or (self.personaje.playerAction == "IDLE_LEFT"))):
                        pos_x = self.personaje.coordenadas_actuales_r[0]-1
                        pos_y = self.personaje.coordenadas_actuales_r[1]
                    elif(((self.personaje.playerAction == "WALK_RIGHT") or (self.personaje.playerAction == "IDLE_RIGHT"))):
                        pos_x = self.personaje.coordenadas_actuales_r[0]+1
                        pos_y = self.personaje.coordenadas_actuales_r[1]
                    else:
                        pos_x = None
                        pos_y = None
                    self.GLOBAL.setCanOpenChest([True,[pos_x,pos_y]])
                    self.GLOBAL.setCanTalkToNPC(False)
            elif(key == pygame.K_i):
                self.GLOBAL.setCanTalkToNPC(False)
                self.GLOBAL.setCanOpenChest([False,[None,None]])
                if(self.slot_selected != None):
                    self.intercambio = True
                    
            elif(key == pygame.K_x):
                self.GLOBAL.setCanTalkToNPC(False)
                self.GLOBAL.setCanOpenChest([False,[None,None]])
                if(self.slot_selected != None and (not self.intercambio) and (self.slot_selected != 'armor_slot' and self.slot_selected != 'mano derecha' and self.slot_selected != 'mano izquierda')):
                    # self.personaje.equipo.objetos["slot_"+str(self.slot_selected)][3] -=1
                    # if(self.personaje.equipo.objetos["slot_"+str(self.slot_selected)][3] == 0):
                    #     #Ha eliminado por completo el objeto
                    #     self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] = None
                    #     self.slot_selected = None
                    res = self.personaje.equipo.removeObjectFromInventory(self.slot_selected)
                    if(res == -1):
                        self.ch1.play(self.error)

    def hasUpKey(self,key,unicode):
        if(self.GLOBAL.getViewMap()):
            # Si se puede ver el mapa, podemos movernos
            if(key == pygame.K_DOWN):
                print("down levantado")
                self.personaje.setDown(False)
            elif(key == pygame.K_UP):
                print("up levantado")
                self.personaje.setUp(False)
            elif(key == pygame.K_LEFT):
                print("left levantado")
                self.personaje.setLeft(False)
            elif(key == pygame.K_RIGHT):
                print("right levantado")
                self.personaje.setRight(False)

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
                self.imagePhoto = None
                pygame.display.update() 
                mixer.music.stop()#para la música
                mixer.music.load("sounds/background.wav") #carga de nuevo la canción normal de fondo
                mixer.music.play(-1)
                try:
                    self.cerrarHilo()
                except Exception as e:
                    print(e)
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
            x_start1 = self.width/1.4706
            y_start1 = self.height/1.7157
            x_size1 = self.width/37.5000
            y_size1 = self.height/21.8750
            x_size4 = self.width/37.5000
            y_size4 = self.height/21.8750
            x_start4 = self.width/120.0000
            y_start4 = self.height/70.0000
            (x,y) = pygame.mouse.get_pos()

            #Botón volver al menú
            if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                self.slot_selected = None
                self.intercambio = False
                self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                if(self.startBoton):
                    self.screen.blit(pygame.transform.scale(self.continuar, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                else:
                    self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                    self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                if(self.GLOBAL.getViewMap()):
                    if(not self.openedInventory):
                        self.screen.blit(pygame.transform.scale(self.butonInv, (self.width/37.5000, self.height/21.8750)),(self.width/1.4706, self.height/1.7157)) 
                    else:
                        self.screen.blit(pygame.transform.scale(self.flecha, (self.width/37.5000, self.height/21.8750)), (self.width/120.0000, self.height/70.0000)) #32 32 10 10
                self.ch1.play(self.pressed)
                pygame.display.update() 
                self.currentTextToShow = ""
                mixer.music.stop()#para la música
                mixer.music.load("sounds/background.wav") #carga de nuevo la canción normal de fondo
                mixer.music.play(-1)
                try:
                    self.cerrarHilo()
                except:
                    pass
                return 'menu'
            
            elif(self.GLOBAL.getViewMap() and self.openedInventory and self.calculateCurrentSlot(x,y) != None):
                slot = self.calculateCurrentSlot(x,y)
                if(slot != 'armor_slot' and slot != 'mano derecha' and slot != 'mano izquierda'):
                    # El nuevo objeto es de inventario, y venimos de cualquiera
                    if(self.personaje.equipo.objetos["slot_"+str(slot)] != None):
                        # Caso 1: estaba en modo intercambio y hay un objeto en el nuevo slot, que no es ni armadura, ni manos
                        if(self.intercambio and not(self.slot_selected == 'armor_slot' or self.slot_selected == 'mano derecha' or self.slot_selected == 'mano izquierda')):
                            objeto_slot_nuevo = self.personaje.equipo.objetos["slot_"+str(slot)]
                            self.personaje.equipo.objetos["slot_"+str(slot)] = self.personaje.equipo.objetos["slot_"+str(self.slot_selected)]
                            self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] = objeto_slot_nuevo
                            self.intercambio = False
                            self.slot_selected = None #ha terminado el intercambio, ya no hay objeto seleccionado
                        elif(self.intercambio and self.slot_selected == 'armor_slot'):
                            # Estaba en modo intercambio, y hay un nuevo objeto en el slot, procediendo de armor slot
                            # Si es una armadura, se deben intercambiar. Si no, que termine el modo intercambio sin hacer nada, y suene el error
                            if(type(self.personaje.equipo.objetos["slot_"+str(slot)][2]) == Armadura):
                                # Se pueden intercambiar
                                objeto_slot_nuevo = self.personaje.equipo.objetos["slot_"+str(slot)]
                                self.personaje.equipo.objetos["slot_"+str(slot)] = self.personaje.equipo.armadura_actual
                                self.personaje.equipo.armadura_actual = objeto_slot_nuevo
                                # Actualizo la CA
                                att = self.personaje.des-10
                                if(att < 0):
                                    att -=1
                                elif(att > 0):
                                    att+=1
                                puntaje = int(att // 2)
                                self.personaje.ca = self.personaje.equipo.armadura_actual[2].nueva_ca + puntaje
                                self.intercambio = False
                                self.slot_selected = None 
                            else:
                                self.ch1.play(self.error)
                                self.intercambio = False
                                self.slot_selected = None 
                        elif(self.intercambio and self.slot_selected == 'mano derecha'):
                            # Si es escudo, hay que actualizar la CA, pues da un +2
                            if(type(self.personaje.equipo.objetos["slot_"+str(slot)][2]) == Escudo):
                                self.personaje.ca +=2
                            # Se intercambia el objeto
                            if(type(self.personaje.equipo.objeto_equipado_mano_derecha)[2] == Escudo):
                                self.personaje.ca -=2
                            objeto_slot_nuevo = self.personaje.equipo.objetos["slot_"+str(slot)]
                            self.personaje.equipo.objetos["slot_"+str(slot)] = self.personaje.equipo.objeto_equipado_mano_derecha
                            self.personaje.equipo.objeto_equipado_mano_derecha = objeto_slot_nuevo
                            self.intercambio = False
                            self.slot_selected = None 

                        elif(self.intercambio and self.slot_selected == 'mano izquierda'):
                            # Si es escudo, hay que actualizar la CA, pues da un +2
                            if(type(self.personaje.equipo.objetos["slot_"+str(slot)][2]) == Escudo):
                                self.personaje.ca +=2
                            # Se intercambia el objeto
                            if(type(self.personaje.equipo.objeto_equipado_mano_izquierda)[2] == Escudo):
                                self.personaje.ca -=2
                            objeto_slot_nuevo = self.personaje.equipo.objetos["slot_"+str(slot)]
                            self.personaje.equipo.objetos["slot_"+str(slot)] = self.personaje.equipo.objeto_equipado_mano_izquierda
                            self.personaje.equipo.objeto_equipado_mano_izquierda = objeto_slot_nuevo
                            self.intercambio = False
                            self.slot_selected = None
                        else:
                            self.slot_selected = slot
                    # Caso 2: estaba en modo intercambio y no hay un objeto en el nuevo slot
                    else:
                        if(self.intercambio and not(self.slot_selected == 'armor_slot' or self.slot_selected == 'mano derecha' or self.slot_selected == 'mano izquierda')):
                            self.personaje.equipo.objetos["slot_"+str(slot)] = self.personaje.equipo.objetos["slot_"+str(self.slot_selected)]
                            self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] = None
                            self.intercambio = False
                            self.slot_selected = None #ha terminado el intercambio, ya no hay objeto seleccionado
                        elif(self.intercambio and self.slot_selected == 'armor_slot'):
                            if(self.personaje.tipo_clase == 'Explorador'):
                                base_ca = 15
                            else:
                                base_ca = 10
                            dif_ca = base_ca - self.personaje.equipo.armadura_actual[2].nueva_ca
                            self.personaje.equipo.objetos["slot_"+str(slot)] = self.personaje.equipo.armadura_actual
                            self.personaje.equipo.armadura_actual = None
                            self.personaje.equipo.num_objetos_actual +=1
                            self.intercambio = False
                            self.slot_selected = None #ha terminado el intercambio, ya no hay objeto seleccionado
                            self.personaje.ca -= dif_ca
                        elif(self.intercambio and self.slot_selected == 'mano derecha'):
                            if(type(self.personaje.equipo.objeto_equipado_mano_derecha[2]) == Escudo):
                                self.personaje.ca -=2
                            self.personaje.equipo.objetos["slot_"+str(slot)] = self.personaje.equipo.objeto_equipado_mano_derecha
                            self.personaje.equipo.objeto_equipado_mano_derecha = None
                            self.personaje.equipo.num_objetos_actual +=1
                            self.intercambio = False
                            self.slot_selected = None #ha terminado el intercambio, ya no hay objeto seleccionado
                        elif(self.intercambio and self.slot_selected == 'mano izquierda'):
                            if(type(self.personaje.equipo.objeto_equipado_mano_izquierda[2]) == Escudo):
                                self.personaje.ca -=2
                            self.personaje.equipo.objetos["slot_"+str(slot)] = self.personaje.equipo.objeto_equipado_mano_izquierda
                            self.personaje.equipo.objeto_equipado_mano_izquierda = None
                            self.personaje.equipo.num_objetos_actual +=1
                            self.intercambio = False
                            self.slot_selected = None #ha terminado el intercambio, ya no hay objeto seleccionado  
                else:
                    # El nuevo objeto es de armadura o mano, y venimos de cualquiera
                    if(self.intercambio and self.slot_selected == 'armor_slot'):
                        # Si hay intercambio, y el slot actual es el de la armadura, y venía de un slot de armadura
                        if(slot == 'armor_slot'):
                            self.ch1.play(self.error)
                            self.intercambio = False
                            self.slot_selected = None #ha terminado el intercambio, ya no hay objeto seleccionado  
                        elif(slot == 'mano derecha'):
                            # Solo se podrán intercambiar si ambos son armaduras
                            if(self.personaje.equipo.objeto_equipado_mano_derecha == None):
                                # Actualizo la CA
                                if(self.personaje.tipo_clase == 'Explorador'):
                                    base_ca = 15
                                else:
                                    base_ca = 10
                                dif_ca = base_ca - self.personaje.equipo.armadura_actual[2].nueva_ca

                                self.personaje.equipo.objeto_equipado_mano_derecha = self.personaje.equipo.armadura_actual
                                self.personaje.equipo.armadura_actual = None
                                self.personaje.ca -= dif_ca
                                self.intercambio = False
                                self.slot_selected = None 
                            elif(type(self.personaje.equipo.objeto_equipado_mano_derecha[2]) == Armadura):
                                objeto_slot_nuevo = self.personaje.equipo.objeto_equipado_mano_derecha
                                self.personaje.equipo.objeto_equipado_mano_derecha = self.personaje.equipo.armadura_actual
                                self.personaje.equipo.armadura_actual = objeto_slot_nuevo
                                # Actualizo la CA
                                att = self.personaje.des-10
                                if(att < 0):
                                    att -=1
                                elif(att > 0):
                                    att+=1
                                puntaje = int(att // 2)
                                self.personaje.ca = self.personaje.equipo.armadura_actual[2].nueva_ca + puntaje
                                self.intercambio = False
                                self.slot_selected = None 
                            else:
                                self.ch1.play(self.error)
                                self.intercambio = False
                                self.slot_selected = None #ha terminado el intercambio, ya no hay objeto seleccionado 
                        elif(slot == 'mano izquierda'):
                            if(self.personaje.equipo.objeto_equipado_mano_izquierda == None):
                                # Actualizo la CA
                                if(self.personaje.tipo_clase == 'Explorador'):
                                    base_ca = 15
                                else:
                                    base_ca = 10
                                dif_ca = base_ca - self.personaje.equipo.armadura_actual[2].nueva_ca

                                self.personaje.equipo.objeto_equipado_mano_izquierda = self.personaje.equipo.armadura_actual
                                self.personaje.equipo.armadura_actual = None
                                self.personaje.ca -= dif_ca
                                self.intercambio = False
                                self.slot_selected = None 
                            elif(type(self.personaje.equipo.objeto_equipado_mano_izquierda[2]) == Armadura):
                                objeto_slot_nuevo = self.personaje.equipo.objeto_equipado_mano_izquierda
                                self.personaje.equipo.objeto_equipado_mano_izquierda = self.personaje.equipo.armadura_actual
                                self.personaje.equipo.armadura_actual = objeto_slot_nuevo
                                # Actualizo la CA
                                att = self.personaje.des-10
                                if(att < 0):
                                    att -=1
                                elif(att > 0):
                                    att+=1
                                puntaje = int(att // 2)
                                self.personaje.ca = self.personaje.equipo.armadura_actual[2].nueva_ca + puntaje
                                self.intercambio = False
                                self.slot_selected = None 
                            else:
                                self.ch1.play(self.error)
                                self.intercambio = False
                                self.slot_selected = None #ha terminado el intercambio, ya no hay objeto seleccionado 
                    

                    elif(self.intercambio and self.slot_selected == 'mano derecha'):
                        if(slot == 'armor_slot'):
                            if(type(self.personaje.equipo.objeto_equipado_mano_derecha[2]) == Armadura):
                                if(self.personaje.equipo.armadura_actual != None):
                                    objeto_slot_antiguo = self.personaje.equipo.objeto_equipado_mano_derecha
                                    self.personaje.equipo.objeto_equipado_mano_derecha = self.personaje.equipo.armadura_actual
                                    self.personaje.equipo.armadura_actual = objeto_slot_antiguo
                                else:
                                    self.personaje.equipo.armadura_actual = self.personaje.equipo.objeto_equipado_mano_derecha
                                    self.personaje.equipo.objeto_equipado_mano_derecha = None
                                # Actualizo la CA
                                att = self.personaje.des-10
                                if(att < 0):
                                    att -=1
                                elif(att > 0):
                                    att+=1
                                puntaje = int(att // 2)
                                self.personaje.ca = self.personaje.equipo.armadura_actual[2].nueva_ca + puntaje
                                self.intercambio = False
                                self.slot_selected = None 
                            else:
                                self.ch1.play(self.error)
                                self.intercambio = False
                                self.slot_selected = None #ha terminado el intercambio, ya no hay objeto seleccionado 
                        elif(slot == 'mano derecha'):
                            self.ch1.play(self.error)
                            self.intercambio = False
                            self.slot_selected = None #ha terminado el intercambio, ya no hay objeto seleccionado 
                        elif(slot == 'mano izquierda'):
                            if(self.personaje.equipo.objeto_equipado_mano_izquierda != None):
                                objeto_slot_nuevo = self.personaje.equipo.objeto_equipado_mano_izquierda
                                self.personaje.equipo.objeto_equipado_mano_izquierda = self.personaje.equipo.objeto_equipado_mano_derecha
                                self.personaje.equipo.objeto_equipado_mano_derecha = objeto_slot_antiguo
                            else:
                                self.personaje.equipo.objeto_equipado_mano_izquierda = self.personaje.equipo.objeto_equipado_mano_derecha
                                self.personaje.equipo.objeto_equipado_mano_derecha = None
                            self.intercambio = False
                            self.slot_selected = None #ha terminado el intercambio, ya no hay objeto seleccionado 
                        
                    elif(self.intercambio and self.slot_selected == 'mano izquierda'):
                        if(slot == 'armor_slot'):
                            if(type(self.personaje.equipo.objeto_equipado_mano_izquierda[2]) == Armadura):
                                if(self.personaje.equipo.armadura_actual != None):
                                    objeto_slot_antiguo = self.personaje.equipo.objeto_equipado_mano_izquierda
                                    self.personaje.equipo.objeto_equipado_mano_izquierda = self.personaje.equipo.armadura_actual
                                    self.personaje.equipo.armadura_actual = objeto_slot_antiguo
                                else:
                                    self.personaje.equipo.armadura_actual = self.personaje.equipo.objeto_equipado_mano_izquierda
                                    self.personaje.equipo.objeto_equipado_mano_izquierda = None
                                # Actualizo la CA
                                att = self.personaje.des-10
                                if(att < 0):
                                    att -=1
                                elif(att > 0):
                                    att+=1
                                puntaje = int(att // 2)
                                self.personaje.ca = self.personaje.equipo.armadura_actual[2].nueva_ca + puntaje
                                self.intercambio = False
                                self.slot_selected = None 
                            else:
                                self.ch1.play(self.error)
                                self.intercambio = False
                                self.slot_selected = None #ha terminado el intercambio, ya no hay objeto seleccionado 
                        elif(slot == 'mano derecha'):
                            if(self.personaje.equipo.objeto_equipado_mano_derecha != None):
                                objeto_slot_nuevo = self.personaje.equipo.objeto_equipado_mano_derecha
                                self.personaje.equipo.objeto_equipado_mano_derecha = self.personaje.equipo.objeto_equipado_mano_izquierda
                                self.personaje.equipo.objeto_equipado_mano_izquierda = objeto_slot_antiguo
                            else:
                                self.personaje.equipo.objeto_equipado_mano_derecha = self.personaje.equipo.objeto_equipado_mano_izquierda
                                self.personaje.equipo.objeto_equipado_mano_izquierda = None
                            self.intercambio = False
                            self.slot_selected = None #ha terminado el intercambio, ya no hay objeto seleccionado 
                        elif(slot == 'mano izquierda'):
                            self.ch1.play(self.error)
                            self.intercambio = False
                            self.slot_selected = None #ha terminado el intercambio, ya no hay objeto seleccionado 
                        
                    elif(self.intercambio and self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] != None):
                        if(slot == 'armor_slot'):
                            if(type(self.personaje.equipo.objetos["slot_"+str(self.slot_selected)][2]) == Armadura):
                                # Se pueden intercambiar
                                if(self.personaje.equipo.armadura_actual != None):
                                    objeto_slot_nuevo = self.personaje.equipo.objetos["slot_"+str(self.slot_selected)]
                                    self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] = self.personaje.equipo.armadura_actual
                                    self.personaje.equipo.armadura_actual = objeto_slot_nuevo
                    
                                else:
                                    self.personaje.equipo.armadura_actual = self.personaje.equipo.objetos["slot_"+str(self.slot_selected)]
                                    self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] = None
                                    self.personaje.equipo.num_objetos_actual -=1
                                 # Actualizo la CA
                                att = self.personaje.des-10
                                if(att < 0):
                                    att -=1
                                elif(att > 0):
                                    att+=1
                                puntaje = int(att // 2)
                                self.personaje.ca = self.personaje.equipo.armadura_actual[2].nueva_ca + puntaje
                                self.intercambio = False
                                self.slot_selected = None   
                                
                            else:
                                self.ch1.play(self.error)
                                self.intercambio = False
                                self.slot_selected = None 
                        elif(slot == 'mano derecha'):
                            if(type(self.personaje.equipo.objetos["slot_"+str(self.slot_selected)][2]) == Escudo):
                                if(self.personaje.equipo.objeto_equipado_mano_derecha != None):
                                    objeto_slot_nuevo = self.personaje.equipo.objeto_equipado_mano_derecha
                                    self.personaje.equipo.objeto_equipado_mano_derecha = self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] 
                                    self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] = objeto_slot_nuevo
                                    if(not type(self.personaje.equipo.objeto_equipado_mano_derecha[2]) == Escudo):
                                        self.personaje.ca +=2
                                    self.intercambio = False
                                    self.slot_selected = None 
                                    
                                else:
                                    self.personaje.equipo.objeto_equipado_mano_derecha = self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] 
                                    self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] = None
                                    self.personaje.equipo.num_objetos_actual -=1
                                    self.personaje.ca +=2
                                    self.intercambio = False
                                    self.slot_selected = None 
                            else:
                                if(self.personaje.equipo.objeto_equipado_mano_derecha != None):
                                    objeto_slot_nuevo = self.personaje.equipo.objeto_equipado_mano_derecha
                                    self.personaje.equipo.objeto_equipado_mano_derecha = self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] 
                                    self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] = objeto_slot_nuevo
                                    self.intercambio = False
                                    self.slot_selected = None 
                                else:
                                    self.personaje.equipo.objeto_equipado_mano_derecha = self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] 
                                    if(type(self.personaje.equipo.objeto_equipado_mano_derecha[2]) == Llave):
                                        print("Llave que abre posición: "+str(self.personaje.equipo.objeto_equipado_mano_derecha[2].puerta))
                                    self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] = None
                                    self.personaje.equipo.num_objetos_actual -=1
                                    self.intercambio = False
                                    self.slot_selected = None 


                        elif(slot == 'mano izquierda'):
                            if(type(self.personaje.equipo.objetos["slot_"+str(self.slot_selected)][2]) == Escudo):
                                if(self.personaje.equipo.objeto_equipado_mano_izquierda != None):
                                    objeto_slot_nuevo = self.personaje.equipo.objeto_equipado_mano_izquierda
                                    self.personaje.equipo.objeto_equipado_mano_izquierda = self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] 
                                    self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] = objeto_slot_nuevo
                                    if(not type(self.personaje.equipo.objeto_equipado_mano_izquierda[2]) == Escudo):
                                        self.personaje.ca +=2
                                    self.intercambio = False
                                    self.slot_selected = None 
                                    
                                else:
                                    self.personaje.equipo.objeto_equipado_mano_izquierda = self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] 
                                    self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] = None
                                    self.personaje.equipo.num_objetos_actual -=1
                                    self.personaje.ca +=2
                                    self.intercambio = False
                                    self.slot_selected = None 
                            else:
                                if(self.personaje.equipo.objeto_equipado_mano_izquierda != None):
                                    objeto_slot_nuevo = self.personaje.equipo.objeto_equipado_mano_izquierda
                                    self.personaje.equipo.objeto_equipado_mano_izquierda = self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] 
                                    self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] = objeto_slot_nuevo
                                    self.intercambio = False
                                    self.slot_selected = None 
                                else:
                                    self.personaje.equipo.objeto_equipado_mano_izquierda = self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] 
                                    self.personaje.equipo.objetos["slot_"+str(self.slot_selected)] = None
                                    self.personaje.equipo.num_objetos_actual -=1
                                    self.intercambio = False
                                    self.slot_selected = None 
                        
                    elif((not self.intercambio) and ((slot == 'armor_slot' and self.personaje.equipo.armadura_actual != None) or (slot == 'mano derecha' and self.personaje.equipo.objeto_equipado_mano_derecha != None) or (slot == 'mano izquierda' and self.personaje.equipo.objeto_equipado_mano_izquierda != None))):
                        # Si no hay intercambio en progreso, y hay algo en dicho slot, seleccionamos ese slot tal cual
                        self.slot_selected = slot
                self.ch1.play(self.pressed)
                return 'partida'

            # Botón abrir inventario
            elif(self.GLOBAL.getViewMap() and (not self.openedInventory) and self.checkIfMouseIsInButton(x_size1,y_size1,x_start1,y_start1,x,y)):
                self.slot_selected = None
                self.intercambio = False
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625

                if(self.availableStart):
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                
                if(self.startBoton):
                    self.screen.blit(pygame.transform.scale(self.continuar, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                else:
                    self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                    self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                self.screen.blit(pygame.transform.scale(self.butonInv_pressed, (self.width/37.5000, self.height/21.8750)),(self.width/1.4706, self.height/1.7157)) 
                self.ch1.play(self.pressed)
                self.openedInventory = True #ya no se puede mover el personaje
                pygame.display.update() 
                return 'partida'
            
            # Botón de volver atrás a la partida
            elif(self.GLOBAL.getViewMap() and self.openedInventory and self.checkIfMouseIsInButton(x_size4,y_size4,x_start4,y_start4,x,y)):
                self.slot_selected = None
                self.intercambio = False
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625

                if(self.availableStart):
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                
                if(self.startBoton):
                    self.screen.blit(pygame.transform.scale(self.continuar, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                else:
                    self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                    self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                self.screen.blit(pygame.transform.scale(self.flecha_pressed, (self.width/37.5000, self.height/21.8750)), (self.width/120.0000, self.height/70.0000)) #32 32 10 10
                self.ch1.play(self.pressed)
                self.openedInventory = False #ya se puede mover el personaje
                pygame.display.update() 
                return 'partida'

            #Botón de enviar mensaje
            elif(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start2,x,y)):
                self.slot_selected = None
                self.intercambio = False
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
                    
                if(self.availableStart):
                    self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                    self.ch1.play(self.pressed)
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                    self.ch1.play(self.error)
                if(self.startBoton):
                    self.screen.blit(pygame.transform.scale(self.continuar, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                else:
                    self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                    self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                if(self.GLOBAL.getViewMap()):
                    if(not self.openedInventory):
                        self.screen.blit(pygame.transform.scale(self.butonInv, (self.width/37.5000, self.height/21.8750)),(self.width/1.4706, self.height/1.7157)) 
                    else:
                        self.screen.blit(pygame.transform.scale(self.flecha, (self.width/37.5000, self.height/21.8750)), (self.width/120.0000, self.height/70.0000)) #32 32 10 10

                if(self.availableStart and self.startBoton):
                    self.startBoton = False
                    self.ProcesamientoPartida.clickBotonPreparado()
                pygame.display.update() 
                return 'partida'
            
            #Botón de pedir turno de palabra
            elif(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start3,x,y)):
                self.slot_selected = None
                self.intercambio = False
                if(not self.startBoton):
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                    self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                    self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                    self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                    self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                    if(self.GLOBAL.getViewMap()):
                        if(not self.openedInventory):
                            self.screen.blit(pygame.transform.scale(self.butonInv, (self.width/37.5000, self.height/21.8750)),(self.width/1.4706, self.height/1.7157)) 
                        else:
                            self.screen.blit(pygame.transform.scale(self.flecha, (self.width/37.5000, self.height/21.8750)), (self.width/120.0000, self.height/70.0000)) #32 32 10 10
                    self.ch1.play(self.pressed)
                    pygame.display.update() 
                return 'partida'
                
            else:
                self.slot_selected = None
                self.intercambio = False
                return 'partida'
        

    def movedMouse(self):
        if(self.GLOBAL.getActualPartidaState() == "loading"):
            x_size = self.width/3.8339
            y_size = self.height/12.2807
            x_start = self.width/2.7907
            y_start = self.height/1.1667
            x_start1 = self.width/1.4706
            y_start1 = self.height/1.7157
            x_size1 = self.width/37.5000
            y_size1 = self.height/21.8750
            (x,y) = pygame.mouse.get_pos()

            #Botón volver al menú
            if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
                if(self.first_timeB):
                    self.first_timeB = False
                    self.first_timeM = True
                    self.first_timeP = True
                    self.first_timeI = True
                    self.first_timeF = True
                    self.ch2.play(self.selected)     
                pygame.display.update() 

            else:
                self.first_timeB = True
                self.first_timeM = True
                self.first_timeP = True
                self.first_timeI = True
                self.first_timeF = True
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
            x_start1 = self.width/1.4706
            y_start1 = self.height/1.7157
            x_size1 = self.width/37.5000
            y_size1 = self.height/21.8750
            x_size4 = self.width/37.5000
            y_size4 = self.height/21.8750
            x_start4 = self.width/120.0000
            y_start4 = self.height/70.0000
            (x,y) = pygame.mouse.get_pos()

            #Botón volver al menú
            if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625

                if(self.availableStart):
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                
                if(self.startBoton):
                    self.screen.blit(pygame.transform.scale(self.continuar, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                else:
                    self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                    self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                if(self.GLOBAL.getViewMap()):
                    if(not self.openedInventory):
                        self.screen.blit(pygame.transform.scale(self.butonInv, (self.width/37.5000, self.height/21.8750)),(self.width/1.4706, self.height/1.7157)) 
                    else:
                        self.screen.blit(pygame.transform.scale(self.flecha, (self.width/37.5000, self.height/21.8750)), (self.width/120.0000, self.height/70.0000)) #32 32 10 10
                if(self.first_timeB):
                    self.first_timeB = False
                    self.first_timeM = True
                    self.first_timeP = True
                    self.first_timeI = True
                    self.first_timeF = True
                    self.ch2.play(self.selected)     
                pygame.display.update() 
            
            # Botón abrir inventario
            elif(self.GLOBAL.getViewMap() and (not self.openedInventory) and self.checkIfMouseIsInButton(x_size1,y_size1,x_start1,y_start1,x,y)):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625

                if(self.availableStart):
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                
                if(self.startBoton):
                    self.screen.blit(pygame.transform.scale(self.continuar, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                else:
                    self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                    self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                self.screen.blit(pygame.transform.scale(self.butonInv_selected, (self.width/37.5000, self.height/21.8750)),(self.width/1.4706, self.height/1.7157)) 
                if(self.first_timeI):
                    self.first_timeI = False
                    self.first_timeM = True
                    self.first_timeB = True
                    self.first_timeP = True
                    self.first_timeF = True
                    self.ch2.play(self.selected)     
                pygame.display.update() 

            # Botón de volver atrás a la partida
            elif(self.GLOBAL.getViewMap() and self.openedInventory and self.checkIfMouseIsInButton(x_size4,y_size4,x_start4,y_start4,x,y)):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625

                if(self.availableStart):
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                
                if(self.startBoton):
                    self.screen.blit(pygame.transform.scale(self.continuar, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                else:
                    self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                    self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                self.screen.blit(pygame.transform.scale(self.flecha_selected, (self.width/37.5000, self.height/21.8750)), (self.width/120.0000, self.height/70.0000)) #32 32 10 10
                if(self.first_timeF):
                    self.first_timeF = False
                    self.first_timeI = True
                    self.first_timeM = True
                    self.first_timeB = True
                    self.first_timeP = True
                    self.ch2.play(self.selected) 
                pygame.display.update() 

            #Botón enviar mensaje
            elif(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start2,x,y)):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
                
                if(self.availableStart):
                    self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                if(self.startBoton):
                    self.screen.blit(pygame.transform.scale(self.continuar, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                else:
                    self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                    self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                if(self.GLOBAL.getViewMap()):
                    if(not self.openedInventory):
                        self.screen.blit(pygame.transform.scale(self.butonInv, (self.width/37.5000, self.height/21.8750)),(self.width/1.4706, self.height/1.7157)) 
                    else:
                        self.screen.blit(pygame.transform.scale(self.flecha, (self.width/37.5000, self.height/21.8750)), (self.width/120.0000, self.height/70.0000)) #32 32 10 10
                if(self.first_timeM and self.availableStart):
                    self.first_timeM = False
                    self.first_timeB = True
                    self.first_timeP = True
                    self.first_timeI = True
                    self.first_timeF = True
                    self.ch2.play(self.selected)     
                pygame.display.update() 
            
            #Botón pedir turno
            elif(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start3,x,y)):
                if(not self.startBoton):
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                    self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                    self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                    self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                    self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                    if(self.GLOBAL.getViewMap()):
                        if(not self.openedInventory):
                            self.screen.blit(pygame.transform.scale(self.butonInv, (self.width/37.5000, self.height/21.8750)),(self.width/1.4706, self.height/1.7157)) 
                        else:
                            self.screen.blit(pygame.transform.scale(self.flecha, (self.width/37.5000, self.height/21.8750)), (self.width/120.0000, self.height/70.0000)) #32 32 10 10
                    if(self.first_timeP):
                        self.first_timeP = False
                        self.first_timeB = True
                        self.first_timeM = True
                        self.first_timeI = True
                        self.first_timeF = True
                        self.ch2.play(self.selected)     
                    pygame.display.update() 

            else:
                self.first_timeB = True
                self.first_timeM = True
                self.first_timeP = True
                self.first_timeI = True
                self.first_timeF = True
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.1290)) #313 57 865 620
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.1200)) #x x 925 625
                
                if(self.availableStart):
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.2658)) #313 57 865 553
                
                if(self.startBoton):
                    self.screen.blit(pygame.transform.scale(self.continuar, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                else:
                    self.screen.blit(pygame.transform.scale(self.enviar_msg, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.2545)) #x x 925 558
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.3873, self.height/1.4403)) #313 57 865 486
                    self.screen.blit(pygame.transform.scale(self.pedir_turno_palabra, (self.width/6.3158, self.height/17.5000)), (self.width/1.2973, self.height/1.4257)) #x x 925 491
                if(self.GLOBAL.getViewMap()):
                    if(not self.openedInventory):
                        self.screen.blit(pygame.transform.scale(self.butonInv, (self.width/37.5000, self.height/21.8750)),(self.width/1.4706, self.height/1.7157)) 
                    else:
                        self.screen.blit(pygame.transform.scale(self.flecha, (self.width/37.5000, self.height/21.8750)), (self.width/120.0000, self.height/70.0000)) #32 32 10 10
                pygame.display.update() 
            
