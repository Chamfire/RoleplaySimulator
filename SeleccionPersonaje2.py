import pygame
from pygame.locals import *
from pygame import mixer

class SeleccionPersonaje2:
    def __init__(self,width,height,screen,ch1,ch2,ch3,ch4,font):
        #screen
        self.screen = screen
        self.opened_screen = None
        self.isOnline = None
        self.personaje = None

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
        self.first_timeCP = True #Botón de crear personaje
        #alineamientos
        self.first_time1 = True 
        self.first_time2 = True
        self.first_time3 = True
        self.first_time4 = True
        self.first_time5 = True
        self.first_time6 = True
        self.first_time7 = True
        self.first_time8 = True
        self.first_time9 = True

        #cargamos las imágenes del menú
        self.backgroundPic = pygame.image.load("images/background.png")
        self.buttonPic = pygame.image.load("images/button.png")
        self.buttonSelectedPic = pygame.image.load("images/button_selected.png")
        self.buttonPressedPic = pygame.image.load("images/button_pressed.png")
        self.capa = pygame.image.load("images/capa.png")
        self.flechaDesplegable = pygame.image.load("images/flecha_menu_desplegable.png")
        self.flechaDesplegable_selected = pygame.image.load("images/flecha_menu_desplegable_selected.png")
        self.bCreate = pygame.image.load("images/button_createPartida.png")
        self.bCreate_selected = pygame.image.load("images/button_createPartida_selected.png")
        self.bCreate_pressed = pygame.image.load("images/button_createPartida_pressed.png")
        self.buttonUnavailablePic = pygame.image.load("images/button_unavailable.png")

        #fuentes y colores
        self.font = font
        self.fuente = pygame.font.SysFont(font, 70)
        self.fuente2 = pygame.font.SysFont(font,600)
        self.color_white = (255,255,255)
        self.color_black = (0,0,0)
        self.color_light_grey = pygame.Color((144,144,144))
        self.color_grey = pygame.Color((208,208,208))
        self.back = self.fuente.render('Volver al menú', True, self.color_white)
        self.crearPersonaje = self.fuente.render('Crear personaje', True, self.color_white)
        

    def setScreen(self,screen):
        self.screen = screen
        #self.width,self.height= (self.screen.get_width(), self.screen.get_height())
    def getScreen(self):
        return self.screen
    

    def refresh(self,op,content):
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
        self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
        self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
        self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
        #alineamiento
        self.screen.blit(self.alineamientoText,(self.width/13.3333, self.height/12.7273)) #90 55
        pygame.draw.rect(self.screen, self.color_grey, self.desplegableAlineamiento, 2)
        self.screen.blit(pygame.transform.scale(self.flechaDesplegable, (self.width/40.0000, self.height/11.6667)), (self.width/2.9340, self.height/6.6667)) #30 60 409 105 
        pygame.draw.rect(self.screen, self.color_grey, self.rect4, 2)
        if(op == 1):
            self.textAlineamiento = content
        else:
            if(self.personaje.tipo_alineamiento != None):
                self.textAlineamiento = self.fuente2.render(self.personaje.tipo_alineamiento[0], True, self.color_white)
            else:
                self.textAlineamiento = self.defaultTextAlineamiento
        self.screen.blit(self.textAlineamiento,(self.width/11.0092, self.height/6.3636)) #109 110
        #edad
        self.screen.blit(self.edadText,(self.width/2.4000, self.height/12.7273)) #500 55
        pygame.draw.rect(self.screen, self.color_grey, self.inputBoxEdad, 2)
        self.screen.blit(self.defaultTextEdad,(self.width/2.3301, self.height/6.3636)) #515 110
        #peso
        self.screen.blit(self.pesoText,(self.width/1.7143, self.height/12.7273)) #700 55
        pygame.draw.rect(self.screen, self.color_grey, self.inputBoxPeso, 2)
        self.screen.blit(self.defaultTextPeso,(self.width/1.6783, self.height/6.3636)) #715 110
        pygame.display.update() 
        #descripción fisica
        self.screen.blit(self.descripcionText,(self.width/13.3333, self.height/3.6842)) #90 190
        pygame.draw.rect(self.screen, self.color_grey, self.inputBoxDescripcion, 2)
        pygame.display.update() 


    def setPersonaje(self,personaje):
        self.personaje = personaje

    def render(self,isOnline):
        #render screen
        self.isOnline = isOnline
        self.opened_screen = None #al iniciar será siempre none
        self.letterwidth = (self.width/3.4286)/14 #cálculo de la base en píxeles 
        self.lettersize = int(self.letterwidth + 0.5 * self.letterwidth) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente2 = pygame.font.SysFont(self.font,self.lettersize)

        self.letterwidth3 = (self.width/3.4286)/18 #cálculo de la base en píxeles 
        self.lettersize3 = int(self.letterwidth3 + 0.5 * self.letterwidth3) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente4 = pygame.font.SysFont(self.font,self.lettersize3)

        self.alineamientoText = self.fuente2.render('Alineamiento', True, self.color_white)
        self.edadText = self.fuente2.render('Edad', True, self.color_white)
        self.pesoText = self.fuente2.render('Peso', True, self.color_white)
        self.descripcionText = self.fuente2.render('Descripción Física', True, self.color_white)
        self.defaultTextAlineamiento = self.fuente2.render('-- Escoge alineamiento --', True, self.color_light_grey)
        self.defaultTextEdad = self.fuente2.render('nº', True, self.color_light_grey)
        self.textAlineamiento = self.defaultTextAlineamiento
        self.defaultTextPeso = self.fuente2.render('XXX.XX', True, self.color_light_grey)
        self.textPeso = self.defaultTextPeso
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
        self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
        self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
        self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
        #alineamiento
        self.screen.blit(self.alineamientoText,(self.width/13.3333, self.height/12.7273)) #90 55
        self.desplegableAlineamiento = pygame.Rect(self.width/13.3333, self.height/6.6667, self.width//3.6364, self.height/11.6667) #90 105 330 60
        pygame.draw.rect(self.screen, self.color_grey, self.desplegableAlineamiento, 2)
        self.rect4 = pygame.Rect(self.width/2.9340, self.height/6.6667, self.width/40.0000, self.height/11.6667) #409 105 30 60  -> rectángulo sobre la flecha del menú desplegable 
        self.screen.blit(pygame.transform.scale(self.flechaDesplegable, (self.width/40.0000, self.height/11.6667)), (self.width/2.9340, self.height/6.6667)) #30 60 409 105 
        pygame.draw.rect(self.screen, self.color_grey, self.rect4, 2)
        self.screen.blit(self.textAlineamiento,(self.width/11.0092, self.height/6.3636)) #109 110
        #parte desplegable. 
        self.legal_bueno = pygame.Rect(self.width/13.3333, self.height/4.2683, self.width/3.4384, self.height/17.5000) #90 164 349 40
        self.lb_text = self.fuente4.render("Legal Bueno", True, self.color_white)
        self.neutral_bueno = pygame.Rect(self.width/13.3333, self.height/3.4483, self.width/3.4384, self.height/17.5000) #90 203 349 40
        self.nb_text = self.fuente4.render("Neutral Bueno", True, self.color_white)
        self.caotico_bueno = pygame.Rect(self.width/13.3333, self.height/2.8926, self.width/3.4384, self.height/17.5000) #90 242 349 40
        self.cb_text = self.fuente4.render("Caótico Bueno", True, self.color_white)
        self.legal_neutral = pygame.Rect(self.width/13.3333, self.height/2.4911, self.width/3.4384, self.height/17.5000) #90 281 349 40
        self.ln_text = self.fuente4.render("Legal Neutral", True, self.color_white)
        self.neutral = pygame.Rect(self.width/13.3333, self.height/2.1875, self.width/3.4384, self.height/17.5000) #90 320 349 40
        self.n_text = self.fuente4.render("Neutral", True, self.color_white)
        self.caotico_neutral = pygame.Rect(self.width/13.3333, self.height/1.9499, self.width/3.4384, self.height/17.5000) #90 359 349 40
        self.cn_text = self.fuente4.render("Caótico Neutral", True, self.color_white)
        self.legal_malvado = pygame.Rect(self.width/13.3333, self.height/1.7588, self.width/3.4384, self.height/17.5000) #90 398 349 40
        self.lm_text = self.fuente4.render("Legal Malvado", True, self.color_white)
        self.neutral_malvado = pygame.Rect(self.width/13.3333, self.height/1.6018, self.width/3.4384, self.height/17.5000) #90 437 349 40
        self.nm_text = self.fuente4.render("Neutral Malvado", True, self.color_white)
        self.caotico_malvado = pygame.Rect(self.width/13.3333, self.height/1.4706, self.width/3.4384, self.height/17.5000) #90 476 349 40
        self.cm_text = self.fuente4.render("Caótico Malvado", True, self.color_white)
        #edad
        self.screen.blit(self.edadText,(self.width/2.4000, self.height/12.7273)) #500 55
        self.inputBoxEdad = pygame.Rect(self.width/2.4000, self.height/6.6667, self.width/12.0000, self.height/11.6667) #500 105 100 60
        pygame.draw.rect(self.screen, self.color_grey, self.inputBoxEdad, 2)
        self.screen.blit(self.defaultTextEdad,(self.width/2.3301, self.height/6.3636)) #515 110
        #peso
        self.screen.blit(self.pesoText,(self.width/1.7143, self.height/12.7273)) #700 55
        self.inputBoxPeso = pygame.Rect(self.width/1.7143, self.height/6.6667, self.width/8.0000, self.height/11.6667) #700 105 150 60
        pygame.draw.rect(self.screen, self.color_grey, self.inputBoxPeso, 2)
        self.screen.blit(self.defaultTextPeso,(self.width/1.6783, self.height/6.3636)) #715 110
        pygame.display.update() 
        #descripción fisica
        self.screen.blit(self.descripcionText,(self.width/13.3333, self.height/3.6842)) #90 190
        self.inputBoxDescripcion = pygame.Rect(self.width/13.3333, self.height/2.9167, self.width/1.2000, self.height/2.3333) #90 240 1000 300
        pygame.draw.rect(self.screen, self.color_grey, self.inputBoxDescripcion, 2)
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

        #Botón volver al menú
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start2,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            self.ch1.play(self.pressed)
            pygame.display.update() 
            return 'menu'
        
        #Botón crear personaje
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            self.ch1.play(self.error)
            pygame.display.update() 
            return 'seleccionPersonaje2'
        
        #Menú desplegable de trasfondos: si le da al recuadro o a la flecha
        elif (self.desplegableAlineamiento.collidepoint((x,y)) or self.rect4.collidepoint((x,y))):
            if(self.opened_screen == None):
                self.refresh(0,None)
                pygame.display.update() 
                self.ch1.play(self.pressed)
                self.screen.blit(pygame.transform.scale(self.flechaDesplegable_selected, (self.width/40.0000, self.height/11.6667)), (self.width/2.9340, self.height/6.6667)) #30 60 409 105 
                pygame.draw.rect(self.screen, self.color_grey, self.rect4, 2)
                pygame.display.update() 

                self.opened_screen = 1 #tipo 1: trasfondos
                pygame.draw.rect(self.screen,self.color_black, self.legal_bueno, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.legal_bueno, 3)
                self.screen.blit(self.lb_text,(self.width/5.4795, self.height/4.2424)) #219 165
                pygame.draw.rect(self.screen,self.color_black, self.neutral_bueno, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.neutral_bueno, 3)
                self.screen.blit(self.nb_text,(self.width/5.7416, self.height/3.4314)) #209 204
                pygame.draw.rect(self.screen,self.color_black, self.caotico_bueno, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.caotico_bueno, 3)
                self.screen.blit(self.cb_text,(self.width/5.7416, self.height/2.8807)) #209 243
                pygame.draw.rect(self.screen,self.color_black, self.legal_neutral, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.legal_neutral, 3)
                self.screen.blit(self.ln_text,(self.width/5.7692, self.height/2.4823)) #208 282
                pygame.draw.rect(self.screen,self.color_black, self.neutral, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.neutral, 3)
                self.screen.blit(self.n_text,(self.width/5.0209, self.height/2.1807)) #239 321 
                pygame.draw.rect(self.screen,self.color_black, self.caotico_neutral, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.caotico_neutral, 3)
                self.screen.blit(self.cn_text,(self.width/6.0302, self.height/1.9444)) #199 360 
                pygame.draw.rect(self.screen,self.color_black, self.legal_malvado, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.legal_malvado, 3)
                self.screen.blit(self.lm_text,(self.width/5.7416, self.height/1.7544)) #209 399
                pygame.draw.rect(self.screen,self.color_black, self.neutral_malvado, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.neutral_malvado, 3)
                self.screen.blit(self.nm_text,(self.width/6.0302, self.height/1.5982)) #199 438 
                pygame.draw.rect(self.screen,self.color_black, self.caotico_malvado, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.caotico_malvado, 3)
                self.screen.blit(self.cm_text,(self.width/6.0302, self.height/1.4675)) #199 477 
                pygame.display.update() 
            else:
                self.ch1.play(self.error)
            return 'seleccionPersonaje2'
        
        #Elección de alineamiento
        elif(self.legal_bueno.collidepoint((x,y)) and self.opened_screen == 1):
            self.personaje.tipo_alineamiento = ("Legal Bueno",0)
            self.ch1.play(self.pressed)
            content = self.fuente2.render('Legal Bueno', True, self.color_white)
            self.refresh(1,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje2'
        
        elif(self.neutral_bueno.collidepoint((x,y)) and self.opened_screen == 1):
            self.personaje.tipo_alineamiento = ("Neutral Bueno",1)
            self.ch1.play(self.pressed)
            content = self.fuente2.render("Neutral Bueno", True, self.color_white)
            self.refresh(1,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje2'
        elif(self.caotico_bueno.collidepoint((x,y)) and self.opened_screen == 1):
            self.personaje.tipo_alineamiento = ("Caótico Bueno",2)
            self.ch1.play(self.pressed)
            content = self.fuente2.render("Caótico Bueno", True, self.color_white)
            self.refresh(1,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje2'
        elif(self.legal_neutral.collidepoint((x,y)) and self.opened_screen == 1):
            self.personaje.tipo_alineamiento = ("Legal Neutral",3)
            self.ch1.play(self.pressed)
            content = self.fuente2.render("Legal Neutral", True, self.color_white)
            self.refresh(1,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje2'
        elif(self.neutral.collidepoint((x,y)) and self.opened_screen == 1):
            self.personaje.tipo_alineamiento = ("Neutral",4)
            self.ch1.play(self.pressed)
            content = self.fuente2.render("Neutral", True, self.color_white)
            self.refresh(1,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje2'
        elif(self.caotico_neutral.collidepoint((x,y)) and self.opened_screen == 1):
            self.personaje.tipo_alineamiento = ("Caótico Neutral",5)
            self.ch1.play(self.pressed)
            content = self.fuente2.render("Caótico Neutral", True, self.color_white)
            self.refresh(1,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje2'
        elif(self.legal_malvado.collidepoint((x,y)) and self.opened_screen == 1):
            self.personaje.tipo_alineamiento = ("Legal Malvado",6)
            self.ch1.play(self.pressed)
            content = self.fuente2.render("Legal Malvado", True, self.color_white)
            self.refresh(1,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje2'
        elif(self.neutral_malvado.collidepoint((x,y)) and self.opened_screen == 1):
            self.personaje.tipo_alineamiento = ("Neutral Malvado",7)
            self.ch1.play(self.pressed)
            content = self.fuente2.render("Neutral Malvado", True, self.color_white)
            self.refresh(1,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje2'
        elif(self.caotico_malvado.collidepoint((x,y)) and self.opened_screen == 1):
            self.personaje.tipo_alineamiento = ("Caótico Malvado",8)
            self.ch1.play(self.pressed)
            content = self.fuente2.render("Caótico Malvado", True, self.color_white)
            self.refresh(1,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje2'

        else:
            self.refresh(0,None)
            pygame.display.update() 
            return 'seleccionPersonaje2'

    def movedMouse(self):
        x_size = self.width/3.8339
        y_size = self.height/12.2807
        x_start = self.width/2.7907
        y_start = self.height/1.1667
        x_start2 = self.width/11.7647
        (x,y) = pygame.mouse.get_pos()

        #Botón volver al menú
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start2,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            if(self.first_timeB):
                self.first_timeB = False
                self.first_timeCP = True
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.ch2.play(self.selected)     
            pygame.display.update() 

        #Botón crear personaje
        elif(self.checkIfMouseIsInButton(x_size,y_size,x_start2,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            if(self.first_timeCP):
                self.first_timeCP = False
                self.first_timeB = True
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.ch2.play(self.selected)     
            pygame.display.update() 

        else:
            self.first_timeB = True
            self.first_timeCP = True
            self.first_time1 = True 
            self.first_time2 = True
            self.first_time3 = True
            self.first_time4 = True
            self.first_time5 = True
            self.first_time6 = True
            self.first_time7 = True
            self.first_time8 = True
            self.first_time9 = True
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            pygame.display.update() 