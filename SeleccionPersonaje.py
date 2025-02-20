import pygame
from pygame.locals import *
from pygame import mixer
import socket
from Global import Global
from Personaje import Personaje

class SeleccionPersonaje:
    #sound

    def __init__(self,width,height,screen,ch1,ch2,ch3,ch4,font,myId):
        #screen
        self.screen = screen
        self.isOnline = None
        self.GLOBAL = Global()
        self.id = myId
        self.font = font
        self.opened_screen = None
        self.textName = None #se modifica al hacer render
        self.emptyText = None #se modifica en render
        self.activeI = False
        self.max_length_name = 13

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

        #cargamos las imágenes del menú
        self.backgroundPic = pygame.image.load("images/background.png")
        self.buttonPic = pygame.image.load("images/button.png")
        self.capa = pygame.image.load("images/capa.png")
        self.buttonSelectedPic = pygame.image.load("images/button_selected.png")
        self.buttonPressedPic = pygame.image.load("images/button_pressed.png")
        self.flechaDesplegable = pygame.image.load("images/flecha_menu_desplegable.png")
        self.bCreate = pygame.image.load("images/button_createPartida.png")
        self.bCreate_selected = pygame.image.load("images/button_createPartida_selected.png")
        self.bCreate_pressed = pygame.image.load("images/button_createPartida_pressed.png")
        self.buttonUnavailablePic = pygame.image.load("images/button_unavailable.png")
        self.defaultIconRaza = pygame.image.load("images/iconos/icon_default_large.png")
        self.default = pygame.image.load("images/iconos/icon_default.png")

        #fuentes y colores
        self.fuente = pygame.font.SysFont(font, 70)
        self.color_white = (255,255,255)
        self.color_grey = pygame.Color((208,208,208))
        self.color_light_grey = pygame.Color((144,144,144))
        self.color_black = (0,0,0)
        self.color_light_purple = pygame.Color((141,69,188))
        self.color_magenta = pygame.Color((121,34,53))
        self.color_purple = pygame.Color((79,32,94))
        self.color_light_pink = pygame.Color((234,135,255))
        self.color_light_red = pygame.Color((188,100,69))
        self.color_light_green = pygame.Color((104,188,69))
        self.color_light_blue = pygame.Color((70,166,188))
        self.back = self.fuente.render('Volver al menú', True, self.color_white)
        self.crearPersonaje = self.fuente.render('Seguir con la ficha', True, self.color_white)

    def setScreen(self,screen):
        self.screen = screen
        #self.width,self.height= (self.screen.get_width(), self.screen.get_height())
    def getScreen(self):
        return self.screen

    def setPassword(self,pswd):
        self.password = pswd

    def setCurrentPartida(self,p):
        self.currentPartida = p

    def refresh(self,op,content):
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
        self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
        self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
        self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
        #-- Envío de mensaje TCP de que pasen a la selección de personajes por parte de servidor 
        #self.rect1 = pygame.Rect(self.width/12.0000, self.height/14.0000,self.width/1.2000, self.height/11.6667) #100 50 1000 60
        #self.rect1 = pygame.Rect(self.width/17.1429, self.height/14.0000,self.width/4.6154, self.height/11.6667) #70 50 260 60 -> rectángulo de ficha personaje
        #self.rect2 = pygame.Rect(self.width/3.6364, self.height/14.0000, self.width/60.0000, self.height/11.6667) #330 50 20 60 -> decoración morada 1
        #self.rect3 = pygame.Rect(self.width/1.5228, self.height/14.0000, self.width/60.0000, self.height/11.6667) #788 50 20 60 -> decoración morada 2
        #self.inputBox = pygame.Rect(self.width/3.4384, self.height/14.0000, self.width/2.7273, self.height/11.6667) #349 50 440 60 -> escribir nombre
        #self.desplegableTrasfondo = pygame.Rect(self.width/1.4870, self.height/14.0000, self.width//4.1379, self.height/11.6667) #807 50 290 60
        #self.rect4 = pygame.Rect(self.width/1.0949, self.height/14.0000, self.width/40.0000, self.height/11.6667) #1096 50 30 60  -> rectángulo sobre la flecha del menú desplegable 
        pygame.draw.rect(self.screen, self.color_light_purple, self.rect1, 0)
        pygame.draw.rect(self.screen, self.color_grey, self.rect1, 2)
        pygame.draw.rect(self.screen, self.color_purple, self.rect2, 0)
        pygame.draw.rect(self.screen, self.color_grey, self.rect2, 2)
        pygame.draw.rect(self.screen, self.color_purple, self.rect3, 0)
        pygame.draw.rect(self.screen, self.color_grey, self.rect3, 2)
        pygame.draw.rect(self.screen, self.color_grey, self.desplegableTrasfondo, 2)
        self.fichaText = self.fuente2.render('Ficha de personaje', True, self.color_white)
        pygame.draw.rect(self.screen,self.color_black, self.inputBox, 0)
        pygame.draw.rect(self.screen,self.color_grey, self.inputBox, 2)
        if(op == 1):
            self.textName = content
        self.screen.blit(self.textName,(self.width/3.2520, self.height/12.7273)) #369 55
        self.defaultTextTrasfondo = self.fuente2.render('-- Escoge trasfondo --', True, self.color_light_grey)
        self.screen.blit(self.fichaText,(self.width/13.3333, self.height/12.7273)) #90 55
        self.screen.blit(self.defaultTextTrasfondo,(self.width/1.4528, self.height/12.7273)) #826 55
        self.screen.blit(pygame.transform.scale(self.flechaDesplegable, (self.width/40.0000, self.height/11.6667)), (self.width/1.0949, self.height/14.0000)) #30 60 1096 50 
        pygame.draw.rect(self.screen, self.color_grey, self.rect4, 2)
        self.screen.blit(pygame.transform.scale(self.defaultIconRaza, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
        self.defaultTextRaza = self.fuente3.render('Raza', True, self.color_white)
        self.screen.blit(self.defaultTextRaza,(self.width/5.4545, self.height/5.3846)) #220 130
        self.screen.blit(pygame.transform.scale(self.default, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
        self.defaultTextClase = self.fuente3.render('Clase', True, self.color_white)
        self.screen.blit(self.defaultTextClase,(self.width/2.6667, self.height/5.3846)) #450 130
        self.defaultRaza = self.fuente3.render('<?>', True, self.color_white)
        self.screen.blit(self.defaultRaza,(self.width/5.1502, self.height/2.0000)) #233 350
        self.screen.blit(self.defaultRaza,(self.width/2.5696, self.height/2.9167)) #467 240
        self.vinculosText = self.fuente2.render('Vínculos', True, self.color_white)
        self.defectosText = self.fuente2.render('Defectos', True, self.color_white)
        self.rasgosText = self.fuente2.render('Rasgos de personalidad', True, self.color_white)
        self.idealesText = self.fuente2.render('Ideales', True, self.color_white)
        self.screen.blit(self.vinculosText,(self.width/2.0000, self.height/4.1176)) #600 170
        self.screen.blit(self.defectosText,(self.width/2.0168, self.height/2.5090)) #595 279
        self.screen.blit(self.rasgosText,(self.width/2.8571, self.height/1.8041)) #420 388
        self.screen.blit(self.idealesText,(self.width/1.9512, self.height/1.4085)) #615 497
        #self.rect5 = pygame.Rect(self.width/1.6901, self.height/5.0000, self.width/80.0000, self.height/6.3636) #710 140 15 110 #rectángulos de colores
        #self.rect6 = pygame.Rect(self.width/1.6901, self.height/2.8112, self.width/80.0000, self.height/6.3636) #710 249 15 110
        #self.rect7 = pygame.Rect(self.width/1.6901, self.height/1.9553, self.width/80.0000, self.height/6.3636) #710 358 15 110
        #self.rect8 = pygame.Rect(self.width/1.6901, self.height/1.4989, self.width/80.0000, self.height/6.3636) #710 467 15 110
        #self.rect9 = pygame.Rect(self.width/1.6575, self.height/5.0000, self.width/3.0000, self.height/6.3636) #724 140 400 110 #recuadro de vínculos
        #self.rect10 = pygame.Rect(self.width/1.6575, self.height/2.8112, self.width/3.0000, self.height/6.3636) #724 249 400 110 #recuadro de defectos
        #self.rect11 = pygame.Rect(self.width/1.6575, self.height/1.9553, self.width/3.0000, self.height/6.3636) #724 358 400 110 #recuadro de rasgos
        #self.rect12 = pygame.Rect(self.width/1.6575, self.height/1.4989, self.width/3.0000, self.height/6.3636) #724 467 400 110 #recuadro de ideales
        pygame.draw.rect(self.screen, self.color_light_purple, self.rect5, 0)
        pygame.draw.rect(self.screen, self.color_grey, self.rect5, 2)
        pygame.draw.rect(self.screen, self.color_light_red, self.rect6, 0)
        pygame.draw.rect(self.screen, self.color_grey, self.rect6, 2)
        pygame.draw.rect(self.screen, self.color_light_green, self.rect7, 0)
        pygame.draw.rect(self.screen, self.color_grey, self.rect7, 2)
        pygame.draw.rect(self.screen, self.color_light_blue, self.rect8, 0)
        pygame.draw.rect(self.screen, self.color_grey, self.rect8, 2)
        pygame.draw.rect(self.screen, self.color_grey, self.rect9, 2)
        pygame.draw.rect(self.screen, self.color_grey, self.rect10, 2)
        pygame.draw.rect(self.screen, self.color_grey, self.rect11, 2)
        pygame.draw.rect(self.screen, self.color_grey, self.rect12, 2)
        self.vinculosText2 = self.fuente2.render('-- Selecciona un vínculo --', True, self.color_light_grey)
        self.defectosText2 = self.fuente2.render('-- Selecciona un defecto --', True, self.color_light_grey)
        self.rasgosText2 = self.fuente2.render('-- Selecciona tu personalidad --', True, self.color_light_grey)
        self.idealesText2 = self.fuente2.render('-- Selecciona un ideal --', True, self.color_light_grey)
        self.screen.blit(self.vinculosText2,(self.width/1.5707, self.height/4.1176)) #764 170
        self.screen.blit(self.defectosText2,(self.width/1.5810, self.height/2.5090)) #759 279
        self.screen.blit(self.rasgosText2,(self.width/1.6238, self.height/1.8041)) #739 388
        self.screen.blit(self.idealesText2,(self.width/1.5306, self.height/1.4085)) #784 497

    def render(self,isOnline):
        #render screen
        self.isOnline = isOnline
        self.personaje = Personaje(False,self.currentPartida,self.id) #False porque no es NPC
        self.letterwidth = (self.width/3.4286)/14 #cálculo de la base en píxeles 
        self.lettersize = int(self.letterwidth + 0.5 * self.letterwidth) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente2 = pygame.font.SysFont(self.font,self.lettersize)
        self.letterwidth2 = (self.width/3.4286)/10 #cálculo de la base en píxeles 
        self.lettersize2 = int(self.letterwidth2 + 0.5 * self.letterwidth2) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente3 = pygame.font.SysFont(self.font,self.lettersize2)
        self.emptyText = self.fuente2.render(' ', True, self.color_white)
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
        self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
        self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
        self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
        #-- Envío de mensaje TCP de que pasen a la selección de personajes por parte de servidor 
        #self.rect1 = pygame.Rect(self.width/12.0000, self.height/14.0000,self.width/1.2000, self.height/11.6667) #100 50 1000 60
        self.rect1 = pygame.Rect(self.width/17.1429, self.height/14.0000,self.width/4.6154, self.height/11.6667) #70 50 260 60 -> rectángulo de ficha personaje
        self.rect2 = pygame.Rect(self.width/3.6364, self.height/14.0000, self.width/60.0000, self.height/11.6667) #330 50 20 60 -> decoración morada 1
        self.rect3 = pygame.Rect(self.width/1.5228, self.height/14.0000, self.width/60.0000, self.height/11.6667) #788 50 20 60 -> decoración morada 2
        self.inputBox = pygame.Rect(self.width/3.4384, self.height/14.0000, self.width/2.7273, self.height/11.6667) #349 50 440 60 -> escribir nombre
        self.desplegableTrasfondo = pygame.Rect(self.width/1.4870, self.height/14.0000, self.width//4.1379, self.height/11.6667) #807 50 290 60
        self.rect4 = pygame.Rect(self.width/1.0949, self.height/14.0000, self.width/40.0000, self.height/11.6667) #1096 50 30 60  -> rectángulo sobre la flecha del menú desplegable 
        pygame.draw.rect(self.screen, self.color_light_purple, self.rect1, 0)
        pygame.draw.rect(self.screen, self.color_grey, self.rect1, 2)
        pygame.draw.rect(self.screen, self.color_purple, self.rect2, 0)
        pygame.draw.rect(self.screen, self.color_grey, self.rect2, 2)
        pygame.draw.rect(self.screen,self.color_grey, self.inputBox, 2)
        pygame.draw.rect(self.screen, self.color_purple, self.rect3, 0)
        pygame.draw.rect(self.screen, self.color_grey, self.rect3, 2)
        pygame.draw.rect(self.screen, self.color_grey, self.desplegableTrasfondo, 2)
        self.fichaText = self.fuente2.render('Ficha de personaje', True, self.color_white)
        self.defaultTextName = self.fuente2.render('Escribe el nombre de tu personaje', True, self.color_light_grey)
        self.textName = self.defaultTextName
        self.defaultTextTrasfondo = self.fuente2.render('-- Escoge trasfondo --', True, self.color_light_grey)
        self.screen.blit(self.fichaText,(self.width/13.3333, self.height/12.7273)) #90 55
        self.screen.blit(self.textName,(self.width/3.2520, self.height/12.7273)) #369 55
        self.screen.blit(self.defaultTextTrasfondo,(self.width/1.4528, self.height/12.7273)) #826 55
        self.screen.blit(pygame.transform.scale(self.flechaDesplegable, (self.width/40.0000, self.height/11.6667)), (self.width/1.0949, self.height/14.0000)) #30 60 1096 50 
        pygame.draw.rect(self.screen, self.color_grey, self.rect4, 2)
        self.screen.blit(pygame.transform.scale(self.defaultIconRaza, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
        self.defaultTextRaza = self.fuente3.render('Raza', True, self.color_white)
        self.screen.blit(self.defaultTextRaza,(self.width/5.4545, self.height/5.3846)) #220 130
        self.screen.blit(pygame.transform.scale(self.default, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
        self.defaultTextClase = self.fuente3.render('Clase', True, self.color_white)
        self.screen.blit(self.defaultTextClase,(self.width/2.6667, self.height/5.3846)) #450 130
        self.defaultRaza = self.fuente3.render('<?>', True, self.color_white)
        self.screen.blit(self.defaultRaza,(self.width/5.1502, self.height/2.0000)) #233 350
        self.screen.blit(self.defaultRaza,(self.width/2.5696, self.height/2.9167)) #467 240
        self.vinculosText = self.fuente2.render('Vínculos', True, self.color_white)
        self.defectosText = self.fuente2.render('Defectos', True, self.color_white)
        self.rasgosText = self.fuente2.render('Rasgos de personalidad', True, self.color_white)
        self.idealesText = self.fuente2.render('Ideales', True, self.color_white)
        self.screen.blit(self.vinculosText,(self.width/2.0000, self.height/4.1176)) #600 170
        self.screen.blit(self.defectosText,(self.width/2.0168, self.height/2.5090)) #595 279
        self.screen.blit(self.rasgosText,(self.width/2.8571, self.height/1.8041)) #420 388
        self.screen.blit(self.idealesText,(self.width/1.9512, self.height/1.4085)) #615 497
        self.rect5 = pygame.Rect(self.width/1.6901, self.height/5.0000, self.width/80.0000, self.height/6.3636) #710 140 15 110 #rectángulos de colores
        self.rect6 = pygame.Rect(self.width/1.6901, self.height/2.8112, self.width/80.0000, self.height/6.3636) #710 249 15 110
        self.rect7 = pygame.Rect(self.width/1.6901, self.height/1.9553, self.width/80.0000, self.height/6.3636) #710 358 15 110
        self.rect8 = pygame.Rect(self.width/1.6901, self.height/1.4989, self.width/80.0000, self.height/6.3636) #710 467 15 110
        self.rect9 = pygame.Rect(self.width/1.6575, self.height/5.0000, self.width/3.0000, self.height/6.3636) #724 140 400 110 #recuadro de vínculos
        self.rect10 = pygame.Rect(self.width/1.6575, self.height/2.8112, self.width/3.0000, self.height/6.3636) #724 249 400 110 #recuadro de defectos
        self.rect11 = pygame.Rect(self.width/1.6575, self.height/1.9553, self.width/3.0000, self.height/6.3636) #724 358 400 110 #recuadro de rasgos
        self.rect12 = pygame.Rect(self.width/1.6575, self.height/1.4989, self.width/3.0000, self.height/6.3636) #724 467 400 110 #recuadro de ideales
        pygame.draw.rect(self.screen, self.color_light_purple, self.rect5, 0)
        pygame.draw.rect(self.screen, self.color_grey, self.rect5, 2)
        pygame.draw.rect(self.screen, self.color_light_red, self.rect6, 0)
        pygame.draw.rect(self.screen, self.color_grey, self.rect6, 2)
        pygame.draw.rect(self.screen, self.color_light_green, self.rect7, 0)
        pygame.draw.rect(self.screen, self.color_grey, self.rect7, 2)
        pygame.draw.rect(self.screen, self.color_light_blue, self.rect8, 0)
        pygame.draw.rect(self.screen, self.color_grey, self.rect8, 2)
        pygame.draw.rect(self.screen, self.color_grey, self.rect9, 2)
        pygame.draw.rect(self.screen, self.color_grey, self.rect10, 2)
        pygame.draw.rect(self.screen, self.color_grey, self.rect11, 2)
        pygame.draw.rect(self.screen, self.color_grey, self.rect12, 2)
        self.vinculosText2 = self.fuente2.render('-- Selecciona un vínculo --', True, self.color_light_grey)
        self.defectosText2 = self.fuente2.render('-- Selecciona un defecto --', True, self.color_light_grey)
        self.rasgosText2 = self.fuente2.render('-- Selecciona tu personalidad --', True, self.color_light_grey)
        self.idealesText2 = self.fuente2.render('-- Selecciona un ideal --', True, self.color_light_grey)
        self.screen.blit(self.vinculosText2,(self.width/1.5707, self.height/4.1176)) #764 170
        self.screen.blit(self.defectosText2,(self.width/1.5810, self.height/2.5090)) #759 279
        self.screen.blit(self.rasgosText2,(self.width/1.6238, self.height/1.8041)) #739 388
        self.screen.blit(self.idealesText2,(self.width/1.5306, self.height/1.4085)) #784 497
        if(not isOnline):
            for i in range(0,len(self.GLOBAL.getOtherPlayers())):
                if(self.GLOBAL.getOtherPlayersIndex(i) != None and self.GLOBAL.getOtherPlayersIndex(i)[1][2]): 
                    socket_temporal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        socket_temporal.connect((self.GLOBAL.getOtherPlayersIndex(i)[1][4],self.GLOBAL.getOtherPlayersIndex(i)[1][5]))
                        msg = str(self.password)+";"+str(self.id)+";seleccion_personaje"
                        socket_temporal.sendall(msg.encode('utf-8'))
                    except:
                        pass
                    finally:
                        socket_temporal.close() #se cierra el socket al terminar
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
        x_start2 = self.width/11.7647
        (x,y) = pygame.mouse.get_pos()

        #Botón crear personaje
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            #self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            #self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            #self.ch1.play(self.pressed)
            #pygame.display.update() 
            self.activeI = True
            pygame.draw.rect(self.screen,self.color_black, self.inputBox, 0)
            pygame.draw.rect(self.screen,self.color_grey, self.inputBox, 2)
            self.screen.blit(self.textName,(self.width/3.2520, self.height/12.7273)) #369 55
            self.ch1.play(self.error)
            return 'seleccionPersonaje'
        #Botón volver al menú
        elif(self.checkIfMouseIsInButton(x_size,y_size,x_start2,y_start,x,y)):
            self.activeI = False
            self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            self.ch1.play(self.pressed)
            pygame.display.update() 
            return 'menu'
        
        #Input de nombre de partida
        elif self.inputBox.collidepoint((x,y)):
            if(self.opened_screen == None):
                if(self.personaje.name == ' '):
                    self.textName= self.emptyText
                self.refresh(1,self.textName)
                pygame.display.update() 
                self.activeI = True
                return 'seleccionPersonaje'
            else:
                self.ch2.play(self.error)
                return 'seleccionPersonaje'

        else:
            self.activeI = False
            pygame.draw.rect(self.screen,self.color_black, self.inputBox, 0)
            pygame.draw.rect(self.screen,self.color_grey, self.inputBox, 2)
            self.screen.blit(self.textName,(self.width/3.2520, self.height/12.7273)) #369 55
            return 'seleccionPersonaje'

    def manageInputBox(self, key, unicode):
        if(self.activeI):
            if key == pygame.K_RETURN:
                self.personaje.name = ' '
            elif key == pygame.K_BACKSPACE:
                self.personaje.name = self.personaje.name[:-1]
                if(len(self.personaje.name) == 0):
                    self.personaje.name = ' '
            else:
                if(len(self.personaje.name)<self.max_length_name):
                    if(self.personaje.name == ' '):
                        self.personaje.name = unicode
                    else:
                        self.personaje.name += unicode
                    #self.widthText = self.letterwidth*len(self.name)
                else:
                    self.ch2.play(self.error)
            content = self.fuente2.render(self.personaje.name, True, self.color_light_pink)
            self.refresh(1,content)
            pygame.display.update() 

    def movedMouse(self):
        x_size = self.width/3.8339
        y_size = self.height/12.2807
        x_start = self.width/2.7907
        y_start = self.height/1.1667
        x_start2 = self.width/11.7647
        (x,y) = pygame.mouse.get_pos()

        #TODO: Botón crear personaje cuando esté toda la funcionalidad

        #Botón volver al menú
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start2,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            if(self.first_timeB):
                self.first_timeB = False
                self.ch2.play(self.selected)     
            pygame.display.update() 

        else:
            self.first_timeB = True
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            #TODO: comprobar que todos los campos están bien antes de printear el botón
            self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            pygame.display.update() 