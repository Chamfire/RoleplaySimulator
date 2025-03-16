import pygame
from pygame.locals import *
from pygame import mixer
import socket
from Global import Global
from Personaje import Personaje
import sqlite3
import random
import pickle
import threading

class SeleccionPersonaje:
    #sound

    def __init__(self,width,height,screen,ch1,ch2,ch3,ch4,font,myId,seed_random):
        #screen
        self.screen = screen
        random.seed = seed_random
        self.isOnline = None
        self.GLOBAL = Global()
        self.id = myId
        self.font = font
        self.opened_screen = None
        self.textName = None #se modifica al hacer render
        self.emptyText = None #se modifica en render
        self.activeI = False
        self.max_length_name = 20
        self.personaje = None
        self.textTrasfondo = None
        self.ip_dest = None
        self.port_dest = None
        self.password = None
        self.vinculos = {0:[None,None,None,None,None,None],1:[None,None,None,None,None,None],2:[None,None,None,None,None,None],3:[None,None,None,None,None,None],4:[None,None,None,None,None,None],5:[None,None,None,None,None,None],6:[None,None,None,None,None,None],7:[None,None,None,None,None,None],8:[None,None,None,None,None,None],9:[None,None,None,None,None,None],10:[None,None,None,None,None,None],11:[None,None,None,None,None,None],12:[None,None,None,None,None,None]}
        self.defectos = {0:[None,None,None,None,None,None],1:[None,None,None,None,None,None],2:[None,None,None,None,None,None],3:[None,None,None,None,None,None],4:[None,None,None,None,None,None],5:[None,None,None,None,None,None],6:[None,None,None,None,None,None],7:[None,None,None,None,None,None],8:[None,None,None,None,None,None],9:[None,None,None,None,None,None],10:[None,None,None,None,None,None],11:[None,None,None,None,None,None],12:[None,None,None,None,None,None]}
        self.rasgos_personalidad = {0:[None,None,None,None,None,None,None,None],1:[None,None,None,None,None,None,None,None],2:[None,None,None,None,None,None,None,None],3:[None,None,None,None,None,None,None,None],4:[None,None,None,None,None,None,None,None],5:[None,None,None,None,None,None,None,None],6:[None,None,None,None,None,None,None,None],7:[None,None,None,None,None,None,None,None],8:[None,None,None,None,None,None,None,None],9:[None,None,None,None,None,None,None,None],10:[None,None,None,None,None,None,None,None],11:[None,None,None,None,None,None,None,None],12:[None,None,None,None,None,None,None,None]}
        self.ideales = {0:[None,None,None,None,None,None],1:[None,None,None,None,None,None],2:[None,None,None,None,None,None],3:[None,None,None,None,None,None],4:[None,None,None,None,None,None],5:[None,None,None,None,None,None],6:[None,None,None,None,None,None],7:[None,None,None,None,None,None],8:[None,None,None,None,None,None],9:[None,None,None,None,None,None],10:[None,None,None,None,None,None],11:[None,None,None,None,None,None],12:[None,None,None,None,None,None]}
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
        self.first_timeCP = True #Botón de seguir con la ficha
        #Del menú desplegable, cada opción no ha sido pulsada aún
        self.first_time1 = True 
        self.first_time2 = True
        self.first_time3 = True
        self.first_time4 = True
        self.first_time5 = True
        self.first_time6 = True
        self.first_time7 = True
        self.first_time8 = True
        self.first_time9 = True
        self.first_time10 = True
        self.first_time11 = True
        self.first_time12 = True
        self.first_time13 = True
        #Vínculos,rasgos, ideales y defectos
        self.first_timed0 = True
        self.first_timed1 = True
        self.first_timed2 = True
        self.first_timed3 = True
        self.first_timed4 = True
        self.first_timed5 = True
        self.first_timed6 = True
        self.first_timed7 = True
        #raza
        self.first_timeR = True #icono de raza en el menú
        self.first_timeR1 = True #desplegable
        self.first_timeR2 = True
        #clase
        self.first_timeC = True #icono de clase en el menú
        self.first_timeC1 = True #desplegable
        self.first_timeC2 = True

        #cargamos las imágenes del menú
        self.backgroundPic = pygame.image.load("images/background.png")
        self.buttonPic = pygame.image.load("images/button.png")
        self.capa = pygame.image.load("images/capa.png")
        self.buttonSelectedPic = pygame.image.load("images/button_selected.png")
        self.buttonPressedPic = pygame.image.load("images/button_pressed.png")
        self.flechaDesplegable = pygame.image.load("images/flecha_menu_desplegable.png")
        self.flechaDesplegable_selected = pygame.image.load("images/flecha_menu_desplegable_selected.png")
        self.bCreate = pygame.image.load("images/button_createPartida.png")
        self.bCreate_selected = pygame.image.load("images/button_createPartida_selected.png")
        self.bCreate_pressed = pygame.image.load("images/button_createPartida_pressed.png")
        self.buttonUnavailablePic = pygame.image.load("images/button_unavailable.png")
        self.defaultIconRaza = pygame.image.load("images/iconos/icon_default_large.png")
        self.defaultIconRaza_selected = pygame.image.load("images/iconos/icon_default_large_selected.png")
        self.default = pygame.image.load("images/iconos/icon_default.png")
        self.screen_icons = pygame.image.load("images/screen_icons.png")
        self.icon_barbarbarian = pygame.image.load("images/iconos/icon_barbarian.png")
        self.icon_explorer = pygame.image.load("images/iconos/icon_explorer.png")
        self.icon_large_dwarf = pygame.image.load("images/iconos/icon_large_dwarf.png")
        self.icon_large_elf = pygame.image.load("images/iconos/icon_large_elf.png")
        self.icon_barbarbarian_selected = pygame.image.load("images/iconos/icon_barbarian_selected.png")
        self.icon_explorer_selected = pygame.image.load("images/iconos/icon_explorer_selected.png")
        self.icon_large_dwarf_selected = pygame.image.load("images/iconos/icon_large_dwarf_selected.png")
        self.icon_large_elf_selected = pygame.image.load("images/iconos/icon_large_elf_selected.png")
        self.defaultSelected = pygame.image.load("images/iconos/icon_default_selected.png")

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
        self.select = self.fuente.render('Selecciona una de las siguientes razas:',True, self.color_white)
        self.select2 = self.fuente.render('Selecciona una de las siguientes clases:',True, self.color_white)

    def setScreen(self,screen):
        self.screen = screen
        #self.width,self.height= (self.screen.get_width(), self.screen.get_height())
    def getScreen(self):
        return self.screen

    def setPassword(self,pswd):
        self.password = pswd

    def setCurrentPartida(self,p):
        self.currentPartida = p

    def getPersonaje(self):
        return self.personaje
    
    def setIpANDPortDest(self,ip_y_port_y_pswd):
        self.ip_dest = ip_y_port_y_pswd[0]
        self.port_dest = ip_y_port_y_pswd[1]
        self.password =ip_y_port_y_pswd[2]

    def getPassword(self):
        return self.password

    def refresh(self,op,content):
        if(op == 7):
            self.opened_screen = None
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
        self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
        if(self.personaje.name != None and self.personaje.name != ' ' and self.personaje.id_trasfondo != None and self.personaje.tipo_raza != None and self.personaje.tipo_clase != None and self.personaje.vinculo != None and self.personaje.defecto != None and self.personaje.rasgo_personalidad != None and self.personaje.ideal != None):
            self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
        else:
            self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
        self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
    
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
        else:
            if(self.personaje.name == ' ' or self.personaje.name == None):
                self.textName = self.defaultTextName
            else:
                self.textName = self.fuente2.render(self.personaje.name, True, self.color_white)
        self.screen.blit(self.textName,(self.width/3.2520, self.height/12.7273)) #369 55
        if(op == 2):
            self.textTrasfondo = content
           
        self.screen.blit(self.fichaText,(self.width/13.3333, self.height/12.7273)) #90 55
        self.screen.blit(self.textTrasfondo,(self.width/1.4528, self.height/12.7273)) #826 55
        self.screen.blit(pygame.transform.scale(self.flechaDesplegable, (self.width/40.0000, self.height/11.6667)), (self.width/1.0949, self.height/14.0000)) #30 60 1096 50 
        pygame.draw.rect(self.screen, self.color_grey, self.rect4, 2)
        self.defaultRaza = self.fuente3.render('<?>', True, self.color_white)
        if(self.personaje.tipo_raza == None):
            self.screen.blit(pygame.transform.scale(self.defaultIconRaza, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
            self.screen.blit(self.defaultRaza,(self.width/5.1502, self.height/2.0000)) #233 350
        elif(self.personaje.tipo_raza == "Enano"):
           self.screen.blit(pygame.transform.scale(self.icon_large_dwarf, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
        elif(self.personaje.tipo_raza == "Elfo"):
            self.screen.blit(pygame.transform.scale(self.icon_large_elf, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
        self.defaultTextRaza = self.fuente3.render('Raza', True, self.color_white)
        self.screen.blit(self.defaultTextRaza,(self.width/5.4545, self.height/5.3846)) #220 130
        
        if(self.personaje.tipo_clase == None):
            self.screen.blit(pygame.transform.scale(self.default, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
            self.screen.blit(self.defaultRaza,(self.width/2.5696, self.height/2.9167)) #467 240
        elif(self.personaje.tipo_clase == "Bárbaro"):
            self.screen.blit(pygame.transform.scale(self.icon_barbarbarian, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
        elif(self.personaje.tipo_clase == "Explorador"):
            self.screen.blit(pygame.transform.scale(self.icon_explorer, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
        self.defaultTextClase = self.fuente3.render('Clase', True, self.color_white)
        self.screen.blit(self.defaultTextClase,(self.width/2.6667, self.height/5.3846)) #450 130
        self.vinculosText = self.fuente2.render('Vínculos', True, self.color_white)
        self.defectosText = self.fuente2.render('Defectos', True, self.color_white)
        self.rasgosText = self.fuente2.render('Rasgos de personalidad', True, self.color_white)
        self.idealesText = self.fuente2.render('Ideales', True, self.color_white)
        self.screen.blit(self.vinculosText,(self.width/2.0000, self.height/4.1176)) #600 170
        self.screen.blit(self.defectosText,(self.width/2.0168, self.height/2.5090)) #595 279
        self.screen.blit(self.rasgosText,(self.width/2.8571, self.height/1.8041)) #420 388
        self.screen.blit(self.idealesText,(self.width/1.9512, self.height/1.4085)) #615 497
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
        if(op == 3):
            self.vinculosText2 = content
        else:
            if(self.personaje.vinculo != None):
                self.vinculosText2 = self.fuente2.render('Vínculo Seleccionado: ('+str(self.personaje.vinculo[1])+')', True, self.color_white)
            else:
                self.vinculosText2 = self.fuente2.render('-- Selecciona un vínculo --', True, self.color_light_grey)
        self.screen.blit(self.vinculosText2,(self.width/1.5707, self.height/4.1176)) #764 170
        if(op == 4):
            self.defectosText2 = content
            self.screen.blit(self.defectosText2,(self.width/1.5707, self.height/2.5090)) #764 279
        else:
            if(self.personaje.defecto != None):
                self.defectosText2 = self.fuente2.render('Defecto Seleccionado: ('+str(self.personaje.defecto[1])+')', True, self.color_white)
                self.screen.blit(self.defectosText2,(self.width/1.5707, self.height/2.5090)) #764 279
            else:
                self.defectosText2 = self.fuente2.render('-- Selecciona un defecto --', True, self.color_light_grey)
                self.screen.blit(self.defectosText2,(self.width/1.5810, self.height/2.5090)) #759 279
        if(op == 5):
            self.rasgosText2 = content
            self.screen.blit(self.rasgosText2,(self.width/1.5707, self.height/1.8041)) #764 388
        else:
            if(self.personaje.rasgo_personalidad != None):
                self.rasgosText2 = self.fuente2.render('Rasgo Seleccionado: ('+str(self.personaje.rasgo_personalidad[1])+')', True, self.color_white)
                self.screen.blit(self.rasgosText2,(self.width/1.5707, self.height/1.8041)) #764 388
            else:
                self.rasgosText2 = self.fuente2.render('-- Selecciona tu personalidad --', True, self.color_light_grey)
                self.screen.blit(self.rasgosText2,(self.width/1.6238, self.height/1.8041)) #739 388
        if(op == 6):
            self.idealesText2 = content
            self.screen.blit(self.idealesText2,(self.width/1.5707, self.height/1.4085)) #764 497
        else:
            if(self.personaje.ideal != None):
                self.idealesText2 = self.fuente2.render('Ideal Seleccionado: ('+str(self.personaje.ideal[1])+')', True, self.color_white)
                self.screen.blit(self.idealesText2,(self.width/1.5707, self.height/1.4085)) #764 497
            else:
                self.idealesText2 = self.fuente2.render('-- Selecciona un ideal --', True, self.color_light_grey)
                self.screen.blit(self.idealesText2,(self.width/1.5306, self.height/1.4085)) #784 497


    def render(self,isOnline):
        #obtenemos de la base de datos los rasgos de personalidad, vínculos, defectos e ideales:
        conn = sqlite3.connect("simuladordnd.db")
        cur = conn.cursor()
        cur.execute("SELECT num_id,vinculo FROM vinculos")
        rows = cur.fetchall()
        for i in range(0,78):
            self.vinculos[(i//6)][(i%6)] = rows[i] #cargo los vínculos en el array
        
        cur.execute("SELECT num_id,defecto FROM defectos")
        rows = cur.fetchall()
        for i in range(0,78):
            self.defectos[(i//6)][(i%6)] = rows[i] #cargo los vínculos en el array
        
        cur.execute("SELECT num_id,ideal FROM ideales")
        rows = cur.fetchall()
        for i in range(0,78):
            self.ideales[(i//6)][(i%6)] = rows[i] #cargo los vínculos en el array

        cur.execute("SELECT num_id,rasgo_personalidad FROM rasgos_personalidad")
        rows = cur.fetchall()
        for i in range(0,104):
            self.rasgos_personalidad[(i//8)][(i%8)] = rows[i] #cargo los vínculos en el array

        #render screen
        self.isOnline = isOnline
        if(not self.isOnline):
            self.personaje = Personaje(False,self.currentPartida,self.id) #False porque no es NPC
        else:
            self.personaje = Personaje(False,None,self.id) #None porque no es Host-> TODO: cuando el host reciba el mensaje, debe cambiarlo
        
        self.letterwidth = (self.width/3.4286)/14 #cálculo de la base en píxeles 
        self.lettersize = int(self.letterwidth + 0.5 * self.letterwidth) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente2 = pygame.font.SysFont(self.font,self.lettersize)
        self.letterwidth2 = (self.width/3.4286)/10 #cálculo de la base en píxeles 
        self.lettersize2 = int(self.letterwidth2 + 0.5 * self.letterwidth2) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente3 = pygame.font.SysFont(self.font,self.lettersize2)
        self.letterwidth3 = (self.width/3.4286)/18 #cálculo de la base en píxeles 
        self.lettersize3 = int(self.letterwidth3 + 0.5 * self.letterwidth3) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente4 = pygame.font.SysFont(self.font,self.lettersize3)
        self.letterwidth4 = (self.width/3.4286)/24.2 #cálculo de la base en píxeles 
        self.lettersize4 = int(self.letterwidth4 + 0.5 * self.letterwidth4) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente5 = pygame.font.SysFont(self.font,self.lettersize4)


        self.emptyText = self.fuente2.render(' ', True, self.color_white)
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
        self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
        self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
        self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
        #-- Envío de mensaje TCP de que pasen a la selección de personajes por parte de servidor 
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
        self.textTrasfondo = self.defaultTextTrasfondo
        self.screen.blit(self.textTrasfondo,(self.width/1.4528, self.height/12.7273)) #826 55
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
                        id_player = self.GLOBAL.getOtherPlayersIndex(i)[0]
                        personaje_player = self.GLOBAL.getListaPersonajeHostIndex(id_player)
                        if(personaje_player != -1):
                            #tiene personaje ya creado, así que le mandamos a la sala de espera, porque el host aún no tiene el personaje
                            #pasamos la clase del personaje a objeto
                            datos_personaje_serialized = pickle.dumps(personaje_player)
                            msg = str(self.password)+";"+str(self.id)+";partida_load_wait:"+str(datos_personaje_serialized)
                        else: 
                            #no tiene personaje creado, así que le mandamos a seleccionPersonaje también
                            msg = str(self.password)+";"+str(self.id)+";seleccion_personaje"
                        socket_temporal.sendall(msg.encode('utf-8'))
                    except Exception as e:
                        print(e)
                    finally:
                        socket_temporal.close() #se cierra el socket al terminar
        pygame.display.update() 
        #precargamos todo lo de la interfaz gráfica en el render
        self.acolito_option = pygame.Rect(self.width/1.4870, self.height/6.4220, self.width/3.7500, self.height/17.5000) #807 109 320 40
        self.acolito_text = self.fuente4.render("Acólito", True, self.color_white)
        self.artesano_option = pygame.Rect(self.width/1.4870, self.height/4.7297, self.width/3.7500, self.height/17.5000) #807 148 320 40
        self.artesano_text = self.fuente4.render("Artesano Gremial", True, self.color_white)
        self.artista_option = pygame.Rect(self.width/1.4870, self.height/3.7433, self.width/3.7500, self.height/17.5000) #807 187 320 40
        self.artista_text = self.fuente4.render("Artista", True, self.color_white)
        self.charlatan_option = pygame.Rect(self.width/1.4870, self.height/3.0973, self.width/3.7500, self.height/17.5000) #807 226 320 40
        self.charlatan_text = self.fuente4.render("Charlatán", True, self.color_white)
        self.criminal_option = pygame.Rect(self.width/1.4870, self.height/2.6415, self.width/3.7500, self.height/17.5000) #807 265 320 40
        self.criminal_text = self.fuente4.render("Criminal", True, self.color_white)
        self.ermitano_option = pygame.Rect(self.width/1.4870, self.height/2.3026, self.width/3.7500, self.height/17.5000) #807 304 320 40
        self.eritano_text = self.fuente4.render("Ermitaño", True, self.color_white)
        self.forastero_option = pygame.Rect(self.width/1.4870, self.height/2.0408, self.width/3.7500, self.height/17.5000) #807 343 320 40
        self.forastero_text = self.fuente4.render("Forastero", True, self.color_white)
        self.heroe_option = pygame.Rect(self.width/1.4870, self.height/1.8325, self.width/3.7500, self.height/17.5000) #807 382 320 40
        self.heroe_text = self.fuente4.render("Héroe del pueblo", True, self.color_white)
        self.huerfano_option = pygame.Rect(self.width/1.4870, self.height/1.6627, self.width/3.7500, self.height/17.5000) #807 421 320 40
        self.huerfano_text = self.fuente4.render("Huérfano", True, self.color_white)
        self.marinero_option = pygame.Rect(self.width/1.4870, self.height/1.5217, self.width/3.7500, self.height/17.5000) #807 460 320 40
        self.marinero_text = self.fuente4.render("Marinero", True, self.color_white)
        self.noble_option = pygame.Rect(self.width/1.4870, self.height/1.4028, self.width/3.7500, self.height/17.5000) #807 499 320 40
        self.noble_text = self.fuente4.render("Noble", True, self.color_white)
        self.sabio_option = pygame.Rect(self.width/1.4870, self.height/1.3011, self.width/3.7500, self.height/17.5000) #807 538 320 40
        self.sabio_text = self.fuente4.render("Sabio", True, self.color_white)
        self.soldado_option = pygame.Rect(self.width/1.4870, self.height/1.2132, self.width/3.7500, self.height/17.5000) #807 577 320 40
        self.soldado_text = self.fuente4.render("Soldado", True, self.color_white)
        #rectángulos de seleccion de defectos, vínculos, ideales y rasgos de personalidad
        self.r1 = pygame.Rect(self.width/15.0000, self.height/7.7778, self.width/1.1538, self.height/11.6667) #80 90 1040 60 
        self.r2 = pygame.Rect(self.width/15.0000, self.height/4.6980, self.width/1.1538, self.height/11.6667) #80 149 1040 60
        self.r3 = pygame.Rect(self.width/15.0000, self.height/3.3654, self.width/1.1538, self.height/11.6667) #80 208 1040 60 
        self.r4 = pygame.Rect(self.width/15.0000, self.height/2.6217, self.width/1.1538, self.height/11.6667) #80 267 1040 60 
        self.r5 = pygame.Rect(self.width/15.0000, self.height/2.1472, self.width/1.1538, self.height/11.6667) #80 326 1040 60 
        self.r6 = pygame.Rect(self.width/15.0000, self.height/1.8182, self.width/1.1538, self.height/11.6667) #80 385 1040 60 
        self.r7 = pygame.Rect(self.width/15.0000, self.height/1.5766, self.width/1.1538, self.height/11.6667) #80 444 1040 60 
        self.r8 = pygame.Rect(self.width/15.0000, self.height/1.3917, self.width/1.1538, self.height/11.6667) #80 503 1040 60  

    def select_option(self,op):
        if(op == "Acólito"):
            pygame.draw.rect(self.screen,self.color_magenta, self.acolito_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artesano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artista_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.charlatan_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.criminal_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.ermitano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.forastero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.heroe_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.huerfano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.marinero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.noble_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.sabio_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.soldado_option, 0)
        elif(op == "Artesano Gremial"):
            pygame.draw.rect(self.screen,self.color_black, self.acolito_option, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.artesano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artista_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.charlatan_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.criminal_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.ermitano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.forastero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.heroe_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.huerfano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.marinero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.noble_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.sabio_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.soldado_option, 0)
        elif(op == "Artista"):
            pygame.draw.rect(self.screen,self.color_black, self.acolito_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artesano_option, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.artista_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.charlatan_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.criminal_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.ermitano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.forastero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.heroe_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.huerfano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.marinero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.noble_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.sabio_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.soldado_option, 0)
        elif(op == "Charlatán"):
            pygame.draw.rect(self.screen,self.color_black, self.acolito_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artesano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artista_option, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.charlatan_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.criminal_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.ermitano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.forastero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.heroe_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.huerfano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.marinero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.noble_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.sabio_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.soldado_option, 0)
        elif(op == "Criminal"):
            pygame.draw.rect(self.screen,self.color_black, self.acolito_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artesano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artista_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.charlatan_option, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.criminal_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.ermitano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.forastero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.heroe_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.huerfano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.marinero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.noble_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.sabio_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.soldado_option, 0)
        elif(op == "Ermitaño"):
            pygame.draw.rect(self.screen,self.color_black, self.acolito_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artesano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artista_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.charlatan_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.criminal_option, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.ermitano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.forastero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.heroe_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.huerfano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.marinero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.noble_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.sabio_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.soldado_option, 0)
        elif(op == "Forastero"):
            pygame.draw.rect(self.screen,self.color_black, self.acolito_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artesano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artista_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.charlatan_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.criminal_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.ermitano_option, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.forastero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.heroe_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.huerfano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.marinero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.noble_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.sabio_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.soldado_option, 0)
        elif(op == "Héroe del pueblo"):
            pygame.draw.rect(self.screen,self.color_black, self.acolito_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artesano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artista_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.charlatan_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.criminal_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.ermitano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.forastero_option, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.heroe_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.huerfano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.marinero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.noble_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.sabio_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.soldado_option, 0)
        elif(op == "Huérfano"):
            pygame.draw.rect(self.screen,self.color_black, self.acolito_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artesano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artista_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.charlatan_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.criminal_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.ermitano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.forastero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.heroe_option, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.huerfano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.marinero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.noble_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.sabio_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.soldado_option, 0)
        elif(op == "Marinero"):
            pygame.draw.rect(self.screen,self.color_black, self.acolito_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artesano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artista_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.charlatan_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.criminal_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.ermitano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.forastero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.heroe_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.huerfano_option, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.marinero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.noble_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.sabio_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.soldado_option, 0)
        elif(op == "Noble"):
            pygame.draw.rect(self.screen,self.color_black, self.acolito_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artesano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artista_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.charlatan_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.criminal_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.ermitano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.forastero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.heroe_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.huerfano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.marinero_option, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.noble_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.sabio_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.soldado_option, 0)
        elif(op == "Sabio"):
            pygame.draw.rect(self.screen,self.color_black, self.acolito_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artesano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artista_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.charlatan_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.criminal_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.ermitano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.forastero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.heroe_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.huerfano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.marinero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.noble_option, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.sabio_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.soldado_option, 0)
        elif(op == "Soldado"):
            pygame.draw.rect(self.screen,self.color_black, self.acolito_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artesano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artista_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.charlatan_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.criminal_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.ermitano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.forastero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.heroe_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.huerfano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.marinero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.noble_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.sabio_option, 0)
            pygame.draw.rect(self.screen,self.color_magenta, self.soldado_option, 0)
        else:
            pygame.draw.rect(self.screen,self.color_black, self.acolito_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artesano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.artista_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.charlatan_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.criminal_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.ermitano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.forastero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.heroe_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.huerfano_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.marinero_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.noble_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.sabio_option, 0)
            pygame.draw.rect(self.screen,self.color_black, self.soldado_option, 0)

        pygame.draw.rect(self.screen,self.color_grey, self.acolito_option, 3)
        self.screen.blit(self.acolito_text,(self.width/1.2834, self.height/6.2500)) #935 112
        pygame.draw.rect(self.screen,self.color_grey, self.artesano_option, 3)
        self.screen.blit(self.artesano_text,(self.width/1.3483, self.height/4.6358)) #890 151
        pygame.draw.rect(self.screen,self.color_grey, self.artista_option, 3)
        self.screen.blit(self.artista_text,(self.width/1.2834, self.height/3.6842)) #935 190
        pygame.draw.rect(self.screen,self.color_grey, self.charlatan_option, 3)
        self.screen.blit(self.charlatan_text,(self.width/1.3015, self.height/3.0568)) #922 229
        pygame.draw.rect(self.screen,self.color_grey, self.criminal_option, 3)
        self.screen.blit(self.criminal_text,(self.width/1.2903, self.height/2.6119)) #930 268
        pygame.draw.rect(self.screen,self.color_grey, self.ermitano_option, 3)
        self.screen.blit(self.eritano_text,(self.width/1.2945, self.height/2.2801)) #927 307
        pygame.draw.rect(self.screen,self.color_grey, self.forastero_option, 3)
        self.screen.blit(self.forastero_text,(self.width/1.3015, self.height/2.0231)) #922 346
        pygame.draw.rect(self.screen,self.color_grey, self.heroe_option, 3)
        self.screen.blit(self.heroe_text,(self.width/1.3483, self.height/1.8182)) #895 385
        pygame.draw.rect(self.screen,self.color_grey, self.huerfano_option, 3)
        self.screen.blit(self.huerfano_text,(self.width/1.2945, self.height/1.6509)) #927 424
        pygame.draw.rect(self.screen,self.color_grey, self.marinero_option, 3)
        self.screen.blit(self.marinero_text,(self.width/1.2945, self.height/1.5119)) #927 463
        pygame.draw.rect(self.screen,self.color_grey, self.noble_option, 3)
        self.screen.blit(self.noble_text,(self.width/1.2766, self.height/1.3944)) #940 502
        pygame.draw.rect(self.screen,self.color_grey, self.sabio_option, 3)
        self.screen.blit(self.sabio_text,(self.width/1.2766, self.height/1.2939)) #940 541
        pygame.draw.rect(self.screen,self.color_grey, self.soldado_option, 3)
        self.screen.blit(self.soldado_text,(self.width/1.2903, self.height/1.2069)) #930 580

    # size_x, size_y: tamaño del botón en x y en y
    # x_start y y_start: posición de la esquina izquierda del botón
    # pos_x y pos_y: posición actual del ratón
    def checkIfMouseIsInButton(self,size_x,size_y,x_start,y_start,pos_x,pos_y):
        if((pos_x >= x_start and pos_x <= size_x+x_start) and (pos_y >= y_start and pos_y <= size_y + y_start)):
            return True
        else:
            return False
        
    def initBarbarianInventory(self):
        # ----- INVENTARIO ENANO ------

        # Gran hacha o arma marcial aleatoria
        opcion = random.randint(1,2)
        armasList = self.personaje.equipo.listaInventario.getArmasList()
        if(opcion == 1):
            #Añado gran hacha
            self.personaje.equipo.addObjectToInventory(armasList["Armas c/c marciales"]["Gran hacha"],"Armas c/c marciales","Gran hacha")
        else:
            #añado un arma marcial c/c aleatoria entre la lista
            num_aleatorio = random.randint(1,18) #hay 22 armas marciales c/c
            arma_escogida = None
            categoria_escogida = None
            nombre_arma_escogida = None
            #Empezaremos por el número, y decreceremos 1, hasta llegar a 1
            for arma_nombre,arma in armasList["Armas c/c marciales"].items():
                if(num_aleatorio == 1):
                    arma_escogida = arma
                    categoria_escogida = "Armas c/c marciales"
                    nombre_arma_escogida = arma_nombre
                else:
                    num_aleatorio -= 1
            self.personaje.equipo.addObjectToInventory(arma_escogida,categoria_escogida,nombre_arma_escogida)


        #2 hachas de mano o cualquier arma simple
        opcion = random.randint(1,2)
        if(opcion == 1):
            self.personaje.equipo.addObjectToInventory(armasList["Armas c/c simples"]["Hacha de mano"],"Armas c/c simples","Hacha de mano")
            self.personaje.equipo.addObjectToInventory(armasList["Armas c/c simples"]["Hacha de mano"],"Armas c/c simples","Hacha de mano")
        else:
            num_aleatorio = random.randint(1,15) #hay 15 armas simples
            arma_escogida = None
            categoria_escogida = None
            nombre_arma_escogida = None
            #Empezaremos por el número, y decreceremos 1, hasta llegar a 1
            if (num_aleatorio <= 11): #marciales
                for arma_nombre,arma in armasList["Armas c/c simples"].items():
                    if(num_aleatorio == 1):
                        arma_escogida = arma
                        categoria_escogida = "Armas c/c simples"  
                        nombre_arma_escogida = arma_nombre
                    else:
                        num_aleatorio -= 1
            else: #a distancia
                num_aleatorio -=11 #de 1 a 4
                for arma_nombre,arma in armasList["Armas a distancia simples"].items():
                    if(num_aleatorio == 1):
                        arma_escogida = arma
                        categoria_escogida = "Armas a distancia simples"
                        nombre_arma_escogida = arma_nombre
                    else:
                        num_aleatorio -= 1
            self.personaje.equipo.addObjectToInventory(arma_escogida,categoria_escogida,nombre_arma_escogida)

        #4 jabalinas y un equipo de explorador
        self.personaje.equipo.addObjectToInventory(armasList["Armas c/c simples"]["Jabalina"],"Armas c/c simples","Jabalina")
        self.personaje.equipo.addObjectToInventory(armasList["Armas c/c simples"]["Jabalina"],"Armas c/c simples","Jabalina")
        self.personaje.equipo.addObjectToInventory(armasList["Armas c/c simples"]["Jabalina"],"Armas c/c simples","Jabalina")
        self.personaje.equipo.addObjectToInventory(armasList["Armas c/c simples"]["Jabalina"],"Armas c/c simples","Jabalina")
        # Equipo de explorador
        objetosList = self.personaje.equipo.listaInventario.getObjetosList()
        self.personaje.equipo.addObjectToInventory(objetosList["Almacenaje"]["Mochila"],"Almacenaje","Mochila")
        self.personaje.equipo.addObjectToInventory(objetosList["Refugio"]["Saco de dormir"],"Refugio","Saco de dormir")
        self.personaje.equipo.addObjectToInventory(objetosList["Kit"]["De cocina"],"Kit","De cocina")
        self.personaje.equipo.addObjectToInventory(objetosList["Otros"]["Yesquero"],"Otros","Yesquero")
        for i in range(0,10):
            self.personaje.equipo.addObjectToInventory(objetosList["Iluminación"]["Antorcha"],"Iluminación","Antorcha")
            self.personaje.equipo.addObjectToInventory(objetosList["Comida"]["Ración"],"Comida","Ración")
        self.personaje.equipo.addObjectToInventory(objetosList["Bebida"]["Odre de agua"],"Bebida","Odre de agua")
        self.personaje.equipo.addObjectToInventory(objetosList["Otros"]["Cuerda de cáñamo"],"Otros","Cuerda de cáñamo")
        #self.personaje.equipo.printEquipoConsolaDebugSuperficial()
        
    def initExplorerInventory(self):
        armaduraList = self.personaje.equipo.listaInventario.getArmaduraList()
        armasList = self.personaje.equipo.listaInventario.getArmasList()
        option = random.randint(1,2)
        # Una cota de escamas o una armadura de cuero
        #se equipa automáticamente
        if(option == 1):
            self.personaje.equipo.armadura_actual = ["Armaduras medias","Cota de escamas",armaduraList["Armaduras medias"]["Cota de escamas"]]
        else:
            self.personaje.equipo.armadura_actual = ["Armaduras ligeras","Cuero", armaduraList["Armaduras ligeras"]["Cuero"]]
        
        #2 espadas cortas o 2 armas simples c/c
        option = random.randint(1,2)
        if(option == 1):
            self.personaje.equipo.addObjectToInventory(armasList["Armas c/c marciales"]["Espada corta"],"Armas c/c marciales","Espada corta")
            self.personaje.equipo.addObjectToInventory(armasList["Armas c/c marciales"]["Espada corta"],"Armas c/c marciales","Espada corta")
        else:
            for i in range(1,2):
                num_aleatorio = random.randint(1,11) #hay 11 armas simples c/c
                arma_escogida = None
                categoria_escogida = None
                nombre_arma_escogida = None
                #Empezaremos por el número, y decreceremos 1, hasta llegar a 1
                for arma_nombre,arma in armasList["Armas c/c simples"].items():
                    if(num_aleatorio == 1):
                        arma_escogida = arma
                        categoria_escogida = "Armas c/c simples"
                        nombre_arma_escogida = arma_nombre
                    else:
                        num_aleatorio -= 1
                self.personaje.equipo.addObjectToInventory(arma_escogida,categoria_escogida,nombre_arma_escogida)
        #un equipo de dungeon o un equipo de explorador
        option = random.randint(1,2)
        if(option == 1):
            # Equipo de dungeon
            objetosList = self.personaje.equipo.listaInventario.getObjetosList()
            self.personaje.equipo.addObjectToInventory(objetosList["Refugio"]["Saco de dormir"],"Refugio","Saco de dormir")
            self.personaje.equipo.addObjectToInventory(objetosList["Mecanico"]["Palanca"],"Mecanico","Palanca")
            self.personaje.equipo.addObjectToInventory(objetosList["Mecanico"]["Martillo"],"Mecanico","Martillo")
            for i in range(0,10):
                self.personaje.equipo.addObjectToInventory(objetosList["Otros"]["Piton"],"Otros","Piton")
                self.personaje.equipo.addObjectToInventory(objetosList["Iluminación"]["Antorcha"],"Iluminación","Antorcha")
                self.personaje.equipo.addObjectToInventory(objetosList["Comida"]["Ración"],"Comida","Ración")
            self.personaje.equipo.addObjectToInventory(objetosList["Otros"]["Yesquero"],"Otros","Yesquero")
            self.personaje.equipo.addObjectToInventory(objetosList["Bebida"]["Odre de agua"],"Bebida","Odre de agua")
            self.personaje.equipo.addObjectToInventory(objetosList["Otros"]["Cuerda de cáñamo"],"Otros","Cuerda de cáñamo")
        else:
            # Equipo de explorador
            objetosList = self.personaje.equipo.listaInventario.getObjetosList()
            self.personaje.equipo.addObjectToInventory(objetosList["Almacenaje"]["Mochila"],"Almacenaje","Mochila")
            self.personaje.equipo.addObjectToInventory(objetosList["Refugio"]["Saco de dormir"],"Refugio","Saco de dormir")
            self.personaje.equipo.addObjectToInventory(objetosList["Kit"]["De cocina"],"Kit","De cocina")
            self.personaje.equipo.addObjectToInventory(objetosList["Otros"]["Yesquero"],"Otros","Yesquero")
            for i in range(0,10):
                self.personaje.equipo.addObjectToInventory(objetosList["Iluminación"]["Antorcha"],"Iluminación","Antorcha")
                self.personaje.equipo.addObjectToInventory(objetosList["Comida"]["Ración"],"Comida","Ración")
            self.personaje.equipo.addObjectToInventory(objetosList["Bebida"]["Odre de agua"],"Bebida","Odre de agua")
            self.personaje.equipo.addObjectToInventory(objetosList["Otros"]["Cuerda de cáñamo"],"Otros","Cuerda de cáñamo")
        
        #Un arco largo y un carcaj con 20 flechas
        self.personaje.equipo.addObjectToInventory(armasList["Armas a distancia marciales"]["Arco largo"],"Armas a distancia marciales","Arco largo")
        #20 flechas
        for i in range(0,20):
            self.personaje.equipo.addObjectToInventory(objetosList["Munición"]["Flecha"],"Munición","Flecha")
        #self.personaje.equipo.printEquipoConsolaDebugSuperficial()


    def clickedMouse(self):
        #click del ratón
        #calculo del tamaño del botón y su posición -> Empezar Simulación
        x_size = self.width/3.8339
        y_size = self.height/12.2807
        x_start = self.width/2.7907
        y_start = self.height/1.1667
        x_start2 = self.width/11.7647
        x_sizeR = self.width/5.0000
        y_sizeR = self.height/1.9444
        x_startR = self.width/8.5714
        y_startR = self.height/3.5000
        x_sizeIB = self.width/5.2632
        y_sizeIB = self.height/2.1875
        x_startIB = self.width/10.0000
        y_startIB = self.height/5.0000
        x_startIE = ((self.width/10.0000) + ((self.width/7.7922)*2))
        x_sizeC = self.width/8.0000
        y_sizeC = self.height/4.6667
        x_startC = self.width/2.8571
        y_startC = self.height/3.5000
        (x,y) = pygame.mouse.get_pos()

        #Botón crear personaje
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            screen = 'seleccionPersonaje'
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            if(self.opened_screen == None): 
                self.activeI = False
                self.opened_screen = None
                
                if(self.personaje.name != None and self.personaje.name != ' ' and self.personaje.id_trasfondo != None and self.personaje.tipo_raza != None and self.personaje.tipo_clase != None and self.personaje.vinculo != None and self.personaje.defecto != None and self.personaje.rasgo_personalidad != None and self.personaje.ideal != None):
                    personaje_muerto = False
                    if(not self.isOnline):
                    #consulta para comprobar que el nombre del personaje no coincida con otro personaje existente para ese jugador
                        conn = sqlite3.connect("simuladordnd.db")
                        cursor = conn.cursor()
                        query_check_same_name = "SELECT name FROM personaje WHERE name = '"+self.personaje.name+"' AND partida_id = '"+self.currentPartida+"' AND id_jugador = '"+self.id+"'"
                        cursor.execute(query_check_same_name)
                        rows = cursor.fetchall() 
                        conn.close()
                        if rows != []:
                            personaje_muerto = True
                        #print(rows)

                    else:
                        #es online: -> hay que hacerle una consulta al servidor,para que nos diga si ese personaje ya está o no muerto
                        #TCP
                        socket_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        socket_c.connect((self.ip_dest, int(self.port_dest)))
                        msg_client = str(self.password) + ":"+self.id+":check_nombre:"+self.personaje.name
                        #patata:pepe:3:id:56384:49234 <- ejemplo mensaje
                        socket_c.sendall(msg_client.encode('utf-8'))
                        respuesta = socket_c.recv(1024).decode('utf-8') #tiene timeout de unos segundos
                        socket_c.close()
                        print('Respuesta TCP a check de nombre: ',respuesta)
                        resp = respuesta.split(':')
                        if(len(resp) == 3):
                            #MENSAJE TIPO 2 -> DESCONEXIÓN
                            [pswd,id_server,contenido] = resp
                            if (pswd != None and pswd == self.password and id_server == self.GLOBAL.getOtherPlayersIndex(0)[0]):
                                if(contenido != None and contenido == "no_usar"):
                                    personaje_muerto = True
                                elif(contenido != None and contenido == "usar"):
                                    personaje_muerto = False
                                else:
                                    personaje_muerto = True
                            else:
                                personaje_muerto = True
                                

                    if personaje_muerto:
                        #el nombre ya existe
                        self.ch1.play(self.error)
                        self.personaje.name = ' ' #reseteamos el nombre
                        error_text =  self.fuente2.render('Ya murió, asúmelo.', True, self.color_light_red)
                        self.refresh(1,error_text)
                    else:
                        #El nombre no existe, podemos continuar reando el personaje
                        self.screen.blit(pygame.transform.scale(self.bCreate_pressed, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
                        self.ch1.play(self.pressed)
                        if(self.personaje.tipo_clase == "Explorador"):
                            self.personaje.des = 15
                            self.personaje.sab = 14
                            self.personaje.fu = 13
                            self.personaje.car = 12
                            self.personaje.int = 10
                            self.personaje.cons = 8
                            self.personaje.ca = 11 #10 + 1(Des,12)
                            self.personaje.salvaciones_comp["fu"] = True
                            self.personaje.salvaciones_comp["des"] = True
                            #Dinero: 5d4x 10
                            self.personaje.po = (random.randint(1,4)+random.randint(1,4)+random.randint(1,4)+random.randint(1,4)+random.randint(1,4))*10
                            self.personaje.initEquipo()
                            self.initExplorerInventory()
                            if(self.personaje.tipo_raza == "Enano"):
                                self.personaje.cons += 2 #tiene un +2 en constitución
                                self.personaje.idiomas_competencia["Común"] = True
                                self.personaje.idiomas_competencia["Enano"] = True
                                #escoger competencias de forma aleatoria
                                posibles_competencias = ["Atletismo", "Perspicacia", "Investigación","Trato con Animales", "Naturaleza", "Percepción", "Sigilo", "Supervivencia"]

                            else:
                                self.personaje.idiomas_competencia["Común"] = True
                                self.personaje.idiomas_competencia["Élfico"] = True
                                self.personaje.habilidades_comp["Percepción"] = True
                                posibles_competencias = ["Atletismo", "Perspicacia", "Investigación","Trato con Animales", "Naturaleza", "Sigilo", "Supervivencia"]
                            
                        elif(self.personaje.tipo_clase == "Bárbaro"):
                            self.personaje.fu = 15
                            self.personaje.car = 14
                            self.personaje.cons = 13
                            self.personaje.sab = 12
                            self.personaje.des = 10
                            self.personaje.ca = 10 #10 + Des (0)
                            self.personaje.int = 8
                            self.personaje.salvaciones_comp["fu"] = True
                            self.personaje.salvaciones_comp["cons"] = True
                            #Dinero: 2d4x 10
                            self.personaje.po = (random.randint(1,4)+random.randint(1,4))*10
                            self.personaje.initEquipo()
                            self.initBarbarianInventory()
                            if(self.personaje.tipo_raza == "Enano"):
                                self.personaje.cons += 2 #tiene un +2 en constitución
                                self.personaje.idiomas_competencia["Común"] = True
                                self.personaje.idiomas_competencia["Enano"] = True
                                #Escoger competencias de forma aleatoria
                                posibles_competencias = ["Atletismo", "Intimidación", "Naturaleza", "Percepción", "Supervivencia", "Trato con Animales"]

                            else:
                                self.personaje.idiomas_competencia["Común"] = True
                                self.personaje.idiomas_competencia["Élfico"] = True
                                self.personaje.habilidades_comp["Percepción"] = True
                                #Escoger competencias de forma aleatoria
                                posibles_competencias = ["Atletismo", "Intimidación", "Naturaleza", "Supervivencia", "Trato con Animales"]
                        escogida = random.randint(0,(len(posibles_competencias)-1))
                        self.personaje.habilidades_comp[posibles_competencias[escogida]] = True
                        posibles_competencias.remove(posibles_competencias[escogida])
                        escogida = random.randint(0,(len(posibles_competencias)-1))
                        self.personaje.habilidades_comp[posibles_competencias[escogida]] = True
                        posibles_competencias.remove(posibles_competencias[escogida])     
                        screen = 'seleccionPersonaje2'
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
                    self.ch1.play(self.error)
                self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
                pygame.display.update() 
            else:
                self.ch1.play(self.error)
            return screen
        
        #Botón volver al menú
        elif(self.checkIfMouseIsInButton(x_size,y_size,x_start2,y_start,x,y)):
            self.activeI = False
            self.opened_screen = None 
            self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            if(self.personaje.name != None and self.personaje.name != ' ' and self.personaje.id_trasfondo != None and self.personaje.tipo_raza != None and self.personaje.tipo_clase != None and self.personaje.vinculo != None and self.personaje.defecto != None and self.personaje.rasgo_personalidad != None and self.personaje.ideal != None):
                self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p       
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            self.personaje = None #reiniciamos el personaje para que si abrimos otra partida, no haya restos de esta
            self.ch1.play(self.pressed)
            pygame.display.update() 
            return 'menu'

        #Raza
        elif(self.checkIfMouseIsInButton(x_sizeR,y_sizeR,x_startR,y_startR,x,y) and (self.opened_screen == None or self.opened_screen == 1)):
            self.activeI = False
            self.refresh(0,None)
            self.opened_screen = 6 
            self.ch1.play(self.pressed)
            self.screen.blit(pygame.transform.scale(self.screen_icons, (self.width/1.7143, self.height/1.2727)), (self.width/30.0000, self.height/16.2791)) 
            self.screen.blit(pygame.transform.scale(self.select, (self.width/2.4000, self.height/14.0000)), (self.width/13.3333, self.height/8.7500))
            self.screen.blit(pygame.transform.scale(self.icon_large_dwarf, (self.width/5.2632, self.height/2.1875)), (self.width/10.0000, self.height/5.0000)) #114 160 120 
            self.screen.blit(pygame.transform.scale(self.icon_large_elf, (self.width/5.2632, self.height/2.1875)), (((self.width/10.0000) + ((self.width/7.7922)*2)), self.height/5.0000)) #114 160 
            pygame.display.update() 
            return 'seleccionPersonaje'
    
        #Icono de enano
        elif(self.checkIfMouseIsInButton(x_sizeIB,y_sizeIB,x_startIB,y_startIB,x,y) and self.opened_screen == 6):
            self.opened_screen = None
            self.personaje.tipo_raza = "Enano"
            self.personaje.tipo_size = "Mediano"
            self.personaje.velocidad = 25
            self.ch1.play(self.pressed)
            self.refresh(0,None)
            pygame.display.update()
            return 'seleccionPersonaje'   
            
        #Icono de elfo
        elif(self.checkIfMouseIsInButton(x_sizeIB,y_sizeIB,x_startIE,y_startIB,x,y) and self.opened_screen == 6):
            self.opened_screen = None
            self.personaje.tipo_raza = "Elfo"
            self.personaje.tipo_size = "Mediano"
            self.personaje.velocidad = 30
            self.ch1.play(self.pressed)
            self.refresh(0,None)
            pygame.display.update()
            return 'seleccionPersonaje' 

        #Clase
        elif(self.checkIfMouseIsInButton(x_sizeC,y_sizeC,x_startC,y_startC,x,y) and (self.opened_screen == None or self.opened_screen == 1)):
            self.activeI = False
            self.refresh(0,None)
            self.opened_screen = 7 
            self.ch1.play(self.pressed)
            self.screen.blit(pygame.transform.scale(self.screen_icons, (self.width/1.7143, self.height/1.2727)), (self.width/30.0000, self.height/16.2791)) 
            self.screen.blit(pygame.transform.scale(self.select2, (self.width/2.4000, self.height/14.0000)), (self.width/13.3333, self.height/8.7500))
            self.screen.blit(pygame.transform.scale(self.icon_barbarbarian, (self.width/5.2632, self.width/5.2632)), (self.width/10.0000, self.height/5.0000)) #114 228 120 140
            self.barbarian_name = self.fuente2.render('Bárbaro', True, self.color_white)
            self.explorer_name = self.fuente2.render('Explorador', True, self.color_white)
            self.screen.blit(self.barbarian_name,(self.width/10.0000, self.height/1.8041)) #120 388
            self.screen.blit(pygame.transform.scale(self.icon_explorer, (self.width/5.2632, self.width/5.2632)), (((self.width/10.0000) + ((self.width/7.7922)*2)), self.height/5.0000)) #114 160 
            self.screen.blit(self.explorer_name,(((self.width/10.0000) + ((self.width/7.7922)*2)), self.height/1.8041)) # 388
            pygame.display.update() 
            return 'seleccionPersonaje'
        
        #Bárbaro
        elif(self.checkIfMouseIsInButton(x_sizeIB,x_sizeIB,x_startIB,y_startIB,x,y) and self.opened_screen == 7):
            self.opened_screen = None
            self.personaje.tipo_clase = "Bárbaro"
            self.personaje.bpc = 2
            self.personaje.max_vida = 12 
            self.personaje.vida_temp = 12
            self.ch1.play(self.pressed)
            self.refresh(0,None)
            pygame.display.update()
            return 'seleccionPersonaje' 
        #Explorador
        elif(self.checkIfMouseIsInButton(x_sizeIB,x_sizeIB,x_startIE,y_startIB,x,y) and self.opened_screen == 7):
            self.opened_screen = None
            self.personaje.tipo_clase = "Explorador"
            self.personaje.max_vida = 10 
            self.personaje.vida_temp = 10
            self.personaje.bpc = 2
            self.ch1.play(self.pressed)
            self.refresh(0,None)
            pygame.display.update()
            return 'seleccionPersonaje' 

        #Input de nombre de personaje
        elif self.inputBox.collidepoint((x,y)):
            if(self.opened_screen == None or self.opened_screen == 1):
                if(self.opened_screen == 1):
                    self.opened_screen = None
                if(self.personaje.name == ' '):
                    self.textName= self.emptyText
                self.refresh(1,self.textName)
                pygame.display.update() 
                self.activeI = True
                return 'seleccionPersonaje'
            else:
                self.ch2.play(self.error)
                return 'seleccionPersonaje'
            

        #Menú desplegable de trasfondos: si le da al recuadro o a la flecha
        elif (self.desplegableTrasfondo.collidepoint((x,y)) or self.rect4.collidepoint((x,y))):
            if(self.opened_screen == None or self.opened_screen == 6):
                #desactivo inputBox
                self.refresh(0,None)
                pygame.display.update() 
                self.ch1.play(self.pressed)
                self.activeI = False
                pygame.draw.rect(self.screen,self.color_black, self.inputBox, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.inputBox, 2)
                if(self.personaje.name == ' '):
                    self.textName = self.defaultTextName
                else:
                    self.textName = self.fuente2.render(self.personaje.name, True, self.color_white)
                self.screen.blit(self.textName,(self.width/3.2520, self.height/12.7273)) #369 55
                self.screen.blit(pygame.transform.scale(self.flechaDesplegable_selected, (self.width/40.0000, self.height/11.6667)), (self.width/1.0949, self.height/14.0000)) #30 60 1096 50 
                pygame.draw.rect(self.screen, self.color_grey, self.rect4, 2)
                pygame.display.update() 

                self.opened_screen = 1 #tipo 1: trasfondos
                pygame.draw.rect(self.screen,self.color_black, self.acolito_option, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.acolito_option, 3)
                self.screen.blit(self.acolito_text,(self.width/1.2834, self.height/6.2500)) #935 112
                pygame.draw.rect(self.screen,self.color_black, self.artesano_option, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.artesano_option, 3)
                self.screen.blit(self.artesano_text,(self.width/1.3483, self.height/4.6358)) #890 151
                pygame.draw.rect(self.screen,self.color_black, self.artista_option, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.artista_option, 3)
                self.screen.blit(self.artista_text,(self.width/1.2834, self.height/3.6842)) #935 190
                pygame.draw.rect(self.screen,self.color_black, self.charlatan_option, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.charlatan_option, 3)
                self.screen.blit(self.charlatan_text,(self.width/1.3015, self.height/3.0568)) #922 229
                pygame.draw.rect(self.screen,self.color_black, self.criminal_option, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.criminal_option, 3)
                self.screen.blit(self.criminal_text,(self.width/1.2903, self.height/2.6119)) #930 268
                pygame.draw.rect(self.screen,self.color_black, self.ermitano_option, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.ermitano_option, 3)
                self.screen.blit(self.eritano_text,(self.width/1.2945, self.height/2.2801)) #927 307
                pygame.draw.rect(self.screen,self.color_black, self.forastero_option, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.forastero_option, 3)
                self.screen.blit(self.forastero_text,(self.width/1.3015, self.height/2.0231)) #922 346
                pygame.draw.rect(self.screen,self.color_black, self.heroe_option, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.heroe_option, 3)
                self.screen.blit(self.heroe_text,(self.width/1.3483, self.height/1.8182)) #895 385
                pygame.draw.rect(self.screen,self.color_black, self.huerfano_option, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.huerfano_option, 3)
                self.screen.blit(self.huerfano_text,(self.width/1.2945, self.height/1.6509)) #927 424
                pygame.draw.rect(self.screen,self.color_black, self.marinero_option, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.marinero_option, 3)
                self.screen.blit(self.marinero_text,(self.width/1.2945, self.height/1.5119)) #927 463
                pygame.draw.rect(self.screen,self.color_black, self.noble_option, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.noble_option, 3)
                self.screen.blit(self.noble_text,(self.width/1.2766, self.height/1.3944)) #940 502
                pygame.draw.rect(self.screen,self.color_black, self.sabio_option, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.sabio_option, 3)
                self.screen.blit(self.sabio_text,(self.width/1.2766, self.height/1.2939)) #940 541
                pygame.draw.rect(self.screen,self.color_black, self.soldado_option, 0)
                pygame.draw.rect(self.screen,self.color_grey, self.soldado_option, 3)
                self.screen.blit(self.soldado_text,(self.width/1.2903, self.height/1.2069)) #930 580
                pygame.display.update() 
            else:
                self.ch1.play(self.error)
            return 'seleccionPersonaje'
        
        #Elección de trasfondo
        elif(self.acolito_option.collidepoint((x,y)) and self.opened_screen == 1):
            if(self.personaje.id_trasfondo == None or (self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Acólito")): #si no tenía acólito seleccionado o no había nada, se resetean los vínculos, defectos, etc
                self.personaje.vinculo = None
                self.personaje.defecto = None
                self.personaje.rasgo_personalidad = None
                self.personaje.ideal = None
                if(self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Acólito"):
                    self.ch4.play(self.error)
            self.personaje.id_trasfondo = ("Acólito",0)
            self.ch1.play(self.pressed)
            content = self.fuente2.render('Acólito', True, self.color_white)
            self.refresh(2,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.artesano_option.collidepoint((x,y)) and self.opened_screen == 1):
            if(self.personaje.id_trasfondo == None or (self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Artesano Gremial")): #si no tenía acólito seleccionado o no había nada, se resetean los vínculos, defectos, etc
                self.personaje.vinculo = None
                self.personaje.defecto = None
                self.personaje.rasgo_personalidad = None
                self.personaje.ideal = None
                if(self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Acólito"):
                    self.ch4.play(self.error)
            self.personaje.id_trasfondo = ("Artesano Gremial",1)
            self.ch1.play(self.pressed)
            content = self.fuente2.render('Artesano Gremial', True, self.color_white)
            self.refresh(2,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.artista_option.collidepoint((x,y)) and self.opened_screen == 1):
            if(self.personaje.id_trasfondo == None or (self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Artista")): #si no tenía acólito seleccionado o no había nada, se resetean los vínculos, defectos, etc
                self.personaje.vinculo = None
                self.personaje.defecto = None
                self.personaje.rasgo_personalidad = None
                self.personaje.ideal = None
                if(self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Acólito"):
                    self.ch4.play(self.error)
            self.personaje.id_trasfondo = ("Artista",2)
            self.ch1.play(self.pressed)
            content = self.fuente2.render('Artista', True, self.color_white)
            self.refresh(2,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.charlatan_option.collidepoint((x,y)) and self.opened_screen == 1):
            if(self.personaje.id_trasfondo == None or (self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Charlatán")): #si no tenía acólito seleccionado o no había nada, se resetean los vínculos, defectos, etc
                self.personaje.vinculo = None
                self.personaje.defecto = None
                self.personaje.rasgo_personalidad = None
                self.personaje.ideal = None
                if(self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Acólito"):
                    self.ch4.play(self.error)
            self.personaje.id_trasfondo = ("Charlatán",3)
            self.ch1.play(self.pressed)
            content = self.fuente2.render('Charlatán', True, self.color_white)
            self.refresh(2,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.criminal_option.collidepoint((x,y)) and self.opened_screen == 1):
            if(self.personaje.id_trasfondo == None or (self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Criminal")): #si no tenía acólito seleccionado o no había nada, se resetean los vínculos, defectos, etc
                self.personaje.vinculo = None
                self.personaje.defecto = None
                self.personaje.rasgo_personalidad = None
                self.personaje.ideal = None
                if(self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Acólito"):
                    self.ch4.play(self.error)
            self.personaje.id_trasfondo = ("Criminal",4)
            self.ch1.play(self.pressed)
            content = self.fuente2.render('Criminal', True, self.color_white)
            self.refresh(2,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.ermitano_option.collidepoint((x,y)) and self.opened_screen == 1):
            if(self.personaje.id_trasfondo == None or (self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Ermitaño")): #si no tenía acólito seleccionado o no había nada, se resetean los vínculos, defectos, etc
                self.personaje.vinculo = None
                self.personaje.defecto = None
                self.personaje.rasgo_personalidad = None
                self.personaje.ideal = None
                if(self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Acólito"):
                    self.ch4.play(self.error)
            self.personaje.id_trasfondo = ("Ermitaño",5)
            self.ch1.play(self.pressed)
            content = self.fuente2.render('Ermitaño', True, self.color_white)
            self.refresh(2,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.forastero_option.collidepoint((x,y)) and self.opened_screen == 1):
            if(self.personaje.id_trasfondo == None or (self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Forastero")): #si no tenía acólito seleccionado o no había nada, se resetean los vínculos, defectos, etc
                self.personaje.vinculo = None
                self.personaje.defecto = None
                self.personaje.rasgo_personalidad = None
                self.personaje.ideal = None
                if(self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Acólito"):
                    self.ch4.play(self.error)
            self.personaje.id_trasfondo = ("Forastero",6)
            self.ch1.play(self.pressed)
            content = self.fuente2.render('Forastero', True, self.color_white)
            self.refresh(2,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.heroe_option.collidepoint((x,y)) and self.opened_screen == 1):
            if(self.personaje.id_trasfondo == None or (self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Héroe del pueblo")): #si no tenía acólito seleccionado o no había nada, se resetean los vínculos, defectos, etc
                self.personaje.vinculo = None
                self.personaje.defecto = None
                self.personaje.rasgo_personalidad = None
                self.personaje.ideal = None
                if(self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Acólito"):
                    self.ch4.play(self.error)
            self.personaje.id_trasfondo = ("Héroe del pueblo",7)
            self.ch1.play(self.pressed)
            content = self.fuente2.render('Héroe del pueblo', True, self.color_white)
            self.refresh(2,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.huerfano_option.collidepoint((x,y)) and self.opened_screen == 1):
            if(self.personaje.id_trasfondo == None or (self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Huérfano")): #si no tenía acólito seleccionado o no había nada, se resetean los vínculos, defectos, etc
                self.personaje.vinculo = None
                self.personaje.defecto = None
                self.personaje.rasgo_personalidad = None
                self.personaje.ideal = None
                if(self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Acólito"):
                    self.ch4.play(self.error)
            self.personaje.id_trasfondo = ("Huérfano",8)
            self.ch1.play(self.pressed)
            content = self.fuente2.render('Huérfano', True, self.color_white)
            self.refresh(2,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.marinero_option.collidepoint((x,y)) and self.opened_screen == 1):
            if(self.personaje.id_trasfondo == None or (self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Marinero")): #si no tenía acólito seleccionado o no había nada, se resetean los vínculos, defectos, etc
                self.personaje.vinculo = None
                self.personaje.defecto = None
                self.personaje.rasgo_personalidad = None
                self.personaje.ideal = None
                if(self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Acólito"):
                    self.ch4.play(self.error)
            self.personaje.id_trasfondo = ("Marinero",9)
            self.ch1.play(self.pressed)
            content = self.fuente2.render('Marinero', True, self.color_white)
            self.refresh(2,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.noble_option.collidepoint((x,y)) and self.opened_screen == 1):
            if(self.personaje.id_trasfondo == None or (self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Noble")): #si no tenía acólito seleccionado o no había nada, se resetean los vínculos, defectos, etc
                self.personaje.vinculo = None
                self.personaje.defecto = None
                self.personaje.rasgo_personalidad = None
                self.personaje.ideal = None
                if(self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Acólito"):
                    self.ch4.play(self.error)
            self.personaje.id_trasfondo = ("Noble",10)
            self.ch1.play(self.pressed)
            content = self.fuente2.render('Noble', True, self.color_white)
            self.refresh(2,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.sabio_option.collidepoint((x,y)) and self.opened_screen == 1):
            if(self.personaje.id_trasfondo == None or (self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Sabio")): #si no tenía acólito seleccionado o no había nada, se resetean los vínculos, defectos, etc
                self.personaje.vinculo = None
                self.personaje.defecto = None
                self.personaje.rasgo_personalidad = None
                self.personaje.ideal = None
                if(self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Acólito"):
                    self.ch4.play(self.error)
            self.personaje.id_trasfondo = ("Sabio",11)
            self.ch1.play(self.pressed)
            content = self.fuente2.render('Sabio', True, self.color_white)
            self.refresh(2,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.soldado_option.collidepoint((x,y)) and self.opened_screen == 1):
            if(self.personaje.id_trasfondo == None or (self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Soldado")): #si no tenía acólito seleccionado o no había nada, se resetean los vínculos, defectos, etc
                self.personaje.vinculo = None
                self.personaje.defecto = None
                self.personaje.rasgo_personalidad = None
                self.personaje.ideal = None
                if(self.personaje.id_trasfondo != None and self.personaje.id_trasfondo[0] != "Acólito"):
                    self.ch4.play(self.error)
            self.personaje.id_trasfondo = ("Soldado",12)
            self.ch1.play(self.pressed)
            content = self.fuente2.render('Soldado', True, self.color_white)
            self.refresh(2,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        
        

        #vínculos
        elif(self.rect9.collidepoint((x,y)) and self.opened_screen == None):
            if(self.personaje.id_trasfondo != None):
                self.activeI = False
                self.ch1.play(self.pressed)
                self.opened_screen = 2
                self.screen.blit(pygame.transform.scale(self.screen_icons,  (self.width/1.0909, self.height/1.2727)), (self.width/24.0000, self.height/14.0000)) #1100 550 50 50
                pygame.draw.rect(self.screen,self.color_white, self.r2, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r3, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r4, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r5, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r6, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r7, 3)
                self.d1 = self.fuente5.render(self.vinculos[self.personaje.id_trasfondo[1]][0][1], True, self.color_white)
                self.screen.blit(self.d1,(self.width/13.3333, self.height/4.2683)) #90 164
                self.d2 = self.fuente5.render(self.vinculos[self.personaje.id_trasfondo[1]][1][1], True, self.color_white)
                self.screen.blit(self.d2,(self.width/13.3333, self.height/3.1390)) #90 223
                self.d3 = self.fuente5.render(self.vinculos[self.personaje.id_trasfondo[1]][2][1], True, self.color_white)
                self.screen.blit(self.d3,(self.width/13.3333, self.height/2.4823)) #90 282
                self.d4 = self.fuente5.render(self.vinculos[self.personaje.id_trasfondo[1]][3][1], True, self.color_white)
                self.screen.blit(self.d4,(self.width/13.3333, self.height/2.0528)) #90 341
                self.d5 = self.fuente5.render(self.vinculos[self.personaje.id_trasfondo[1]][4][1], True, self.color_white)
                self.screen.blit(self.d5,(self.width/13.3333, self.height/1.7500)) #90 400
                self.d6 = self.fuente5.render(self.vinculos[self.personaje.id_trasfondo[1]][5][1], True, self.color_white)
                self.screen.blit(self.d6,(self.width/13.3333, self.height/1.5251)) #90 459
                pygame.display.update() 
            else:
                self.ch1.play(self.error)
            return 'seleccionPersonaje'
        #defectos
        elif(self.rect10.collidepoint((x,y)) and self.opened_screen == None):
            if(self.personaje.id_trasfondo != None):
                self.activeI = False
                self.ch1.play(self.pressed)
                self.opened_screen = 3
                #El defecto 42 es el texto más largo -> Forastero último posible defecto
                self.screen.blit(pygame.transform.scale(self.screen_icons,  (self.width/1.0909, self.height/1.2727)), (self.width/24.0000, self.height/14.0000)) #1100 550 50 50
                pygame.draw.rect(self.screen,self.color_white, self.r2, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r3, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r4, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r5, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r6, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r7, 3)
                self.d1 = self.fuente5.render(self.defectos[self.personaje.id_trasfondo[1]][0][1], True, self.color_white)
                self.screen.blit(self.d1,(self.width/13.3333, self.height/4.2683)) #90 164
                self.d2 = self.fuente5.render(self.defectos[self.personaje.id_trasfondo[1]][1][1], True, self.color_white)
                self.screen.blit(self.d2,(self.width/13.3333, self.height/3.1390)) #90 223
                self.d3 = self.fuente5.render(self.defectos[self.personaje.id_trasfondo[1]][2][1], True, self.color_white)
                self.screen.blit(self.d3,(self.width/13.3333, self.height/2.4823)) #90 282
                self.d4 = self.fuente5.render(self.defectos[self.personaje.id_trasfondo[1]][3][1], True, self.color_white)
                self.screen.blit(self.d4,(self.width/13.3333, self.height/2.0528)) #90 341
                self.d5 = self.fuente5.render(self.defectos[self.personaje.id_trasfondo[1]][4][1], True, self.color_white)
                self.screen.blit(self.d5,(self.width/13.3333, self.height/1.7500)) #90 400
                self.d6 = self.fuente5.render(self.defectos[self.personaje.id_trasfondo[1]][5][1], True, self.color_white)
                self.screen.blit(self.d6,(self.width/13.3333, self.height/1.5251)) #90 459

                pygame.display.update() 
            else:
                self.ch1.play(self.error)
            return 'seleccionPersonaje'
        #rasgos
        elif(self.rect11.collidepoint((x,y)) and self.opened_screen == None):
            if(self.personaje.id_trasfondo != None):
                self.activeI = False
                self.ch1.play(self.pressed)
                self.opened_screen = 4
                self.screen.blit(pygame.transform.scale(self.screen_icons,  (self.width/1.0909, self.height/1.2727)), (self.width/24.0000, self.height/14.0000)) #1100 550 50 50
                pygame.draw.rect(self.screen,self.color_white, self.r1, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r2, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r3, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r4, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r5, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r6, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r7, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r8, 3)
                self.d0 = self.fuente5.render(self.rasgos_personalidad[self.personaje.id_trasfondo[1]][0][1], True, self.color_white)
                self.screen.blit(self.d0,(self.width/13.3333, self.height/6.6667)) #90 105
                self.d1 = self.fuente5.render(self.rasgos_personalidad[self.personaje.id_trasfondo[1]][1][1], True, self.color_white)
                self.screen.blit(self.d1,(self.width/13.3333, self.height/4.2683)) #90 164
                self.d2 = self.fuente5.render(self.rasgos_personalidad[self.personaje.id_trasfondo[1]][2][1], True, self.color_white)
                self.screen.blit(self.d2,(self.width/13.3333, self.height/3.1390)) #90 223
                self.d3 = self.fuente5.render(self.rasgos_personalidad[self.personaje.id_trasfondo[1]][3][1], True, self.color_white)
                self.screen.blit(self.d3,(self.width/13.3333, self.height/2.4823)) #90 282
                self.d4 = self.fuente5.render(self.rasgos_personalidad[self.personaje.id_trasfondo[1]][4][1], True, self.color_white)
                self.screen.blit(self.d4,(self.width/13.3333, self.height/2.0528)) #90 341
                self.d5 = self.fuente5.render(self.rasgos_personalidad[self.personaje.id_trasfondo[1]][5][1], True, self.color_white)
                self.screen.blit(self.d5,(self.width/13.3333, self.height/1.7500)) #90 400
                self.d6 = self.fuente5.render(self.rasgos_personalidad[self.personaje.id_trasfondo[1]][6][1], True, self.color_white)
                self.screen.blit(self.d6,(self.width/13.3333, self.height/1.5251)) #90 459
                self.d7 = self.fuente5.render(self.rasgos_personalidad[self.personaje.id_trasfondo[1]][7][1], True, self.color_white)
                self.screen.blit(self.d7,(self.width/13.3333, self.height/1.3514)) #90 518
                pygame.display.update() 
            else:
                self.ch1.play(self.error)
            return 'seleccionPersonaje'
        #ideales
        elif(self.rect12.collidepoint((x,y)) and self.opened_screen == None):
            if(self.personaje.id_trasfondo != None):
                self.activeI = False
                self.ch1.play(self.pressed)
                self.opened_screen = 5
                self.screen.blit(pygame.transform.scale(self.screen_icons,  (self.width/1.0909, self.height/1.2727)), (self.width/24.0000, self.height/14.0000)) #1100 550 50 50
                pygame.draw.rect(self.screen,self.color_white, self.r2, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r3, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r4, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r5, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r6, 3)
                pygame.draw.rect(self.screen,self.color_white, self.r7, 3)
                self.d1 = self.fuente5.render(self.ideales[self.personaje.id_trasfondo[1]][0][1], True, self.color_white)
                self.screen.blit(self.d1,(self.width/13.3333, self.height/4.2683)) #90 164
                self.d2 = self.fuente5.render(self.ideales[self.personaje.id_trasfondo[1]][1][1], True, self.color_white)
                self.screen.blit(self.d2,(self.width/13.3333, self.height/3.1390)) #90 223
                self.d3 = self.fuente5.render(self.ideales[self.personaje.id_trasfondo[1]][2][1], True, self.color_white)
                self.screen.blit(self.d3,(self.width/13.3333, self.height/2.4823)) #90 282
                self.d4 = self.fuente5.render(self.ideales[self.personaje.id_trasfondo[1]][3][1], True, self.color_white)
                self.screen.blit(self.d4,(self.width/13.3333, self.height/2.0528)) #90 341
                self.d5 = self.fuente5.render(self.ideales[self.personaje.id_trasfondo[1]][4][1], True, self.color_white)
                self.screen.blit(self.d5,(self.width/13.3333, self.height/1.7500)) #90 400
                self.d6 = self.fuente5.render(self.ideales[self.personaje.id_trasfondo[1]][5][1], True, self.color_white)
                self.screen.blit(self.d6,(self.width/13.3333, self.height/1.5251)) #90 459
                pygame.display.update() 
            else:
                self.ch1.play(self.error)
            return 'seleccionPersonaje'
        
        elif(self.r1.collidepoint((x,y)) and self.opened_screen == 4):
            self.personaje.rasgo_personalidad = (self.rasgos_personalidad[self.personaje.id_trasfondo[1]][0][1],1)
            self.ch1.play(self.pressed)
            content = self.fuente2.render('Rasgo Seleccionado: (1)', True, self.color_white)
            self.refresh(5,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.r2.collidepoint((x,y)) and self.opened_screen != None and self.opened_screen >=2 and self.opened_screen<=5):
            if(self.opened_screen == 2):
                self.personaje.vinculo = (self.vinculos[self.personaje.id_trasfondo[1]][0][1],1)
                text = "Vínculo Seleccionado: (1)"
                op = 3
            elif(self.opened_screen == 3):
                self.personaje.defecto = (self.defectos[self.personaje.id_trasfondo[1]][0][1],1)
                text = "Defecto Seleccionado: (1)"
                op = 4
            elif(self.opened_screen == 4):
                self.personaje.rasgo_personalidad = (self.rasgos_personalidad[self.personaje.id_trasfondo[1]][1][1],2)
                text = "Rasgo Seleccionado: (2)"
                op = 5
            else:
                self.personaje.ideal = (self.ideales[self.personaje.id_trasfondo[1]][0][1],1)
                text = "Ideal Seleccionado: (1)"
                op = 6
            self.ch1.play(self.pressed)
            content = self.fuente2.render(text, True, self.color_white)
            self.refresh(op,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.r3.collidepoint((x,y)) and self.opened_screen != None and self.opened_screen >=2 and self.opened_screen<=5):
            if(self.opened_screen == 2):
                self.personaje.vinculo = (self.vinculos[self.personaje.id_trasfondo[1]][1][1],2)
                text = "Vínculo Seleccionado: (2)"
                op = 3
            elif(self.opened_screen == 3):
                self.personaje.defecto = (self.defectos[self.personaje.id_trasfondo[1]][1][1],2)
                text = "Defecto Seleccionado: (2)"
                op = 4
            elif(self.opened_screen == 4):
                self.personaje.rasgo_personalidad = (self.rasgos_personalidad[self.personaje.id_trasfondo[1]][2][1],3)
                text = "Rasgo Seleccionado: (3)"
                op = 5
            else:
                self.personaje.ideal = (self.ideales[self.personaje.id_trasfondo[1]][1][1],2)
                text = "Ideal Seleccionado: (2)"
                op = 6
            self.ch1.play(self.pressed)
            content = self.fuente2.render(text, True, self.color_white)
            self.refresh(op,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.r4.collidepoint((x,y)) and self.opened_screen != None and self.opened_screen >=2 and self.opened_screen<=5):
            if(self.opened_screen == 2):
                self.personaje.vinculo = (self.vinculos[self.personaje.id_trasfondo[1]][2][1],3)
                text = "Vínculo Seleccionado: (3)"
                op = 3
            elif(self.opened_screen == 3):
                self.personaje.defecto = (self.defectos[self.personaje.id_trasfondo[1]][2][1],3)
                text = "Defecto Seleccionado: (3)"
                op = 4
            elif(self.opened_screen == 4):
                self.personaje.rasgo_personalidad = (self.rasgos_personalidad[self.personaje.id_trasfondo[1]][3][1],4)
                text = "Rasgo Seleccionado: (4)"
                op = 5
            else:
                self.personaje.ideal = (self.ideales[self.personaje.id_trasfondo[1]][2][1],3)
                text = "Ideal Seleccionado: (3)"
                op = 6
            self.ch1.play(self.pressed)
            content = self.fuente2.render(text, True, self.color_white)
            self.refresh(op,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.r5.collidepoint((x,y)) and self.opened_screen != None and self.opened_screen >=2 and self.opened_screen<=5):
            if(self.opened_screen == 2):
                self.personaje.vinculo = (self.vinculos[self.personaje.id_trasfondo[1]][3][1],4)
                text = "Vínculo Seleccionado: (4)"
                op = 3
            elif(self.opened_screen == 3):
                self.personaje.defecto = (self.defectos[self.personaje.id_trasfondo[1]][3][1],4)
                text = "Defecto Seleccionado: (4)"
                op = 4
            elif(self.opened_screen == 4):
                self.personaje.rasgo_personalidad = (self.rasgos_personalidad[self.personaje.id_trasfondo[1]][4][1],5)
                text = "Rasgo Seleccionado: (5)"
                op = 5
            else:
                self.personaje.ideal = (self.ideales[self.personaje.id_trasfondo[1]][3][1],4)
                text = "Ideal Seleccionado: (4)"
                op = 6
            self.ch1.play(self.pressed)
            content = self.fuente2.render(text, True, self.color_white)
            self.refresh(op,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.r6.collidepoint((x,y)) and self.opened_screen != None and self.opened_screen >=2 and self.opened_screen<=5):
            if(self.opened_screen == 2):
                self.personaje.vinculo = (self.vinculos[self.personaje.id_trasfondo[1]][4][1],5)
                text = "Vínculo Seleccionado: (5)"
                op = 3
            elif(self.opened_screen == 3):
                self.personaje.defecto = (self.defectos[self.personaje.id_trasfondo[1]][4][1],5)
                text = "Defecto Seleccionado: (5)"
                op = 4
            elif(self.opened_screen == 4):
                self.personaje.rasgo_personalidad = (self.rasgos_personalidad[self.personaje.id_trasfondo[1]][5][1],6)
                text = "Rasgo Seleccionado: (6)"
                op = 5
            else:
                self.personaje.ideal = (self.ideales[self.personaje.id_trasfondo[1]][4][1],5)
                text = "Ideal Seleccionado: (5)"
                op = 6
            self.ch1.play(self.pressed)
            content = self.fuente2.render(text, True, self.color_white)
            self.refresh(op,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.r7.collidepoint((x,y)) and self.opened_screen != None and self.opened_screen >=2 and self.opened_screen<=5):
            if(self.opened_screen == 2):
                self.personaje.vinculo = (self.vinculos[self.personaje.id_trasfondo[1]][5][1],6)
                text = "Vínculo Seleccionado: (6)"
                op = 3
            elif(self.opened_screen == 3):
                self.personaje.defecto = (self.defectos[self.personaje.id_trasfondo[1]][5][1],6)
                text = "Defecto Seleccionado: (6)"
                op = 4
            elif(self.opened_screen == 4):
                self.personaje.rasgo_personalidad = (self.rasgos_personalidad[self.personaje.id_trasfondo[1]][6][1],7)
                text = "Rasgo Seleccionado: (7)"
                op = 5
            else:
                self.personaje.ideal = (self.ideales[self.personaje.id_trasfondo[1]][5][1],6)
                text = "Ideal Seleccionado: (6)"
                op = 6
            self.ch1.play(self.pressed)
            content = self.fuente2.render(text, True, self.color_white)
            self.refresh(op,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        elif(self.r8.collidepoint((x,y)) and self.opened_screen == 4):
            self.personaje.rasgo_personalidad = (self.rasgos_personalidad[self.personaje.id_trasfondo[1]][7][1],7)
            self.ch1.play(self.pressed)
            content = self.fuente2.render('Rasgo Seleccionado: (8)', True, self.color_white)
            self.refresh(5,content)
            self.opened_screen = None
            pygame.display.update() 
            return 'seleccionPersonaje'
        else:
            self.activeI = False
            self.opened_screen = None #TODO: Check si hay pantallas de raza o clase abiertas
            if(self.personaje.name == ' '):
                self.textName = self.defaultTextName
            else:
                self.textName = self.fuente2.render(self.personaje.name, True, self.color_white)
            self.screen.blit(self.textName,(self.width/3.2520, self.height/12.7273)) #369 55
            self.refresh(0,None)
            pygame.display.update() 
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
        x_sizeR = self.width/5.0000
        y_sizeR = self.height/1.9444
        x_startR = self.width/8.5714
        y_startR = self.height/3.5000
        x_sizeIB = self.width/5.2632
        y_sizeIB = self.height/2.1875
        x_startIB = self.width/10.0000
        y_startIB = self.height/5.0000
        x_startIE = ((self.width/10.0000) + ((self.width/7.7922)*2))
        x_sizeC = self.width/8.0000
        y_sizeC = self.height/4.6667
        x_startC = self.width/2.8571
        y_startC = self.height/3.5000
        (x,y) = pygame.mouse.get_pos()

        #Botón seguir con la ficha
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            if(self.personaje.name != None and self.personaje.name != ' ' and self.personaje.id_trasfondo != None and self.personaje.tipo_raza != None and self.personaje.tipo_clase != None and self.personaje.vinculo != None and self.personaje.defecto != None and self.personaje.rasgo_personalidad != None and self.personaje.ideal != None):
                self.screen.blit(pygame.transform.scale(self.bCreate_selected, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            if(self.opened_screen != 6 and self.opened_screen != 7 and self.opened_screen != 2 and self.opened_screen != 3 and self.opened_screen != 4 and self.opened_screen != 5):
                if(self.personaje.tipo_raza == None):
                    self.screen.blit(pygame.transform.scale(self.defaultIconRaza, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
                    self.screen.blit(self.defaultRaza,(self.width/5.1502, self.height/2.0000)) #233 350
                elif(self.personaje.tipo_raza == "Enano"):
                    self.screen.blit(pygame.transform.scale(self.icon_large_dwarf, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
                elif(self.personaje.tipo_raza == "Elfo"):
                    self.screen.blit(pygame.transform.scale(self.icon_large_elf, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
                if(self.personaje.tipo_clase == None):
                    self.screen.blit(pygame.transform.scale(self.default, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
                    self.screen.blit(self.defaultRaza,(self.width/2.5696, self.height/2.9167)) #467 240
                elif(self.personaje.tipo_clase == "Bárbaro"):
                    self.screen.blit(pygame.transform.scale(self.icon_barbarbarian, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
                elif(self.personaje.tipo_clase == "Explorador"):
                    self.screen.blit(pygame.transform.scale(self.icon_explorer, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
            if(self.first_timeCP):
                self.first_timeCP = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeB = True
                if(self.personaje.name != None and self.personaje.name != ' ' and self.personaje.id_trasfondo != None and self.personaje.tipo_raza != None and self.personaje.tipo_clase != None and self.personaje.vinculo != None and self.personaje.defecto != None and self.personaje.rasgo_personalidad != None and self.personaje.ideal != None):
                    self.ch2.play(self.selected)
            pygame.display.update() 

        #Botón volver al menú
        elif(self.checkIfMouseIsInButton(x_size,y_size,x_start2,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            if(self.personaje.name != None and self.personaje.name != ' ' and self.personaje.id_trasfondo != None and self.personaje.tipo_raza != None and self.personaje.tipo_clase != None and self.personaje.vinculo != None and self.personaje.defecto != None and self.personaje.rasgo_personalidad != None and self.personaje.ideal != None):
                self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            if(self.opened_screen != 6 and self.opened_screen != 7 and self.opened_screen != 2 and self.opened_screen != 3 and self.opened_screen != 4 and self.opened_screen != 5):
                if(self.personaje.tipo_raza == None):
                    self.screen.blit(pygame.transform.scale(self.defaultIconRaza, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
                    self.screen.blit(self.defaultRaza,(self.width/5.1502, self.height/2.0000)) #233 350
                elif(self.personaje.tipo_raza == "Enano"):
                    self.screen.blit(pygame.transform.scale(self.icon_large_dwarf, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
                elif(self.personaje.tipo_raza == "Elfo"):
                    self.screen.blit(pygame.transform.scale(self.icon_large_elf, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
                if(self.personaje.tipo_clase == None):
                    self.screen.blit(pygame.transform.scale(self.default, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
                    self.screen.blit(self.defaultRaza,(self.width/2.5696, self.height/2.9167)) #467 240
                elif(self.personaje.tipo_clase == "Bárbaro"):
                    self.screen.blit(pygame.transform.scale(self.icon_barbarbarian, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
                elif(self.personaje.tipo_clase == "Explorador"):
                    self.screen.blit(pygame.transform.scale(self.icon_explorer, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
            if(self.first_timeB):
                self.first_timeB = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch2.play(self.selected)     
            pygame.display.update() 

        #Raza
        elif(self.checkIfMouseIsInButton(x_sizeR,y_sizeR,x_startR,y_startR,x,y) and (self.opened_screen == None or self.opened_screen == 1)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            if(self.personaje.name != None and self.personaje.name != ' ' and self.personaje.id_trasfondo != None and self.personaje.tipo_raza != None and self.personaje.tipo_clase != None and self.personaje.vinculo != None and self.personaje.defecto != None and self.personaje.rasgo_personalidad != None and self.personaje.ideal != None):
                self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            if(self.personaje.tipo_raza == None):
                self.screen.blit(pygame.transform.scale(self.defaultIconRaza_selected, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
                self.screen.blit(self.defaultRaza,(self.width/5.1502, self.height/2.0000)) #233 350
            elif(self.personaje.tipo_raza == "Enano"):
                self.screen.blit(pygame.transform.scale(self.icon_large_dwarf_selected, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
            elif(self.personaje.tipo_raza == "Elfo"):
                self.screen.blit(pygame.transform.scale(self.icon_large_elf_selected, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
            if(self.personaje.tipo_clase == None):
                self.screen.blit(pygame.transform.scale(self.default, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
                self.screen.blit(self.defaultRaza,(self.width/2.5696, self.height/2.9167)) #467 240
            elif(self.personaje.tipo_clase == "Bárbaro"):
                self.screen.blit(pygame.transform.scale(self.icon_barbarbarian, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
            elif(self.personaje.tipo_clase == "Explorador"):
                self.screen.blit(pygame.transform.scale(self.icon_explorer, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
            if(self.first_timeR):
                self.first_timeR = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeB = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch2.play(self.selected) 
            pygame.display.update() 
            return 'seleccionPersonaje'
    
        #Icono de enano
        elif(self.checkIfMouseIsInButton(x_sizeIB,y_sizeIB,x_startIB,y_startIB,x,y) and self.opened_screen == 6):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            if(self.personaje.name != None and self.personaje.name != ' ' and self.personaje.id_trasfondo != None and self.personaje.tipo_raza != None and self.personaje.tipo_clase != None and self.personaje.vinculo != None and self.personaje.defecto != None and self.personaje.rasgo_personalidad != None and self.personaje.ideal != None):
                self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            self.screen.blit(pygame.transform.scale(self.icon_large_dwarf_selected, (self.width/5.2632, self.height/2.1875)), (self.width/10.0000, self.height/5.0000)) #114 160 120 
            self.screen.blit(pygame.transform.scale(self.icon_large_elf, (self.width/5.2632, self.height/2.1875)), (((self.width/10.0000) + ((self.width/7.7922)*2)), self.height/5.0000)) #114 160 
            if(self.first_timeR1):
                self.first_timeR1 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeB = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch2.play(self.selected) 
            pygame.display.update()
            return 'seleccionPersonaje'   
            
        #Icono de elfo
        elif(self.checkIfMouseIsInButton(x_sizeIB,y_sizeIB,x_startIE,y_startIB,x,y) and self.opened_screen == 6):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            if(self.personaje.name != None and self.personaje.name != ' ' and self.personaje.id_trasfondo != None and self.personaje.tipo_raza != None and self.personaje.tipo_clase != None and self.personaje.vinculo != None and self.personaje.defecto != None and self.personaje.rasgo_personalidad != None and self.personaje.ideal != None):
                self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            self.screen.blit(pygame.transform.scale(self.icon_large_dwarf, (self.width/5.2632, self.height/2.1875)), (self.width/10.0000, self.height/5.0000)) #114 160 120 
            self.screen.blit(pygame.transform.scale(self.icon_large_elf_selected, (self.width/5.2632, self.height/2.1875)), (((self.width/10.0000) + ((self.width/7.7922)*2)), self.height/5.0000)) #114 160 
            if(self.first_timeR2):
                self.first_timeR2 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeB = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch2.play(self.selected) 
            pygame.display.update()
            return 'seleccionPersonaje' 

        #Clase
        elif(self.checkIfMouseIsInButton(x_sizeC,y_sizeC,x_startC,y_startC,x,y) and (self.opened_screen == None or self.opened_screen == 1)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            if(self.personaje.name != None and self.personaje.name != ' ' and self.personaje.id_trasfondo != None and self.personaje.tipo_raza != None and self.personaje.tipo_clase != None and self.personaje.vinculo != None and self.personaje.defecto != None and self.personaje.rasgo_personalidad != None and self.personaje.ideal != None):
                self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            if(self.personaje.tipo_raza == None):
                self.screen.blit(pygame.transform.scale(self.defaultIconRaza, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
                self.screen.blit(self.defaultRaza,(self.width/5.1502, self.height/2.0000)) #233 350
            elif(self.personaje.tipo_raza == "Enano"):
                self.screen.blit(pygame.transform.scale(self.icon_large_dwarf, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
            elif(self.personaje.tipo_raza == "Elfo"):
                self.screen.blit(pygame.transform.scale(self.icon_large_elf, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
            if(self.personaje.tipo_clase == None):
                self.screen.blit(pygame.transform.scale(self.defaultSelected, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
                self.screen.blit(self.defaultRaza,(self.width/2.5696, self.height/2.9167)) #467 240
            elif(self.personaje.tipo_clase == "Bárbaro"):
                self.screen.blit(pygame.transform.scale(self.icon_barbarbarian_selected, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
            elif(self.personaje.tipo_clase == "Explorador"):
                self.screen.blit(pygame.transform.scale(self.icon_explorer_selected, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
            if(self.first_timeC):
                self.first_timeC = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeB = True
                self.first_timeR = True
                self.first_timeCP = True
                self.ch2.play(self.selected) 
            pygame.display.update() 
            return 'seleccionPersonaje'
        
        #Bárbaro
        elif(self.checkIfMouseIsInButton(x_sizeIB,x_sizeIB,x_startIB,y_startIB,x,y) and self.opened_screen == 7):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            if(self.personaje.name != None and self.personaje.name != ' ' and self.personaje.id_trasfondo != None and self.personaje.tipo_raza != None and self.personaje.tipo_clase != None and self.personaje.vinculo != None and self.personaje.defecto != None and self.personaje.rasgo_personalidad != None and self.personaje.ideal != None):
                self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            self.screen.blit(pygame.transform.scale(self.icon_barbarbarian_selected, (self.width/5.2632, self.width/5.2632)), (self.width/10.0000, self.height/5.0000)) #114 228 120 140
            self.screen.blit(pygame.transform.scale(self.icon_explorer, (self.width/5.2632, self.width/5.2632)), (((self.width/10.0000) + ((self.width/7.7922)*2)), self.height/5.0000)) #114 160 
            if(self.first_timeC1):
                self.first_timeC1 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeR = True
                self.first_timeC2 = True
                self.first_timeB = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch2.play(self.selected) 
            pygame.display.update()
            return 'seleccionPersonaje' 
        #Explorador
        elif(self.checkIfMouseIsInButton(x_sizeIB,x_sizeIB,x_startIE,y_startIB,x,y) and self.opened_screen == 7):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            if(self.personaje.name != None and self.personaje.name != ' ' and self.personaje.id_trasfondo != None and self.personaje.tipo_raza != None and self.personaje.tipo_clase != None and self.personaje.vinculo != None and self.personaje.defecto != None and self.personaje.rasgo_personalidad != None and self.personaje.ideal != None):
                self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            self.screen.blit(pygame.transform.scale(self.icon_barbarbarian, (self.width/5.2632, self.width/5.2632)), (self.width/10.0000, self.height/5.0000)) #114 228 120 140
            self.screen.blit(pygame.transform.scale(self.icon_explorer_selected, (self.width/5.2632, self.width/5.2632)), (((self.width/10.0000) + ((self.width/7.7922)*2)), self.height/5.0000)) #114 160 
            if(self.first_timeC2):
                self.first_timeC2 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeR = True
                self.first_timeB = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch2.play(self.selected) 
            pygame.display.update()
            return 'seleccionPersonaje' 

        elif(self.acolito_option.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Acólito")
            if(self.first_time1):
                self.first_time1 = False
                self.first_timeB = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch3.play(self.selected)    
            pygame.display.update() 

        elif(self.artesano_option.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Artesano Gremial")
            if(self.first_time2):
                self.first_time2 = False
                self.first_time1 = True 
                self.first_timeB = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch4.play(self.selected) 
            pygame.display.update() 

        elif(self.artista_option.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Artista")
            if(self.first_time3):
                self.first_time3 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_timeB = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch2.play(self.selected) 
            pygame.display.update() 

        elif(self.charlatan_option.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Charlatán")
            if(self.first_time4):
                self.first_time4 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_timeB = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch3.play(self.selected) 
            pygame.display.update() 

        elif(self.criminal_option.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Criminal")
            if(self.first_time5):
                self.first_time5 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_timeB = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch4.play(self.selected) 
            pygame.display.update() 

        elif(self.ermitano_option.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Ermitaño")
            if(self.first_time6):
                self.first_time6 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_timeB = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch2.play(self.selected) 
            pygame.display.update() 

        elif(self.forastero_option.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Forastero")
            if(self.first_time7):
                self.first_time7 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_timeB = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch3.play(self.selected) 
            pygame.display.update() 

        elif(self.heroe_option.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Héroe del pueblo")
            if(self.first_time8):
                self.first_time8 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_timeB = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch4.play(self.selected) 
            pygame.display.update() 

        elif(self.huerfano_option.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Huérfano")
            if(self.first_time9):
                self.first_time9 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_timeB = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch2.play(self.selected) 
            pygame.display.update() 

        elif(self.marinero_option.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Marinero")
            if(self.first_time10):
                self.first_time10 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_timeB = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch3.play(self.selected) 
            pygame.display.update() 

        elif(self.noble_option.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Noble")
            if(self.first_time11):
                self.first_time11 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_timeB = True
                self.first_time12 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch4.play(self.selected) 
            pygame.display.update() 

        elif(self.sabio_option.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Sabio")
            if(self.first_time12):
                self.first_time12 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_timeB = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch2.play(self.selected) 
            pygame.display.update() 

        elif(self.soldado_option.collidepoint((x,y)) and self.opened_screen == 1):
            self.select_option("Soldado")
            if(self.first_time13):
                self.first_time13 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_timeB = True
                self.first_timed0 = True
                self.first_timed1 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch3.play(self.selected) 
            pygame.display.update() 

        elif(self.r1.collidepoint((x,y)) and self.opened_screen == 4): #este rectángulo solo aparece en rasgos de personalidad
            pygame.draw.rect(self.screen,self.color_magenta, self.r1, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r1, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r2, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r2, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r3, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r3, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r4, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r4, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r5, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r5, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r6, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r6, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r7, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r7, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r8, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r8, 3)
            self.screen.blit(self.d0,(self.width/13.3333, self.height/6.6667)) #90 105
            self.screen.blit(self.d1,(self.width/13.3333, self.height/4.2683)) #90 164
            self.screen.blit(self.d2,(self.width/13.3333, self.height/3.1390)) #90 223
            self.screen.blit(self.d3,(self.width/13.3333, self.height/2.4823)) #90 282
            self.screen.blit(self.d4,(self.width/13.3333, self.height/2.0528)) #90 341
            self.screen.blit(self.d5,(self.width/13.3333, self.height/1.7500)) #90 400
            self.screen.blit(self.d6,(self.width/13.3333, self.height/1.5251)) #90 459
            self.screen.blit(self.d7,(self.width/13.3333, self.height/1.3514)) #90 518

            if(self.first_timed0):
                self.first_timed0 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_timeB = True
                self.first_timed1 = True
                self.first_time13 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch3.play(self.selected) 
            pygame.display.update() 

        elif(self.r8.collidepoint((x,y)) and self.opened_screen == 4): #este rectángulo solo aparece en rasgos de personalidad
            pygame.draw.rect(self.screen,self.color_black, self.r1, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r1, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r2, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r2, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r3, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r3, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r4, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r4, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r5, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r5, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r6, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r6, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r7, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r7, 3)
            pygame.draw.rect(self.screen,self.color_magenta, self.r8, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r8, 3)
            self.screen.blit(self.d0,(self.width/13.3333, self.height/6.6667)) #90 105
            self.screen.blit(self.d1,(self.width/13.3333, self.height/4.2683)) #90 164
            self.screen.blit(self.d2,(self.width/13.3333, self.height/3.1390)) #90 223
            self.screen.blit(self.d3,(self.width/13.3333, self.height/2.4823)) #90 282
            self.screen.blit(self.d4,(self.width/13.3333, self.height/2.0528)) #90 341
            self.screen.blit(self.d5,(self.width/13.3333, self.height/1.7500)) #90 400
            self.screen.blit(self.d6,(self.width/13.3333, self.height/1.5251)) #90 459
            self.screen.blit(self.d7,(self.width/13.3333, self.height/1.3514)) #90 518
            if(self.first_timed7):
                self.first_timed7 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_timeB = True
                self.first_timed1 = True
                self.first_time13 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed0 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch3.play(self.selected) 
            pygame.display.update() 
        elif(self.r2.collidepoint((x,y)) and self.opened_screen != None and self.opened_screen>=2 and self.opened_screen<=5): 
            pygame.draw.rect(self.screen,self.color_magenta, self.r2, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r2, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r3, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r3, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r4, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r4, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r5, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r5, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r6, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r6, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r7, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r7, 3)
            self.screen.blit(self.d1,(self.width/13.3333, self.height/4.2683)) #90 164
            self.screen.blit(self.d2,(self.width/13.3333, self.height/3.1390)) #90 223
            self.screen.blit(self.d3,(self.width/13.3333, self.height/2.4823)) #90 282
            self.screen.blit(self.d4,(self.width/13.3333, self.height/2.0528)) #90 341
            self.screen.blit(self.d5,(self.width/13.3333, self.height/1.7500)) #90 400
            self.screen.blit(self.d6,(self.width/13.3333, self.height/1.5251)) #90 459

            if(self.opened_screen == 4):
                pygame.draw.rect(self.screen,self.color_black, self.r1, 0)
                pygame.draw.rect(self.screen,self.color_white, self.r1, 3)
                pygame.draw.rect(self.screen,self.color_black, self.r8, 0)
                pygame.draw.rect(self.screen,self.color_white, self.r8, 3)
                self.screen.blit(self.d0,(self.width/13.3333, self.height/6.6667)) #90 105
                self.screen.blit(self.d7,(self.width/13.3333, self.height/1.3514)) #90 518

            if(self.first_timed1):
                self.first_timed1 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_timeB = True
                self.first_timed0 = True
                self.first_time13 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch3.play(self.selected) 
            pygame.display.update() 
        elif(self.r3.collidepoint((x,y)) and self.opened_screen != None and self.opened_screen>=2 and self.opened_screen<=5): 
            pygame.draw.rect(self.screen,self.color_black, self.r2, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r2, 3)
            pygame.draw.rect(self.screen,self.color_magenta, self.r3, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r3, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r4, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r4, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r5, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r5, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r6, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r6, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r7, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r7, 3)
            self.screen.blit(self.d1,(self.width/13.3333, self.height/4.2683)) #90 164
            self.screen.blit(self.d2,(self.width/13.3333, self.height/3.1390)) #90 223
            self.screen.blit(self.d3,(self.width/13.3333, self.height/2.4823)) #90 282
            self.screen.blit(self.d4,(self.width/13.3333, self.height/2.0528)) #90 341
            self.screen.blit(self.d5,(self.width/13.3333, self.height/1.7500)) #90 400
            self.screen.blit(self.d6,(self.width/13.3333, self.height/1.5251)) #90 459

            if(self.opened_screen == 4):
                pygame.draw.rect(self.screen,self.color_black, self.r1, 0)
                pygame.draw.rect(self.screen,self.color_white, self.r1, 3)
                pygame.draw.rect(self.screen,self.color_black, self.r8, 0)
                pygame.draw.rect(self.screen,self.color_white, self.r8, 3)
                self.screen.blit(self.d0,(self.width/13.3333, self.height/6.6667)) #90 105
                self.screen.blit(self.d7,(self.width/13.3333, self.height/1.3514)) #90 518
            if(self.first_timed2):
                self.first_timed2 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_timeB = True
                self.first_timed1 = True
                self.first_time13 = True
                self.first_timed0 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch3.play(self.selected) 
            pygame.display.update() 
        elif(self.r4.collidepoint((x,y)) and self.opened_screen != None and self.opened_screen>=2 and self.opened_screen<=5): 
            pygame.draw.rect(self.screen,self.color_black, self.r2, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r2, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r3, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r3, 3)
            pygame.draw.rect(self.screen,self.color_magenta, self.r4, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r4, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r5, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r5, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r6, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r6, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r7, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r7, 3)
            self.screen.blit(self.d1,(self.width/13.3333, self.height/4.2683)) #90 164
            self.screen.blit(self.d2,(self.width/13.3333, self.height/3.1390)) #90 223
            self.screen.blit(self.d3,(self.width/13.3333, self.height/2.4823)) #90 282
            self.screen.blit(self.d4,(self.width/13.3333, self.height/2.0528)) #90 341
            self.screen.blit(self.d5,(self.width/13.3333, self.height/1.7500)) #90 400
            self.screen.blit(self.d6,(self.width/13.3333, self.height/1.5251)) #90 459

            if(self.opened_screen == 4):
                pygame.draw.rect(self.screen,self.color_black, self.r1, 0)
                pygame.draw.rect(self.screen,self.color_white, self.r1, 3)
                pygame.draw.rect(self.screen,self.color_black, self.r8, 0)
                pygame.draw.rect(self.screen,self.color_white, self.r8, 3)
                self.screen.blit(self.d0,(self.width/13.3333, self.height/6.6667)) #90 105
                self.screen.blit(self.d7,(self.width/13.3333, self.height/1.3514)) #90 518
            if(self.first_timed3):
                self.first_timed3 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_timeB = True
                self.first_timed1 = True
                self.first_time13 = True
                self.first_timed2 = True
                self.first_timed0 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch3.play(self.selected) 
            pygame.display.update() 
        elif(self.r5.collidepoint((x,y)) and self.opened_screen != None and self.opened_screen>=2 and self.opened_screen<=5): 
            pygame.draw.rect(self.screen,self.color_black, self.r2, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r2, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r3, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r3, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r4, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r4, 3)
            pygame.draw.rect(self.screen,self.color_magenta, self.r5, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r5, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r6, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r6, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r7, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r7, 3)
            self.screen.blit(self.d1,(self.width/13.3333, self.height/4.2683)) #90 164
            self.screen.blit(self.d2,(self.width/13.3333, self.height/3.1390)) #90 223
            self.screen.blit(self.d3,(self.width/13.3333, self.height/2.4823)) #90 282
            self.screen.blit(self.d4,(self.width/13.3333, self.height/2.0528)) #90 341
            self.screen.blit(self.d5,(self.width/13.3333, self.height/1.7500)) #90 400
            self.screen.blit(self.d6,(self.width/13.3333, self.height/1.5251)) #90 459

            if(self.opened_screen == 4):
                pygame.draw.rect(self.screen,self.color_black, self.r1, 0)
                pygame.draw.rect(self.screen,self.color_white, self.r1, 3)
                pygame.draw.rect(self.screen,self.color_black, self.r8, 0)
                pygame.draw.rect(self.screen,self.color_white, self.r8, 3)
                self.screen.blit(self.d0,(self.width/13.3333, self.height/6.6667)) #90 105
                self.screen.blit(self.d7,(self.width/13.3333, self.height/1.3514)) #90 518
            if(self.first_timed4):
                self.first_timed4 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_timeB = True
                self.first_timed1 = True
                self.first_time13 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed0 = True
                self.first_timed5 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch3.play(self.selected) 
            pygame.display.update() 
        elif(self.r6.collidepoint((x,y)) and self.opened_screen != None and self.opened_screen>=2 and self.opened_screen<=5): 
            pygame.draw.rect(self.screen,self.color_black, self.r2, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r2, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r3, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r3, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r4, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r4, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r5, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r5, 3)
            pygame.draw.rect(self.screen,self.color_magenta, self.r6, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r6, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r7, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r7, 3)
            self.screen.blit(self.d1,(self.width/13.3333, self.height/4.2683)) #90 164
            self.screen.blit(self.d2,(self.width/13.3333, self.height/3.1390)) #90 223
            self.screen.blit(self.d3,(self.width/13.3333, self.height/2.4823)) #90 282
            self.screen.blit(self.d4,(self.width/13.3333, self.height/2.0528)) #90 341
            self.screen.blit(self.d5,(self.width/13.3333, self.height/1.7500)) #90 400
            self.screen.blit(self.d6,(self.width/13.3333, self.height/1.5251)) #90 459

            if(self.opened_screen == 4):
                pygame.draw.rect(self.screen,self.color_black, self.r1, 0)
                pygame.draw.rect(self.screen,self.color_white, self.r1, 3)
                pygame.draw.rect(self.screen,self.color_black, self.r8, 0)
                pygame.draw.rect(self.screen,self.color_white, self.r8, 3)
                self.screen.blit(self.d0,(self.width/13.3333, self.height/6.6667)) #90 105
                self.screen.blit(self.d7,(self.width/13.3333, self.height/1.3514)) #90 518
            if(self.first_timed5):
                self.first_timed5 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_timeB = True
                self.first_timed1 = True
                self.first_time13 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed0 = True
                self.first_timed6 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch3.play(self.selected) 
            pygame.display.update() 
        elif(self.r7.collidepoint((x,y)) and self.opened_screen != None and self.opened_screen>=2 and self.opened_screen<=5): 
            pygame.draw.rect(self.screen,self.color_black, self.r2, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r2, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r3, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r3, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r4, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r4, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r5, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r5, 3)
            pygame.draw.rect(self.screen,self.color_black, self.r6, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r6, 3)
            pygame.draw.rect(self.screen,self.color_magenta, self.r7, 0)
            pygame.draw.rect(self.screen,self.color_white, self.r7, 3)
            self.screen.blit(self.d1,(self.width/13.3333, self.height/4.2683)) #90 164
            self.screen.blit(self.d2,(self.width/13.3333, self.height/3.1390)) #90 223
            self.screen.blit(self.d3,(self.width/13.3333, self.height/2.4823)) #90 282
            self.screen.blit(self.d4,(self.width/13.3333, self.height/2.0528)) #90 341
            self.screen.blit(self.d5,(self.width/13.3333, self.height/1.7500)) #90 400
            self.screen.blit(self.d6,(self.width/13.3333, self.height/1.5251)) #90 459

            if(self.opened_screen == 4):
                pygame.draw.rect(self.screen,self.color_black, self.r1, 0)
                pygame.draw.rect(self.screen,self.color_white, self.r1, 3)
                pygame.draw.rect(self.screen,self.color_black, self.r8, 0)
                pygame.draw.rect(self.screen,self.color_white, self.r8, 3)
                self.screen.blit(self.d0,(self.width/13.3333, self.height/6.6667)) #90 105
                self.screen.blit(self.d7,(self.width/13.3333, self.height/1.3514)) #90 518
            if(self.first_timed6):
                self.first_timed6 = False
                self.first_time1 = True 
                self.first_time2 = True
                self.first_time3 = True
                self.first_time4 = True
                self.first_time5 = True
                self.first_time6 = True
                self.first_time7 = True
                self.first_time8 = True
                self.first_time9 = True
                self.first_time10 = True
                self.first_time11 = True
                self.first_time12 = True
                self.first_timeB = True
                self.first_timed1 = True
                self.first_time13 = True
                self.first_timed2 = True
                self.first_timed3 = True
                self.first_timed4 = True
                self.first_timed5 = True
                self.first_timed0 = True
                self.first_timed7 = True
                self.first_timeR1 = True
                self.first_timeR2 = True
                self.first_timeC1 = True
                self.first_timeC2 = True
                self.first_timeR = True
                self.first_timeC = True
                self.first_timeCP = True
                self.ch3.play(self.selected) 
            pygame.display.update() 

        else:
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
            self.first_time10 = True
            self.first_time11 = True
            self.first_time12 = True
            self.first_time13 = True
            self.first_timed0 = True
            self.first_timed1 = True
            self.first_timed2 = True
            self.first_timed3 = True
            self.first_timed4 = True
            self.first_timed5 = True
            self.first_timed6 = True
            self.first_timed7 = True
            self.first_timeR1 = True
            self.first_timeR2 = True
            self.first_timeC1 = True
            self.first_timeC2 = True
            self.first_timeR = True
            self.first_timeC = True
            self.first_timeCP = True
            if(self.opened_screen == 1):
                self.select_option("default")
                if(self.personaje.tipo_raza == None):
                    self.screen.blit(pygame.transform.scale(self.defaultIconRaza, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
                    self.screen.blit(self.defaultRaza,(self.width/5.1502, self.height/2.0000)) #233 350
                elif(self.personaje.tipo_raza == "Enano"):
                    self.screen.blit(pygame.transform.scale(self.icon_large_dwarf, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
                elif(self.personaje.tipo_raza == "Elfo"):
                    self.screen.blit(pygame.transform.scale(self.icon_large_elf, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
                if(self.personaje.tipo_clase == None):
                    self.screen.blit(pygame.transform.scale(self.default, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
                    self.screen.blit(self.defaultRaza,(self.width/2.5696, self.height/2.9167)) #467 240
                elif(self.personaje.tipo_clase == "Bárbaro"):
                    self.screen.blit(pygame.transform.scale(self.icon_barbarbarian, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
                elif(self.personaje.tipo_clase == "Explorador"):
                    self.screen.blit(pygame.transform.scale(self.icon_explorer, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
            elif(self.opened_screen != None and self.opened_screen >=2 and self.opened_screen <=5):
                pygame.draw.rect(self.screen,self.color_black, self.r2, 0)
                pygame.draw.rect(self.screen,self.color_white, self.r2, 3)
                pygame.draw.rect(self.screen,self.color_black, self.r3, 0)
                pygame.draw.rect(self.screen,self.color_white, self.r3, 3)
                pygame.draw.rect(self.screen,self.color_black, self.r4, 0)
                pygame.draw.rect(self.screen,self.color_white, self.r4, 3)
                pygame.draw.rect(self.screen,self.color_black, self.r5, 0)
                pygame.draw.rect(self.screen,self.color_white, self.r5, 3)
                pygame.draw.rect(self.screen,self.color_black, self.r6, 0)
                pygame.draw.rect(self.screen,self.color_white, self.r6, 3)
                pygame.draw.rect(self.screen,self.color_black, self.r7, 0)
                pygame.draw.rect(self.screen,self.color_white, self.r7, 3)
                self.screen.blit(self.d1,(self.width/13.3333, self.height/4.2683)) #90 164
                self.screen.blit(self.d2,(self.width/13.3333, self.height/3.1390)) #90 223
                self.screen.blit(self.d3,(self.width/13.3333, self.height/2.4823)) #90 282
                self.screen.blit(self.d4,(self.width/13.3333, self.height/2.0528)) #90 341
                self.screen.blit(self.d5,(self.width/13.3333, self.height/1.7500)) #90 400
                self.screen.blit(self.d6,(self.width/13.3333, self.height/1.5251)) #90 459

                if(self.opened_screen == 4):
                    pygame.draw.rect(self.screen,self.color_black, self.r1, 0)
                    pygame.draw.rect(self.screen,self.color_white, self.r1, 3)
                    pygame.draw.rect(self.screen,self.color_black, self.r8, 0)
                    pygame.draw.rect(self.screen,self.color_white, self.r8, 3)
                    self.screen.blit(self.d0,(self.width/13.3333, self.height/6.6667)) #90 105
                    self.screen.blit(self.d7,(self.width/13.3333, self.height/1.3514)) #90 518
            elif(self.opened_screen == 6):
                self.screen.blit(pygame.transform.scale(self.icon_large_dwarf, (self.width/5.2632, self.height/2.1875)), (self.width/10.0000, self.height/5.0000)) #114 160 120 
                self.screen.blit(pygame.transform.scale(self.icon_large_elf, (self.width/5.2632, self.height/2.1875)), (((self.width/10.0000) + ((self.width/7.7922)*2)), self.height/5.0000)) #114 160 
            elif(self.opened_screen == 7):
                self.screen.blit(pygame.transform.scale(self.icon_barbarbarian, (self.width/5.2632, self.width/5.2632)), (self.width/10.0000, self.height/5.0000)) #114 228 120 140
                self.screen.blit(pygame.transform.scale(self.icon_explorer, (self.width/5.2632, self.width/5.2632)), (((self.width/10.0000) + ((self.width/7.7922)*2)), self.height/5.0000)) #114 160 
            if(self.opened_screen == None):
                if(self.personaje.tipo_raza == None):
                    self.screen.blit(pygame.transform.scale(self.defaultIconRaza, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
                    self.screen.blit(self.defaultRaza,(self.width/5.1502, self.height/2.0000)) #233 350
                elif(self.personaje.tipo_raza == "Enano"):
                    self.screen.blit(pygame.transform.scale(self.icon_large_dwarf, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
                elif(self.personaje.tipo_raza == "Elfo"):
                    self.screen.blit(pygame.transform.scale(self.icon_large_elf, (self.width/5.0000, self.height/1.9444)), (self.width/8.5714, self.height/3.5000)) #240 360 140 200
                if(self.personaje.tipo_clase == None):
                    self.screen.blit(pygame.transform.scale(self.default, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
                    self.screen.blit(self.defaultRaza,(self.width/2.5696, self.height/2.9167)) #467 240
                elif(self.personaje.tipo_clase == "Bárbaro"):
                    self.screen.blit(pygame.transform.scale(self.icon_barbarbarian, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
                elif(self.personaje.tipo_clase == "Explorador"):
                    self.screen.blit(pygame.transform.scale(self.icon_explorer, (self.width/8.0000, self.height/4.6667)), (self.width/2.8571, self.height/3.5000)) #150 150 420 200
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/11.7647, self.height/1.1667)) #313 s 102 p
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/7.4074, self.height/1.1570)) #190 s 162 p
            if(self.personaje.name != None and self.personaje.name != ' ' and self.personaje.id_trasfondo != None and self.personaje.tipo_raza != None and self.personaje.tipo_clase != None and self.personaje.vinculo != None and self.personaje.defecto != None and self.personaje.rasgo_personalidad != None and self.personaje.ideal != None):
                self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            else:
                self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667)) #313 s 430 p
            self.screen.blit(pygame.transform.scale(self.crearPersonaje, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570)) #190 s 490 p
            pygame.display.update() 