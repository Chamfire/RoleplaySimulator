import pygame
from pygame.locals import *
from pygame import mixer
import random
import threading
from llama_cpp import Llama
from ConsultaDescripcion import ConsultaDescripcion
from Personaje import Personaje
import ctypes
import sqlite3
import pickle
from Global import Global
import socket

class SeleccionPersonaje2:
    def __init__(self,width,height,screen,ch1,ch2,ch3,ch4,font,model_path,consultaDescripcion,id,seed_random):
        #screen
        self.screen = screen
        random.seed = seed_random
        self.opened_screen = None
        self.isOnline = None
        self.personaje = None
        self.emptyText = None #se modifica en render
        self.defaultTextEdad = None
        self.model_path = model_path
        self.searching = False
        self.consultaDescripcion = consultaDescripcion
        self.descripcionSearchingText = None
        self.hiloConsultaDescripcion = None
        self.ip_dest = None
        self.port_dest = None
        self.id = id
        self.numJugadores = None #esto se recibe como parámetro para el host
        self.password = None
        self.GLOBAL = Global()

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
        #inputbox
        self.activeI = False
        #roll descripción
        self.first_timeRD = True

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
        self.color_dark_red_sat = pygame.Color((121,58,58))
        self.color_light_grey = pygame.Color((144,144,144))
        self.color_magenta = pygame.Color((121,34,53))
        self.color_light_pink = pygame.Color((234,135,255))
        self.color_grey = pygame.Color((208,208,208))
        self.back = self.fuente.render('Volver al menú', True, self.color_white)
        self.crearPersonaje = self.fuente.render('Crear personaje', True, self.color_white)
        self.gd = self.fuente.render('Generar Descripción',True,self.color_white)
        

    def setScreen(self,screen):
        self.screen = screen
        #self.width,self.height= (self.screen.get_width(), self.screen.get_height())
    def getScreen(self):
        return self.screen
    
    def getPersonaje(self):
        return self.personaje
    
    def setNumJugadores(self,n):
        self.numJugadores = n

    def setIpANDPort(self,ip_y_Port_psw):
        self.ip_dest = ip_y_Port_psw[0]
        self.port_dest = ip_y_Port_psw[1]
        self.password = ip_y_Port_psw[2]
    
    def renderTextBlock(self):
        lineSpacing = -2
        spaceWidth, fontHeight = self.fuente3.size(" ")[0], self.fuente3.size("Tg")[1]

        listOfWords = self.response.split(" ")
        imageList = [self.fuente3.render(word, True, self.color_white) for word in listOfWords]

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
                self.screen.blit(image, (round(x), y))
                lineLeft += image.get_width() 
            lineBottom += fontHeight + lineSpacing


    def refresh(self,op,content):
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
        self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
        if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching and self.personaje.descripcion_fisica != None):
            #tiene los campos rellenados
            self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
        else:
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
        if(op == 2):
            self.textEdad = content
        else:
            if(self.personaje.edad != ' '):
                self.textEdad = self.fuente2.render(self.personaje.edad, True, self.color_white)
            else:
                self.textEdad = self.defaultTextEdad
        self.screen.blit(self.edadText,(self.width/2.4000, self.height/12.7273)) #500 55
        pygame.draw.rect(self.screen, self.color_grey, self.inputBoxEdad, 2)
        self.screen.blit(self.textEdad,(self.width/2.3301, self.height/6.3636)) #515 110
        #peso
        self.screen.blit(self.pesoText,(self.width/1.7143, self.height/12.7273)) #700 55
        pygame.draw.rect(self.screen, self.color_grey, self.inputBoxPeso, 2)
        self.screen.blit(self.defaultTextPeso,(self.width/1.6783, self.height/6.3636)) #715 110
        pygame.display.update() 
        #descripción fisica
        self.screen.blit(self.descripcionText,(self.width/13.3333, self.height/3.6842)) #90 190
        pygame.draw.rect(self.screen, self.color_grey, self.inputBoxDescripcion, 2)
        if(self.searching):
            self.screen.blit(self.descripcionSearchingText,(self.width/11.4286, self.height/2.8000)) #105 250
        else:
            if(op == 3):
                self.responseText = self.fuente3.render(self.response,True,self.color_white)
                self.renderTextBlock()
                #self.screen.blit(self.responseText,(self.width/11.4286, self.height/2.8000)) #105 250 
            else:
                self.screen.blit(self.descripcionDefaultText1,(self.width/11.4286, self.height/2.8000)) #105 250
                self.screen.blit(self.descripcionDefaultText2,(self.width/11.4286, self.height/2.4138)) #105 290
        if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.5444, self.height/1.2727)) #313 x h x 777 x 550
        else:
            self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.5444, self.height/1.2727)) #313 x h x 777 x 550
        self.screen.blit(pygame.transform.scale(self.gd, (self.width/5.1502, self.height/17.5000)), (self.width/1.4688, self.height/1.2613)) #233 x h x 817 x 555
        pygame.display.update() 

    def setResponse(self,r):
        self.response = r
        self.personaje.descripcion_fisica = self.response
        self.searching = False

    def setPersonaje(self,personaje):
        self.personaje = personaje

    def render(self,isOnline):
        #render screen
        self.isOnline = isOnline
        self.opened_screen = None #al iniciar será siempre none
        self.letterwidth = (self.width/3.4286)/14 #cálculo de la base en píxeles 
        self.lettersize = int(self.letterwidth + 0.5 * self.letterwidth) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente2 = pygame.font.SysFont(self.font,self.lettersize)

        self.letterwidth2 = (self.width/3.4286)/16 #cálculo de la base en píxeles 
        self.lettersize2 = int(self.letterwidth2 + 0.5 * self.letterwidth2) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente3 = pygame.font.SysFont(self.font,self.lettersize2)

        self.letterwidth3 = (self.width/3.4286)/18 #cálculo de la base en píxeles 
        self.lettersize3 = int(self.letterwidth3 + 0.5 * self.letterwidth3) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente4 = pygame.font.SysFont(self.font,self.lettersize3)

        self.emptyText = self.fuente2.render(' ', True, self.color_white)
        self.alineamientoText = self.fuente2.render('Alineamiento', True, self.color_white)
        self.edadText = self.fuente2.render('Edad', True, self.color_white)
        self.pesoText = self.fuente2.render('Peso', True, self.color_white)
        self.descripcionText = self.fuente2.render('Descripción Física', True, self.color_white)
        self.defaultTextAlineamiento = self.fuente2.render('-- Escoge alineamiento --', True, self.color_light_grey)
        if(self.personaje.tipo_raza == "Enano"):
            self.defaultTextEdad = self.fuente2.render('1-350', True, self.color_light_grey)
            #60-80kg para un elfo
            peso = str(random.randint(60, 80))
            self.personaje.peso = peso
            self.defaultTextPeso = self.fuente2.render(str(peso+'kg'), True, self.color_white)
        elif(self.personaje.tipo_raza == "Elfo"):
            self.defaultTextEdad = self.fuente2.render('1-750', True, self.color_light_grey)
            #45-66kg para un elfo
            peso = str(random.randint(45, 67))
            self.personaje.peso = peso
            self.defaultTextPeso = self.fuente2.render(str(peso+'kg'), True, self.color_white)
        self.textEdad = self.defaultTextEdad
        self.textAlineamiento = self.defaultTextAlineamiento
    
        self.textPeso = self.defaultTextPeso
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
        self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
        if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching and self.personaje.descripcion_fisica != None):
            #tiene los campos rellenados
            self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
        else:
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
        self.screen.blit(self.textEdad,(self.width/2.3301, self.height/6.3636)) #515 110
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
        self.descripcionDefaultText1 = self.fuente3.render('¡Ya casi estamos!', True, self.color_light_grey)
        self.descripcionDefaultText2 = self.fuente3.render('Pulsa el botón de Generar Descripción para darle una buena descripción a tu personaje.', True, self.color_light_grey)
        self.descripcionSearchingText = self.fuente3.render('Generando descripción física. Este proceso puede tardar entre 10 y 15 segundos...',True,self.color_magenta)
        self.screen.blit(self.descripcionDefaultText1,(self.width/11.4286, self.height/2.8000)) #105 250
        self.screen.blit(self.descripcionDefaultText2,(self.width/11.4286, self.height/2.4138)) #105 290
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.5444, self.height/1.2727)) #313 x h x 777 x 550
        self.screen.blit(pygame.transform.scale(self.gd, (self.width/5.1502, self.height/17.5000)), (self.width/1.4688, self.height/1.2613)) #233 x h x 817 x 555
        pygame.display.update() 


    # size_x, size_y: tamaño del botón en x y en y
    # x_start y y_start: posición de la esquina izquierda del botón
    # pos_x y pos_y: posición actual del ratón
    def checkIfMouseIsInButton(self,size_x,size_y,x_start,y_start,pos_x,pos_y):
        if((pos_x >= x_start and pos_x <= size_x+x_start) and (pos_y >= y_start and pos_y <= size_y + y_start)):
            return True
        else:
            return False
        
    def select_option(self,op):
        if(op == "Legal Bueno"):
            pygame.draw.rect(self.screen,self.color_magenta, self.legal_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.legal_neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.legal_malvado, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral_malvado, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_malvado, 0)

        elif(op == "Neutral Bueno"):
            pygame.draw.rect(self.screen,self.color_black, self.legal_bueno, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.neutral_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.legal_neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.legal_malvado, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral_malvado, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_malvado, 0)
        elif(op == "Caótico Bueno"):
            pygame.draw.rect(self.screen,self.color_black, self.legal_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral_bueno, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.caotico_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.legal_neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.legal_malvado, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral_malvado, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_malvado, 0)
        elif(op == "Legal Neutral"):
            pygame.draw.rect(self.screen,self.color_black, self.legal_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_bueno, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.legal_neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.legal_malvado, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral_malvado, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_malvado, 0)
        elif(op == "Neutral"):
            pygame.draw.rect(self.screen,self.color_black, self.legal_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.legal_neutral, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.legal_malvado, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral_malvado, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_malvado, 0)
        elif(op == "Caótico Neutral"):
            pygame.draw.rect(self.screen,self.color_black, self.legal_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.legal_neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.caotico_neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.legal_malvado, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral_malvado, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_malvado, 0)
        elif(op == "Legal Malvado"):
            pygame.draw.rect(self.screen,self.color_black, self.legal_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.legal_neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_neutral, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.legal_malvado, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral_malvado, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_malvado, 0)
        elif(op == "Neutral Malvado"):
            pygame.draw.rect(self.screen,self.color_black, self.legal_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.legal_neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.legal_malvado, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.neutral_malvado, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_malvado, 0)
        elif(op == "Caótico Malvado"):
            pygame.draw.rect(self.screen,self.color_black, self.legal_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.legal_neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.legal_malvado, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral_malvado, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.caotico_malvado, 0)
        else:
            pygame.draw.rect(self.screen,self.color_black, self.legal_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_bueno, 0)
            pygame.draw.rect(self.screen,self.color_black, self.legal_neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_neutral, 0)
            pygame.draw.rect(self.screen,self.color_black, self.legal_malvado, 0)
            pygame.draw.rect(self.screen,self.color_black, self.neutral_malvado, 0)
            pygame.draw.rect(self.screen,self.color_black, self.caotico_malvado, 0)

        pygame.draw.rect(self.screen,self.color_grey, self.legal_bueno, 3)
        self.screen.blit(self.lb_text,(self.width/5.4795, self.height/4.2424)) #219 165
        pygame.draw.rect(self.screen,self.color_grey, self.neutral_bueno, 3)
        self.screen.blit(self.nb_text,(self.width/5.7416, self.height/3.4314)) #209 204
        pygame.draw.rect(self.screen,self.color_grey, self.caotico_bueno, 3)
        self.screen.blit(self.cb_text,(self.width/5.7416, self.height/2.8807)) #209 243
        pygame.draw.rect(self.screen,self.color_grey, self.legal_neutral, 3)
        self.screen.blit(self.ln_text,(self.width/5.7692, self.height/2.4823)) #208 282
        pygame.draw.rect(self.screen,self.color_grey, self.neutral, 3)
        self.screen.blit(self.n_text,(self.width/5.0209, self.height/2.1807)) #239 321 
        pygame.draw.rect(self.screen,self.color_grey, self.caotico_neutral, 3)
        self.screen.blit(self.cn_text,(self.width/6.0302, self.height/1.9444)) #199 360 
        pygame.draw.rect(self.screen,self.color_grey, self.legal_malvado, 3)
        self.screen.blit(self.lm_text,(self.width/5.7416, self.height/1.7544)) #209 399
        pygame.draw.rect(self.screen,self.color_grey, self.neutral_malvado, 3)
        self.screen.blit(self.nm_text,(self.width/6.0302, self.height/1.5982)) #199 438 
        pygame.draw.rect(self.screen,self.color_grey, self.caotico_malvado, 3)
        self.screen.blit(self.cm_text,(self.width/6.0302, self.height/1.4675)) #199 477 

    def checkIfIsNumber(self,n):
        try:
            number = int(n)
            return True
        except:
            return False
        
    def closeHiloBusquedaDescripcion(self):
        #si está activo, que lo detenga
        if self.hiloConsultaDescripcion != None and self.hiloConsultaDescripcion.is_alive():
            ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(self.hiloConsultaDescripcion.ident), ctypes.py_object(SystemExit)
            )

    def clickedMouse(self):
        #click del ratón
        #calculo del tamaño del botón y su posición -> Empezar Simulación
        x_size = self.width/3.8339
        y_size = self.height/12.2807
        x_start = self.width/2.7907
        y_start = self.height/1.1667
        x_start2 = self.width/11.7647
        x_start3 = self.width/1.5444
        y_start2 = self.height/1.2727
        (x,y) = pygame.mouse.get_pos()

        #Botón volver al menú
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start2,y_start,x,y)):
            self.opened_screen = None
            self.activeI = False
            self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching and self.personaje.descripcion_fisica != None):
                #tiene los campos rellenados
                self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
                self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p

            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
                self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p

            self.ch1.play(self.pressed)
            self.personaje = None
            pygame.display.update() 
            return 'menu'
        
        #Botón generar descripción
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start3,y_start2,x,y)):
            if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching):
                self.opened_screen = None
                self.activeI = False
                if(self.personaje.tipo_raza == "Enano"):
                    if(self.personaje.edad == ' '):
                        self.textEdad = self.defaultTextEdad
                    elif(self.personaje.edad != ' ' and self.checkIfIsNumber(self.personaje.edad) and int(self.personaje.edad) >=1 and int(self.personaje.edad) <=350):
                        self.textEdad = self.fuente2.render(self.personaje.edad, True, self.color_white)
                    else:
                        self.textEdad = self.fuente2.render('1-350', True, self.color_dark_red_sat)
                        self.personaje.edad = ' '
                        self.ch1.play(self.error)
                elif(self.personaje.tipo_raza == "Elfo"):
                    if(self.personaje.edad == ' '):
                        self.textEdad = self.defaultTextEdad
                    elif(self.personaje.edad != ' ' and self.checkIfIsNumber(self.personaje.edad) and int(self.personaje.edad) >=1 and int(self.personaje.edad) <=750):
                        self.textEdad = self.fuente2.render(self.personaje.edad, True, self.color_white)
                    else:
                        self.textEdad = self.fuente2.render('1-750', True, self.color_dark_red_sat)
                        self.personaje.edad = ' '
                        self.ch1.play(self.error)
                self.searching = True
                self.refresh(2,self.textEdad)
                pygame.display.update() 
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
                if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching and self.personaje.descripcion_fisica != None):
                    #tiene los campos rellenados
                    self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
                    self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
                    self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
                self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.5444, self.height/1.2727)) #313 x h x 777 x 550
                self.screen.blit(pygame.transform.scale(self.gd, (self.width/5.1502, self.height/17.5000)), (self.width/1.4688, self.height/1.2613)) #233 x h x 817 x 555
                self.ch1.play(self.pressed)

                self.consultaDescripcion.initialize(self.personaje,self.model_path)
                self.hiloConsultaDescripcion = threading.Thread(target=self.consultaDescripcion.consultaDescripcion)
                self.hiloConsultaDescripcion.start()
                

                pygame.display.update() 
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.5444, self.height/1.2727)) #313 x h x 777 x 550
                self.screen.blit(pygame.transform.scale(self.gd, (self.width/5.1502, self.height/17.5000)), (self.width/1.4688, self.height/1.2613)) #233 x h x 817 x 555
                pygame.display.update() 
            else:
                self.opened_screen = None
                self.activeI = False
                if(self.personaje.tipo_raza == "Enano"):
                    if(self.personaje.edad == ' '):
                        self.textEdad = self.defaultTextEdad
                    elif(self.personaje.edad != ' ' and self.checkIfIsNumber(self.personaje.edad) and int(self.personaje.edad) >=1 and int(self.personaje.edad) <=350):
                        self.textEdad = self.fuente2.render(self.personaje.edad, True, self.color_white)
                    else:
                        self.textEdad = self.fuente2.render('1-350', True, self.color_dark_red_sat)
                        self.personaje.edad = ' '
                        self.ch1.play(self.error)
                elif(self.personaje.tipo_raza == "Elfo"):
                    if(self.personaje.edad == ' '):
                        self.textEdad = self.defaultTextEdad
                    elif(self.personaje.edad != ' ' and self.checkIfIsNumber(self.personaje.edad) and int(self.personaje.edad) >=1 and int(self.personaje.edad) <=750):
                        self.textEdad = self.fuente2.render(self.personaje.edad, True, self.color_white)
                    else:
                        self.textEdad = self.fuente2.render('1-750', True, self.color_dark_red_sat)
                        self.personaje.edad = ' '
                        self.ch1.play(self.error)
                self.refresh(2,self.textEdad)
                pygame.display.update() 
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
                self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
                if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching and self.personaje.descripcion_fisica != None):
                    #tiene los campos rellenados
                    self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
                    self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
                    self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.5444, self.height/1.2727)) #313 x h x 777 x 550
                self.screen.blit(pygame.transform.scale(self.gd, (self.width/5.1502, self.height/17.5000)), (self.width/1.4688, self.height/1.2613)) #233 x h x 817 x 555
                self.ch1.play(self.error)

            return 'seleccionPersonaje2'
        
        #Botón crear personaje
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            screen = 'seleccionPersonaje2'
            self.opened_screen = None
            self.activeI = False
            if(self.personaje.tipo_raza == "Enano"):
                if(self.personaje.edad == ' '):
                    self.textEdad = self.defaultTextEdad
                elif(self.personaje.edad != ' ' and self.checkIfIsNumber(self.personaje.edad) and int(self.personaje.edad) >=1 and int(self.personaje.edad) <=350):
                    self.textEdad = self.fuente2.render(self.personaje.edad, True, self.color_white)
                else:
                    self.textEdad = self.fuente2.render('1-350', True, self.color_dark_red_sat)
                    self.personaje.edad = ' '
                    self.ch1.play(self.error)
            elif(self.personaje.tipo_raza == "Elfo"):
                if(self.personaje.edad == ' '):
                    self.textEdad = self.defaultTextEdad
                elif(self.personaje.edad != ' ' and self.checkIfIsNumber(self.personaje.edad) and int(self.personaje.edad) >=1 and int(self.personaje.edad) <=750):
                    self.textEdad = self.fuente2.render(self.personaje.edad, True, self.color_white)
                else:
                    self.textEdad = self.fuente2.render('1-750', True, self.color_dark_red_sat)
                    self.personaje.edad = ' '
                    self.ch1.play(self.error)
            self.refresh(2,self.textEdad)
            pygame.display.update() 

            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.5444, self.height/1.2727)) #313 x h x 777 x 550
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.5444, self.height/1.2727)) #313 x h x 777 x 550
            self.screen.blit(pygame.transform.scale(self.gd, (self.width/5.1502, self.height/17.5000)), (self.width/1.4688, self.height/1.2613)) #233 x h x 817 x 555
            if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching and self.personaje.descripcion_fisica != None):
                #tiene los campos rellenados
                self.screen.blit(pygame.transform.scale(self.bCreate_pressed, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
                self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
                self.ch1.play(self.pressed)
                if(not self.isOnline):
                    #guardamos en la bbdd la ficha del jugador
                    conn = sqlite3.connect("simuladordnd.db")
                    cursor = conn.cursor()
                    #trasfondo: num_trasfondo es la pk, que se autoincrementa sola
                    query_save_trasfondo = """INSERT INTO trasfondo (tipo_trasfondo, vinculo, defecto, ideal, rasgo_personalidad, num_trasfondo) 
                                                VALUES (?,?,?,?,?,?)"""
                    id_t = self.personaje.id_trasfondo[1]
                    id_trasfondo = str(self.personaje.id_trasfondo[0])+"_"+str((self.personaje.vinculo[1]+id_t*6))+"_"+str((self.personaje.defecto[1]+ id_t*6))+"_"+str((self.personaje.ideal[1]+id_t*6))+"_"+str((self.personaje.rasgo_personalidad[1]+id_t*8))
                    data_trasfondo = (self.personaje.id_trasfondo[0],(self.personaje.vinculo[1]+id_t*6) ,(self.personaje.defecto[1]+ id_t*6),(self.personaje.ideal[1]+id_t*6),(self.personaje.rasgo_personalidad[1]+id_t*8),id_trasfondo)
                    #print(data_trasfondo)
                    query_check_same_trasfondo = "SELECT num_trasfondo FROM trasfondo WHERE num_trasfondo = '"+id_trasfondo+"'"
                    cursor.execute(query_check_same_trasfondo)
                    rows = cursor.fetchall() 
                    #print(rows)
                    if rows != []:
                        #existe esa combinación en la bbdd
                        pass
                    else:
                        #si no existe esa combinación aún en la bbdd
                        cursor.execute(query_save_trasfondo, data_trasfondo)

                    #personaje
                    query_save_personaje = """INSERT INTO personaje (name, sm1, sm2, sm3, nivel, inspiracion,esta_muerto,bpc,cons,fu,des,sab,car,int,coordenadas_actuales,vida_temp,max_vida,ca,edad,peso,pc,pp,pe,po,ppt,velocidad,descripcion_fisica,tipo_raza,tipo_clase,tipo_alineamiento,id_trasfondo,tipo_size,partida_id,id_jugador,num_npc_partida) 
                                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
                        
                    data_personaje = (self.personaje.name, self.personaje.sm1,self.personaje.sm2,self.personaje.sm3,self.personaje.nivel,self.personaje.inspiracion,self.personaje.esta_muerto,self.personaje.bpc,self.personaje.cons,self.personaje.fu,self.personaje.des,self.personaje.sab,self.personaje.car,self.personaje.int,self.personaje.coordenadas_actuales,self.personaje.vida_temp,self.personaje.max_vida,self.personaje.ca,self.personaje.edad,self.personaje.peso,self.personaje.pc,self.personaje.pp,self.personaje.pe,self.personaje.po,self.personaje.ppt,self.personaje.velocidad,self.personaje.descripcion_fisica,self.personaje.tipo_raza,self.personaje.tipo_clase,self.personaje.tipo_alineamiento[0],id_trasfondo,self.personaje.tipo_size,self.personaje.partida_id,self.id,None) 
                    conn.execute(query_save_personaje,data_personaje)

                    #competencias de idioma
                    data_idiomas_comp = []
                    query_save_comp_idioma = """INSERT INTO comp_idioma (tipo_language,name,partida_id,id_jugador,num_npc_partida)
                                                VALUES (?,?,?,?,?)"""
                    for idioma,isCompetent in self.personaje.idiomas_competencia.items():
                        if(isCompetent):
                            data_idiomas_comp += [(idioma,self.personaje.name,self.personaje.partida_id,self.id,None)]
                    conn.executemany(query_save_comp_idioma,data_idiomas_comp)
                    
                    #salvaciones de competencia
                    data_salvaciones_comp = []
                    query_save_salvaciones_comp = """INSERT INTO salvaciones_comp (tipo_caracteristica,name,partida_id,id_jugador,num_npc_partida)
                                                    VALUES(?,?,?,?,?)"""
                    for salvacion, isCompetent in self.personaje.salvaciones_comp.items():
                        if(isCompetent):
                            data_salvaciones_comp += [(salvacion,self.personaje.name,self.personaje.partida_id,self.id,None)]
                    conn.executemany(query_save_salvaciones_comp,data_salvaciones_comp)

                    #habilidades de competencia
                    data_habilidades_comp = []
                    query_save_habilidades_comp = """INSERT INTO habilidades_comp (tipo_habilidad,name,partida_id,id_jugador,num_npc_partida)
                                                    VALUES(?,?,?,?,?)"""
                    for habilidad, isCompetent in self.personaje.habilidades_comp.items():
                        if(isCompetent):
                            data_habilidades_comp += [(habilidad,self.personaje.name,self.personaje.partida_id,self.id,None)]
                    conn.executemany(query_save_habilidades_comp,data_habilidades_comp)

                    #inventario
                    data_inventario = []
                    query_save_inventario = """INSERT INTO inventario (cantidad,name_obj,categoria_obj,name,partida_id,id_jugador,num_npc_partida,procedencia,lista_nombre,slot)
                                                VALUES(?,?,?,?,?,?,?,?,?,?)"""
                    for slot_name, objeto in self.personaje.equipo.objetos.items():
                        if(objeto != None):
                            tipo = str(type(objeto[2]))
                            tipo_nombre = tipo[25:-2]
                            data_inventario += [(objeto[3],objeto[1],objeto[0],self.personaje.name,self.personaje.partida_id,self.id,None,'Equipo',tipo_nombre,slot_name)]
                    conn.executemany(query_save_inventario,data_inventario)


                    #como no tiene armadura equipada, ni objetos al empezar, no se almacenarán aquí, pero si se extraerán de la base de datos en la sala de espera
                    conn.commit()
                    conn.close()
                    if(self.numJugadores == 1):
                        screen = 'partida'
                    else:
                        lista_personajes = self.GLOBAL.getListaPersonajeHost()
                        if(lista_personajes != None and len(lista_personajes) == (self.numJugadores-1)):#sin contar al host
                            screen = 'partida' #desde partida enviará el mensaje de que todos vayan a partida
                        else:    
                            screen = 'partida_load_wait'
                else:
                    datos_personaje_serialized = pickle.dumps(self.personaje)
                    msg = str(self.password)+":"+str(self.id)+":enviar_personaje:"+str(datos_personaje_serialized)
                    socket_temporal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket_temporal.connect((self.ip_dest,self.port_dest))
                    socket_temporal.sendall(msg.encode('utf-8'))
                    respuesta = socket_temporal.recv(1024).decode('utf-8') #tiene timeout de unos segundos
                    print('Respuesta TCP a qué sala ir(podría ser el último en hacerse la ficha): ',respuesta)
                    socket_temporal.close()
                    resp = respuesta.split(':')
                    if(len(resp) == 3):
                        [pswd,id_server,contenido] = resp
                        if (pswd != None and pswd == self.password and id_server == self.GLOBAL.getOtherPlayersIndex(0)[0]):
                            if(contenido != None and contenido == "ve_salaEspera2"):
                                screen = contenido
                            elif(contenido != None and contenido == "ve_partida"):
                                screen = contenido
                            else:
                                screen = "seleccionPersonaje2"
                                self.ch1.play(self.error)
                        else:
                            screen = "seleccionPersonaje2"
                            self.ch1.play(self.error)

            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
                self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
                self.ch1.play(self.error)
            pygame.display.update() 
            return screen
        
        #Input de edad
        elif self.inputBoxEdad.collidepoint((x,y)):
            if(self.opened_screen == None or self.opened_screen == 1):
                if(self.opened_screen == 1):
                    self.opened_screen = None
                if(self.personaje.edad == ' '):
                    self.textEdad= self.emptyText
                self.refresh(2,self.textEdad)
                pygame.display.update() 
                self.activeI = True
                return 'seleccionPersonaje2'
            else:
                self.ch2.play(self.error)
                return 'seleccionPersonaje2'
        
        #Menú desplegable de trasfondos: si le da al recuadro o a la flecha
        elif (self.desplegableAlineamiento.collidepoint((x,y)) or self.rect4.collidepoint((x,y))):
            if(self.personaje.tipo_raza == "Enano"):
                if(self.personaje.edad == ' '):
                    self.textEdad = self.defaultTextEdad
                elif(self.personaje.edad != ' ' and self.checkIfIsNumber(self.personaje.edad) and int(self.personaje.edad) >=1 and int(self.personaje.edad) <=350):
                    self.textEdad = self.fuente2.render(self.personaje.edad, True, self.color_white)
                else:
                    self.textEdad = self.fuente2.render('1-350', True, self.color_dark_red_sat)
                    self.personaje.edad = ' '
                    self.ch1.play(self.error)
            elif(self.personaje.tipo_raza == "Elfo"):
                if(self.personaje.edad == ' '):
                    self.textEdad = self.defaultTextEdad
                elif(self.personaje.edad != ' ' and self.checkIfIsNumber(self.personaje.edad) and int(self.personaje.edad) >=1 and int(self.personaje.edad) <=750):
                    self.textEdad = self.fuente2.render(self.personaje.edad, True, self.color_white)
                else:
                    self.textEdad = self.fuente2.render('1-750', True, self.color_dark_red_sat)
                    self.personaje.edad = ' '
                    self.ch1.play(self.error)
            self.refresh(2,self.textEdad)
            pygame.display.update() 
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
            if(self.personaje.tipo_raza == "Enano"):
                if(self.personaje.edad == ' '):
                    self.textEdad = self.defaultTextEdad
                elif(self.personaje.edad != ' ' and self.checkIfIsNumber(self.personaje.edad) and int(self.personaje.edad) >=1 and int(self.personaje.edad) <=350):
                    self.textEdad = self.fuente2.render(self.personaje.edad, True, self.color_white)
                else:
                    self.textEdad = self.fuente2.render('1-350', True, self.color_dark_red_sat)
                    self.personaje.edad = ' '
                    self.ch1.play(self.error)
            elif(self.personaje.tipo_raza == "Elfo"):
                if(self.personaje.edad == ' '):
                    self.textEdad = self.defaultTextEdad
                elif(self.personaje.edad != ' ' and self.checkIfIsNumber(self.personaje.edad) and int(self.personaje.edad) >=1 and int(self.personaje.edad) <=750):
                    self.textEdad = self.fuente2.render(self.personaje.edad, True, self.color_white)
                else:
                    self.textEdad = self.fuente2.render('1-750', True, self.color_dark_red_sat)
                    self.personaje.edad = ' '
                    self.ch1.play(self.error)
            self.refresh(2,self.textEdad)
            pygame.display.update() 
            self.opened_screen = None
            return 'seleccionPersonaje2'
        

    def manageInputBox(self, key, unicode):
        if(self.activeI):
            if key == pygame.K_RETURN:
                self.personaje.edad = ' '
            elif key == pygame.K_BACKSPACE:
                self.personaje.edad = self.personaje.edad[:-1]
                if(len(self.personaje.edad) == 0):
                    self.personaje.edad = ' '
            else:
                if(len(self.personaje.edad)<3): #la edad puede ser de 1 a 350 para enanos, y de 1 a 750 elfos -> 3 dígitos
                    if(self.personaje.edad == ' '):
                        self.personaje.edad = unicode
                    else:
                        self.personaje.edad += unicode
                    #self.widthText = self.letterwidth*len(self.name)
                else:
                    self.ch2.play(self.error)
            content = self.fuente2.render(self.personaje.edad, True, self.color_light_pink)
            self.refresh(2,content)
            pygame.display.update() 

    def movedMouse(self):
        x_size = self.width/3.8339
        y_size = self.height/12.2807
        x_start = self.width/2.7907
        y_start = self.height/1.1667
        x_start2 = self.width/11.7647
        x_start3 = self.width/1.5444
        y_start2 = self.height/1.2727
        (x,y) = pygame.mouse.get_pos()

        #Botón volver al menú
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start2,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching and self.personaje.descripcion_fisica != None):
                #tiene los campos rellenados
                self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
                self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
                self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.5444, self.height/1.2727)) #313 x h x 777 x 550
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.5444, self.height/1.2727)) #313 x h x 777 x 550
            self.screen.blit(pygame.transform.scale(self.gd, (self.width/5.1502, self.height/17.5000)), (self.width/1.4688, self.height/1.2613)) #233 x h x 817 x 555
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
                self.first_timeRD = True
                self.ch2.play(self.selected)     
            pygame.display.update() 

        #Botón crear personaje
        elif(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching and self.personaje.descripcion_fisica != None):
                #tiene los campos rellenados
                self.screen.blit(pygame.transform.scale(self.bCreate_selected, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
                self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
                self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.5444, self.height/1.2727)) #313 x h x 777 x 550
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.5444, self.height/1.2727)) #313 x h x 777 x 550
            self.screen.blit(pygame.transform.scale(self.gd, (self.width/5.1502, self.height/17.5000)), (self.width/1.4688, self.height/1.2613)) #233 x h x 817 x 555
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
                self.first_timeRD = True
                if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching and self.personaje.descripcion_fisica != None):
                    self.ch2.play(self.selected)     
            pygame.display.update() 

        #generar descripción
        elif(self.checkIfMouseIsInButton(x_size,y_size,x_start3,y_start2,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching and self.personaje.descripcion_fisica != None):
                #tiene los campos rellenados
                self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
                self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
                self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching):
                self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.5444, self.height/1.2727)) #313 x h x 777 x 550
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.5444, self.height/1.2727)) #313 x h x 777 x 550
            self.screen.blit(pygame.transform.scale(self.gd, (self.width/5.1502, self.height/17.5000)), (self.width/1.4688, self.height/1.2613)) #233 x h x 817 x 555
            if(self.first_timeRD):
                self.first_timeRD = False
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
                self.first_timeCP = True
                if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching):
                    self.ch2.play(self.selected)    
                else:
                    pass 
            pygame.display.update() 

        elif(self.legal_bueno.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Legal Bueno")
            if(self.first_time1):
                self.first_time1 = False
                self.first_timeB = True
                self.first_timeCP = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_timeRD = True
                self.ch3.play(self.selected)    
            pygame.display.update() 
        elif(self.neutral_bueno.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Neutral Bueno")
            if(self.first_time2):
                self.first_time2 = False
                self.first_timeB = True
                self.first_timeCP = True 
                self.first_timeB = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_timeRD = True
                self.ch3.play(self.selected)    
            pygame.display.update() 
        elif(self.caotico_bueno.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Caótico Bueno")
            if(self.first_time3):
                self.first_time3 = False
                self.first_timeB = True
                self.first_timeCP = True 
                self.first_time1 = True
                self.first_time2 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_timeRD = True
                self.ch3.play(self.selected)    
            pygame.display.update() 
        elif(self.legal_neutral.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Legal Neutral")
            if(self.first_time4):
                self.first_time4 = False
                self.first_timeB = True
                self.first_timeCP = True 
                self.first_time1 = True
                self.first_time2 = True
                self.first_time3 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_timeRD = True
                self.ch3.play(self.selected)    
            pygame.display.update() 
        elif(self.neutral.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Neutral")
            if(self.first_time5):
                self.first_time5 = False
                self.first_timeB = True
                self.first_timeCP = True 
                self.first_time1 = True
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_timeRD = True
                self.ch3.play(self.selected)    
            pygame.display.update() 
        elif(self.caotico_neutral.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Caótico Neutral")
            if(self.first_time6):
                self.first_time6 = False
                self.first_timeB = True
                self.first_timeCP = True 
                self.first_time1 = True
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_timeRD = True
                self.ch3.play(self.selected)    
            pygame.display.update() 
        elif(self.legal_malvado.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Legal Malvado")
            if(self.first_time7):
                self.first_time7 = False
                self.first_timeB = True
                self.first_timeCP = True 
                self.first_time1 = True
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_timeRD = True
                self.ch3.play(self.selected)    
            pygame.display.update() 
        elif(self.neutral_malvado.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Neutral Malvado")
            if(self.first_time8):
                self.first_time8 = False
                self.first_timeB = True
                self.first_timeCP = True 
                self.first_time1 = True
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time9 = True
                self.first_timeRD = True
                self.ch3.play(self.selected)    
            pygame.display.update() 
        elif(self.caotico_malvado.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Caótico Malvado")
            if(self.first_time9):
                self.first_time9 = False
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
                self.first_timeRD = True
                self.ch3.play(self.selected)    
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
            self.first_timeRD = True
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            #TODO: Comprobar requisitos para crear personaje botón
            if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching and self.personaje.descripcion_fisica != None):
                #tiene los campos rellenados
                self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
                self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
                self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            if(self.personaje.edad != None and self.personaje.edad != ' ' and not self.searching):
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.5444, self.height/1.2727)) #313 x h x 777 x 550
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.5444, self.height/1.2727)) #313 x h x 777 x 550
            self.screen.blit(pygame.transform.scale(self.gd, (self.width/5.1502, self.height/17.5000)), (self.width/1.4688, self.height/1.2613)) #233 x h x 817 x 555
            if(self.opened_screen == 1):
                self.select_option("default")
            pygame.display.update() 