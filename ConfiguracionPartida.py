import pygame
from pygame.locals import *
from pygame import mixer
import sqlite3
from Partida import Partida
from datetime import datetime

class ConfiguracionPartida:
    def __init__(self,width,height,screen,ch1,ch2,ch3,ch4,local_ip,font,id):
        #screen
        self.screen = screen
        self.font = font
        self.id = id
        self.pic = None
        self.name = None

        #musica
        self.pressed =  pygame.mixer.Sound('sounds/button_pressed.wav')
        self.pressed_exit = pygame.mixer.Sound('sounds/button_pressed_ogg.ogg')
        self.selected = pygame.mixer.Sound('sounds/selected_button.wav')
        self.error = pygame.mixer.Sound('sounds/error.wav')

        #widht y height
        self.width = width
        self.height = height

        self.partidas = {"p1": None, "p2": None, "p3": None}
        self.local_ip = local_ip
        #self.public_ip = public_ip
        self.port = None
        

        #canales
        self.ch1 = ch1
        self.ch2 = ch2
        self.ch3 = ch3
        self.ch4 = ch4

        #variables
        self.first_timeB = True # Aún no has pulsado el botón volver al menú de selección de partidas (cancelar)
        self.first_timeC = True #Aún no has pulsado el botón de crear partida
        self.first_timeI = True #Aún no has pulsado el Icono de ubicación
        self.first_timeBG = True #Aún no has pulsado el botón de guardar la ubicación
        self.currentPartida = None #p1, p2 o p3
        self.activeI = False #La InputBox no está activa
        self.activeI2 = False #La InputBox no está activa
        self.opened_screen = False #la pantalla de selección de escenarios no está por defecto abierta

        #cargamos las imágenes del menú
        self.backgroundPic = pygame.image.load("images/background.png")
        self.capa = pygame.image.load("images/capa.png")
        self.buttonPic = pygame.image.load("images/button.png")
        self.buttonSelectedPic = pygame.image.load("images/button_selected.png")
        self.buttonPressedPic = pygame.image.load("images/button_pressed.png")
        self.buttonUnavailable = pygame.image.load("images/button_unavailable.png")
        self.line = pygame.image.load("images/line.png")
        self.bCreate = pygame.image.load("images/button_createPartida.png")
        self.bCreate_selected = pygame.image.load("images/button_createPartida_selected.png")
        self.bCreate_pressed = pygame.image.load("images/button_createPartida_pressed.png")
        self.buttonUnavailablePic = pygame.image.load("images/button_unavailable.png")
        self.dice1 = pygame.image.load("images/dice_number_b.png")
        self.dice2 = pygame.image.load("images/dice_number2_b.png")
        self.dice3 = pygame.image.load("images/dice_number3_b.png")
        self.dice4 = pygame.image.load("images/dice_number4_b.png")
        self.dice5 = pygame.image.load("images/dice_number5_b.png")
        self.dice6 = pygame.image.load("images/dice_number6_b.png")
        self.dice1_selected = pygame.image.load("images/dice_number_selected.png")
        self.dice2_selected = pygame.image.load("images/dice_number2_selected.png")
        self.dice3_selected = pygame.image.load("images/dice_number3_selected.png")
        self.dice4_selected = pygame.image.load("images/dice_number4_selected.png")
        self.dice5_selected = pygame.image.load("images/dice_number5_selected.png")
        self.dice6_selected = pygame.image.load("images/dice_number6_selected.png")
        self.default = pygame.image.load("images/iconos/icon_default.png")
        self.defaultSelected = pygame.image.load("images/iconos/icon_default_selected.png")
        self.screen_icons = pygame.image.load("images/screen_icons.png")
        self.ubicacion = {}
        self.ubicacionSelected = {}
        for i in range(0,6):
            self.ubicacion[i] = pygame.image.load("images/ubicaciones/ubicacion_"+str(i)+".png")
            self.ubicacionSelected[i] = pygame.image.load("images/ubicaciones/ubicacion_"+str(i)+"_selected.png")

        #fuentes y colores
        self.fuente = pygame.font.SysFont(font, 70)
        self.color_white = (255,255,255)
        self.color_black = (0,0,0)
        self.light_pink = (244,201,208)
        self.color_light_pink = pygame.Color((234,135,255))
        self.color_grey = pygame.Color((208,208,208))
        self.color_dark_grey = pygame.Color((119,119,119))
        self.color_dark_red = pygame.Color((146,0,0))
        self.color_dark_red_sat = pygame.Color((121,58,58))
        self.back = self.fuente.render('Cancelar', True, self.color_white)
        self.crearT = self.fuente.render('Crear Partida', True, self.color_white)
        self.guardarT = self.fuente.render('Guardar Cambios', True, self.color_white)
        self.partidaNombreLabel = self.fuente.render('Nombre de la partida:', True, self.light_pink)
        self.nJugadoresLabel = self.fuente.render('Número de jugadores:', True, self.light_pink)
        self.passwordLabel = self.fuente.render('Contraseña de acceso a la partida:', True, self.light_pink)
        self.ubicacionLabel = self.fuente.render('Ubicación de la historia:', True, self.light_pink)
        #self.serverPortIPLabel = self.fuente.render('Código de localización:', True, self.light_pink)
        self.select = self.fuente.render('- Escoge una ubicación -',True, self.color_grey)
        self.back2 = self.fuente.render('Guardar y volver', True, self.color_white)
        self.select2 = self.fuente.render('Selecciona la ubicación para tu partida:',True, self.color_white)

        #self.portLabel = None
        self.introduceTextLen = 28
        self.max_lenght_name = 12
        self.introduceTextLen2 = 27
        self.max_lenght_name2 = 16



    def setScreen(self,screen):
        self.screen = screen
        #self.width,self.height= (self.screen.get_width(), self.screen.get_height())
    def getScreen(self):
        return self.screen
    def setCurrentPartida(self,p):
        self.currentPartida = p
    def loadPartida(self,row):
        self.partidas[self.currentPartida].num_jugadores = row[0]
        self.partidas[self.currentPartida].ubicacion_historia = row[1]
        self.partidas[self.currentPartida].server_code = row[2]
        self.partidas[self.currentPartida].server_port = None #str(self.local_ip)+":"+str(self.port)
        self.partidas[self.currentPartida].horas_jugadas = row[3]
        self.partidas[self.currentPartida].ultima_conexion = row[4]
        self.partidas[self.currentPartida].numPartida = row[5]
        self.partidas[self.currentPartida].nombre = row[6]

    def refresh(self):
        self.opened_screen = False #por si vuelve a abrir más tarde la pantalla
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
        self.screen.blit(pygame.transform.scale(self.partidaNombreLabel, (self.width/4.0000, self.height/17.5000)), (self.width/12.0000, self.height/11.6667)) #300 40 100 60
        self.screen.blit(pygame.transform.scale(self.line, (self.width/4.0000, self.height/100.0000)), (self.width/12.0000, self.height/7.5269)) #300 7 100 93
        self.screen.blit(pygame.transform.scale(self.nJugadoresLabel, (self.width/4.0000, self.height/17.5000)), (self.width/12.0000, self.height/5.0000)) #300 40 100 140
        self.screen.blit(pygame.transform.scale(self.line, (self.width/4.0000, self.height/100.0000)), (self.width/12.0000, self.height/4.0462)) #300 7 100 173
        self.screen.blit(pygame.transform.scale(self.passwordLabel, (self.width/2.4000, self.height/17.5000)), (self.width/12.0000, self.height/3.1818)) #500 40 100 220
        self.screen.blit(pygame.transform.scale(self.line, (self.width/2.4000, self.height/100.0000)), (self.width/12.0000, self.height/2.7668)) #500 7 100 253
        self.screen.blit(pygame.transform.scale(self.ubicacionLabel, (self.width/3.4286, self.height/17.5000)), (self.width/12.0000, self.height/2.3333)) #350 40 100 300
        self.screen.blit(pygame.transform.scale(self.line, (self.width/3.4286, self.height/100.0000)), (self.width/12.0000, self.height/2.1021)) #350 7 100 333
        #self.screen.blit(pygame.transform.scale(self.serverPortIPLabel, (self.width/3.4286, self.height/17.5000)), (self.width/1.8462, self.height/2.3333))#350 40 650 300
        #self.screen.blit(pygame.transform.scale(self.line, (self.width/3.4286, self.height/100.0000)), (self.width/1.8462, self.height/2.1021))
        #self.screen.blit(pygame.transform.scale(self.portLabel, (self.width/4.0000, self.height/17.5000)), (self.width/1.7778, self.height/1.9444)) #300 40 675 360
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/4.0956, self.height/12.2807)), (self.width/2.4000, self.height/1.1667))#293 57 500 600
        self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/2.1053, self.height/1.1570)) #150 40 570 605
        if(self.partidas[self.currentPartida].num_jugadores == 6):
            self.screen.blit(pygame.transform.scale(self.dice1, (self.width/24.0000, self.height/14.0000)), (self.width/2.8571, self.height/4.8276))#50 50 420 145
            self.screen.blit(pygame.transform.scale(self.dice2, (self.width/24.0000, self.height/14.0000)), (self.width/2.5000, self.height/4.8276))#50 50 480 145
            self.screen.blit(pygame.transform.scale(self.dice3, (self.width/24.0000, self.height/14.0000)), (self.width/2.2222, self.height/4.8276))#50 50 540 145
            self.screen.blit(pygame.transform.scale(self.dice4, (self.width/24.0000, self.height/14.0000)), (self.width/2.0000, self.height/4.8276))#50 50 600 145
            self.screen.blit(pygame.transform.scale(self.dice5, (self.width/24.0000, self.height/14.0000)), (self.width/1.8182, self.height/4.8276))#50 50 660 145
            self.screen.blit(pygame.transform.scale(self.dice6_selected, (self.width/24.0000, self.height/14.0000)), (self.width/1.6667, self.height/4.8276))#50 50 720 145
        elif(self.partidas[self.currentPartida].num_jugadores == 5):
            self.screen.blit(pygame.transform.scale(self.dice1, (self.width/24.0000, self.height/14.0000)), (self.width/2.8571, self.height/4.8276))#50 50 420 145
            self.screen.blit(pygame.transform.scale(self.dice2, (self.width/24.0000, self.height/14.0000)), (self.width/2.5000, self.height/4.8276))#50 50 480 145
            self.screen.blit(pygame.transform.scale(self.dice3, (self.width/24.0000, self.height/14.0000)), (self.width/2.2222, self.height/4.8276))#50 50 540 145
            self.screen.blit(pygame.transform.scale(self.dice4, (self.width/24.0000, self.height/14.0000)), (self.width/2.0000, self.height/4.8276))#50 50 600 145
            self.screen.blit(pygame.transform.scale(self.dice5_selected, (self.width/24.0000, self.height/14.0000)), (self.width/1.8182, self.height/4.8276))#50 50 660 145
            self.screen.blit(pygame.transform.scale(self.dice6, (self.width/24.0000, self.height/14.0000)), (self.width/1.6667, self.height/4.8276))#50 50 720 145
        elif(self.partidas[self.currentPartida].num_jugadores == 4):
            self.screen.blit(pygame.transform.scale(self.dice1, (self.width/24.0000, self.height/14.0000)), (self.width/2.8571, self.height/4.8276))#50 50 420 145
            self.screen.blit(pygame.transform.scale(self.dice2, (self.width/24.0000, self.height/14.0000)), (self.width/2.5000, self.height/4.8276))#50 50 480 145
            self.screen.blit(pygame.transform.scale(self.dice3, (self.width/24.0000, self.height/14.0000)), (self.width/2.2222, self.height/4.8276))#50 50 540 145
            self.screen.blit(pygame.transform.scale(self.dice4_selected, (self.width/24.0000, self.height/14.0000)), (self.width/2.0000, self.height/4.8276))#50 50 600 145
            self.screen.blit(pygame.transform.scale(self.dice5, (self.width/24.0000, self.height/14.0000)), (self.width/1.8182, self.height/4.8276))#50 50 660 145
            self.screen.blit(pygame.transform.scale(self.dice6, (self.width/24.0000, self.height/14.0000)), (self.width/1.6667, self.height/4.8276))#50 50 720 145
        elif(self.partidas[self.currentPartida].num_jugadores == 3):
            self.screen.blit(pygame.transform.scale(self.dice1, (self.width/24.0000, self.height/14.0000)), (self.width/2.8571, self.height/4.8276))#50 50 420 145
            self.screen.blit(pygame.transform.scale(self.dice2, (self.width/24.0000, self.height/14.0000)), (self.width/2.5000, self.height/4.8276))#50 50 480 145
            self.screen.blit(pygame.transform.scale(self.dice3_selected, (self.width/24.0000, self.height/14.0000)), (self.width/2.2222, self.height/4.8276))#50 50 540 145
            self.screen.blit(pygame.transform.scale(self.dice4, (self.width/24.0000, self.height/14.0000)), (self.width/2.0000, self.height/4.8276))#50 50 600 145
            self.screen.blit(pygame.transform.scale(self.dice5, (self.width/24.0000, self.height/14.0000)), (self.width/1.8182, self.height/4.8276))#50 50 660 145
            self.screen.blit(pygame.transform.scale(self.dice6, (self.width/24.0000, self.height/14.0000)), (self.width/1.6667, self.height/4.8276))#50 50 720 145
        elif(self.partidas[self.currentPartida].num_jugadores == 2):
            self.screen.blit(pygame.transform.scale(self.dice1, (self.width/24.0000, self.height/14.0000)), (self.width/2.8571, self.height/4.8276))#50 50 420 145
            self.screen.blit(pygame.transform.scale(self.dice2_selected, (self.width/24.0000, self.height/14.0000)), (self.width/2.5000, self.height/4.8276))#50 50 480 145
            self.screen.blit(pygame.transform.scale(self.dice3, (self.width/24.0000, self.height/14.0000)), (self.width/2.2222, self.height/4.8276))#50 50 540 145
            self.screen.blit(pygame.transform.scale(self.dice4, (self.width/24.0000, self.height/14.0000)), (self.width/2.0000, self.height/4.8276))#50 50 600 145
            self.screen.blit(pygame.transform.scale(self.dice5, (self.width/24.0000, self.height/14.0000)), (self.width/1.8182, self.height/4.8276))#50 50 660 145
            self.screen.blit(pygame.transform.scale(self.dice6, (self.width/24.0000, self.height/14.0000)), (self.width/1.6667, self.height/4.8276))#50 50 720 145
        else: #es 1
            self.screen.blit(pygame.transform.scale(self.dice1_selected, (self.width/24.0000, self.height/14.0000)), (self.width/2.8571, self.height/4.8276))#50 50 420 145
            self.screen.blit(pygame.transform.scale(self.dice2, (self.width/24.0000, self.height/14.0000)), (self.width/2.5000, self.height/4.8276))#50 50 480 145
            self.screen.blit(pygame.transform.scale(self.dice3, (self.width/24.0000, self.height/14.0000)), (self.width/2.2222, self.height/4.8276))#50 50 540 145
            self.screen.blit(pygame.transform.scale(self.dice4, (self.width/24.0000, self.height/14.0000)), (self.width/2.0000, self.height/4.8276))#50 50 600 145
            self.screen.blit(pygame.transform.scale(self.dice5, (self.width/24.0000, self.height/14.0000)), (self.width/1.8182, self.height/4.8276))#50 50 660 145
            self.screen.blit(pygame.transform.scale(self.dice6, (self.width/24.0000, self.height/14.0000)), (self.width/1.6667, self.height/4.8276))#50 50 720 145
        if(self.partidas[self.currentPartida].ubicacion_historia != None):
            self.screen.blit(pygame.transform.scale(self.ubicacion[self.partidas[self.currentPartida].ubicacion_historia], (self.width/4.8000, self.width/4.8000)), (self.width/12.0000, self.height/2.0000))
        else:
            self.screen.blit(pygame.transform.scale(self.default, (self.width/4.8000, self.width/4.8000)), (self.width/12.0000, self.height/2.0000)) #250w 250w 100 350 
            self.screen.blit(pygame.transform.scale(self.select, (self.width/7.5000, self.height/21.8750)), (self.width/8.2759, self.height/1.5217)) #160 32 145 460
        
        
        if((self.partidas[self.currentPartida].nombre != None and self.partidas[self.currentPartida].nombre != ' ') and (self.partidas[self.currentPartida].ubicacion_historia != None) and (self.partidas[self.currentPartida].server_code != None and self.partidas[self.currentPartida].server_code != ' ')):
            self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/4.0956, self.height/12.2807)), (self.width/1.4760, self.height/1.1667))
        else:
            self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.4760, self.height/1.1667))
        self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.3889, self.height/1.1570))

    def render(self,pic,name):
        self.pic = pic
        self.name = name
        #calculo tamaño de letras a mostrar
        self.letterwidth = (self.width/3.4286)/14 #cálculo de la base en píxeles 
        self.lettersize = self.letterwidth + 0.5 * self.letterwidth #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuenteText = pygame.font.SysFont(self.font, int(self.lettersize))
        self.emptyText = self.fuenteText.render(' ', True, self.color_dark_grey)
        self.introduceText = self.fuenteText.render('--- Nombre de la partida ---' , True, self.color_dark_grey)
        self.emptyText2 = self.fuenteText.render(' ', True, self.color_dark_grey)
        self.introduceText2 = self.fuenteText.render('--- Contraseña de acceso ---' , True, self.color_dark_grey)
        self.introduceText3 = self.fuenteText.render('Nombre ya existente' , True, self.color_dark_red_sat)
        self.opened_screen = False #por si vuelve a abrir más tarde la pantalla
        #de la input box
        #InputBox
            #self.widthText = self.letterwidth*len(self.name)
        #render screen
        conn = sqlite3.connect("simuladordnd.db")
        cur = conn.cursor()
        if(self.currentPartida == "p1"):
            #cargamos la partida 1, si existe: el orden de las columnas será ese
            cur.execute("SELECT num_jugadores,ubicacion_historia,server_code,horas_jugadas,ultima_conexion,numPartida,nombre FROM partida WHERE numPartida = 'p1'")
                #TODO asignar los atributos a los atributos internos de las partidas que tengo aquí cargadas
            rows = cur.fetchall()
            if(len(rows) == 0):
                self.partidas[self.currentPartida] = Partida()
                self.partidas[self.currentPartida].numPartida = 1
            else:
                self.loadPartida(rows[0])
        elif(self.currentPartida == "p2"):
            #TODO asignar los atributos a los atributos internos de las partidas que tengo aquí cargadas
            cur.execute("SELECT num_jugadores,ubicacion_historia,server_code,horas_jugadas,ultima_conexion,numPartida,nombre FROM partida WHERE numPartida = 'p2'")
            rows = cur.fetchall()
            if(len(rows) == 0):
                self.partidas[self.currentPartida] = Partida()
                self.partidas[self.currentPartida].numPartida = 2
            else:
                self.loadPartida(rows[0])
        elif(self.currentPartida == "p3"):
            #TODO asignar los atributos a los atributos internos de las partidas que tengo aquí cargadas
            cur.execute("SELECT num_jugadores,ubicacion_historia,server_code,horas_jugadas,ultima_conexion,numPartida,nombre FROM partida WHERE numPartida = 'p3'")
            rows = cur.fetchall()
            if(len(rows) == 0):
                self.partidas[self.currentPartida] = Partida()
                self.partidas[self.currentPartida].numPartida = 3
            else:
                self.loadPartida(rows[0])
        else:
            #por defecto va a ser p1, si acaso se perdiera el valor
            self.currentPartida = "p1"
            cur.execute("SELECT num_jugadores,ubicacion_historia,server_code,horas_jugadas,ultima_conexion,numPartida,nombre FROM partida WHERE numPartida = 'p1'")
                #TODO asignar los atributos a los atributos internos de las partidas que tengo aquí cargadas
            rows = cur.fetchall()
            if(len(rows) == 0):
                self.partidas[self.currentPartida] = Partida()
                self.partidas[self.currentPartida].numPartida = 1
            else:
                self.loadPartida(rows[0])
        cur.close()
        conn.close() #cerramos la conexión con la bbdd
        #Creamos el texto del código del servidor

        #Input del nombre
        if(self.partidas[self.currentPartida].nombre == None):
            self.partidas[self.currentPartida].nombre = ' '
            self.textNombrePartida = self.introduceText
        else:
            self.textNombrePartida = self.fuenteText.render(self.partidas[self.currentPartida].nombre, True, self.color_dark_grey)
        #Input de la contraseña
        if(self.partidas[self.currentPartida].server_code == None):
            self.partidas[self.currentPartida].server_code = ' '
            self.textPassword = self.introduceText2
        else:
            self.textPassword = self.fuenteText.render(self.partidas[self.currentPartida].server_code, True, self.color_dark_grey)
        
        #self.portLabel = self.fuente.render(self.partidas[self.currentPartida].server_port, True, self.color_white)
        self.refresh()
        #nombre partida
        self.inputBox = pygame.Rect(self.width/2.8571, self.height/11.6667, self.width/3.4286, self.height/11.6667) #420 60 350 60
        pygame.draw.rect(self.screen, self.color_grey, self.inputBox, 2)
        self.screen.blit(self.textNombrePartida, (self.width/2.7650, self.height/10.7692)) #434 x 65
        #password
        self.inputBox2 = pygame.Rect(self.width/1.9355, self.height/3.2558, self.width/3.2432, self.height/11.6667) #620 215 370 60
        pygame.draw.rect(self.screen, self.color_grey, self.inputBox2, 2)
        self.screen.blit(self.textPassword, (self.width/1.8927, self.height/3.1818)) #634 220
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
            x_size = self.width/4.0956
            y_size = self.height/12.2807
            x_start = self.width/2.4000
            y_start = self.height/1.1667
            x_startC = self.width/1.4760
            x_sized = self.width/24.0000
            y_sized = self.height/14.0000
            x_startd1 = self.width/2.8571
            y_startd =  self.height/4.8276
            x_startd2 = self.width/2.5000
            x_startd3 = self.width/2.2222
            x_startd4 = self.width/2.0000
            x_startd5 = self.width/1.8182
            x_startd6 = self.width/1.6667
            x_sizeI = self.width/4.8000
            y_sizeI = self.width/4.8000
            x_startI = self.width/12.0000
            y_startI = self.height/2.0000
            (x,y) = pygame.mouse.get_pos()

            #Botón volver al menú
            if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                self.activeI = False
                self.activeI2 = False
                if(not self.opened_screen):
                    self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/4.0956, self.height/12.2807)), (self.width/2.4000, self.height/1.1667))#293 57 500 600
                    self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/2.1053, self.height/1.1570)) #150 40 570 605
                    if(self.partidas[self.currentPartida].nombre != None and self.partidas[self.currentPartida].ubicacion_historia != None and self.partidas[self.currentPartida].server_code != None):
                        self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/4.0956, self.height/12.2807)), (self.width/1.4760, self.height/1.1667))
                    else:
                        self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.4760, self.height/1.1667))
                    self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.3889, self.height/1.1570))
                    self.ch1.play(self.pressed)
                    pygame.display.update() 
                    return 'seleccionPartidas'
                else:
                    self.ch1.play(self.error)
                    return 'configuracionPartida'
            
            
            #numero jugadores
            elif(self.checkIfMouseIsInButton(x_sized,y_sized,x_startd1,y_startd,x,y)):
                if(not self.opened_screen):
                    self.screen.blit(pygame.transform.scale(self.dice1_selected, (self.width/24.0000, self.height/14.0000)), (self.width/2.8571, self.height/4.8276))#50 50 420 145
                    self.screen.blit(pygame.transform.scale(self.dice2, (self.width/24.0000, self.height/14.0000)), (self.width/2.5000, self.height/4.8276))#50 50 480 145
                    self.screen.blit(pygame.transform.scale(self.dice3, (self.width/24.0000, self.height/14.0000)), (self.width/2.2222, self.height/4.8276))#50 50 540 145
                    self.screen.blit(pygame.transform.scale(self.dice4, (self.width/24.0000, self.height/14.0000)), (self.width/2.0000, self.height/4.8276))#50 50 600 145
                    self.screen.blit(pygame.transform.scale(self.dice5, (self.width/24.0000, self.height/14.0000)), (self.width/1.8182, self.height/4.8276))#50 50 660 145
                    self.screen.blit(pygame.transform.scale(self.dice6, (self.width/24.0000, self.height/14.0000)), (self.width/1.6667, self.height/4.8276))#50 50 720 145
                    self.ch1.play(self.pressed)
                    self.partidas[self.currentPartida].num_jugadores = 1
                    pygame.display.update() 
                else:
                    pass
                return 'configuracionPartida'
            elif(self.checkIfMouseIsInButton(x_sized,y_sized,x_startd2,y_startd,x,y)):
                if(not self.opened_screen):
                    self.screen.blit(pygame.transform.scale(self.dice1, (self.width/24.0000, self.height/14.0000)), (self.width/2.8571, self.height/4.8276))#50 50 420 145
                    self.screen.blit(pygame.transform.scale(self.dice2_selected, (self.width/24.0000, self.height/14.0000)), (self.width/2.5000, self.height/4.8276))#50 50 480 145
                    self.screen.blit(pygame.transform.scale(self.dice3, (self.width/24.0000, self.height/14.0000)), (self.width/2.2222, self.height/4.8276))#50 50 540 145
                    self.screen.blit(pygame.transform.scale(self.dice4, (self.width/24.0000, self.height/14.0000)), (self.width/2.0000, self.height/4.8276))#50 50 600 145
                    self.screen.blit(pygame.transform.scale(self.dice5, (self.width/24.0000, self.height/14.0000)), (self.width/1.8182, self.height/4.8276))#50 50 660 145
                    self.screen.blit(pygame.transform.scale(self.dice6, (self.width/24.0000, self.height/14.0000)), (self.width/1.6667, self.height/4.8276))#50 50 720 145
                    self.ch1.play(self.pressed)
                    self.partidas[self.currentPartida].num_jugadores = 2
                    pygame.display.update() 
                else:
                    pass
                return 'configuracionPartida'
            elif(self.checkIfMouseIsInButton(x_sized,y_sized,x_startd3,y_startd,x,y)):
                if(not self.opened_screen):
                    self.screen.blit(pygame.transform.scale(self.dice1, (self.width/24.0000, self.height/14.0000)), (self.width/2.8571, self.height/4.8276))#50 50 420 145
                    self.screen.blit(pygame.transform.scale(self.dice2, (self.width/24.0000, self.height/14.0000)), (self.width/2.5000, self.height/4.8276))#50 50 480 145
                    self.screen.blit(pygame.transform.scale(self.dice3_selected, (self.width/24.0000, self.height/14.0000)), (self.width/2.2222, self.height/4.8276))#50 50 540 145
                    self.screen.blit(pygame.transform.scale(self.dice4, (self.width/24.0000, self.height/14.0000)), (self.width/2.0000, self.height/4.8276))#50 50 600 145
                    self.screen.blit(pygame.transform.scale(self.dice5, (self.width/24.0000, self.height/14.0000)), (self.width/1.8182, self.height/4.8276))#50 50 660 145
                    self.screen.blit(pygame.transform.scale(self.dice6, (self.width/24.0000, self.height/14.0000)), (self.width/1.6667, self.height/4.8276))#50 50 720 145
                    self.ch1.play(self.pressed)
                    self.partidas[self.currentPartida].num_jugadores = 3
                    pygame.display.update() 
                else:
                    pass
                return 'configuracionPartida'
            elif(self.checkIfMouseIsInButton(x_sized,y_sized,x_startd4,y_startd,x,y)):
                if(not self.opened_screen):
                    self.screen.blit(pygame.transform.scale(self.dice1, (self.width/24.0000, self.height/14.0000)), (self.width/2.8571, self.height/4.8276))#50 50 420 145
                    self.screen.blit(pygame.transform.scale(self.dice2, (self.width/24.0000, self.height/14.0000)), (self.width/2.5000, self.height/4.8276))#50 50 480 145
                    self.screen.blit(pygame.transform.scale(self.dice3, (self.width/24.0000, self.height/14.0000)), (self.width/2.2222, self.height/4.8276))#50 50 540 145
                    self.screen.blit(pygame.transform.scale(self.dice4_selected, (self.width/24.0000, self.height/14.0000)), (self.width/2.0000, self.height/4.8276))#50 50 600 145
                    self.screen.blit(pygame.transform.scale(self.dice5, (self.width/24.0000, self.height/14.0000)), (self.width/1.8182, self.height/4.8276))#50 50 660 145
                    self.screen.blit(pygame.transform.scale(self.dice6, (self.width/24.0000, self.height/14.0000)), (self.width/1.6667, self.height/4.8276))#50 50 720 145
                    self.ch1.play(self.pressed)
                    self.partidas[self.currentPartida].num_jugadores = 4
                    pygame.display.update() 
                else:
                    pass
                return 'configuracionPartida'
            elif(self.checkIfMouseIsInButton(x_sized,y_sized,x_startd5,y_startd,x,y)):
                if(not self.opened_screen):
                    self.screen.blit(pygame.transform.scale(self.dice1, (self.width/24.0000, self.height/14.0000)), (self.width/2.8571, self.height/4.8276))#50 50 420 145
                    self.screen.blit(pygame.transform.scale(self.dice2, (self.width/24.0000, self.height/14.0000)), (self.width/2.5000, self.height/4.8276))#50 50 480 145
                    self.screen.blit(pygame.transform.scale(self.dice3, (self.width/24.0000, self.height/14.0000)), (self.width/2.2222, self.height/4.8276))#50 50 540 145
                    self.screen.blit(pygame.transform.scale(self.dice4, (self.width/24.0000, self.height/14.0000)), (self.width/2.0000, self.height/4.8276))#50 50 600 145
                    self.screen.blit(pygame.transform.scale(self.dice5_selected, (self.width/24.0000, self.height/14.0000)), (self.width/1.8182, self.height/4.8276))#50 50 660 145
                    self.screen.blit(pygame.transform.scale(self.dice6, (self.width/24.0000, self.height/14.0000)), (self.width/1.6667, self.height/4.8276))#50 50 720 145
                    self.ch1.play(self.pressed)
                    self.partidas[self.currentPartida].num_jugadores = 5
                else:
                    pass
                pygame.display.update() 
                return 'configuracionPartida'
            elif(self.checkIfMouseIsInButton(x_sized,y_sized,x_startd6,y_startd,x,y)):
                if(not self.opened_screen):
                    self.screen.blit(pygame.transform.scale(self.dice1, (self.width/24.0000, self.height/14.0000)), (self.width/2.8571, self.height/4.8276))#50 50 420 145
                    self.screen.blit(pygame.transform.scale(self.dice2, (self.width/24.0000, self.height/14.0000)), (self.width/2.5000, self.height/4.8276))#50 50 480 145
                    self.screen.blit(pygame.transform.scale(self.dice3, (self.width/24.0000, self.height/14.0000)), (self.width/2.2222, self.height/4.8276))#50 50 540 145
                    self.screen.blit(pygame.transform.scale(self.dice4, (self.width/24.0000, self.height/14.0000)), (self.width/2.0000, self.height/4.8276))#50 50 600 145
                    self.screen.blit(pygame.transform.scale(self.dice5, (self.width/24.0000, self.height/14.0000)), (self.width/1.8182, self.height/4.8276))#50 50 660 145
                    self.screen.blit(pygame.transform.scale(self.dice6_selected, (self.width/24.0000, self.height/14.0000)), (self.width/1.6667, self.height/4.8276))#50 50 720 145
                    self.ch1.play(self.pressed)
                    self.partidas[self.currentPartida].num_jugadores = 6
                    pygame.display.update() 
                else:
                    pass
                return 'configuracionPartida'
            
            #crear partida
            elif(self.checkIfMouseIsInButton(x_size,y_size,x_startC,y_start,x,y)):
                pantalla = 'configuracionPartida'
                self.activeI = False
                self.activeI2 = False
                if(not self.opened_screen):
                    pantalla = 'salaEspera'
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/4.0956, self.height/12.2807)), (self.width/2.4000, self.height/1.1667))#293 57 500 600
                    self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/2.1053, self.height/1.1570)) #150 40 570 605
                    if((self.partidas[self.currentPartida].nombre != None and self.partidas[self.currentPartida].nombre != ' ') and (self.partidas[self.currentPartida].ubicacion_historia != None) and (self.partidas[self.currentPartida].server_code != None and self.partidas[self.currentPartida].server_code != ' ')):
                        self.screen.blit(pygame.transform.scale(self.bCreate_pressed, (self.width/4.0956, self.height/12.2807)), (self.width/1.4760, self.height/1.1667))
                        # ------------- Guardamos la configuración de la partida ----------- #
                        conn = sqlite3.connect("simuladordnd.db")
                        cursor = conn.cursor()
                        query_save_partida = """INSERT INTO partida
                                                (server_code, numPartida, ultima_conexion, horas_jugadas, ubicacion_historia, num_jugadores, nombre) 
                                                VALUES (?,?,?,?,?,?,?)"""
                        
                        actual_time = datetime.now()
                        if(self.partidas[self.currentPartida].ubicacion_historia == 0):
                            ubicacion = 'Mazmorra'
                        elif(self.partidas[self.currentPartida].ubicacion_historia == 1):
                            ubicacion = 'Mar'
                        elif(self.partidas[self.currentPartida].ubicacion_historia == 2):
                            ubicacion = 'Ciudad Futurista'
                        elif(self.partidas[self.currentPartida].ubicacion_historia == 3):
                            ubicacion = 'Desierto'
                        elif(self.partidas[self.currentPartida].ubicacion_historia == 4):
                            ubicacion = 'Aldea Medieval'
                        else:
                            ubicacion = 'Bosque'
                        data_partida = (self.partidas[self.currentPartida].server_code,self.currentPartida,actual_time, 0,ubicacion, self.partidas[self.currentPartida].num_jugadores, self.partidas[self.currentPartida].nombre)
                        
                        #comprobamos si el jugador existe ya en la bbdd (si no ha creado ninguna partida, habrá que registrarlo)
                        sql_get_me = "SELECT id_jugador,is_my_id FROM jugador"
                        cursor.execute(sql_get_me)
                        rows = cursor.fetchall() #para llegar a esta pantalla, la pantalla tiene que existir sí o sí
                        print(rows)
                        existo = False
                        if rows != []:
                            for row in rows:
                                if(row[1] == True):
                                    if(row[0] == self.id):
                                        #existe, y es tu id
                                        existo = True
                                        break
                                    else:
                                        #si se corrompió el archivo y te tuvo que reasignar otra id, se va a actualizar ahora en la bbdd
                                        query_update_id = "UPDATE jugador SET id_jugador = '"+self.id+"' WHERE id_jugador = '"+row[0]+"';"
                                        cursor.execute(query_update_id)
                                        conn.commit() 
                                        existo = True
                                        break
                                        

                        else:
                            existo = False

                        if(not existo):
                            #hay que meterlo
                            data_jugador_yo = (self.id,True,self.pic,self.name)
                            query_save_me = """INSERT INTO jugador
                                                (id_jugador,is_my_id,pic,name) 
                                                VALUES (?,?,?,?)"""
                            cursor.execute(query_save_me,data_jugador_yo)
                        else:
                            #siempre actualizaremos nombre y pic del host por si hubieran sido modificados
                            query_update_pic = "UPDATE jugador SET pic = "+str(self.pic)+" WHERE id_jugador = '"+self.id+"';"
                            cursor.execute(query_update_pic)
                            query_update_name = "UPDATE jugador SET name = '"+self.name+"' WHERE id_jugador = '"+self.id+"';"
                            cursor.execute(query_update_name)
                            conn.commit() 

                        #es la primera vez que asignamos este jugador a la partida sí o sí (la partida no existía)
                        data_jugador_partida = (0,self.currentPartida,self.id) #nMuertes_partida,partida_id,id_jugador
                        query_save_partida_jugador = """INSERT INTO partida_jugador
                                                        (nMuertes_partida,partida_id,id_jugador) 
                                                        VALUES (?,?,?)"""
                        try:
                            cursor.execute(query_save_partida, data_partida)
                            cursor.execute(query_save_partida_jugador,data_jugador_partida)
                            conn.commit()
                        except sqlite3.IntegrityError as e:
                            print(e)
                            pantalla = 'configuracionPartida'
                            self.textNombrePartida = self.introduceText3
                            self.ch1.play(self.error)
                            self.partidas[self.currentPartida].nombre = ' '
                            self.refresh()
                            pygame.draw.rect(self.screen, self.color_dark_red, self.inputBox, 2)
                            self.screen.blit(self.textNombrePartida, (self.width/2.7650, self.height/10.7692))

                            if(self.partidas[self.currentPartida].server_code == ' '):
                                self.textPassword = self.introduceText2
                            else:
                                self.textPassword = self.fuenteText.render(self.partidas[self.currentPartida].server_code, True, self.color_grey)
                            pygame.draw.rect(self.screen, self.color_grey, self.inputBox2, 2)
                            self.screen.blit(self.textPassword, (self.width/1.8927, self.height/3.1818)) #634 220
                            pygame.display.update() 
                        finally:
                            self.ch1.play(self.pressed)
                            conn.close()

                    else:
                        self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.4760, self.height/1.1667))
                        self.ch1.play(self.error)
                        pantalla = 'configuracionPartida'
                    self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.3889, self.height/1.1570))
                    pygame.display.update() 
                else:
                    self.ch1.play(self.error)
                return pantalla
            
            #Icono de ubicación
            elif(self.checkIfMouseIsInButton(x_sizeI,y_sizeI,x_startI,y_startI,x,y)):
                self.activeI = False
                self.activeI2 = False
                if(self.opened_screen):
                    self.ch3.play(self.error)
                else:
                    self.screen.blit(pygame.transform.scale(self.screen_icons, (self.width/1.7143, self.height/1.2727)), (self.width/3.0000, self.height/16.2791)) #self.width/30.0000
                    self.screen.blit(pygame.transform.scale(self.select2, (self.width/2.4000, self.height/14.0000)), (self.width/2.6667, self.height/8.7500)) #self.width/13.3333
                    if(self.partidas[self.currentPartida].ubicacion_historia == None):
                        self.screen.blit(pygame.transform.scale(self.default, (self.width/4.8000, self.width/4.8000)), (self.width/12.0000, self.height/2.0000)) #250w 250w 100 350 
                        self.screen.blit(pygame.transform.scale(self.select, (self.width/7.5000, self.height/21.8750)), (self.width/8.2759, self.height/1.5217)) #160 32 145 460
                        self.screen.blit(pygame.transform.scale(self.buttonUnavailable, (self.width/3.8339, self.height/12.2807)), (self.width/1.6901, self.height/1.4000)) #self.width/3.4286
                        self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/1.5789, self.height/1.3861))#self.width/3.0000
                        #por defecto, no se pone ninguna. Pero el botón de guardar estará en gris.
                        #imagenes
                    else:
                        self.screen.blit(pygame.transform.scale(self.ubicacion[self.partidas[self.currentPartida].ubicacion_historia], (self.width/4.8000, self.width/4.8000)), (self.width/12.0000, self.height/2.0000))
                        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.6901, self.height/1.4000))
                        self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/1.5789, self.height/1.3861))
                    for i in range(0,6):
                        x_size = self.width/10.5263
                        y_size = self.width/10.5263
                        x_start = (self.width/2.2514) +  ((self.width/7.7922)*(i%3))
                        y_start = (self.height/5.0000) +((self.height/4.5455)*(i//3))
                        if(self.partidas[self.currentPartida].ubicacion_historia == i):
                            #self.screen.blit(pygame.transform.scale(self.ubicacionSelected[i], (114,114)), (173+154*(i%3),140+154*(i//3)))
                            self.screen.blit(pygame.transform.scale(self.ubicacionSelected[i], (x_size, y_size)), (x_start, y_start))
                        else:
                            #self.screen.blit(pygame.transform.scale(self.ubicacion[i], (114,114)), (173+154*(i%3),140+154*(i//3)))
                            self.screen.blit(pygame.transform.scale(self.ubicacion[i], (x_size, y_size)), (x_start, y_start))#imagenes
                    self.opened_screen = True
                    self.ch2.play(self.pressed)
                pygame.display.update()
                return 'configuracionPartida'
            
            elif self.opened_screen:
                self.activeI = False
                self.activeI2 = False
                x_size = self.width/3.8339
                y_size = self.height/12.2807
                x_start = self.width/1.6901
                y_start = self.height/1.4000
                #botón de guardar
                if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                    if(self.partidas[self.currentPartida].ubicacion_historia != None):
                        self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.6901, self.height/1.4000))
                        self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/1.5789, self.height/1.3861))
                        pygame.display.update()
                        self.ch1.play(self.pressed)
                        self.refresh()
                        pygame.draw.rect(self.screen, self.color_grey, self.inputBox, 2)
                        self.screen.blit(self.textNombrePartida, (self.width/2.7650, self.height/10.7692))

                        #password
                        pygame.draw.rect(self.screen, self.color_grey, self.inputBox2, 2)
                        self.screen.blit(self.textPassword, (self.width/1.8927, self.height/3.1818)) #634 220
                        pygame.display.update() 

                    else:
                        self.ch3.play(self.error)
                else:
                    someSelected = 0
                    for i in range(0,6):
                        x_size = self.width/10.5263
                        y_size = self.width/10.5263
                        x_start = (self.width/2.2514) +  ((self.width/7.7922)*(i%3))
                        y_start = (self.height/5.0000) +((self.height/4.5455)*(i//3))
                        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                            self.partidas[self.currentPartida].ubicacion_historia = i
                            #self.screen.blit(pygame.transform.scale(self.avatarJugadorSelected[i], (114,114)), (173+154*(i%3),140+154*(i//3)))
                            self.screen.blit(pygame.transform.scale(self.ubicacionSelected[i], (x_size, y_size)), (x_start, y_start))
                            self.screen.blit(pygame.transform.scale(self.ubicacion[i], (self.width/4.8000, self.width/4.8000)), (self.width/12.0000, self.height/2.0000))
                            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.6901, self.height/1.4000))
                            self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/1.5789, self.height/1.3861))
                            self.ch4.play(self.pressed)
                            someSelected = 1
                        else:
                            #self.screen.blit(pygame.transform.scale(self.avatarJugador[i], (114,114)), (173+154*(i%3),140+154*(i//3)))
                            self.screen.blit(pygame.transform.scale(self.ubicacion[i], (x_size, y_size)), (x_start, y_start))#imagenes
                    
                    if(someSelected == 0 and self.partidas[self.currentPartida].ubicacion_historia is not None):
                        x_size = self.width/10.5263
                        y_size = self.width/10.5263
                        x_start = (self.width/2.2514) +  ((self.width/7.7922)*(self.partidas[self.currentPartida].ubicacion_historia %3))
                        y_start = (self.height/5.0000) +((self.height/4.5455)*(self.partidas[self.currentPartida].ubicacion_historia //3))
                        self.screen.blit(pygame.transform.scale(self.ubicacionSelected[self.partidas[self.currentPartida].ubicacion_historia], (x_size, y_size)), (x_start, y_start))
                        self.screen.blit(pygame.transform.scale(self.ubicacion[self.partidas[self.currentPartida].ubicacion_historia], (self.width/4.8000, self.width/4.8000)), (self.width/12.0000, self.height/2.0000))
                        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.6901, self.height/1.4000))
                        self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/1.5789, self.height/1.3861))
                pygame.display.update() 
                return 'configuracionPartida'   
    
            #Input de nombre de partida
            elif self.inputBox.collidepoint((x,y)):
                if(not self.opened_screen):
                    self.refresh()
                    pygame.draw.rect(self.screen, self.color_light_pink, self.inputBox, 2)
                    if(self.partidas[self.currentPartida].nombre == ' '):
                        self.textNombrePartida = self.emptyText
                        self.screen.blit(self.textNombrePartida, (self.width/2.7650, self.height/10.7692))
                    else:
                        self.screen.blit(self.textNombrePartida, (self.width/2.7650, self.height/10.7692))

                    if(self.partidas[self.currentPartida].server_code == ' '):
                        self.textPassword = self.introduceText2
                    else:
                        self.textPassword = self.fuenteText.render(self.partidas[self.currentPartida].server_code, True, self.color_grey)
                    pygame.draw.rect(self.screen, self.color_grey, self.inputBox2, 2)
                    self.screen.blit(self.textPassword, (self.width/1.8927, self.height/3.1818)) #634 220
                    pygame.display.update() 
                    self.activeI = True
                    self.activeI2 = False
                    return 'configuracionPartida'
                else:
                    self.ch2.play(self.error)
                    return 'configuracionPartida'
            #Input de contraseña
            elif self.inputBox2.collidepoint((x,y)):
                if(not self.opened_screen):
                    self.refresh()
                    pygame.draw.rect(self.screen, self.color_light_pink, self.inputBox2, 2)
                    if(self.partidas[self.currentPartida].server_code == ' '):
                        self.textPassword = self.emptyText
                        self.screen.blit(self.textPassword, (self.width/1.8927, self.height/3.1818)) #634 220
                    else:
                        self.screen.blit(self.textPassword, (self.width/1.8927, self.height/3.1818)) #634 220

                    if(self.partidas[self.currentPartida].nombre == ' '):
                        self.textNombrePartida = self.introduceText
                    else:
                        self.textNombrePartida = self.fuenteText.render(self.partidas[self.currentPartida].nombre, True, self.color_grey)
                    pygame.draw.rect(self.screen, self.color_grey, self.inputBox, 2)
                    self.screen.blit(self.textNombrePartida, (self.width/2.7650, self.height/10.7692)) #434 x 65
                    pygame.display.update() 
                    self.activeI2 = True
                    self.activeI = False
                    return 'configuracionPartida'
                else:
                    self.ch2.play(self.error)
                    return 'configuracionPartida'
            else:
                #nombre partida
                self.activeI = False
                self.activeI2 = False
                if(self.partidas[self.currentPartida].nombre == ' '):
                    self.textNombrePartida = self.introduceText
                else:
                    self.textNombrePartida = self.fuenteText.render(self.partidas[self.currentPartida].nombre, True, self.color_grey)

                if(self.partidas[self.currentPartida].server_code == ' '):
                    self.textPassword = self.introduceText2
                else:
                    self.textPassword = self.fuenteText.render(self.partidas[self.currentPartida].server_code, True, self.color_grey)
                self.refresh()
                pygame.draw.rect(self.screen, self.color_grey, self.inputBox, 2)
                self.screen.blit(self.textNombrePartida, (self.width/2.7650, self.height/10.7692)) #434 x 65
                #password
                pygame.draw.rect(self.screen, self.color_grey, self.inputBox2, 2)
                self.screen.blit(self.textPassword, (self.width/1.8927, self.height/3.1818)) #634 220
                pygame.display.update() 
                return 'configuracionPartida'
        
    def manageInputBox(self, key, unicode):
        if(self.activeI):
            self.activeI2 = False
            if key == pygame.K_RETURN:
                self.partidas[self.currentPartida].nombre = ' '
            elif key == pygame.K_BACKSPACE:
                self.partidas[self.currentPartida].nombre = self.partidas[self.currentPartida].nombre[:-1]
                if(len(self.partidas[self.currentPartida].nombre) == 0):
                    self.partidas[self.currentPartida].nombre = ' '
            else:
                if(len(self.partidas[self.currentPartida].nombre)<self.max_lenght_name):
                    if(self.partidas[self.currentPartida].nombre == ' '):
                        self.partidas[self.currentPartida].nombre = unicode
                    else:
                        self.partidas[self.currentPartida].nombre += unicode
                    #self.widthText = self.letterwidth*len(self.name)
                else:
                    self.ch2.play(self.error)
            self.refresh()
            pygame.draw.rect(self.screen, self.color_light_pink, self.inputBox, 2)
            self.textNombrePartida = self.fuenteText.render(self.partidas[self.currentPartida].nombre, True, self.color_light_pink)
            self.screen.blit(self.textNombrePartida, (self.width/2.7650, self.height/10.7692))

            if(self.partidas[self.currentPartida].server_code == ' '):
                self.textPassword = self.introduceText2
            else:
                self.textPassword = self.fuenteText.render(self.partidas[self.currentPartida].server_code, True, self.color_grey)
            #password
            pygame.draw.rect(self.screen, self.color_grey, self.inputBox2, 2)
            self.screen.blit(self.textPassword, (self.width/1.8927, self.height/3.1818)) #634 220
            pygame.display.update() 

        elif(self.activeI2):
            self.activeI = False
            if key == pygame.K_RETURN:
                self.partidas[self.currentPartida].server_code = ' '
            elif key == pygame.K_BACKSPACE:
                self.partidas[self.currentPartida].server_code = self.partidas[self.currentPartida].server_code[:-1]
                if(len(self.partidas[self.currentPartida].server_code) == 0):
                    self.partidas[self.currentPartida].server_code = ' '
            else:
                if(len(self.partidas[self.currentPartida].server_code)<self.max_lenght_name2):
                    if(self.partidas[self.currentPartida].server_code == ' '):
                        self.partidas[self.currentPartida].server_code = unicode
                    else:
                        self.partidas[self.currentPartida].server_code += unicode
                    #self.widthText = self.letterwidth*len(self.name)
                else:
                    self.ch2.play(self.error)
            self.refresh()
            if(self.partidas[self.currentPartida].nombre == ' '):
                self.textNombrePartida = self.introduceText
            else:
                self.textNombrePartida = self.fuenteText.render(self.partidas[self.currentPartida].nombre, True, self.color_grey)
            pygame.draw.rect(self.screen, self.color_grey, self.inputBox, 2)
            #self.screen.blit(pygame.transform.scale(self.textName, (self.widthText, self.height/14.0000)), (self.width/1.5894, self.height/6.6667))
            self.screen.blit(self.textNombrePartida, (self.width/2.7650, self.height/10.7692))

            #password
            pygame.draw.rect(self.screen, self.color_light_pink, self.inputBox2, 2)
            self.textPassword = self.fuenteText.render(self.partidas[self.currentPartida].server_code, True, self.color_light_pink)
            self.screen.blit(self.textPassword, (self.width/1.8927, self.height/3.1818)) #634 220
            pygame.display.update() 
        else:
            pass

    def movedMouse(self):
            x_size = self.width/4.0956
            y_size = self.height/12.2807
            x_start = self.width/2.4000
            y_start = self.height/1.1667
            x_startC = self.width/1.4760
            x_sizeI = self.width/4.8000
            y_sizeI = self.width/4.8000
            x_startI = self.width/12.0000
            y_startI = self.height/2.0000
            (x,y) = pygame.mouse.get_pos()

            #Botón volver al menú
            if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                if(not self.opened_screen):
                    self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/4.0956, self.height/12.2807)), (self.width/2.4000, self.height/1.1667))#293 57 500 600
                    self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/2.1053, self.height/1.1570)) #150 40 570 605
                    if((self.partidas[self.currentPartida].nombre != None and self.partidas[self.currentPartida].nombre != ' ') and (self.partidas[self.currentPartida].ubicacion_historia != None) and (self.partidas[self.currentPartida].server_code != None and self.partidas[self.currentPartida].server_code != ' ')):
                        self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/4.0956, self.height/12.2807)), (self.width/1.4760, self.height/1.1667))
                    else:
                        self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.4760, self.height/1.1667))
                
                    self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.3889, self.height/1.1570))
                    if(self.first_timeB):
                        self.first_timeB = False
                        self.first_timeC = True
                        self.first_timeI = True
                        self.first_timeBG = True
                        self.ch2.play(self.selected)     
                    pygame.display.update() 
                else:
                    self.first_timeC = True
                    self.first_timeB = True
                    self.first_timeI = True
                    self.first_timeBG = True
            #Botón crear partida
            elif(self.checkIfMouseIsInButton(x_size,y_size,x_startC,y_start,x,y)):
                if(not self.opened_screen):
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/4.0956, self.height/12.2807)), (self.width/2.4000, self.height/1.1667))#293 57 500 600
                    self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/2.1053, self.height/1.1570)) #150 40 570 605
                    if((self.partidas[self.currentPartida].nombre != None and self.partidas[self.currentPartida].nombre != ' ') and (self.partidas[self.currentPartida].ubicacion_historia != None) and (self.partidas[self.currentPartida].server_code != None and self.partidas[self.currentPartida].server_code != ' ')):
                        self.screen.blit(pygame.transform.scale(self.bCreate_selected, (self.width/4.0956, self.height/12.2807)), (self.width/1.4760, self.height/1.1667))
                        if(self.first_timeC):
                            self.first_timeC = False
                            self.first_timeB = True
                            self.first_timeI = True
                            self.first_timeBG = True
                            self.ch2.play(self.selected)     
                    else:
                        self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.4760, self.height/1.1667))
                        if(self.first_timeC):
                            self.first_timeC = False
                            self.first_timeB = True
                            self.first_timeI = True
                            self.first_timeBG = True
                    self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.3889, self.height/1.1570))
                    pygame.display.update() 
                else:
                    self.first_timeC = True
                    self.first_timeB = True
                    self.first_timeI = True
                    self.first_timeBG = True
            #Icono
            elif(self.checkIfMouseIsInButton(x_sizeI,y_sizeI,x_startI,y_startI,x,y)):
                if(not self.opened_screen):
                    if(self.partidas[self.currentPartida].ubicacion_historia != None):
                        self.screen.blit(pygame.transform.scale(self.ubicacionSelected[self.partidas[self.currentPartida].ubicacion_historia], (self.width/4.8000, self.width/4.8000)), (self.width/12.0000, self.height/2.0000))
                        if(self.first_timeI):
                            self.first_timeI = False
                            self.first_timeC = True
                            self.first_timeB = True
                            self.first_timeBG = True
                            self.ch2.play(self.selected)
                    else:
                        self.screen.blit(pygame.transform.scale(self.defaultSelected, (self.width/4.8000, self.width/4.8000)), (self.width/12.0000, self.height/2.0000)) #250w 250w 100 350 
                        self.screen.blit(pygame.transform.scale(self.select, (self.width/7.5000, self.height/21.8750)), (self.width/8.2759, self.height/1.5217)) #160 32 145 460
                        if(self.first_timeI):
                            self.first_timeI = False
                            self.first_timeC = True
                            self.first_timeB = True
                            self.first_timeBG = True
                            self.ch2.play(self.selected)
                    pygame.display.update() 
                else:
                    self.first_timeB = True
                    self.first_timeC = True
                    self.first_timeI = True
                    self.first_timeBG = True
            
            elif(self.opened_screen):
                x_size = self.width/3.8339
                y_size = self.height/12.2807
                x_start = self.width/1.6901
                y_start = self.height/1.4000
                if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
                    if(self.partidas[self.currentPartida].ubicacion_historia is not None and self.opened_screen):
                        self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.6901, self.height/1.4000))
                        self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/1.5789, self.height/1.3861))
                        if(self.first_timeBG):
                            self.first_timeBG = False  
                            self.first_timeB = True
                            self.first_timeC = True
                            self.first_timeI = True
                            self.ch1.play(self.selected)
                    elif(self.opened_screen):
                        self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.6901, self.height/1.4000))
                        self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/1.5789, self.height/1.3861))
                    else:
                        pass
                    pygame.display.update()
                else:
                    self.first_timeB = True
                    self.first_timeC = True
                    self.first_timeI = True
                    self.first_timeBG = True
                    if(self.partidas[self.currentPartida].ubicacion_historia is not None):
                        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/1.6901, self.height/1.4000))
                        self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/1.5789, self.height/1.3861))
                    else:
                        self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/3.8339, self.height/12.2807)), (self.width/1.6901, self.height/1.4000))
                        self.screen.blit(pygame.transform.scale(self.back2, (self.width/6.0000, self.height/17.5000)), (self.width/1.5789, self.height/1.3861))
                    self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/4.0956, self.height/12.2807)), (self.width/2.4000, self.height/1.1667))#293 57 500 600
                    self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/2.1053, self.height/1.1570)) #150 40 570 605
                    pygame.display.update()
            
            else:
                self.first_timeB = True
                self.first_timeC = True
                self.first_timeI = True
                self.first_timeBG = True
                self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/4.0956, self.height/12.2807)), (self.width/2.4000, self.height/1.1667))#293 57 500 600
                self.screen.blit(pygame.transform.scale(self.back, (self.width/8.0000, self.height/17.5000)), (self.width/2.1053, self.height/1.1570)) #150 40 570 605
                if((self.partidas[self.currentPartida].nombre != None and self.partidas[self.currentPartida].nombre != ' ') and (self.partidas[self.currentPartida].ubicacion_historia != None) and (self.partidas[self.currentPartida].server_code != None and self.partidas[self.currentPartida].server_code != ' ')):
                    self.screen.blit(pygame.transform.scale(self.bCreate, (self.width/4.0956, self.height/12.2807)), (self.width/1.4760, self.height/1.1667))
                else:
                    self.screen.blit(pygame.transform.scale(self.buttonUnavailablePic, (self.width/4.0956, self.height/12.2807)), (self.width/1.4760, self.height/1.1667))
                if(self.partidas[self.currentPartida].ubicacion_historia != None):
                    self.screen.blit(pygame.transform.scale(self.ubicacion[self.partidas[self.currentPartida].ubicacion_historia], (self.width/4.8000, self.width/4.8000)), (self.width/12.0000, self.height/2.0000))
                else:
                    self.screen.blit(pygame.transform.scale(self.default, (self.width/4.8000, self.width/4.8000)), (self.width/12.0000, self.height/2.0000)) #250w 250w 100 350 
                    self.screen.blit(pygame.transform.scale(self.select, (self.width/7.5000, self.height/21.8750)), (self.width/8.2759, self.height/1.5217)) #160 32 145 460
        
                
                self.screen.blit(pygame.transform.scale(self.crearT, (self.width/6.3158, self.height/17.5000)), (self.width/1.3889, self.height/1.1570))
                pygame.display.update() 