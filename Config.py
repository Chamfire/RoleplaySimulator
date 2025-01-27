import pygame
from pygame.locals import *
from pygame import mixer

class Config:
    #sound

    def __init__(self,width,height,screen,ch1,ch2,ch3,ch4,fps,dmvoz,music,effects,font):
        #screen
        self.screen = screen

        #musica
        self.pressed =  pygame.mixer.Sound('sounds/button_pressed.wav')
        self.pressed_exit = pygame.mixer.Sound('sounds/button_pressed_ogg.ogg')
        self.selected = pygame.mixer.Sound('sounds/selected_button.wav')

        #widht y height
        self.width = width
        self.height = height
        self.volumeMusic = music
        self.volumeEffects = effects

        #canales
        self.ch1 = ch1
        self.ch2 = ch2
        self.ch3 = ch3
        self.ch4 = ch4

        #variables
        self.first_timeB = True # Aún no has pulsado el botón volver al menú
        self.first_time60 = True
        self.first_time90 = True
        self.first_time120 = True
        self.first_time144 = True
        self.first_timeY = True
        self.first_timeN = True
        self.clickedSlider1 = False
        self.clickedSlider2 = False

        self.fps_var = fps
        self.dmvoz = dmvoz

        #cargamos las imágenes del menú
        self.backgroundPic = pygame.image.load("images/background.png")
        self.buttonPic = pygame.image.load("images/button.png")
        self.buttonSelectedPic = pygame.image.load("images/button_selected.png")
        self.buttonPressedPic = pygame.image.load("images/button_pressed.png")
        self.capa = pygame.image.load("images/capa.png")
        self.miniButtonPic = pygame.image.load("images/mini_button.png")
        self.miniButtonChoosedPic = pygame.image.load("images/mini_button_choosed.png")
        self.miniButtonSelectedPic = pygame.image.load("images/mini_button_selected.png")
        self.sliderPic = pygame.image.load("images/slider.png")
        self.selectorPic = pygame.image.load("images/selector.png")

        #fuentes y colores
        self.fuente = pygame.font.SysFont(font, 70)
        self.color_white = (255,255,255)
        self.back = self.fuente.render('Volver al menú', True, self.color_white)
        self.musica = self.fuente.render('Música',True, self.color_white)
        self.efectos = self.fuente.render('Efectos',True, self.color_white)
        self.fps = self.fuente.render('FPS',True, self.color_white)
        self.dmvoice = self.fuente.render('Activar voz DM',True, self.color_white)
        self.fps60 = self.fuente.render('60',True, self.color_white)
        self.fps90 = self.fuente.render('90',True, self.color_white)
        self.fps120 = self.fuente.render('120',True, self.color_white)
        self.fps144 = self.fuente.render('144',True, self.color_white)
        self.yes = self.fuente.render('Sí',True, self.color_white)
        self.no = self.fuente.render('No',True, self.color_white)

    def setScreen(self,screen):
        self.screen = screen
        #self.width,self.height= (self.screen.get_width(), self.screen.get_height())
    def getScreen(self):
        return self.screen
    def getFPS(self):
        return self.fps_var
    def getDMVoice(self):
        return self.dmvoz
    def getConfigMusic(self):
        return (self.volumeMusic,self.volumeEffects)

    def render(self):
        #render screen
        sliderXsize = self.width/2.4242 #tamaño del slider
        sliderXStart = self.width/2.5000 #posición en la que empieza el slider 1 a dibujarse
        sliderXEnd = sliderXStart + sliderXsize
        x_sizeS1 = self.width/34.2857
        #x, y es la posición actual del ratón
        if(self.volumeMusic == 0):
            self.s1x = sliderXStart
        elif(self.volumeMusic == 1):
            self.s1x = sliderXEnd - x_sizeS1
        else:
            #está dentro de los rangos
            self.s1x = sliderXStart + self.volumeMusic*(sliderXEnd - x_sizeS1 - sliderXStart)

        if(self.volumeEffects == 0):
            self.s2x = sliderXStart
        elif(self.volumeEffects == 1):
            self.s2x = sliderXEnd - x_sizeS1
        else:
            #está dentro de los rangos
            self.s2x = sliderXStart + self.volumeEffects*(sliderXEnd - x_sizeS1 - sliderXStart)
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa, (self.width/1.2000, self.height/1.2963)), (self.width/12.0000, self.height/7.0000))
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
        self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
        self.screen.blit(pygame.transform.scale(self.musica, (self.width/12.0000, self.height/17.5000)), (self.width/6.0000, self.height/3.5000))
        self.screen.blit(pygame.transform.scale(self.efectos, (self.width/10.9091, self.height/17.5000)), (self.width/6.0000, self.height/2.5926))
        self.screen.blit(pygame.transform.scale(self.fps, (self.width/20.0000, self.height/17.5000)), (self.width/6.0000, self.height/2.0588))
        self.screen.blit(pygame.transform.scale(self.sliderPic, (self.width/2.4242, self.height/35.0000)), (self.width/2.5000, self.height/3.2558))
        self.screen.blit(pygame.transform.scale(self.selectorPic, (self.width/34.2857, self.height/20.0000)), (self.s1x, self.height/3.3816)) #800 width width start
        self.screen.blit(pygame.transform.scale(self.sliderPic, (self.width/2.4242, self.height/35.0000)), (self.width/2.5000, self.height/2.4561))
        self.screen.blit(pygame.transform.scale(self.selectorPic, (self.width/34.2857, self.height/20.0000)), (self.s2x, self.height/2.5090)) #800 width start
        if(self.fps_var == 60):
            self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
        elif(self.fps_var == 90):
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
        elif(self.fps_var == 120):
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
        elif(self.fps_var == 144):
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
        self.screen.blit(pygame.transform.scale(self.fps60, (self.width/30.0000, self.height/20.0000)), (self.width/2.3077, self.height/2.0408))
        self.screen.blit(pygame.transform.scale(self.fps90, (self.width/30.0000, self.height/20.0000)), (self.width/1.8605, self.height/2.0408))
        self.screen.blit(pygame.transform.scale(self.fps120, (self.width/24.0000, self.height/20.0000)), (self.width/1.5686, self.height/2.0408))
        self.screen.blit(pygame.transform.scale(self.fps144, (self.width/24.0000, self.height/20.0000)), (self.width/1.3483, self.height/2.0408))
        self.screen.blit(pygame.transform.scale(self.dmvoice, (self.width/5.5000, self.height/17.5000)), (self.width/6.0000, self.height/1.7073))

        #Sí -> Dmvoz
        if(self.dmvoz):
            self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
        else:
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
        self.screen.blit(pygame.transform.scale(self.yes, (self.width/34.2857, self.height/20.0000)), (self.width/1.8576, self.height/1.6867))
        self.screen.blit(pygame.transform.scale(self.no, (self.width/26.6667, self.height/20.0000)), (self.width/1.5625, self.height/1.6867))
        pygame.display.update() 

    # size_x, size_y: tamaño del botón en x y en y
    # x_start y y_start: posición de la esquina izquierda del botón
    # pos_x y pos_y: posición actual del ratón
    def checkIfMouseIsInButton(self,size_x,size_y,x_start,y_start,pos_x,pos_y):
        if((pos_x >= x_start and pos_x <= size_x+x_start) and (pos_y >= y_start and pos_y <= size_y + y_start)):
            return True
        else:
            return False

    def releasedMouse(self):
        #cuando levantamos el ratón, devolvemos la configuración de volumen
        if(self.clickedSlider1):
            self.clickedSlider1 = False
            return (self.volumeMusic,self.volumeEffects)
        elif(self.clickedSlider2):
            self.clickedSlider2 = False
            return (self.volumeMusic,self.volumeEffects)
        return None

    def clickedMouse(self):
        #click del ratón
        #calculo del tamaño del botón y su posición -> Empezar Simulación
        x_size = self.width/3.8339
        y_size = self.height/12.2807
        x_start = self.width/2.7907
        y_start = self.height/1.1667

        #fps 60
        x_size1 = self.width/10.0000
        y_size1 = self.height/12.2807
        x_start1 = self.width/2.5000
        y_start1 = self.height/2.1084
        #fps 90
        x_start2 = self.width/1.9835
        #fps 120
        x_start3 = self.width/1.6438
        #fps 144
        x_start4 = self.width/1.4035

        #yes
        x_startY = self.width/1.9835
        y_startY = self.height/1.7284
        #no
        x_startN = self.width/1.6438

        #slider musica
        x_sizeS1 = self.width/34.2857
        y_sizeS1 = self.height/20.0000
        y_startS1 = self.height/3.3816

        y_startS2 = self.height/2.5090

        (x,y) = pygame.mouse.get_pos()

        #Botón volver al menú
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps60, (self.width/30.0000, self.height/20.0000)), (self.width/2.3077, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps90, (self.width/30.0000, self.height/20.0000)), (self.width/1.8605, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps120, (self.width/24.0000, self.height/20.0000)), (self.width/1.5686, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps144, (self.width/24.0000, self.height/20.0000)), (self.width/1.3483, self.height/2.0408))
            if(self.dmvoz):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            else:
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.yes, (self.width/34.2857, self.height/20.0000)), (self.width/1.8576, self.height/1.6867))
            self.screen.blit(pygame.transform.scale(self.no, (self.width/26.6667, self.height/20.0000)), (self.width/1.5625, self.height/1.6867))
            self.ch1.play(self.pressed)
            pygame.display.update() 
            return 'menu'
        
        #Boton fps 60
        elif(self.checkIfMouseIsInButton(x_size1,y_size1,x_start1,y_start1,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps60, (self.width/30.0000, self.height/20.0000)), (self.width/2.3077, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps90, (self.width/30.0000, self.height/20.0000)), (self.width/1.8605, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps120, (self.width/24.0000, self.height/20.0000)), (self.width/1.5686, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps144, (self.width/24.0000, self.height/20.0000)), (self.width/1.3483, self.height/2.0408))
            if(self.dmvoz):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            else:
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.yes, (self.width/34.2857, self.height/20.0000)), (self.width/1.8576, self.height/1.6867))
            self.screen.blit(pygame.transform.scale(self.no, (self.width/26.6667, self.height/20.0000)), (self.width/1.5625, self.height/1.6867))
            self.fps_var = 60
            self.ch1.play(self.pressed)
            pygame.display.update() 
            return 'options'
        #Boton fps 90
        elif(self.checkIfMouseIsInButton(x_size1,y_size1,x_start2,y_start1,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps60, (self.width/30.0000, self.height/20.0000)), (self.width/2.3077, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps90, (self.width/30.0000, self.height/20.0000)), (self.width/1.8605, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps120, (self.width/24.0000, self.height/20.0000)), (self.width/1.5686, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps144, (self.width/24.0000, self.height/20.0000)), (self.width/1.3483, self.height/2.0408))
            if(self.dmvoz):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            else:
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.yes, (self.width/34.2857, self.height/20.0000)), (self.width/1.8576, self.height/1.6867))
            self.screen.blit(pygame.transform.scale(self.no, (self.width/26.6667, self.height/20.0000)), (self.width/1.5625, self.height/1.6867))
            self.fps_var = 90
            self.ch1.play(self.pressed)
            pygame.display.update() 
            return 'options'
        #Boton fps 120
        elif(self.checkIfMouseIsInButton(x_size1,y_size1,x_start3,y_start1,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps60, (self.width/30.0000, self.height/20.0000)), (self.width/2.3077, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps90, (self.width/30.0000, self.height/20.0000)), (self.width/1.8605, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps120, (self.width/24.0000, self.height/20.0000)), (self.width/1.5686, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps144, (self.width/24.0000, self.height/20.0000)), (self.width/1.3483, self.height/2.0408))
            if(self.dmvoz):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            else:
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.yes, (self.width/34.2857, self.height/20.0000)), (self.width/1.8576, self.height/1.6867))
            self.screen.blit(pygame.transform.scale(self.no, (self.width/26.6667, self.height/20.0000)), (self.width/1.5625, self.height/1.6867))
            self.fps_var = 120
            
            self.ch1.play(self.pressed)
            pygame.display.update() 
            return 'options'
        #Boton fps 144
        elif(self.checkIfMouseIsInButton(x_size1,y_size1,x_start4,y_start1,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps60, (self.width/30.0000, self.height/20.0000)), (self.width/2.3077, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps90, (self.width/30.0000, self.height/20.0000)), (self.width/1.8605, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps120, (self.width/24.0000, self.height/20.0000)), (self.width/1.5686, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps144, (self.width/24.0000, self.height/20.0000)), (self.width/1.3483, self.height/2.0408))
            if(self.dmvoz):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            else:
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.yes, (self.width/34.2857, self.height/20.0000)), (self.width/1.8576, self.height/1.6867))
            self.screen.blit(pygame.transform.scale(self.no, (self.width/26.6667, self.height/20.0000)), (self.width/1.5625, self.height/1.6867))
            self.fps_var = 144
            self.ch1.play(self.pressed)
            pygame.display.update() 
            return 'options'
        
        #boton yes
        elif(self.checkIfMouseIsInButton(x_size1,y_size1,x_startY,y_startY,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(self.fps_var == 60):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 90):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 120):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 144):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps60, (self.width/30.0000, self.height/20.0000)), (self.width/2.3077, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps90, (self.width/30.0000, self.height/20.0000)), (self.width/1.8605, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps120, (self.width/24.0000, self.height/20.0000)), (self.width/1.5686, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps144, (self.width/24.0000, self.height/20.0000)), (self.width/1.3483, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.dmvoice, (self.width/5.5000, self.height/17.5000)), (self.width/6.0000, self.height/1.7073))
            self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.yes, (self.width/34.2857, self.height/20.0000)), (self.width/1.8576, self.height/1.6867))
            self.screen.blit(pygame.transform.scale(self.no, (self.width/26.6667, self.height/20.0000)), (self.width/1.5625, self.height/1.6867))
            self.dmvoz = True
            self.ch1.play(self.pressed)
            pygame.display.update() 
            return 'options'

        #boton no
        elif(self.checkIfMouseIsInButton(x_size1,y_size1,x_startN,y_startY,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(self.fps_var == 60):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 90):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 120):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 144):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps60, (self.width/30.0000, self.height/20.0000)), (self.width/2.3077, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps90, (self.width/30.0000, self.height/20.0000)), (self.width/1.8605, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps120, (self.width/24.0000, self.height/20.0000)), (self.width/1.5686, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps144, (self.width/24.0000, self.height/20.0000)), (self.width/1.3483, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.dmvoice, (self.width/5.5000, self.height/17.5000)), (self.width/6.0000, self.height/1.7073))
            self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.yes, (self.width/34.2857, self.height/20.0000)), (self.width/1.8576, self.height/1.6867))
            self.screen.blit(pygame.transform.scale(self.no, (self.width/26.6667, self.height/20.0000)), (self.width/1.5625, self.height/1.6867))
            self.dmvoz = False
            self.ch1.play(self.pressed)
            pygame.display.update() 
            return 'options'
        
        #Slider música
        elif(self.checkIfMouseIsInButton(x_sizeS1,y_sizeS1,self.s1x,y_startS1,x,y)):
            #solo detectaremos que está clickeado -> cuando clickeas, solo se activa al clickear, el resto es movimiento
            self.clickedSlider1 = True
            return 'options'
        elif(self.checkIfMouseIsInButton(x_sizeS1,y_sizeS1,self.s2x,y_startS2,x,y)):
            #solo detectaremos que está clickeado
            self.clickedSlider2 = True
            return 'options'
        else:
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(self.fps_var == 60):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 90):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 120):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 144):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps60, (self.width/30.0000, self.height/20.0000)), (self.width/2.3077, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps90, (self.width/30.0000, self.height/20.0000)), (self.width/1.8605, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps120, (self.width/24.0000, self.height/20.0000)), (self.width/1.5686, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps144, (self.width/24.0000, self.height/20.0000)), (self.width/1.3483, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.dmvoice, (self.width/5.5000, self.height/17.5000)), (self.width/6.0000, self.height/1.7073))
            if(self.dmvoz):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            else:
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.yes, (self.width/34.2857, self.height/20.0000)), (self.width/1.8576, self.height/1.6867))
            self.screen.blit(pygame.transform.scale(self.no, (self.width/26.6667, self.height/20.0000)), (self.width/1.5625, self.height/1.6867))
            
            pygame.display.update() 
            return 'options'
        

    def movedMouse(self):
        x_size = self.width/3.8339
        y_size = self.height/12.2807
        x_start = self.width/2.7907
        y_start = self.height/1.1667

        #fps 60
        x_size1 = self.width/10.0000
        y_size1 = self.height/12.2807
        x_start1 = self.width/2.5000
        y_start1 = self.height/2.1084
        #fps 90
        x_start2 = self.width/1.9835
        #fps 120
        x_start3 = self.width/1.6438
        #fps 144
        x_start4 = self.width/1.4035

        #yes
        x_startY = self.width/1.9835
        y_startY = self.height/1.7284
        #no
        x_startN = self.width/1.6438

        #slider musica
        x_sizeS1 = self.width/34.2857
        y_sizeS1 = self.height/20.0000
        y_startS1 = self.height/3.3816

        y_startS2 = self.height/2.5090

        (x,y) = pygame.mouse.get_pos()


        #independientemente de donde esté el ratón, si se clickeó para los sliders:
        #Estamos moviendonos configurando el slider1
        if(self.clickedSlider1):
            sliderXsize = self.width/2.4242 #tamaño del slider
            sliderXStart = self.width/2.5000 #posición en la que empieza el slider 1 a dibujarse
            sliderXEnd = sliderXStart + sliderXsize
            #x, y es la posición actual del ratón
            if(x <= sliderXStart):
                self.s1x = sliderXStart
                self.volumeMusic = 0
            elif(x>= sliderXEnd - x_sizeS1):
                self.s1x = sliderXEnd - x_sizeS1
                self.volumeMusic = 1
            else:
                #está dentro de los rangos
                self.s1x = x
                self.volumeMusic = (self.s1x - sliderXStart) /(sliderXEnd - x_sizeS1 - sliderXStart)
            #actualizamos esta parte de la pantalla
            self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
            self.screen.blit(pygame.transform.scale(self.capa, (self.width/1.2000, self.height/1.2963)), (self.width/12.0000, self.height/7.0000))
            self.screen.blit(pygame.transform.scale(self.musica, (self.width/12.0000, self.height/17.5000)), (self.width/6.0000, self.height/3.5000))
            self.screen.blit(pygame.transform.scale(self.efectos, (self.width/10.9091, self.height/17.5000)), (self.width/6.0000, self.height/2.5926))
            self.screen.blit(pygame.transform.scale(self.fps, (self.width/20.0000, self.height/17.5000)), (self.width/6.0000, self.height/2.0588))
            self.screen.blit(pygame.transform.scale(self.sliderPic, (self.width/2.4242, self.height/35.0000)), (self.width/2.5000, self.height/3.2558))
            self.screen.blit(pygame.transform.scale(self.selectorPic, (self.width/34.2857, self.height/20.0000)), (self.s1x, self.height/3.3816)) #800 width width start
            self.screen.blit(pygame.transform.scale(self.sliderPic, (self.width/2.4242, self.height/35.0000)), (self.width/2.5000, self.height/2.4561))
            self.screen.blit(pygame.transform.scale(self.selectorPic, (self.width/34.2857, self.height/20.0000)), (self.s2x, self.height/2.5090)) #800 width start
        #en el segundo slider
        elif(self.clickedSlider2):
            sliderXsize = self.width/2.4242 #tamaño del slider
            sliderXStart = self.width/2.5000 #posición en la que empieza el slider a dibujarse
            sliderXEnd = sliderXStart + sliderXsize
            #x, y es la posición actual del ratón
            if(x <= sliderXStart):
                self.s2x = sliderXStart
                self.volumeEffects = 0
            elif(x>= sliderXEnd - x_sizeS1):
                self.s2x = sliderXEnd - x_sizeS1 #S1 mide lo mismo que S2 de ancho
                self.volumeEffects = 1
            else:
                #está dentro de los rangos
                self.s2x = x
                self.volumeEffects = (self.s2x - sliderXStart) /(sliderXEnd - x_sizeS1 - sliderXStart)

            #actualizamos esta parte de la pantalla
            self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
            self.screen.blit(pygame.transform.scale(self.capa, (self.width/1.2000, self.height/1.2963)), (self.width/12.0000, self.height/7.0000))
            self.screen.blit(pygame.transform.scale(self.musica, (self.width/12.0000, self.height/17.5000)), (self.width/6.0000, self.height/3.5000))
            self.screen.blit(pygame.transform.scale(self.efectos, (self.width/10.9091, self.height/17.5000)), (self.width/6.0000, self.height/2.5926))
            self.screen.blit(pygame.transform.scale(self.fps, (self.width/20.0000, self.height/17.5000)), (self.width/6.0000, self.height/2.0588))
            self.screen.blit(pygame.transform.scale(self.sliderPic, (self.width/2.4242, self.height/35.0000)), (self.width/2.5000, self.height/3.2558))
            self.screen.blit(pygame.transform.scale(self.selectorPic, (self.width/34.2857, self.height/20.0000)), (self.s1x, self.height/3.3816)) #800 width width start
            self.screen.blit(pygame.transform.scale(self.sliderPic, (self.width/2.4242, self.height/35.0000)), (self.width/2.5000, self.height/2.4561))
            self.screen.blit(pygame.transform.scale(self.selectorPic, (self.width/34.2857, self.height/20.0000)), (self.s2x, self.height/2.5090)) #800 width start
        else:
            #no pasa nada, pues no estamos sobre ningún slider
            pass

        #Botón volver al menú
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(self.fps_var == 60):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 90):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 120):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 144):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps60, (self.width/30.0000, self.height/20.0000)), (self.width/2.3077, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps90, (self.width/30.0000, self.height/20.0000)), (self.width/1.8605, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps120, (self.width/24.0000, self.height/20.0000)), (self.width/1.5686, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps144, (self.width/24.0000, self.height/20.0000)), (self.width/1.3483, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.dmvoice, (self.width/5.5000, self.height/17.5000)), (self.width/6.0000, self.height/1.7073))
            if(self.dmvoz):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            else:
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.yes, (self.width/34.2857, self.height/20.0000)), (self.width/1.8576, self.height/1.6867))
            self.screen.blit(pygame.transform.scale(self.no, (self.width/26.6667, self.height/20.0000)), (self.width/1.5625, self.height/1.6867))
            if(self.first_timeB):
                self.first_timeB = False
                self.first_time60 = True
                self.first_time90 = True
                self.first_time120 = True
                self.first_time144 = True
                self.first_timeY = True
                self.first_timeN = True
                self.ch2.play(self.selected)     
            pygame.display.update() 

        #Boton fps 60
        elif(self.checkIfMouseIsInButton(x_size1,y_size1,x_start1,y_start1,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(self.fps_var == 60):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 90):
                self.screen.blit(pygame.transform.scale(self.miniButtonSelectedPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 120):
                self.screen.blit(pygame.transform.scale(self.miniButtonSelectedPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 144):
                self.screen.blit(pygame.transform.scale(self.miniButtonSelectedPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps60, (self.width/30.0000, self.height/20.0000)), (self.width/2.3077, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps90, (self.width/30.0000, self.height/20.0000)), (self.width/1.8605, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps120, (self.width/24.0000, self.height/20.0000)), (self.width/1.5686, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps144, (self.width/24.0000, self.height/20.0000)), (self.width/1.3483, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.dmvoice, (self.width/5.5000, self.height/17.5000)), (self.width/6.0000, self.height/1.7073))
            if(self.dmvoz):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            else:
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.yes, (self.width/34.2857, self.height/20.0000)), (self.width/1.8576, self.height/1.6867))
            self.screen.blit(pygame.transform.scale(self.no, (self.width/26.6667, self.height/20.0000)), (self.width/1.5625, self.height/1.6867))
            if(self.first_time60):
                self.first_timeB = True
                self.first_time60 = False
                self.first_time90 = True
                self.first_time120 = True
                self.first_time144 = True
                self.first_timeY = True
                self.first_timeN = True
                if(self.fps_var != 60):
                    self.ch4.play(self.selected) 
            pygame.display.update() 

        #Boton fps 90
        elif(self.checkIfMouseIsInButton(x_size1,y_size1,x_start2,y_start1,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(self.fps_var == 60):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonSelectedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 90):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 120):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonSelectedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 144):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonSelectedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps60, (self.width/30.0000, self.height/20.0000)), (self.width/2.3077, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps90, (self.width/30.0000, self.height/20.0000)), (self.width/1.8605, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps120, (self.width/24.0000, self.height/20.0000)), (self.width/1.5686, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps144, (self.width/24.0000, self.height/20.0000)), (self.width/1.3483, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.dmvoice, (self.width/5.5000, self.height/17.5000)), (self.width/6.0000, self.height/1.7073))
            if(self.dmvoz):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            else:
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.yes, (self.width/34.2857, self.height/20.0000)), (self.width/1.8576, self.height/1.6867))
            self.screen.blit(pygame.transform.scale(self.no, (self.width/26.6667, self.height/20.0000)), (self.width/1.5625, self.height/1.6867))
            if(self.first_time90):
                self.first_timeB = True
                self.first_time60 = True
                self.first_time90 = False
                self.first_time120 = True
                self.first_time144 = True
                self.first_timeY = True
                self.first_timeN = True
                if(self.fps_var != 90):
                    self.ch2.play(self.selected) 
            
            pygame.display.update() 

        #Boton fps 120
        elif(self.checkIfMouseIsInButton(x_size1,y_size1,x_start3,y_start1,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(self.fps_var == 60):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonSelectedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 90):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonSelectedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 120):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 144):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonSelectedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps60, (self.width/30.0000, self.height/20.0000)), (self.width/2.3077, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps90, (self.width/30.0000, self.height/20.0000)), (self.width/1.8605, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps120, (self.width/24.0000, self.height/20.0000)), (self.width/1.5686, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps144, (self.width/24.0000, self.height/20.0000)), (self.width/1.3483, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.dmvoice, (self.width/5.5000, self.height/17.5000)), (self.width/6.0000, self.height/1.7073))
            if(self.dmvoz):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            else:
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.yes, (self.width/34.2857, self.height/20.0000)), (self.width/1.8576, self.height/1.6867))
            self.screen.blit(pygame.transform.scale(self.no, (self.width/26.6667, self.height/20.0000)), (self.width/1.5625, self.height/1.6867))
            if(self.first_time120):
                self.first_timeB = True
                self.first_time60 = True
                self.first_time90 = True
                self.first_time120 = False
                self.first_time144 = True
                self.first_timeY = True
                self.first_timeN = True
                if(self.fps_var != 120):
                    self.ch3.play(self.selected) 
            
            pygame.display.update() 

        #Boton fps 144
        elif(self.checkIfMouseIsInButton(x_size1,y_size1,x_start4,y_start1,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(self.fps_var == 60):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonSelectedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 90):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonSelectedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 120):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonSelectedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 144):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps60, (self.width/30.0000, self.height/20.0000)), (self.width/2.3077, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps90, (self.width/30.0000, self.height/20.0000)), (self.width/1.8605, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps120, (self.width/24.0000, self.height/20.0000)), (self.width/1.5686, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps144, (self.width/24.0000, self.height/20.0000)), (self.width/1.3483, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.dmvoice, (self.width/5.5000, self.height/17.5000)), (self.width/6.0000, self.height/1.7073))
            if(self.dmvoz):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            else:
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.yes, (self.width/34.2857, self.height/20.0000)), (self.width/1.8576, self.height/1.6867))
            self.screen.blit(pygame.transform.scale(self.no, (self.width/26.6667, self.height/20.0000)), (self.width/1.5625, self.height/1.6867))
            if(self.first_time144):
                self.first_timeB = True
                self.first_time60 = True
                self.first_time90 = True
                self.first_time120 = True
                self.first_time144 = False
                self.first_timeY = True
                self.first_timeN = True
                if(self.fps_var != 144):
                    self.ch4.play(self.selected) 
            pygame.display.update() 

        #Boton yes
        elif(self.checkIfMouseIsInButton(x_size1,y_size1,x_startY,y_startY,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(self.fps_var == 60):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 90):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 120):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 144):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps60, (self.width/30.0000, self.height/20.0000)), (self.width/2.3077, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps90, (self.width/30.0000, self.height/20.0000)), (self.width/1.8605, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps120, (self.width/24.0000, self.height/20.0000)), (self.width/1.5686, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps144, (self.width/24.0000, self.height/20.0000)), (self.width/1.3483, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.dmvoice, (self.width/5.5000, self.height/17.5000)), (self.width/6.0000, self.height/1.7073))
            if(self.dmvoz):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            else:
                self.screen.blit(pygame.transform.scale(self.miniButtonSelectedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.yes, (self.width/34.2857, self.height/20.0000)), (self.width/1.8576, self.height/1.6867))
            self.screen.blit(pygame.transform.scale(self.no, (self.width/26.6667, self.height/20.0000)), (self.width/1.5625, self.height/1.6867))
            if(self.first_timeY):
                self.first_timeB = True
                self.first_time60 = True
                self.first_time90 = True
                self.first_time120 = True
                self.first_time144 = True
                self.first_timeY = False
                self.first_timeN = True
                if(not self.dmvoz):
                    self.ch4.play(self.selected) 
            pygame.display.update() 
        
        #Boton no
        elif(self.checkIfMouseIsInButton(x_size1,y_size1,x_startN,y_startY,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(self.fps_var == 60):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 90):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 120):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 144):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps60, (self.width/30.0000, self.height/20.0000)), (self.width/2.3077, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps90, (self.width/30.0000, self.height/20.0000)), (self.width/1.8605, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps120, (self.width/24.0000, self.height/20.0000)), (self.width/1.5686, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps144, (self.width/24.0000, self.height/20.0000)), (self.width/1.3483, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.dmvoice, (self.width/5.5000, self.height/17.5000)), (self.width/6.0000, self.height/1.7073))
            if(self.dmvoz):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonSelectedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            else:
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.yes, (self.width/34.2857, self.height/20.0000)), (self.width/1.8576, self.height/1.6867))
            self.screen.blit(pygame.transform.scale(self.no, (self.width/26.6667, self.height/20.0000)), (self.width/1.5625, self.height/1.6867))
            if(self.first_timeN):
                self.first_timeB = True
                self.first_time60 = True
                self.first_time90 = True
                self.first_time120 = True
                self.first_time144 = True
                self.first_timeY = True
                self.first_timeN = False
                if(self.dmvoz):
                    self.ch4.play(self.selected) 
            pygame.display.update() 

        else:
            self.first_timeB = True
            self.first_time60 = True
            self.first_time90 = True
            self.first_time120 = True
            self.first_time144 = True
            self.first_timeY = True
            self.first_timeN = True
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(self.fps_var == 60):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 90):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 120):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            elif(self.fps_var == 144):
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/2.5000, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/2.1084))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.4035, self.height/2.1084))
            self.screen.blit(pygame.transform.scale(self.fps60, (self.width/30.0000, self.height/20.0000)), (self.width/2.3077, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps90, (self.width/30.0000, self.height/20.0000)), (self.width/1.8605, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps120, (self.width/24.0000, self.height/20.0000)), (self.width/1.5686, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.fps144, (self.width/24.0000, self.height/20.0000)), (self.width/1.3483, self.height/2.0408))
            self.screen.blit(pygame.transform.scale(self.dmvoice, (self.width/5.5000, self.height/17.5000)), (self.width/6.0000, self.height/1.7073))
            if(self.dmvoz):
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            else:
                self.screen.blit(pygame.transform.scale(self.miniButtonPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.9835, self.height/1.7284))
                self.screen.blit(pygame.transform.scale(self.miniButtonChoosedPic, (self.width/10.0000, self.height/12.2807)), (self.width/1.6438, self.height/1.7284))
            self.screen.blit(pygame.transform.scale(self.yes, (self.width/34.2857, self.height/20.0000)), (self.width/1.8576, self.height/1.6867))
            self.screen.blit(pygame.transform.scale(self.no, (self.width/26.6667, self.height/20.0000)), (self.width/1.5625, self.height/1.6867))
            pygame.display.update() 
        
    
