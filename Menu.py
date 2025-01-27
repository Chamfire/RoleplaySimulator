import pygame
from pygame.locals import *
from pygame import mixer

class Menu:
    #sound

    def __init__(self,width,height,screen,ch1,ch2,ch3,ch4,logged,picture,name,font):
        #screen
        self.screen = screen

        #log in
        self.logged = logged
        self.picture = picture #foto del avatar que le toca
        self.max_lenght_name = 13
        self.name = name

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
        self.first_timeS = True # Aún no has pulsado el botón start
        self.first_timeO = True # lo mismo para el botón Opciones
        self.first_timeE = True # lo mismo para el botón Exit
        self.first_timeL = True # lo mismo para el botón Login
        self.first_timeC = True # lo mismo para el botón Créditos

        #cargamos las imágenes del menú
        self.backgroundPic = pygame.image.load("images/background.png")
        self.titlePic = pygame.image.load("images/title.png")
        self.buttonPic = pygame.image.load("images/button.png")
        self.buttonSelectedPic = pygame.image.load("images/button_selected.png")
        self.buttonPressedPic = pygame.image.load("images/button_pressed.png")
        self.buttonUnavailablePic = pygame.image.load("images/button_unavailable.png")
        self.loginPic = pygame.image.load("images/login.png")
        self.loginSelectedPic = pygame.image.load("images/login_selected.png")
        self.loginPressedPic = pygame.image.load("images/login_pressed.png")
        self.creditsPic = pygame.image.load("images/credits.png")
        self.creditsSelectedPic = pygame.image.load("images/credits_selected.png")
        self.creditsPressedPic = pygame.image.load("images/credits_pressed.png")

        #fuentes y colores
        self.fuente = pygame.font.SysFont(font, 70)
        self.fuente2 = pygame.font.SysFont(font,600)
        self.color_white = (255,255,255)
        self.color_dark_red = (107,0,0)
        self.titleText = self.fuente2.render('  Roleplay          Simulator  ',True,self.color_white)
        self.start = self.fuente.render('Empezar simulación', True, self.color_white)
        self.options = self.fuente.render('Configuración', True, self.color_white)
        self.exit = self.fuente.render('Salir', True, self.color_white)
        self.tooltip1 = self.fuente.render('Iniciar sesión', True, self.color_white)
        self.tooltip2 = self.fuente.render('Créditos', True, self.color_white)
        if(self.name != ' ' and self.logged and (self.picture is not None)):
            self.textName = self.fuente.render(name, True, self.color_white)
        else:
            self.textName = None


    def render(self):
        #render screen
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.titleText, (self.width/1.0000, self.height/3.8889)), (0, self.height/28.0000)) #1200 180 0 25
        if(self.logged and (self.picture is not None)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
            self.letterwidth = (self.width/8.0000)/(self.max_lenght_name+1) #the width for 1 letter
            self.widthText = self.letterwidth*self.max_lenght_name
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
            #print("text to show: "+text_to_show+".")
            #print(one_side, other_side)
            self.textName = self.fuente.render(text_to_show, True, self.color_white)
            self.screen.blit(pygame.transform.scale(self.textName, (self.widthText, self.height/17.5000)), (self.width/1.5287, self.height/1.1864))
        else:
            self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
            self.screen.blit(pygame.transform.scale(self.tooltip1, (self.width/8.0000, self.height/17.5000)), (self.width/1.5287, self.height/1.1864))
        self.screen.blit(pygame.transform.scale(self.loginPic, (self.width/10.5263, self.width/10.5263)), (self.width/1.5000, self.height-(self.height/6.034)-(self.width/10.5263)))
        self.screen.blit(pygame.transform.scale(self.tooltip2, (self.width/12.0000, self.height/17.5000)), (self.width/4.6154, self.height/1.1864))
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.4374))
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.2635))
        self.screen.blit(pygame.transform.scale(self.start, (self.width/5.1064, self.height/17.5000)), (self.width/2.5532, self.height/1.6471))
        self.screen.blit(pygame.transform.scale(self.options, (self.width/7.5949, self.height/17.5000)), (self.width/2.3762, self.height/1.4228))
        self.screen.blit(pygame.transform.scale(self.exit, (self.width/21.8182, self.height/17.5000)), (self.width/2.1622, self.height/1.2522))
        self.screen.blit(pygame.transform.scale(self.creditsPic, (self.width/10.5263, self.width/10.5263)), (self.width/4.7059, self.height-(self.height/6.034)-(self.width/10.5263)))
        #refresca la pantalla para cargar el simulador
        pygame.display.update() 
    
    def setLog(self,log):
        self.logged = log

    def setPicture(self,picture):
        self.picture = picture
    def setName(self,name):

        self.name = name

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
        y_startS = self.height/1.6667
        y_startO = self.height/1.4374
        y_startE = self.height/1.2635
        x_sizeL = self.width/10.5263
        y_sizeL = self.height/6.1404
        x_startL = self.width/1.5000
        y_startL = self.height/1.4894
        x_startC = self.width/4.7059

        (x,y) = pygame.mouse.get_pos()

        #Botón Empezar Simulación
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_startS,x,y)):
            ret = 'menu'
            if(self.logged and (self.picture is not None)):
                self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
                self.ch1.play(self.pressed)
                ret = 'seleccionPartidas'
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
                self.ch1.play(self.error)
            self.screen.blit(pygame.transform.scale(self.loginPic, (self.width/10.5263, self.width/10.5263)), (self.width/1.5000, self.height-(self.height/6.034)-(self.width/10.5263)))
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.4374))
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.2635))
            self.screen.blit(pygame.transform.scale(self.start, (self.width/5.1064, self.height/17.5000)), (self.width/2.5532, self.height/1.6471))
            self.screen.blit(pygame.transform.scale(self.options, (self.width/7.5949, self.height/17.5000)), (self.width/2.3762, self.height/1.4228))
            self.screen.blit(pygame.transform.scale(self.exit, (self.width/21.8182, self.height/17.5000)), (self.width/2.1622, self.height/1.2522))
            self.screen.blit(pygame.transform.scale(self.creditsPic, (self.width/10.5263, self.width/10.5263)), (self.width/4.7059, self.height-(self.height/6.034)-(self.width/10.5263)))
            pygame.display.update() 
            return ret

        #Botón opciones
        elif(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_startO,x,y)):
            if(self.logged and (self.picture is not None)):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
            self.screen.blit(pygame.transform.scale(self.loginPic, (self.width/10.5263, self.width/10.5263)), (self.width/1.5000, self.height-(self.height/6.034)-(self.width/10.5263)))
            self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.4374))
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.2635))
            self.screen.blit(pygame.transform.scale(self.start, (self.width/5.1064, self.height/17.5000)), (self.width/2.5532, self.height/1.6471))
            self.screen.blit(pygame.transform.scale(self.options, (self.width/7.5949, self.height/17.5000)), (self.width/2.3762, self.height/1.4228))
            self.screen.blit(pygame.transform.scale(self.exit, (self.width/21.8182, self.height/17.5000)), (self.width/2.1622, self.height/1.2522))
            self.screen.blit(pygame.transform.scale(self.creditsPic, (self.width/10.5263, self.width/10.5263)), (self.width/4.7059, self.height-(self.height/6.034)-(self.width/10.5263)))
            self.ch1.play(self.pressed)
            pygame.display.update() 
            return 'options'

        #Botón exit
        elif(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_startE,x,y)):
            self.ch1.play(self.pressed_exit)
            if(self.logged and (self.picture is not None)):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
            self.screen.blit(pygame.transform.scale(self.loginPic, (self.width/10.5263, self.width/10.5263)), (self.width/1.5000, self.height-(self.height/6.034)-(self.width/10.5263)))
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.4374))
            self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.2635))
            self.screen.blit(pygame.transform.scale(self.start, (self.width/5.1064, self.height/17.5000)), (self.width/2.5532, self.height/1.6471))
            self.screen.blit(pygame.transform.scale(self.options, (self.width/7.5949, self.height/17.5000)), (self.width/2.3762, self.height/1.4228))
            self.screen.blit(pygame.transform.scale(self.exit, (self.width/21.8182, self.height/17.5000)), (self.width/2.1622, self.height/1.2522))
            self.screen.blit(pygame.transform.scale(self.creditsPic, (self.width/10.5263, self.width/10.5263)), (self.width/4.7059, self.height-(self.height/6.034)-(self.width/10.5263)))
            pygame.display.update() 
            while True:
                if(self.ch1.get_busy()):
                    pass
                else:
                    break
            return 'quit' #le decimos que cierre el juego

        #Botón login
        elif(self.checkIfMouseIsInButton(x_sizeL,y_sizeL,x_startL,y_startL,x,y)):
            if(self.logged and (self.picture is not None)):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))

            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.4374))
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.2635))
            self.screen.blit(pygame.transform.scale(self.start, (self.width/5.1064, self.height/17.5000)), (self.width/2.5532, self.height/1.6471))
            self.screen.blit(pygame.transform.scale(self.options, (self.width/7.5949, self.height/17.5000)), (self.width/2.3762, self.height/1.4228))
            self.screen.blit(pygame.transform.scale(self.exit, (self.width/21.8182, self.height/17.5000)), (self.width/2.1622, self.height/1.2522))
            self.screen.blit(pygame.transform.scale(self.loginPressedPic, (self.width/10.5263, self.width/10.5263)), (self.width/1.5000, self.height-(self.height/6.034)-(self.width/10.5263)))
            self.screen.blit(pygame.transform.scale(self.creditsPic, (self.width/10.5263, self.width/10.5263)), (self.width/4.7059, self.height-(self.height/6.034)-(self.width/10.5263)))
            self.ch1.play(self.pressed)
            pygame.display.update() 
            return 'login'
        
        #Botón créditos
        elif(self.checkIfMouseIsInButton(x_sizeL,y_sizeL,x_startC,y_startL,x,y)):
            if(self.logged and (self.picture is not None)):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))

            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.4374))
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.2635))
            self.screen.blit(pygame.transform.scale(self.start, (self.width/5.1064, self.height/17.5000)), (self.width/2.5532, self.height/1.6471))
            self.screen.blit(pygame.transform.scale(self.options, (self.width/7.5949, self.height/17.5000)), (self.width/2.3762, self.height/1.4228))
            self.screen.blit(pygame.transform.scale(self.exit, (self.width/21.8182, self.height/17.5000)), (self.width/2.1622, self.height/1.2522))
            self.screen.blit(pygame.transform.scale(self.loginPic, (self.width/10.5263, self.width/10.5263)), (self.width/1.5000, self.height-(self.height/6.034)-(self.width/10.5263)))
            self.screen.blit(pygame.transform.scale(self.creditsPressedPic, (self.width/10.5263, self.width/10.5263)), (self.width/4.7059, self.height-(self.height/6.034)-(self.width/10.5263)))
            self.ch1.play(self.pressed)
            pygame.display.update() 
            return 'credits'
        else:
            return 'menu'
        
    def setScreen(self,screen):
        self.screen = screen
        #self.width,self.height= (self.screen.get_width(), self.screen.get_height())
    def getScreen(self):
        return self.screen
    
    
        
    def movedMouse(self):
        x_size = self.width/3.8339
        y_size = self.height/12.2807
        x_start = self.width/2.7907
        y_startS = self.height/1.6667
        y_startO = self.height/1.4374
        y_startE = self.height/1.2635
        x_sizeL = self.width/10.5263
        y_sizeL = self.height/6.1404
        x_startL = self.width/1.5000
        y_startL = self.height/1.4894
        x_startC = self.width/4.7059
        (x,y) = pygame.mouse.get_pos()
        
        #Botón Empezar Simulación
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_startS,x,y)):
            if(self.logged and (self.picture is not None)):
                self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
                if(self.first_timeS):
                    self.first_timeS = False
                    self.first_timeO = True
                    self.first_timeE = True
                    self.ch2.play(self.selected)
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
            self.screen.blit(pygame.transform.scale(self.loginPic, (self.width/10.5263, self.width/10.5263)), (self.width/1.5000, self.height-(self.height/6.034)-(self.width/10.5263)))
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.4374))
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.2635))
            self.screen.blit(pygame.transform.scale(self.start, (self.width/5.1064, self.height/17.5000)), (self.width/2.5532, self.height/1.6471))
            self.screen.blit(pygame.transform.scale(self.options, (self.width/7.5949, self.height/17.5000)), (self.width/2.3762, self.height/1.4228))
            self.screen.blit(pygame.transform.scale(self.exit, (self.width/21.8182, self.height/17.5000)), (self.width/2.1622, self.height/1.2522))
            self.screen.blit(pygame.transform.scale(self.creditsPic, (self.width/10.5263, self.width/10.5263)), (self.width/4.7059, self.height-(self.height/6.034)-(self.width/10.5263)))
            pygame.display.update() 

        #Botón opciones
        elif(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_startO,x,y)):
            if(self.logged and (self.picture is not None)):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
            self.screen.blit(pygame.transform.scale(self.loginPic, (self.width/10.5263, self.width/10.5263)), (self.width/1.5000, self.height-(self.height/6.034)-(self.width/10.5263)))
            self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.4374))
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.2635))
            self.screen.blit(pygame.transform.scale(self.start, (self.width/5.1064, self.height/17.5000)), (self.width/2.5532, self.height/1.6471))
            self.screen.blit(pygame.transform.scale(self.options, (self.width/7.5949, self.height/17.5000)), (self.width/2.3762, self.height/1.4228))
            self.screen.blit(pygame.transform.scale(self.exit, (self.width/21.8182, self.height/17.5000)), (self.width/2.1622, self.height/1.2522))
            self.screen.blit(pygame.transform.scale(self.creditsPic, (self.width/10.5263, self.width/10.5263)), (self.width/4.7059, self.height-(self.height/6.034)-(self.width/10.5263)))
            if(self.first_timeO):
                self.first_timeO = False
                self.first_timeS = True
                self.first_timeE = True
                self.ch3.play(self.selected)
            pygame.display.update() 
            
        #Botón exit
        elif(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_startE,x,y)):
            if(self.logged and (self.picture is not None)):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
            self.screen.blit(pygame.transform.scale(self.loginPic, (self.width/10.5263, self.width/10.5263)), (self.width/1.5000, self.height-(self.height/6.034)-(self.width/10.5263)))
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.4374))
            self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.2635))
            self.screen.blit(pygame.transform.scale(self.start, (self.width/5.1064, self.height/17.5000)), (self.width/2.5532, self.height/1.6471))
            self.screen.blit(pygame.transform.scale(self.options, (self.width/7.5949, self.height/17.5000)), (self.width/2.3762, self.height/1.4228))
            self.screen.blit(pygame.transform.scale(self.exit, (self.width/21.8182, self.height/17.5000)), (self.width/2.1622, self.height/1.2522))
            self.screen.blit(pygame.transform.scale(self.creditsPic, (self.width/10.5263, self.width/10.5263)), (self.width/4.7059, self.height-(self.height/6.034)-(self.width/10.5263)))
            if(self.first_timeE):
                self.first_timeE = False
                self.first_timeO = True
                self.first_timeS = True
                self.ch4.play(self.selected)
            pygame.display.update() 

        #Botón login
        elif(self.checkIfMouseIsInButton(x_sizeL,y_sizeL,x_startL,y_startL,x,y)):
            if(self.logged and (self.picture is not None)):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))

            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.4374))
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.2635))
            self.screen.blit(pygame.transform.scale(self.start, (self.width/5.1064, self.height/17.5000)), (self.width/2.5532, self.height/1.6471))
            self.screen.blit(pygame.transform.scale(self.options, (self.width/7.5949, self.height/17.5000)), (self.width/2.3762, self.height/1.4228))
            self.screen.blit(pygame.transform.scale(self.exit, (self.width/21.8182, self.height/17.5000)), (self.width/2.1622, self.height/1.2522))
            self.screen.blit(pygame.transform.scale(self.loginSelectedPic, (self.width/10.5263, self.width/10.5263)), (self.width/1.5000, self.height-(self.height/6.034)-(self.width/10.5263)))
            self.screen.blit(pygame.transform.scale(self.creditsPic, (self.width/10.5263, self.width/10.5263)), (self.width/4.7059, self.height-(self.height/6.034)-(self.width/10.5263)))
            if(self.first_timeL):
                self.first_timeL = False
                self.first_timeE = True
                self.first_timeO = True
                self.first_timeS = True
                self.ch4.play(self.selected)
            pygame.display.update() 

        #Botón créditos
        elif(self.checkIfMouseIsInButton(x_sizeL,y_sizeL,x_startC,y_startL,x,y)):
            if(self.logged and (self.picture is not None)):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
            self.screen.blit(pygame.transform.scale(self.loginPic, (self.width/10.5263, self.width/10.5263)), (self.width/1.5000, self.height-(self.height/6.034)-(self.width/10.5263)))
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.4374))
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.2635))
            self.screen.blit(pygame.transform.scale(self.start, (self.width/5.1064, self.height/17.5000)), (self.width/2.5532, self.height/1.6471))
            self.screen.blit(pygame.transform.scale(self.options, (self.width/7.5949, self.height/17.5000)), (self.width/2.3762, self.height/1.4228))
            self.screen.blit(pygame.transform.scale(self.exit, (self.width/21.8182, self.height/17.5000)), (self.width/2.1622, self.height/1.2522))
            self.screen.blit(pygame.transform.scale(self.creditsSelectedPic, (self.width/10.5263, self.width/10.5263)), (self.width/4.7059, self.height-(self.height/6.034)-(self.width/10.5263)))
            if(self.first_timeC):
                self.first_timeC = False
                self.first_timeL = True
                self.first_timeE = True
                self.first_timeO = True
                self.first_timeS = True
                self.ch4.play(self.selected)
            pygame.display.update() 


        else:
            self.first_timeC = True
            self.first_timeL = True
            self.first_timeO = True
            self.first_timeS = True
            self.first_timeE = True
            if(self.logged and (self.picture is not None)):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339,self.height/12.2807)), (self.width/2.7907, self.height/1.6667))
            self.screen.blit(pygame.transform.scale(self.loginPic, (self.width/10.5263, self.width/10.5263)), (self.width/1.5000, self.height-(self.height/6.034)-(self.width/10.5263)))
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.4374))
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.2635))
            self.screen.blit(pygame.transform.scale(self.start, (self.width/5.1064, self.height/17.5000)), (self.width/2.5532, self.height/1.6471))
            self.screen.blit(pygame.transform.scale(self.options, (self.width/7.5949, self.height/17.5000)), (self.width/2.3762, self.height/1.4228))
            self.screen.blit(pygame.transform.scale(self.exit, (self.width/21.8182, self.height/17.5000)), (self.width/2.1622, self.height/1.2522))
            self.screen.blit(pygame.transform.scale(self.creditsPic, (self.width/10.5263, self.width/10.5263)), (self.width/4.7059, self.height-(self.height/6.034)-(self.width/10.5263)))
            pygame.display.update()  

