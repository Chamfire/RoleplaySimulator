import pygame
from pygame.locals import *
from pygame import mixer

class Login:
    #sound

    def __init__(self,width,height,screen,ch1,ch2,ch3,ch4,name,logged,picture,ml,font):
        #screen
        self.screen = screen
        self.picture = picture
        self.logged = logged
        self.name = name #nombre del jugador
        self.font = font

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
        self.activeI = False #La InputBox no está activa
        self.first_timeI = True #Icono no ha sido aún pulsado
        self.opened_screen = False #la pantalla de selección de iconos por defecto no está abierta
        self.first_timeBG = True #Aún no has pulsado el botón guardar y volver de la pantalla de selección de iconos

        #cargamos las imágenes del menú
        self.backgroundPic = pygame.image.load("images/background.png")
        self.buttonPic = pygame.image.load("images/button.png")
        self.buttonSelectedPic = pygame.image.load("images/button_selected.png")
        self.buttonPressedPic = pygame.image.load("images/button_pressed.png")
        self.buttonUnavailable = pygame.image.load("images/button_unavailable.png")
        self.capa = pygame.image.load("images/capa.png")
        self.screen_icons = pygame.image.load("images/screen_icons.png")
        self.avatarJugador = {}
        self.avatarJugadorSelected = {}
        for i in range(0,6):
            self.avatarJugador[i] = pygame.image.load("images/iconos/icon_"+str(i)+".png")
            self.avatarJugadorSelected[i] = pygame.image.load("images/iconos/icon_"+str(i)+"_selected.png")
        self.default = pygame.image.load("images/iconos/icon_default.png")
        self.defaultSelected = pygame.image.load("images/iconos/icon_default_selected.png")

        #fuentes y colores
        self.fuente = pygame.font.SysFont(font, 70)
        self.color_white = (255,255,255)
        self.color_grey = pygame.Color((208,208,208))
        self.color_light_pink = pygame.Color((234,135,255))
        self.back2 = self.fuente.render('Guardar y volver', True, self.color_white)
        self.back = self.fuente.render('Volver al menú', True, self.color_white)
        self.select = self.fuente.render('- Escoge un icono -',True, self.color_grey)
        self.select2 = self.fuente.render('Selecciona uno de los siguientes iconos:',True, self.color_white)
        self.selectWhite = self.fuente.render('- Escoge un icono -',True, self.color_white)
        self.introduceTextLen = 13
        self.max_lenght_name = ml
    


    def setScreen(self,screen):
        self.screen = screen
        #self.width,self.height= (self.screen.get_width(), self.screen.get_height())
    def getScreen(self):
        return self.screen
    def getName(self):
        return self.name
    def getLog(self):
        return self.logged
    def getPicture(self):
        return self.picture
    
    def render(self):
        #render screen
        self.letterwidth = (self.width/3.4286)/14 #cálculo de la base en píxeles 
        self.lettersize = self.letterwidth + 0.5 * self.letterwidth #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.opened_screen = False #por si vuelve a abrir más tarde la pantalla
        self.fuenteText = pygame.font.SysFont(self.font, int(self.lettersize))
        self.emptyText = self.fuenteText.render(' ', True, self.color_light_pink)
        self.introduceText = self.fuenteText.render('-  Introduce tu nombre  -' , True, self.color_grey)
        #de la input box
        #InputBox
        if(self.name == ' '):
            self.textName = self.introduceText
            #self.widthText = self.letterwidth*self.introduceTextLen
        else:
            #self.textName = self.fuente.render(self.name, True, self.color_grey)
            self.textName = self.fuenteText.render(self.name, True, self.color_grey)
            #self.widthText = self.letterwidth*len(self.name)
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
        self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
        self.inputBox = pygame.Rect(self.width/1.6000, self.height/7.0000, self.width/3.4286, self.height/11.6667) #750 x 100, 350 60
        pygame.draw.rect(self.screen, self.color_grey, self.inputBox, 2)
        #self.screen.blit(pygame.transform.scale(self.textName, (self.widthText, self.height/14.0000)), (self.width/1.5894, self.height/6.6667)) #340 x 50, 755, 105
        self.screen.blit(self.textName, (self.width/1.57, self.height/6.6667))
        if(self.picture is not None):
            self.screen.blit(pygame.transform.scale(self.avatarJugador[self.picture], (self.width/3.4286, self.width/3.4286)), (self.width/1.6000, self.height/3.5000))
        else:
            self.screen.blit(pygame.transform.scale(self.default, (self.width/3.4286, self.width/3.4286)), (self.width/1.6000, self.height/3.5000))
            self.screen.blit(pygame.transform.scale(self.select, (self.width/5.4545, self.width/26.0870)), (self.width/1.4724, self.height/2.0000))
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
        x_sizeI = self.width/3.4286
        y_sizeI = self.height/2.0000
        x_startI = self.width/1.6000
        y_startI = self.height/3.5000
        (x,y) = pygame.mouse.get_pos()

        #Botón volver al menú
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            self.activeI = False
            self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            pygame.draw.rect(self.screen, self.color_grey, self.inputBox, 2)
            if(self.name == ' '):
                #self.widthText = self.letterwidth*self.introduceTextLen
                self.textName = self.introduceText
            #self.screen.blit(pygame.transform.scale(self.textName, (self.widthText, self.height/14.0000)), (self.width/1.5894, self.height/6.6667))
            self.screen.blit(self.textName, (self.width/1.57, self.height/6.6667))
            self.ch1.play(self.pressed)
            pygame.display.update() 
            return 'menu'
        #Input para el nombre
        elif self.inputBox.collidepoint((x,y)):
            if(not self.opened_screen):
                self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
                self.screen.blit(pygame.transform.scale(self.capa, (self.width,self.height)), (0, 0))
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
                pygame.draw.rect(self.screen, self.color_light_pink, self.inputBox, 2)
                if(self.name == ' '):
                    self.textName = self.emptyText
                    #self.widthText = self.letterwidth
                    #self.screen.blit(pygame.transform.scale(self.textName, (self.widthText, self.height/14.0000)), (self.width/1.5894, self.height/6.6667))
                    self.screen.blit(self.textName, (self.width/1.57, self.height/6.6667))
                else:
                    #self.screen.blit(pygame.transform.scale(self.textName, (self.widthText, self.height/14.0000)), (self.width/1.5894, self.height/6.6667))
                    self.screen.blit(self.textName, (self.width/1.57, self.height/6.6667))
                if(self.picture is not None):
                    self.screen.blit(pygame.transform.scale(self.avatarJugador[self.picture], (self.width/3.4286, self.width/3.4286)), (self.width/1.6000, self.height/3.5000))
                else:
                    self.screen.blit(pygame.transform.scale(self.default, (self.width/3.4286, self.width/3.4286)), (self.width/1.6000, self.height/3.5000))
                    self.screen.blit(pygame.transform.scale(self.select, (self.width/5.4545, self.width/26.0870)), (self.width/1.4724, self.height/2.0000))
                pygame.display.update() 
                self.activeI = True
            else:
                self.ch2.play(self.error)
            return 'login'
        
        #Icon
        elif(self.checkIfMouseIsInButton(x_sizeI,y_sizeI,x_startI,y_startI,x,y)):
            if(self.opened_screen):
                self.ch3.play(self.error)
            else:
                self.screen.blit(pygame.transform.scale(self.screen_icons, (self.width/1.7143, self.height/1.2727)), (self.width/30.0000, self.height/16.2791))
                self.screen.blit(pygame.transform.scale(self.select2, (self.width/2.4000, self.height/14.0000)), (self.width/13.3333, self.height/8.7500))
                if(self.picture is None):
                    self.screen.blit(pygame.transform.scale(self.default, (self.width/3.4286, self.width/3.4286)), (self.width/1.6000, self.height/3.5000))
                    self.screen.blit(pygame.transform.scale(self.select, (self.width/5.4545, self.width/26.0870)), (self.width/1.4724, self.height/2.0000))
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailable, (self.width/3.8339, self.height/12.2807)), (self.width/3.4286, self.height/1.4000))
                    self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/3.0000, self.height/1.3861))
                    #por defecto, no se pone ninguna. Pero el botón de guardar estará en gris.
                    #imagenes
                else:
                    self.screen.blit(pygame.transform.scale(self.avatarJugador[self.picture], (self.width/3.4286, self.width/3.4286)), (self.width/1.6000, self.height/3.5000))
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/3.4286, self.height/1.4000))
                    self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/3.0000, self.height/1.3861))
                for i in range(0,6):
                    x_size = self.width/10.5263
                    y_size = self.width/10.5263
                    x_start = (self.width/6.9364) +  ((self.width/7.7922)*(i%3))
                    y_start = (self.height/5.0000) +((self.height/4.5455)*(i//3))
                    if(self.picture == i):
                        #self.screen.blit(pygame.transform.scale(self.avatarJugadorSelected[i], (114,114)), (173+154*(i%3),140+154*(i//3)))
                        self.screen.blit(pygame.transform.scale(self.avatarJugadorSelected[i], (x_size, y_size)), (x_start, y_start))
                    else:
                        #self.screen.blit(pygame.transform.scale(self.avatarJugador[i], (114,114)), (173+154*(i%3),140+154*(i//3)))
                        self.screen.blit(pygame.transform.scale(self.avatarJugador[i], (x_size, y_size)), (x_start, y_start))#imagenes
                self.opened_screen = True
                self.ch2.play(self.pressed)
            pygame.display.update()
            return 'login'
        
        elif self.opened_screen:
            x_size = self.width/3.8339
            y_size = self.height/12.2807
            x_start = self.width/3.4286
            y_start = self.height/1.4000
            #botón de guardar
            if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                if(self.picture is not None):
                    self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/3.4286, self.height/1.4000))
                    self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/3.0000, self.height/1.3861))
                    pygame.display.update()
                    self.ch1.play(self.pressed)
                    self.render()
                else:
                    self.ch3.play(self.error)
            else:
                someSelected = 0
                for i in range(0,6):
                    x_size = self.width/10.5263
                    y_size = self.width/10.5263
                    x_start = (self.width/6.9364) +  ((self.width/7.7922)*(i%3))
                    y_start = (self.height/5.0000) +((self.height/4.5455)*(i//3))
                    if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                        self.picture = i
                        #self.screen.blit(pygame.transform.scale(self.avatarJugadorSelected[i], (114,114)), (173+154*(i%3),140+154*(i//3)))
                        self.screen.blit(pygame.transform.scale(self.avatarJugadorSelected[i], (x_size, y_size)), (x_start, y_start))
                        self.screen.blit(pygame.transform.scale(self.avatarJugador[i], (self.width/3.4286, self.width/3.4286)), (self.width/1.6000, self.height/3.5000))
                        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/3.4286, self.height/1.4000))
                        self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/3.0000, self.height/1.3861))
                        self.ch4.play(self.pressed)
                        someSelected = 1
                    else:
                        #self.screen.blit(pygame.transform.scale(self.avatarJugador[i], (114,114)), (173+154*(i%3),140+154*(i//3)))
                        self.screen.blit(pygame.transform.scale(self.avatarJugador[i], (x_size, y_size)), (x_start, y_start))#imagenes
                
                if(someSelected == 0 and self.picture is not None):
                    x_size = self.width/10.5263
                    y_size = self.width/10.5263
                    x_start = (self.width/6.9364) +  ((self.width/7.7922)*(self.picture%3))
                    y_start = (self.height/5.0000) +((self.height/4.5455)*(self.picture//3))
                    self.screen.blit(pygame.transform.scale(self.avatarJugadorSelected[self.picture], (x_size, y_size)), (x_start, y_start))
                    self.screen.blit(pygame.transform.scale(self.avatarJugador[self.picture], (self.width/3.4286, self.width/3.4286)), (self.width/1.6000, self.height/3.5000))
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/3.4286, self.height/1.4000))
                    self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/3.0000, self.height/1.3861))
            pygame.display.update() 
            return 'login'   
         
        else:
            self.activeI = False
            pygame.draw.rect(self.screen, self.color_grey, self.inputBox, 2)
            if(self.name == ' '):
                self.textName = self.introduceText
                #self.widthText = self.letterwidth*self.introduceTextLen
            else:
                self.textName = self.fuenteText.render(self.name, True, self.color_grey)
                #self.widthText = self.letterwidth*len(self.name)
            #self.screen.blit(pygame.transform.scale(self.textName, (self.widthText, self.height/14.0000)), (self.width/1.5894, self.height/6.6667))
            self.screen.blit(self.textName, (self.width/1.57, self.height/6.6667))
            if(self.picture is not None):
                self.screen.blit(pygame.transform.scale(self.avatarJugador[self.picture], (self.width/3.4286, self.width/3.4286)), (self.width/1.6000, self.height/3.5000))
            else:
                self.screen.blit(pygame.transform.scale(self.default, (self.width/3.4286, self.width/3.4286)), (self.width/1.6000, self.height/3.5000))
                self.screen.blit(pygame.transform.scale(self.select, (self.width/5.4545, self.width/26.0870)), (self.width/1.4724, self.height/2.0000))
            pygame.display.update() 
            return 'login'
        
    def manageInputBox(self, key, unicode):
        # Si se ha hecho click sobre el cuadro de texto, se puede escribir. Si no, no.
        if(self.activeI):
            # Si la tecla pulsada es return, se resetea el nombre
            if key == pygame.K_RETURN:
                self.name = ' '
            
            # Si la tecla pulsada es la de borrar caracteres, se borra el último caracter escrito.
            # Si al borrarlo, la longitud de la cadena es 0, automáticamente vuelve a poner una String vacía
            elif key == pygame.K_BACKSPACE: 
                self.name = self.name[:-1]
                if(len(self.name) == 0):
                    self.name = ' '
            else:
                # Siempre que no se exceda la longitud máxima posible de caracteres, se podrá escribir
                if(len(self.name)<self.max_lenght_name):
                    # En ningún texto se permitirá el uso de ':' ni de ';', pues son los símbolos empleados para el paso de mensajes
                    if(unicode != ':' and unicode != ';'):
                        # Añadimos los caracteres correspondientes que vamos introduciendo
                        if(self.name == ' '):
                            self.name = unicode
                        else:
                            self.name += unicode
                    else:
                        # Se ejecutará un sonido de error, que actuará como feedback para el usuario
                        self.ch2.play(self.error)
                else:
                    self.ch2.play(self.error)

            # Si el nombre final no es vacío, entonces el usuario habrá iniciado sesión parcialmente, a falta de determinar su icono de perfil.
            if(self.name != ' '):
                self.logged = True
            else:
                self.logged = False
            # Se refresca la pantalla con el nuevo texto en color rosa para distinguir con respecto al texto blanco normal
            # También se marcará el borde del cuadro de texto en rosa, para indicar que se puede continuar escribiendo
            self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
            self.screen.blit(pygame.transform.scale(self.capa, (self.width,self.height)), (0, 0))
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            pygame.draw.rect(self.screen, self.color_light_pink, self.inputBox, 2)
            self.textName = self.fuenteText.render(self.name, True, self.color_light_pink)
            self.screen.blit(self.textName, (self.width/1.57, self.height/6.6667))
            if(self.picture is not None):
                self.screen.blit(pygame.transform.scale(self.avatarJugador[self.picture], (self.width/3.4286, self.width/3.4286)), (self.width/1.6000, self.height/3.5000))
            else:
                self.screen.blit(pygame.transform.scale(self.default, (self.width/3.4286, self.width/3.4286)), (self.width/1.6000, self.height/3.5000))
                self.screen.blit(pygame.transform.scale(self.select, (self.width/5.4545, self.width/26.0870)), (self.width/1.4724, self.height/2.0000))
            pygame.display.update() 
        else:
            pass

    def movedMouse(self):
        x_size = self.width/3.8339
        y_size = self.height/12.2807
        x_start = self.width/2.7907
        y_start = self.height/1.1667
        x_sizeI = self.width/3.4286
        y_sizeI = self.height/2.0000
        x_startI = self.width/1.6000
        y_startI = self.height/3.5000
        (x,y) = pygame.mouse.get_pos()

        #Botón volver al menú
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(self.picture is not None):
                if(self.opened_screen):
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/3.4286, self.height/1.4000))
                    self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/3.0000, self.height/1.3861))
                self.screen.blit(pygame.transform.scale(self.avatarJugador[self.picture], (self.width/3.4286, self.width/3.4286)), (self.width/1.6000, self.height/3.5000))
            else:
                if(self.opened_screen):
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailable, (self.width/3.8339, self.height/12.2807)), (self.width/3.4286, self.height/1.4000))
                    self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/3.0000, self.height/1.3861))
                self.screen.blit(pygame.transform.scale(self.default, (self.width/3.4286, self.width/3.4286)), (self.width/1.6000, self.height/3.5000))
                self.screen.blit(pygame.transform.scale(self.select, (self.width/5.4545, self.width/26.0870)), (self.width/1.4724, self.height/2.0000))    
            if(self.first_timeB):
                self.first_timeI = True
                self.first_timeB = False
                self.first_timeBG = True
                self.ch3.play(self.selected)
            pygame.display.update() 
        
        #Icono
        elif(self.checkIfMouseIsInButton(x_sizeI,y_sizeI,x_startI,y_startI,x,y)):
            if(not self.opened_screen):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
                if(self.picture is not None):
                    self.screen.blit(pygame.transform.scale(self.avatarJugadorSelected[self.picture], (self.width/3.4286, self.width/3.4286)), (self.width/1.6000, self.height/3.5000))

                else:
                    self.screen.blit(pygame.transform.scale(self.defaultSelected, (self.width/3.4286, self.width/3.4286)), (self.width/1.6000, self.height/3.5000))
                    self.screen.blit(pygame.transform.scale(self.selectWhite, (self.width/5.4545, self.width/26.0870)), (self.width/1.4724, self.height/2.0000))
                
                if(self.first_timeI):
                    self.first_timeI = False
                    self.first_timeB = True
                    self.first_timeBG = True
                    self.ch3.play(self.selected)     
                pygame.display.update() 
            else:
                for i in range(0,6):
                    someSelected = 0
                    x_size = self.width/10.5263
                    y_size = self.width/10.5263
                    x_start = (self.width/6.9364) +  ((self.width/7.7922)*(i%3))
                    y_start = (self.height/5.0000) +((self.height/4.5455)*(i//3))
                    if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                        self.picture = i
                        #self.screen.blit(pygame.transform.scale(self.avatarJugadorSelected[i], (114,114)), (173+154*(i%3),140+154*(i//3)))
                        self.screen.blit(pygame.transform.scale(self.avatarJugadorSelected[i], (x_size, y_size)), (x_start, y_start))
                        someSelected = 1
                    else:
                        #self.screen.blit(pygame.transform.scale(self.avatarJugador[i], (114,114)), (173+154*(i%3),140+154*(i//3)))
                        self.screen.blit(pygame.transform.scale(self.avatarJugador[i], (x_size, y_size)), (x_start, y_start))#imagenes
                if(someSelected == 0 and self.picture is not None):
                    x_size = self.width/10.5263
                    y_size = self.width/10.5263
                    x_start = (self.width/6.9364) +  ((self.width/7.7922)*(self.picture%3))
                    y_start = (self.height/5.0000) +((self.height/4.5455)*(self.picture//3))
                    self.screen.blit(pygame.transform.scale(self.avatarJugadorSelected[self.picture], (x_size, y_size)), (x_start, y_start))
                if(self.picture is not None):
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/3.4286, self.height/1.4000))
                    self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/3.0000, self.height/1.3861))
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailable, (self.width/3.8339, self.height/12.2807)), (self.width/3.4286, self.height/1.4000))
                    self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/3.0000, self.height/1.3861))
                pygame.display.update() 
        
        #botón guardar y salir
        elif(self.opened_screen):
            x_size = self.width/3.8339
            y_size = self.height/12.2807
            x_start = self.width/3.4286
            y_start = self.height/1.4000
            if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                if(self.picture is not None and self.opened_screen):
                    self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/3.4286, self.height/1.4000))
                    self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/3.0000, self.height/1.3861))
                    if(self.first_timeBG):
                        self.first_timeBG = False  
                        self.first_timeB = True
                        self.first_timeI = True
                        self.ch1.play(self.selected)
                elif(self.opened_screen):
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailable, (self.width/3.8339, self.height/12.2807)), (self.width/3.4286, self.height/1.4000))
                    self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/3.0000, self.height/1.3861))
                else:
                    pass
                pygame.display.update()
            else:
                self.first_timeB = True
                self.first_timeI = True
                self.first_timeBG = True
                if(self.picture is not None):
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/3.4286, self.height/1.4000))
                    self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/3.0000, self.height/1.3861))
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailable, (self.width/3.8339, self.height/12.2807)), (self.width/3.4286, self.height/1.4000))
                    self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/3.0000, self.height/1.3861))
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
                pygame.display.update()
        else:
            self.first_timeB = True
            self.first_timeI = True
            self.first_timeBG = True
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(self.picture is not None):
                self.screen.blit(pygame.transform.scale(self.avatarJugador[self.picture], (self.width/3.4286, self.width/3.4286)), (self.width/1.6000, self.height/3.5000))
            else:
                self.screen.blit(pygame.transform.scale(self.default, (self.width/3.4286, self.width/3.4286)), (self.width/1.6000, self.height/3.5000))
                self.screen.blit(pygame.transform.scale(self.select, (self.width/5.4545, self.width/26.0870)), (self.width/1.4724, self.height/2.0000))
            pygame.display.update() 
        