import pygame
from pygame.locals import *
from pygame import mixer

class SeleccionPersonaje2:
    def __init__(self,width,height,screen,ch1,ch2,ch3,ch4,font):
        #screen
        self.screen = screen

        #musica
        self.pressed =  pygame.mixer.Sound('sounds/button_pressed.wav')
        self.pressed_exit = pygame.mixer.Sound('sounds/button_pressed_ogg.ogg')
        self.selected = pygame.mixer.Sound('sounds/selected_button.wav')

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
        self.buttonSelectedPic = pygame.image.load("images/button_selected.png")
        self.buttonPressedPic = pygame.image.load("images/button_pressed.png")
        self.capa = pygame.image.load("images/capa.png")
        self.flechaDesplegable = pygame.image.load("images/flecha_menu_desplegable.png")
        self.flechaDesplegable_selected = pygame.image.load("images/flecha_menu_desplegable_selected.png")

        #fuentes y colores
        self.font = font
        self.fuente = pygame.font.SysFont(font, 70)
        self.fuente2 = pygame.font.SysFont(font,600)
        self.color_white = (255,255,255)
        self.color_black = (0,0,0)
        self.color_light_grey = pygame.Color((144,144,144))
        self.color_grey = pygame.Color((208,208,208))
        self.back = self.fuente.render('Volver al menú', True, self.color_white)
        

    def setScreen(self,screen):
        self.screen = screen
        #self.width,self.height= (self.screen.get_width(), self.screen.get_height())
    def getScreen(self):
        return self.screen

    def render(self,isOnline):
        #render screen
        self.letterwidth = (self.width/3.4286)/14 #cálculo de la base en píxeles 
        self.lettersize = int(self.letterwidth + 0.5 * self.letterwidth) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente2 = pygame.font.SysFont(self.font,self.lettersize)
        self.alineamientoText = self.fuente2.render('Alineamiento', True, self.color_white)
        self.edadText = self.fuente2.render('Edad', True, self.color_white)
        self.pesoText = self.fuente2.render('Peso (X.XX)', True, self.color_white)
        self.descripcionText = self.fuente2.render('Descripción Física', True, self.color_white)
        self.defaultTextAlineamiento = self.fuente2.render('-- Escoge alineamiento --', True, self.color_light_grey)
        self.defaultTextEdad = self.fuente2.render('nº', True, self.color_light_grey)
        self.textAlineamiento = self.defaultTextAlineamiento
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
        self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
        self.screen.blit(self.alineamientoText,(self.width/13.3333, self.height/12.7273)) #90 55
        self.desplegableAlineamiento = pygame.Rect(self.width/13.3333, self.height/6.6667, self.width//3.6364, self.height/11.6667) #90 105 330 60
        pygame.draw.rect(self.screen, self.color_grey, self.desplegableAlineamiento, 2)
        self.rect4 = pygame.Rect(self.width/2.9340, self.height/6.6667, self.width/40.0000, self.height/11.6667) #409 105 30 60  -> rectángulo sobre la flecha del menú desplegable 
        self.screen.blit(pygame.transform.scale(self.flechaDesplegable, (self.width/40.0000, self.height/11.6667)), (self.width/2.9340, self.height/6.6667)) #30 60 409 105 
        pygame.draw.rect(self.screen, self.color_grey, self.rect4, 2)
        self.screen.blit(self.textAlineamiento,(self.width/11.0092, self.height/6.3636)) #109 110
        self.screen.blit(self.edadText,(self.width/2.4000, self.height/12.7273)) #500 55
        self.inputBoxEdad = pygame.Rect(self.width/2.4000, self.height/6.6667, self.width/12.0000, self.height/11.6667) #500 105 100 60
        pygame.draw.rect(self.screen, self.color_grey, self.inputBoxEdad, 2)
        self.screen.blit(self.defaultTextEdad,(self.width/2.3301, self.height/6.3636)) #515 110
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
            return 'seleccionPersonaje2'

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