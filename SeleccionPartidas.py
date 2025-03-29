import pygame
from pygame.locals import *
from pygame import mixer
import sqlite3
from Partida import Partida

class SeleccionPartidas:
    #sound

    def __init__(self,width,height,screen,ch1,ch2,ch3,ch4,font,id):
        #screen
        self.screen = screen
        self.partidas = {0: None, 1: None, 2: None}
        self.font = font
        self.id = id

        #musica
        self.pressed =  pygame.mixer.Sound('sounds/button_pressed.wav')
        self.pressed_exit = pygame.mixer.Sound('sounds/button_pressed_ogg.ogg')
        self.selected = pygame.mixer.Sound('sounds/selected_button.wav')
        self.partida_deleted = pygame.mixer.Sound('sounds/error.wav')
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
        self.first_timeJ = True # Aún no has pulsado el botón online
        self.first_timeS1 = True # Aún no has pulsado el botón del slot 1
        self.first_timeB1 = True #las papeleras
        self.first_timeS2 = True # Aún no has pulsado el botón del slot 2
        self.first_timeB2 = True
        self.first_timeS3 = True # Aún no has pulsado el botón del slot 3
        self.first_timeB3 = True
        self.partidaToLoad = None
        self.pic = None
        self.name = None

        #cargamos las imágenes del menú
        self.backgroundPic = pygame.image.load("images/background.png")
        self.buttonPic = pygame.image.load("images/button.png")
        self.buttonSelectedPic = pygame.image.load("images/button_selected.png")
        self.buttonPressedPic = pygame.image.load("images/button_pressed.png")
        self.line = pygame.image.load("images/line.png")
        self.dice1 = pygame.image.load("images/dice_number.png")
        self.dice2 = pygame.image.load("images/dice_number2.png")
        self.dice3 = pygame.image.load("images/dice_number3.png")
        self.empty = pygame.image.load("images/empty_partida.png")
        self.empty_selected = pygame.image.load("images/empty_partida_selected.png")
        self.empty_pressed = pygame.image.load("images/empty_partida_pressed.png")
        self.filled = pygame.image.load("images/filled_partida.png")
        self.filled_selected = pygame.image.load("images/filled_partida_selected.png")
        self.filled_pressed = pygame.image.load("images/filled_partida_pressed.png")
        self.capa = pygame.image.load("images/capa.png")
        self.join = pygame.image.load("images/join_partida.png")
        self.join_selected = pygame.image.load("images/join_partida_selected.png")
        self.join_pressed = pygame.image.load("images/join_partida_pressed.png")
        self.bin = pygame.image.load("images/bin.png")
        self.bin_selected = pygame.image.load("images/bin_selected.png")
        self.bin_pressed = pygame.image.load("images/bin_pressed.png")
        
        #fuentes y colores
        self.fuente = pygame.font.SysFont(font, 70)
        self.color_white = (255,255,255)
        self.color_black = (0,0,0)
        self.light_pink = (244,201,208)
        self.light_purple = (255,111,241)
        self.back = self.fuente.render('Volver al menú', True, self.color_white)
        self.partidasText = self.fuente.render('Partidas', True, self.color_white)
        self.online = self.fuente.render('Online', True, self.color_white)
        self.labelP = {0: None, 1: None, 2: None}

    def setScreen(self,screen):
        self.screen = screen
    def getScreen(self):
        return self.screen
    def getPartidaToLoad(self):
        return self.partidaToLoad
    
    def loadPartida(self,row,p):
        self.partidas[p] = Partida()
        self.partidas[p].nombre = row[0]
        self.labelP[p] = self.fuente2.render(self.partidas[p].nombre, True, self.light_purple)

    def render(self,pic,name):
        self.pic = pic
        self.name = name
        #cargamos las partidas
        self.letterwidth = (self.width/3.4286)/11 #cálculo de la base en píxeles 
        self.lettersize = int(self.letterwidth + 0.5 * self.letterwidth) #multiplicamos la base x 0.5 y se lo sumamos a la base para hacerlo proporcional al tamaño que queremos
        self.fuente2 = pygame.font.SysFont(self.font, self.lettersize)
        conn = sqlite3.connect("simuladordnd.db")
        cur = conn.cursor()
        cur.execute("SELECT nombre FROM partida WHERE numPartida = 'p1'")
        rows = cur.fetchall()
        if(len(rows) != 0):
            self.loadPartida(rows[0],0)
        cur.execute("SELECT nombre FROM partida WHERE numPartida = 'p2'")
        rows = cur.fetchall()
        if(len(rows) != 0):
            self.loadPartida(rows[0],1)
        cur.execute("SELECT nombre FROM partida WHERE numPartida = 'p3'")
        rows = cur.fetchall()
        if(len(rows) != 0):
            self.loadPartida(rows[0],2)


        #vamos a comprobar el id de la bbdd:
        sql_get_me = "SELECT id_jugador,is_my_id FROM jugador"
        cur.execute(sql_get_me)
        rows = cur.fetchall()
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
                        cur.execute(query_update_id)
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
            cur.execute(query_save_me,data_jugador_yo)
            conn.commit() 
        else:
            #siempre actualizaremos nombre y pic del host por si hubieran sido modificados
            query_update_pic = "UPDATE jugador SET pic = "+str(self.pic)+" WHERE id_jugador = '"+self.id+"';"
            cur.execute(query_update_pic)
            query_update_name = "UPDATE jugador SET name = '"+self.name+"' WHERE id_jugador = '"+self.id+"';"
            cur.execute(query_update_name)
            conn.commit() 

        self.newGame = self.fuente2.render('+ Nueva Partida', True, self.light_pink)
        cur.close()
        conn.close() #cerramos la conexión con la bbdd

        #render screen
        self.screen.blit(pygame.transform.scale(self.backgroundPic, (self.width,self.height)), (0, 0)) #0,0 es la posición desde donde empieza a dibujar
        self.screen.blit(pygame.transform.scale(self.capa,  (self.width,self.height)), (0, 0))
        self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
        self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
        self.screen.blit(pygame.transform.scale(self.partidasText, (self.width/9.2308, self.height/17.5000)), (self.width/12.0000, self.height/11.6667)) #130 40 100 60
        self.screen.blit(pygame.transform.scale(self.line, (self.width/7.0588, self.height/46.6667)), (self.width/12.0000, self.height/7.3684)) # 170 15 100 95
        if(self.partidas[0] is None):
            self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
            self.screen.blit(self.newGame, (self.width/5.7143, self.height/4.1176)) # 210 170
        else:
            self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
            self.screen.blit(self.labelP[0], (self.width/5.0000, self.height/4.1176)) #240 170
            self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/4.1667)) #65 65 595 168
        self.screen.blit(pygame.transform.scale(self.dice1, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/4.6667)) #100 100 100 150
        if(self.partidas[1] is None):
            self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305
            self.screen.blit(self.newGame, (self.width/5.7143, self.height/2.1875))  #210 320
        else:  
            self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305  
            self.screen.blit(self.labelP[1], (self.width/5.0000, self.height/2.1875)) #240 320
            self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/2.2013)) #65 65 595 318 [+13]
        self.screen.blit(pygame.transform.scale(self.dice2, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/2.3333))#100 100 100 300
        if(self.partidas[2] is None):
            self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
            self.screen.blit(self.newGame, (self.width/5.7143, self.height/1.4894)) #210 470
        else:
            self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
            self.screen.blit(self.labelP[2], (self.width/5.0000, self.height/1.4894)) #240 470
            self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/1.4957)) #65 65 595 468
        self.screen.blit(pygame.transform.scale(self.dice3, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/1.5556)) #100 100 100 450
            
        self.screen.blit(pygame.transform.scale(self.join, (self.width/2.6667,self.width/2.6667)), (self.width/1.7391, self.height/5.6000-(abs(self.height/1.5556-self.width/2.6667))))#450 450 690 125
        self.screen.blit(pygame.transform.scale(self.online, (self.width/6.6667, self.height/10.0000)), (self.width/1.4581, self.height/2.2951-(abs(self.height/1.5556-self.width/2.6667))/3)) #180 70 823 305
        #self.width/1.6667
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
        x_sizeJ = self.width/2.6667
        y_sizeJ = self.width/2.6667
        x_startJ = self.width/1.7391
        y_startJ = self.height/5.6000-(abs(self.height/1.5556-self.width/2.6667))
        x_sizeS1 = self.width/2.1818
        y_sizeS1 = self.height/7.7778
        x_startS1 = self.width/8.8889
        y_startS1 = self.height/4.5161
        y_startS2 = self.height/2.2951
        y_startS3 =self.height/1.5385
        x_size_b1 = self.width/11.4286 #self.width/18.4615 -> 105
        y_size_b1 = self.height/7.5269 #self.height/10.7692 -> 93
        x_start_b1 = self.width/2.0690 #self.width/2.0168 ->  580
        y_start_b1 = self.height/4.5161  #self.height/4.1667 -> 155
        y_start_b2 = self.height/2.2951 #self.height/2.2013 -> 305
        y_start_b3 = self.height/1.5385 #self.height/1.4957 -> 455
        
        (x,y) = pygame.mouse.get_pos()

        #Botón volver al menú
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPressedPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            self.screen.blit(pygame.transform.scale(self.join, (self.width/2.6667,self.width/2.6667)), (self.width/1.7391, self.height/5.6000-(abs(self.height/1.5556-self.width/2.6667)))) #450 450 720 140
            self.screen.blit(pygame.transform.scale(self.online, (self.width/6.6667, self.height/10.0000)), (self.width/1.4581, self.height/2.2951-(abs(self.height/1.5556-self.width/2.6667))/3)) #180 70 853 320
            
            self.ch1.play(self.pressed)
            pygame.display.update() 
            return 'menu'
        
        #Botón online
        elif(self.checkIfMouseIsInButton(x_sizeJ,y_sizeJ,x_startJ,y_startJ,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            self.screen.blit(pygame.transform.scale(self.join_pressed, (self.width/2.6667,self.width/2.6667)), (self.width/1.7391, self.height/5.6000-(abs(self.height/1.5556-self.width/2.6667)))) #450 450 720 140
            self.screen.blit(pygame.transform.scale(self.online, (self.width/6.6667, self.height/10.0000)), (self.width/1.4581, self.height/2.2951-(abs(self.height/1.5556-self.width/2.6667))/3)) #180 70 853 320
            self.ch3.play(self.pressed)
            pygame.display.update() 
            return 'joinPartida'
        
        #Botón slot 1
        elif(self.checkIfMouseIsInButton(x_sizeS1,y_sizeS1,x_startS1,y_startS1,x,y)):
            pantalla = 'configuracionPartida'
            deleted = False
            if(self.partidas[0] is None):
                self.screen.blit(pygame.transform.scale(self.empty_pressed, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/4.1176)) #210 170
                self.partidaToLoad = "p1"
            else:
                if(self.checkIfMouseIsInButton(x_size_b1,y_size_b1,x_start_b1,y_start_b1,x,y)):
                    self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                    self.screen.blit(self.labelP[0], (self.width/5.0000, self.height/4.1176)) #240 170
                    self.screen.blit(pygame.transform.scale(self.bin_pressed, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/4.1667)) #65 65 595 168
                    #Eliminamos la partida--------------
                    pantalla = 'seleccionPartidas'
                    self.partidas[0] = None
                    conn = sqlite3.connect("simuladordnd.db")
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM partida WHERE numPartida='p1'")
                    conn.commit()
                    cursor.close()
                    conn.close() #cerramos la conexión con la bbdd
                    #------------------------------------
                    self.ch3.play(self.partida_deleted) 
                    deleted = True
                    self.movedMouse() #para refrescar la pantalla -> actualizar el slot a vacío
                else:
                    self.screen.blit(pygame.transform.scale(self.filled_pressed, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                    self.screen.blit(self.labelP[0], (self.width/5.0000, self.height/4.1176)) #240 170
                    self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/4.1667)) #65 65 595 168
                    self.partidaToLoad = "p1"
                    pantalla = 'salaEspera'
            self.screen.blit(pygame.transform.scale(self.dice1, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/4.6667)) #100 100 100 150
            if(self.partidas[1] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/2.1875)) #210 320
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305
                self.screen.blit(self.labelP[1], (self.width/5.0000, self.height/2.1875)) #240 320
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/2.2013)) #65 65 595 318 [+13]
            self.screen.blit(pygame.transform.scale(self.dice2, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/2.3333))#100 100 100 300
            if(self.partidas[2] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/1.4894)) #210 470
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                self.screen.blit(self.labelP[2], (self.width/5.0000, self.height/1.4894)) #240 470
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/1.4957)) #65 65 595 468
            self.screen.blit(pygame.transform.scale(self.dice3, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/1.5556)) #100 100 100 450
            if(not deleted):
                self.ch1.play(self.pressed)
            pygame.display.update() 
            return pantalla
        
        #Botón slot 2
        elif(self.checkIfMouseIsInButton(x_sizeS1,y_sizeS1,x_startS1,y_startS2,x,y)):
            pantalla = 'configuracionPartida'
            deleted = False
            if(self.partidas[0] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/4.1176)) #210 170
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                self.screen.blit(self.labelP[0], (self.width/5.0000, self.height/4.1176)) #240 170
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/4.1667)) #65 65 595 168
            self.screen.blit(pygame.transform.scale(self.dice1, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/4.6667)) #100 100 100 150
            if(self.partidas[1] is None):
                self.screen.blit(pygame.transform.scale(self.empty_pressed, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/2.1875)) #210 320
                self.partidaToLoad = "p2"
            else:
                if(self.checkIfMouseIsInButton(x_size_b1,y_size_b1,x_start_b1,y_start_b2,x,y)):
                    self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305    
                    self.screen.blit(self.labelP[1], (self.width/5.0000, self.height/2.1875)) #240 320
                    self.screen.blit(pygame.transform.scale(self.bin_pressed, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/2.2013)) #65 65 595 318 [+13]
                    #TODO: borrar partida
                    pantalla = 'seleccionPartidas'
                    self.partidas[1] = None
                    conn = sqlite3.connect("simuladordnd.db")
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM partida WHERE numPartida='p2'")
                    conn.commit()
                    cursor.close()
                    conn.close() #cerramos la conexión con la bbdd
                    #------------------------------------
                    deleted = True
                    self.ch3.play(self.partida_deleted)
                    self.movedMouse()
                else:
                    self.screen.blit(pygame.transform.scale(self.filled_pressed, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305    
                    self.screen.blit(self.labelP[1], (self.width/5.0000, self.height/2.1875)) #240 320
                    self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/2.2013)) #65 65 595 318 [+13]
                    self.partidaToLoad = "p2"
                    pantalla = 'salaEspera'
            self.screen.blit(pygame.transform.scale(self.dice2, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/2.3333))#100 100 100 300
            if(self.partidas[2] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/1.4894)) #210 470
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                self.screen.blit(self.labelP[2], (self.width/5.0000, self.height/1.4894)) #240 470
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/1.4957)) #65 65 595 468
            self.screen.blit(pygame.transform.scale(self.dice3, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/1.5556)) #100 100 100 450
            if(not deleted):
                self.ch1.play(self.pressed)
            pygame.display.update() 
            return pantalla
        
        #Botón slot 3
        elif(self.checkIfMouseIsInButton(x_sizeS1,y_sizeS1,x_startS1,y_startS3,x,y)):
            pantalla = 'configuracionPartida'
            deleted = False
            if(self.partidas[0] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/4.1176)) #210 170
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                self.screen.blit(self.labelP[0], (self.width/5.0000, self.height/4.1176)) #240 170
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/4.1667)) #65 65 595 168
            self.screen.blit(pygame.transform.scale(self.dice1, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/4.6667)) #100 100 100 150
            if(self.partidas[1] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/2.1875)) #210 320
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305
                self.screen.blit(self.labelP[1], (self.width/5.0000, self.height/2.1875)) #240 320
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/2.2013)) #65 65 595 318 [+13]
            self.screen.blit(pygame.transform.scale(self.dice2, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/2.3333))#100 100 100 300
            if(self.partidas[2] is None):
                self.screen.blit(pygame.transform.scale(self.empty_pressed, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/1.4894)) #210 470
                self.partidaToLoad = "p3"
            else:
                if(self.checkIfMouseIsInButton(x_size_b1,y_size_b1,x_start_b1,y_start_b3,x,y)):
                    self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                    self.screen.blit(self.labelP[2], (self.width/5.0000, self.height/1.4894)) #240 470
                    self.screen.blit(pygame.transform.scale(self.bin_pressed, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/1.4957)) #65 65 595 468
                    pantalla = 'seleccionPartidas'
                    self.partidas[2] = None
                    conn = sqlite3.connect("simuladordnd.db")
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM partida WHERE numPartida='p3'")
                    conn.commit()
                    cursor.close()
                    conn.close() #cerramos la conexión con la bbdd
                    #------------------------------------
                    deleted = True
                    self.ch3.play(self.partida_deleted)
                    self.movedMouse()
                else:
                    self.screen.blit(pygame.transform.scale(self.filled_pressed, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                    self.screen.blit(self.labelP[2], (self.width/5.0000, self.height/1.4894)) #240 470
                    self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/1.4957)) #65 65 595 468
                    self.partidaToLoad = "p3"
                    pantalla = 'salaEspera'
            self.screen.blit(pygame.transform.scale(self.dice3, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/1.5556)) #100 100 100 450
            if(not deleted):
                self.ch1.play(self.pressed)
            pygame.display.update() 
            return pantalla

        else:
            return 'seleccionPartidas'
        

    def movedMouse(self):
        x_size = self.width/3.8339
        y_size = self.height/12.2807
        x_start = self.width/2.7907
        y_start = self.height/1.1667
        x_sizeJ = self.width/2.6667
        y_sizeJ = self.width/2.6667
        x_startJ = self.width/1.7391
        y_startJ = self.height/5.6000-(abs(self.height/1.5556-self.width/2.6667))
        x_sizeS1 = self.width/2.1818
        y_sizeS1 = self.height/7.7778
        x_startS1 = self.width/8.8889
        y_startS1 = self.height/4.5161
        y_startS2 = self.height/2.2951
        y_startS3 =self.height/1.5385
        x_size_b1 = self.width/11.4286 #self.width/18.4615 -> 105
        y_size_b1 = self.height/7.5269 #self.height/10.7692 -> 93
        x_start_b1 = self.width/2.0690 #self.width/2.0168 ->  580
        y_start_b1 = self.height/4.5161  #self.height/4.1667 -> 155
        y_start_b2 = self.height/2.2951 #self.height/2.2013 -> 305
        y_start_b3 = self.height/1.5385 #self.height/1.4957 -> 455
        (x,y) = pygame.mouse.get_pos()

        #Botón volver al menú
        if(self.checkIfMouseIsInButton(x_size,y_size,x_start,y_start,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonSelectedPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(self.partidas[0] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/4.1176)) #210 170
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                self.screen.blit(self.labelP[0], (self.width/5.0000, self.height/4.1176)) #240 170
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/4.1667)) #65 65 595 168
            self.screen.blit(pygame.transform.scale(self.dice1, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/4.6667)) #100 100 100 150
            if(self.partidas[1] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/2.1875)) #210 320
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305  
                self.screen.blit(self.labelP[1], (self.width/5.0000, self.height/2.1875)) #240 320
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/2.2013)) #65 65 595 318 [+13]
            self.screen.blit(pygame.transform.scale(self.dice2, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/2.3333))#100 100 100 300
            if(self.partidas[2] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/1.4894)) #210 470
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                self.screen.blit(self.labelP[2], (self.width/5.0000, self.height/1.4894)) #240 470
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/1.4957)) #65 65 595 468
            self.screen.blit(pygame.transform.scale(self.dice3, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/1.5556)) #100 100 100 450
        
            self.screen.blit(pygame.transform.scale(self.join, (self.width/2.6667,self.width/2.6667)), (self.width/1.7391, self.height/5.6000-(abs(self.height/1.5556-self.width/2.6667)))) #450 450 720 140
            self.screen.blit(pygame.transform.scale(self.online, (self.width/6.6667, self.height/10.0000)), (self.width/1.4581, self.height/2.2951-(abs(self.height/1.5556-self.width/2.6667))/3)) #180 70 853 320
            if(self.first_timeB):
                self.first_timeB = False
                self.first_timeJ = True
                self.first_timeS1 = True
                self.first_timeS2 = True
                self.first_timeS3 = True
                self.first_timeB1 = True
                self.first_timeB2 = True
                self.first_timeB3 = True
                self.ch2.play(self.selected)     
            pygame.display.update() 
        
        #Botón online
        elif(self.checkIfMouseIsInButton(x_sizeJ,y_sizeJ,x_startJ,y_startJ,x,y)):
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(self.partidas[0] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/4.1176)) #210 170
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                self.screen.blit(self.labelP[0], (self.width/5.0000, self.height/4.1176)) #240 170
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/4.1667)) #65 65 595 168
            self.screen.blit(pygame.transform.scale(self.dice1, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/4.6667)) #100 100 100 150
            if(self.partidas[1] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/2.1875)) #210 320
            else: 
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305  
                self.screen.blit(self.labelP[1], (self.width/5.0000, self.height/2.1875)) #240 320
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/2.2013)) #65 65 595 318 [+13]
            self.screen.blit(pygame.transform.scale(self.dice2, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/2.3333))#100 100 100 300
            if(self.partidas[2] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/1.4894)) #210 470
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                self.screen.blit(self.labelP[2], (self.width/5.0000, self.height/1.4894)) #240 470
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/1.4957)) #65 65 595 468
            self.screen.blit(pygame.transform.scale(self.dice3, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/1.5556)) #100 100 100 450
        
            self.screen.blit(pygame.transform.scale(self.join_selected, (self.width/2.6667,self.width/2.6667)), (self.width/1.7391, self.height/5.6000-(abs(self.height/1.5556-self.width/2.6667)))) #450 450 720 140
            self.screen.blit(pygame.transform.scale(self.online, (self.width/6.6667, self.height/10.0000)), (self.width/1.4581, self.height/2.2951-(abs(self.height/1.5556-self.width/2.6667))/3)) #180 70 853 320
            if(self.first_timeB):
                self.first_timeB = False
                self.first_timeJ = True
                self.first_timeS1 = True
                self.first_timeS2 = True
                self.first_timeS3 = True
                self.first_timeB1 = True
                self.first_timeB2 = True
                self.first_timeB3 = True
                self.ch2.play(self.selected)     
            pygame.display.update() 
        
        #Botón slot 1
        elif(self.checkIfMouseIsInButton(x_sizeS1,y_sizeS1,x_startS1,y_startS1,x,y)):
            if(self.partidas[0] is None):
                self.screen.blit(pygame.transform.scale(self.empty_selected, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/4.1176)) #210 170
                if(self.first_timeS1):
                    self.first_timeS1 = False
                    self.first_timeB1 = True
                    self.first_timeS2 = True
                    self.first_timeS3 = True
                    self.first_timeB = True
                    self.first_timeJ = True
                    self.first_timeB2 = True
                    self.first_timeB3 = True
                    self.ch2.play(self.selected) 
            else:
                if(self.checkIfMouseIsInButton(x_size_b1,y_size_b1,x_start_b1,y_start_b1,x,y)):
                    self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                    self.screen.blit(self.labelP[0], (self.width/5.0000, self.height/4.1176)) #240 170
                    self.screen.blit(pygame.transform.scale(self.bin_selected, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/4.1667)) #65 65 595 168
                    if(self.first_timeB1):
                        self.first_timeB1 = False
                        self.first_timeS1 = True
                        self.first_timeS2 = True
                        self.first_timeS3 = True
                        self.first_timeB = True
                        self.first_timeJ = True
                        self.first_timeB2 = True
                        self.first_timeB3 = True
                        self.ch2.play(self.selected) 
                else:
                    self.screen.blit(pygame.transform.scale(self.filled_selected, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                    self.screen.blit(self.labelP[0], (self.width/5.0000, self.height/4.1176)) #240 170
                    self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/4.1667)) #65 65 595 168
                    if(self.first_timeS1):
                        self.first_timeS1 = False
                        self.first_timeB1 = True
                        self.first_timeS2 = True
                        self.first_timeS3 = True
                        self.first_timeB = True
                        self.first_timeJ = True
                        self.first_timeB2 = True
                        self.first_timeB3 = True
                        self.ch2.play(self.selected) 
            self.screen.blit(pygame.transform.scale(self.dice1, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/4.6667)) #100 100 100 150
            if(self.partidas[1] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/2.1875)) #210 320
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305
                self.screen.blit(self.labelP[1], (self.width/5.0000, self.height/2.1875)) #240 320
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/2.2013)) #65 65 595 318 [+13]
            self.screen.blit(pygame.transform.scale(self.dice2, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/2.3333))#100 100 100 300
            if(self.partidas[2] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/1.4894)) #210 470
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                self.screen.blit(self.labelP[2], (self.width/5.0000, self.height/1.4894)) #240 470
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/1.4957)) #65 65 595 468
            self.screen.blit(pygame.transform.scale(self.dice3, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/1.5556)) #100 100 100 450
            self.screen.blit(pygame.transform.scale(self.join, (self.width/2.6667,self.width/2.6667)), (self.width/1.7391, self.height/5.6000-(abs(self.height/1.5556-self.width/2.6667)))) #450 450 720 140
            self.screen.blit(pygame.transform.scale(self.online, (self.width/6.6667, self.height/10.0000)), (self.width/1.4581, self.height/2.2951-(abs(self.height/1.5556-self.width/2.6667))/3)) #180 70 853 320    
            pygame.display.update() 
            
        
        #Botón slot 2
        elif(self.checkIfMouseIsInButton(x_sizeS1,y_sizeS1,x_startS1,y_startS2,x,y)):
            if(self.partidas[0] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/4.1176)) #210 170
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                self.screen.blit(self.labelP[0], (self.width/5.0000, self.height/4.1176)) #240 170
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/4.1667)) #65 65 595 168
            self.screen.blit(pygame.transform.scale(self.dice1, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/4.6667)) #100 100 100 150
            if(self.partidas[1] is None):
                self.screen.blit(pygame.transform.scale(self.empty_selected, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/2.1875)) #210 320
                if(self.first_timeS2):
                    self.first_timeS2 = False
                    self.first_timeB1 = True
                    self.first_timeS1 = True
                    self.first_timeS3 = True
                    self.first_timeB = True
                    self.first_timeJ = True
                    self.first_timeB2 = True
                    self.first_timeB3 = True
                    self.ch2.play(self.selected) 
            else:
                if(self.checkIfMouseIsInButton(x_size_b1,y_size_b1,x_start_b1,y_start_b2,x,y)):
                    self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305    
                    self.screen.blit(self.labelP[1], (self.width/5.0000, self.height/2.1875)) #240 320
                    self.screen.blit(pygame.transform.scale(self.bin_selected, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/2.2013)) #65 65 595 318 [+13]
                    if(self.first_timeB2):
                        self.first_timeB2 = False
                        self.first_timeS1 = True
                        self.first_timeS2 = True
                        self.first_timeS3 = True
                        self.first_timeB = True
                        self.first_timeJ = True
                        self.first_timeS2 = True
                        self.first_timeB3 = True
                        self.ch2.play(self.selected) 
                else:
                    self.screen.blit(pygame.transform.scale(self.filled_selected, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305    
                    self.screen.blit(self.labelP[1], (self.width/5.0000, self.height/2.1875)) #240 320
                    self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/2.2013)) #65 65 595 318 [+13]
                    if(self.first_timeS2):
                        self.first_timeS2 = False
                        self.first_timeS1 = True
                        self.first_timeB2 = True
                        self.first_timeS3 = True
                        self.first_timeB = True
                        self.first_timeJ = True
                        self.first_timeB1 = True
                        self.first_timeB3 = True
                        self.ch2.play(self.selected) 
            self.screen.blit(pygame.transform.scale(self.dice2, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/2.3333))#100 100 100 300
            if(self.partidas[2] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/1.4894)) #210 470
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                self.screen.blit(self.labelP[2], (self.width/5.0000, self.height/1.4894)) #240 470
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/1.4957)) #65 65 595 468
            self.screen.blit(pygame.transform.scale(self.dice3, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/1.5556)) #100 100 100 450
            self.screen.blit(pygame.transform.scale(self.join, (self.width/2.6667,self.width/2.6667)), (self.width/1.7391, self.height/5.6000-(abs(self.height/1.5556-self.width/2.6667)))) #450 450 720 140
            self.screen.blit(pygame.transform.scale(self.online, (self.width/6.6667, self.height/10.0000)), (self.width/1.4581, self.height/2.2951-(abs(self.height/1.5556-self.width/2.6667))/3)) #180 70 853 320   
            pygame.display.update() 
           
        
        #Botón slot 3
        elif(self.checkIfMouseIsInButton(x_sizeS1,y_sizeS1,x_startS1,y_startS3,x,y)):
            if(self.partidas[0] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/4.1176)) #210 170
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                self.screen.blit(self.labelP[0], (self.width/5.0000, self.height/4.1176)) #240 170
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/4.1667)) #65 65 595 168
            self.screen.blit(pygame.transform.scale(self.dice1, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/4.6667)) #100 100 100 150
            if(self.partidas[1] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/2.1875)) #210 320
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305
                self.screen.blit(self.labelP[1], (self.width/5.0000, self.height/2.1875)) #240 320
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/2.2013)) #65 65 595 318 [+13]
            self.screen.blit(pygame.transform.scale(self.dice2, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/2.3333))#100 100 100 300
            if(self.partidas[2] is None):
                self.screen.blit(pygame.transform.scale(self.empty_selected, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/1.4894)) #210 470
                if(self.first_timeS3):
                    self.first_timeS3 = False
                    self.first_timeB1 = True
                    self.first_timeS1 = True
                    self.first_timeS2 = True
                    self.first_timeB = True
                    self.first_timeJ = True
                    self.first_timeB2 = True
                    self.first_timeB3 = True
                    self.ch2.play(self.selected) 
            else:
                if(self.checkIfMouseIsInButton(x_size_b1,y_size_b1,x_start_b1,y_start_b3,x,y)):
                    self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                    self.screen.blit(self.labelP[2], (self.width/5.0000, self.height/1.4894)) #240 470
                    self.screen.blit(pygame.transform.scale(self.bin_selected, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/1.4957)) #65 65 595 468
                    if(self.first_timeB3):
                        self.first_timeB3 = False
                        self.first_timeS1 = True
                        self.first_timeS2 = True
                        self.first_timeS3 = True
                        self.first_timeB = True
                        self.first_timeJ = True
                        self.first_timeB2 = True
                        self.first_timeB1 = True
                        self.ch2.play(self.selected) 
                else:
                    self.screen.blit(pygame.transform.scale(self.filled_selected, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                    self.screen.blit(self.labelP[2], (self.width/5.0000, self.height/1.4894)) #240 470
                    self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/1.4957)) #65 65 595 468
                    if(self.first_timeS3):
                        self.first_timeS3 = False
                        self.first_timeS1 = True
                        self.first_timeS2 = True
                        self.first_timeB1 = True
                        self.first_timeB = True
                        self.first_timeJ = True
                        self.first_timeB2 = True
                        self.first_timeB3 = True
                        self.ch2.play(self.selected) 
            self.screen.blit(pygame.transform.scale(self.dice3, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/1.5556)) #100 100 100 450
            self.screen.blit(pygame.transform.scale(self.join, (self.width/2.6667,self.width/2.6667)), (self.width/1.7391, self.height/5.6000-(abs(self.height/1.5556-self.width/2.6667)))) #450 450 720 140
            self.screen.blit(pygame.transform.scale(self.online, (self.width/6.6667, self.height/10.0000)), (self.width/1.4581, self.height/2.2951-(abs(self.height/1.5556-self.width/2.6667))/3)) #180 70 853 320  
            pygame.display.update() 
            
        else:
            self.first_timeB = True
            self.first_timeJ = True
            self.first_timeS1 = True
            self.first_timeS2 = True
            self.first_timeS3 = True
            self.first_timeB1 = True
            self.first_timeB2 = True
            self.first_timeB3 = True
            self.screen.blit(pygame.transform.scale(self.buttonPic, (self.width/3.8339, self.height/12.2807)), (self.width/2.7907, self.height/1.1667))
            self.screen.blit(pygame.transform.scale(self.back, (self.width/6.3158, self.height/17.5000)), (self.width/2.4490, self.height/1.1570))
            if(self.partidas[0] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/4.1176)) #210 170
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/4.5161)) #550 90 135 155
                self.screen.blit(self.labelP[0], (self.width/5.0000, self.height/4.1176)) #240 170
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/4.1667)) #65 65 595 168
            self.screen.blit(pygame.transform.scale(self.dice1, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/4.6667)) #100 100 100 150
            if(self.partidas[1] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/2.1875)) #210 320
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/2.2951))  #550 90 135 305  
                self.screen.blit(self.labelP[1], (self.width/5.0000, self.height/2.1875)) #240 320
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/2.2013)) #65 65 595 318 [+13]
            self.screen.blit(pygame.transform.scale(self.dice2, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/2.3333))#100 100 100 300
            if(self.partidas[2] is None):
                self.screen.blit(pygame.transform.scale(self.empty, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                self.screen.blit(self.newGame, (self.width/5.7143, self.height/1.4894)) #210 470
            else:
                self.screen.blit(pygame.transform.scale(self.filled, (self.width/2.1818, self.height/7.7778)), (self.width/8.8889, self.height/1.5385))  #550 90 135 455
                self.screen.blit(self.labelP[2], (self.width/5.0000, self.height/1.4894)) #240 470
                self.screen.blit(pygame.transform.scale(self.bin, (self.width/18.4615, self.height/10.7692)), (self.width/2.0168, self.height/1.4957)) #65 65 595 468
            self.screen.blit(pygame.transform.scale(self.dice3, (self.height/7.0000, self.height/7.0000)), ((self.width/8.8889)-(self.height/14.0000), self.height/1.5556)) #100 100 100 450
        
            
            self.screen.blit(pygame.transform.scale(self.join, (self.width/2.6667,self.width/2.6667)), (self.width/1.7391, self.height/5.6000-(abs(self.height/1.5556-self.width/2.6667)))) #450 450 720 140
            self.screen.blit(pygame.transform.scale(self.online, (self.width/6.6667, self.height/10.0000)), (self.width/1.4581, self.height/2.2951-(abs(self.height/1.5556-self.width/2.6667))/3)) #180 70 853 320
            pygame.display.update() 
