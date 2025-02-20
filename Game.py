import pygame
from pygame.locals import *
from pygame import mixer
import sys
from Menu import Menu
from Credits import Credits
from Config import Config
from Login import Login
from SeleccionPartidas import SeleccionPartidas
import os
from Configuracion import Configuracion
from Jugador import Jugador
from SalaEspera import SalaEspera
from CrearTablas import CrearTablas
from ConfiguracionPartida import ConfiguracionPartida
from UnionPartida import UnionPartida
from Global import Global
from ServerDisconected import ServerDisconected
from SeleccionPersonaje import SeleccionPersonaje
import socket
import threading
#import requests


class Game:
    #inits
    def __init__(self):
        pygame.init()
        self.font = 'agencyfb'
        #self.font = 'agencyfbnormal'
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) 
        #self.screen = pygame.display.set_mode((1500,600)) #para pruebas de tamaño 1
        #self.screen = pygame.display.set_mode((974,550)) #para pruebas de tamaño 2
        info = pygame.display.Info()
        self.msg_delay = 0.2
        #print(info.current_w,info.current_h)
        rel = (info.current_w/info.current_h)
        if(1.7 <= rel <= 1.8): #aprox 16 x 9 -> 1.77
            self.width,self.height= (self.screen.get_width(), self.screen.get_height())
            #se queda Fullscreen
            pass
        elif(rel < 1.7):
            temp_width,temp_height= (self.screen.get_width(), self.screen.get_height())
            for i in reversed(range(0,temp_height)):
                n_rel = temp_width/i
                if(1.7 <= n_rel <= 1.8):
                    self.width,self.height= (temp_width,i)
                    break
                else:
                    pass

        else: #mayor de 1.8
            temp_width,temp_height= (self.screen.get_width(), self.screen.get_height())
            for i in reversed(range(0,temp_width)):
                n_rel = i/temp_height
                if(1.7 <= n_rel <= 1.8):
                    self.width,self.height= (i,temp_height)
                    break
                else:
                    pass


        os.environ['SDL_VIDEODRIVER'] = 'dummy'

        pygame.font.init()
        pygame.mixer.init()
        self.configuration = Configuracion()
        self.configuration.loadConfigurationFromFile()
        self.perfil = Jugador()
        self.perfil.loadPerfilFromFile()
        #print(self.configuration.getConfiguration())

        self.clock = pygame.time.Clock()

        self.ch1 = pygame.mixer.Channel(0)
        self.ch2 = pygame.mixer.Channel(1)
        self.ch3 = pygame.mixer.Channel(2)
        self.ch4 = pygame.mixer.Channel(3)
        self.ch5 = pygame.mixer.Channel(4) #para el hilo de TCP
        self.minimized = False
        self.online = False #para pasarselo como parámetro a self.joinPartida y saber cuál de las 2 pantallas cargar

        gestor_bbdd = CrearTablas() #creamos todas las tablas para la bbdd e insertamos los datos necesarios 

        #establecemos la configuración de volumen de la música
        self.change_music(self.configuration.volMusica,self.configuration.volEffects)

        self.changedScreen = False #si está a true, se refrescará la pantalla que diga currentScreen
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.local_ip,self.public_ip = self.getLocalAndPublicIP()
        self.local_ip = self.getLocalIP()
        #(self.freePortTCP, self.freePortUDP) = self.findFreePort()
        
        self.max_length_name = 13
        pygame.display.set_caption('DND_Simulator') #nombre de la ventana
        self.currentScreen = "menu"
        self.GLOBAL = Global()
        self.GLOBAL.setNoEnPartida() #establecemos que no está en partida
        self.GLOBAL.initialize() #inicializamos las variables globales
        self.menu = Menu(self.width, self.height,self.screen,self.ch1,self.ch2,self.ch3,self.ch4,self.perfil.logged,self.perfil.avatarPicPerfil,self.perfil.name,self.font)
        self.credits = Credits(self.width, self.height,None,self.ch1,self.ch2,self.ch3,self.ch4,self.font)
        self.options = Config(self.width, self.height,None,self.ch1,self.ch2,self.ch3,self.ch4,self.configuration.fps,self.configuration.dmVoice,self.configuration.volMusica, self.configuration.volEffects,self.font)
        self.login = Login(self.width, self.height,None,self.ch1,self.ch2,self.ch3,self.ch4,self.perfil.name,self.perfil.logged,self.perfil.avatarPicPerfil,self.max_length_name,self.font)
        self.seleccionPartidas = SeleccionPartidas(self.width, self.height,None,self.ch1,self.ch2,self.ch3,self.ch4,self.font,self.perfil.id)
        self.configuracionPartida = ConfiguracionPartida(self.width, self.height,None,self.ch1,self.ch2,self.ch3,self.ch4,self.local_ip,self.font,self.perfil.id)
        self.salaEspera = SalaEspera(self.width, self.height,None,self.ch1,self.ch2,self.ch3,self.ch4,self.perfil.avatarPicPerfil,self.perfil.name,self.max_length_name,self.local_ip,self.font,self.perfil.id,self.msg_delay,self.ch5)
        self.joinPartida = UnionPartida(self.width, self.height,None,self.ch1,self.ch2,self.ch3,self.ch4,self.font,self.perfil.id)
        self.serverDisc = ServerDisconected(self.width, self.height,None,self.ch1,self.ch2,self.ch3,self.ch4,self.font)
        self.seleccionPersonaje = SeleccionPersonaje(self.width, self.height,None,self.ch1,self.ch2,self.ch3,self.ch4,self.font,self.perfil.id)
        #Cargamos la música, y precargamos las imágenes y textos en el bufer
        mixer.music.load('sounds/background.wav')
        mixer.music.play(-1)
        

    def run(self):
        self.menu.render()
        while self.currentScreen != 'quit':
            #nombre del simulador
            screenToRefresh = self.GLOBAL.getRefreshScreen()
            if screenToRefresh != None:
                #nos ha llegado información de los hilos
                if screenToRefresh == "salaEspera" and not self.GLOBAL.getNoEnPartida(): #como estamos ya en esa sala, no hace falta cambiar la pantalla
                    self.GLOBAL.setRefreshScreen(None)
                    self.salaEspera.refresh() #refrescamos la pantalla
                elif screenToRefresh == "server_disc":
                    self.currentScreen = screenToRefresh
                    self.GLOBAL.setCurrentScreen(screenToRefresh)
                    self.GLOBAL.setRefreshScreen(None)
                    self.screen = self.salaEspera.getScreen() #es la única forma de tomar la pantalla
                    self.serverDisc.setScreen(self.screen)
                    self.salaEspera.escuchaUDP.closeSocketUDPServer()
                    self.salaEspera.enviarEstadoUDP.desconectar()
                    self.joinPartida.escuchaTCPClient.closeSocketTCPServerSinMSG()
                    self.serverDisc.render()
                elif screenToRefresh == "seleccionPersonaje":
                    self.currentScreen = screenToRefresh
                    self.GLOBAL.setCurrentScreen(screenToRefresh)
                    self.GLOBAL.setRefreshScreen(None)
                    self.screen = self.salaEspera.getScreen()
                    self.seleccionPersonaje.setScreen(self.screen)
                    self.seleccionPersonaje.render(self.online)
                else:
                    pass

            if pygame.display.get_active() and self.minimized:
                self.minimized = False #ya hemos renderizado de nuevo los objetos
                if self.currentScreen == "menu":
                    self.menu.render()
                elif self.currentScreen == "credits":
                    self.credits.render()
                elif self.currentScreen == "options":
                    self.options.render()
                elif self.currentScreen == "login":
                    self.login.render()
                elif self.currentScreen == "seleccionPartidas":
                    self.seleccionPartidas.render(self.perfil.avatarPicPerfil,self.perfil.name)
                elif self.currentScreen == "configuracionPartida":
                    self.configuracionPartida.render(self.perfil.avatarPicPerfil,self.perfil.name)
                elif self.currentScreen == "salaEspera":
                    self.salaEspera.render(self.online)
                elif self.currentScreen == "joinPartida":
                    self.joinPartida.render()
                elif self.currentScreen == "server_disc":
                    self.serverDisc.render()
                elif self.currentScreen == "seleccionPersonaje":
                    self.seleccionPersonaje.render(self.online)
            if not pygame.display.get_active():
                self.minimized = True #se ha hecho escape para ir al escritorio

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.currentScreen = 'quit'
                    self.GLOBAL.setCurrentScreen('quit')
                #si le maximiza, o resizea la pantalla
                #elif event.type == VIDEORESIZE: #no lo voy a permitir
                #    self.width,self.height= (self.screen.get_width(), self.screen.get_height())
                    #print(self.width,self.height)
                #    size = event.dict['size']
                #    if self.currentScreen == "menu":
                #        self.menu.resize(self.width,self.height,size)
                #    elif self.currentScreen == "credits":
                #        self.credits.resize(self.width,self.height,size)
                #    elif self.currentScreen == "options":
                #        self.options.resize(self.width,self.height,size)
                #    elif self.currentScreen == "login":
                #        self.login.resize(self.width,self.height,size)
                #    elif self.currentScreen == "seleccionPartidas":
                #        self.seleccionPartidas.resize(self.width,self.height,size)
                #click del mouse
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.currentScreen == "menu":
                        screenToChange = self.menu.clickedMouse()
                        self.online = False
                        if(screenToChange != self.currentScreen):
                            self.changedScreen = True
                            self.currentScreen = screenToChange
                            self.GLOBAL.setCurrentScreen(screenToChange)
                            self.screen = self.menu.getScreen()
                    elif self.currentScreen == "credits":
                        screenToChange = self.credits.clickedMouse()
                        self.online = False
                        if(screenToChange != self.currentScreen):
                            self.changedScreen = True
                            self.currentScreen = screenToChange
                            self.GLOBAL.setCurrentScreen(screenToChange)
                            self.screen = self.credits.getScreen()
                    elif self.currentScreen == "options":
                        screenToChange = self.options.clickedMouse()
                        self.online = False
                        self.configuration.fps = self.options.getFPS()
                        self.configuration.dmVoice = self.options.getDMVoice()
                        if(screenToChange != self.currentScreen):
                            self.changedScreen = True
                            self.currentScreen = screenToChange
                            self.GLOBAL.setCurrentScreen(screenToChange)
                            self.screen = self.options.getScreen()
                    elif self.currentScreen == "seleccionPartidas":
                        screenToChange = self.seleccionPartidas.clickedMouse()
                        self.online = False
                        if(screenToChange != self.currentScreen):
                            self.changedScreen = True
                            self.currentScreen = screenToChange
                            self.GLOBAL.setCurrentScreen(screenToChange)
                            self.screen = self.seleccionPartidas.getScreen()
                            self.configuracionPartida.setCurrentPartida(self.seleccionPartidas.getPartidaToLoad())
                            self.salaEspera.setCurrentPartida(self.seleccionPartidas.getPartidaToLoad())
                            #TODO: también a la sala de espera, y las otras pantallas que gestionan las partidas, y lo mismo desde sus refrescos
                    elif self.currentScreen == "login":
                        screenToChange = self.login.clickedMouse()
                        self.online = False
                        if(screenToChange != self.currentScreen):
                            self.changedScreen = True
                            self.currentScreen = screenToChange
                            self.GLOBAL.setCurrentScreen(screenToChange)
                            self.screen = self.login.getScreen()
                            self.perfil.logged= self.login.getLog()
                            self.menu.setLog(self.perfil.logged) #hay que actualizar la variable logged del menú
                            self.perfil.avatarPicPerfil = self.login.getPicture()
                            self.menu.setPicture(self.perfil.avatarPicPerfil)
                            self.salaEspera.setSelfIcono(self.perfil.avatarPicPerfil)
                            self.perfil.name = self.login.getName()
                            self.menu.setName(self.perfil.name)
                            self.salaEspera.setSelfName(self.perfil.name)
                    elif self.currentScreen == "configuracionPartida":
                        screenToChange = self.configuracionPartida.clickedMouse()
                        self.online = False
                        if(screenToChange != self.currentScreen):
                            self.changedScreen = True
                            self.currentScreen = screenToChange
                            self.GLOBAL.setCurrentScreen(screenToChange)
                            self.screen = self.configuracionPartida.getScreen()
                    elif self.currentScreen == "salaEspera":
                        screenToChange = self.salaEspera.clickedMouse()
                        if(screenToChange != self.currentScreen):
                            self.changedScreen = True
                            self.currentScreen = screenToChange
                            self.GLOBAL.setCurrentScreen(screenToChange)
                            if(screenToChange != "seleccionPersonaje"): #si no se carga una partida, y volvemos hacia atrás, cerramos el socket
                                self.online = False
                                self.salaEspera.escuchaTCP.closeSocketTCPServer()
                                self.salaEspera.escuchaUDP.closeSocketUDPServer()
                                self.salaEspera.enviarEstadoUDP.desconectar()
                                try:
                                    #solo se podrá cerrar si eres el cliente
                                    self.joinPartida.escuchaTCPClient.closeSocketTCPServer()
                                except:
                                    pass
                            else: #si la siguiente es seleccionPersonaje le pasamos la contraseña
                                self.seleccionPersonaje.setPassword(self.salaEspera.getPassword())
                                self.seleccionPersonaje.setCurrentPartida(self.salaEspera.getCurrentPartida())
                            self.screen = self.salaEspera.getScreen()
                    elif self.currentScreen == "joinPartida":
                        self.joinPartida.setNameYAvatar(self.perfil.name,self.perfil.avatarPicPerfil)
                        screenToChange = self.joinPartida.clickedMouse()
                        if(screenToChange != self.currentScreen):
                            self.changedScreen = True
                            self.currentScreen = screenToChange
                            self.GLOBAL.setCurrentScreen(screenToChange)
                            if(self.currentScreen == "salaEspera"):
                                self.online = True
                                self.salaEspera.setNumJugadoresYOtherPlayers(self.joinPartida.getNumJugadoresAndJugadoresAndPort())
                                self.salaEspera.setPortUDPYSocketUDP(self.joinPartida.getPortUDPYSocket())
                                self.salaEspera.setPassword(self.joinPartida.getPassword())
                            self.screen = self.joinPartida.getScreen()
                    elif self.currentScreen == "server_disc":
                        screenToChange = self.serverDisc.clickedMouse()
                        self.online = False
                        if(screenToChange != self.currentScreen):
                            self.changedScreen = True
                            self.currentScreen = screenToChange
                            self.GLOBAL.setCurrentScreen(screenToChange)
                            self.screen = self.serverDisc.getScreen()
                    elif self.currentScreen == "seleccionPersonaje":
                        screenToChange = self.seleccionPersonaje.clickedMouse()
                        if(screenToChange != self.currentScreen):
                            self.changedScreen = True
                            self.currentScreen = screenToChange
                            self.GLOBAL.setCurrentScreen(screenToChange)
                            self.screen = self.seleccionPersonaje.getScreen()
                            if(screenToChange != "partida"):
                                self.online = False
                                self.salaEspera.escuchaTCP.closeSocketTCPServer()
                                self.salaEspera.escuchaUDP.closeSocketUDPServer()
                                self.salaEspera.enviarEstadoUDP.desconectar()
                                try:
                                    #solo se podrá cerrar si eres el cliente
                                    self.joinPartida.escuchaTCPClient.closeSocketTCPServer()
                                except:
                                    pass 
                             
                    #ahora toca actualizar
                    if self.changedScreen:
                        self.changedScreen = False
                        if (self.currentScreen == "menu"):
                            self.menu.setScreen(self.screen)
                            self.menu.render()
                        elif (self.currentScreen == "credits"):
                            self.credits.setScreen(self.screen)
                            self.credits.render()
                        elif (self.currentScreen == "options"):
                            self.options.setScreen(self.screen)
                            self.options.render()
                        elif (self.currentScreen == "login"):
                            self.login.setScreen(self.screen)
                            self.login.render()
                        elif(self.currentScreen == "seleccionPartidas"):
                            self.seleccionPartidas.setScreen(self.screen)
                            self.seleccionPartidas.render(self.perfil.avatarPicPerfil,self.perfil.name)
                        elif(self.currentScreen == "configuracionPartida"):
                            self.configuracionPartida.setScreen(self.screen)
                            self.configuracionPartida.render(self.perfil.avatarPicPerfil,self.perfil.name)
                        elif(self.currentScreen == "salaEspera"):
                            self.salaEspera.setScreen(self.screen)
                            self.salaEspera.render(self.online)
                        elif(self.currentScreen == "joinPartida"):
                            self.joinPartida.setScreen(self.screen)
                            self.joinPartida.render()
                        elif(self.currentScreen == "server_disc"):
                            self.serverDisc.setScreen(self.screen)
                            self.serverDisc.render()
                        elif(self.currentScreen == "seleccionPersonaje"):
                            self.seleccionPersonaje.setScreen(self.screen)
                            self.seleccionPersonaje.render(self.online)
                        else:
                            self.screen.fill((0,0,0))
                            pygame.display.flip()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.currentScreen == "options":
                        out = self.options.releasedMouse()
                        if(out is not None):
                            (self.configuration.volMusica,self.configuration.volEffects) = out
                            self.change_music(self.configuration.volMusica,self.configuration.volEffects)
                    else: 
                        pass
                elif event.type == pygame.KEYDOWN:
                    if self.currentScreen == "login":
                        self.login.manageInputBox(event.key,event.unicode)
                    elif self.currentScreen == "configuracionPartida":
                        self.configuracionPartida.manageInputBox(event.key,event.unicode)
                    elif self.currentScreen == "joinPartida":
                        self.joinPartida.manageInputBox(event.key,event.unicode)
                    elif self.currentScreen == "seleccionPersonaje":
                        self.seleccionPersonaje.manageInputBox(event.key,event.unicode)
                        pass
                    else:
                        pass
                elif event.type == pygame.MOUSEMOTION:
                    if self.currentScreen == "menu":
                        self.menu.movedMouse()
                    elif self.currentScreen == "credits":
                        self.credits.movedMouse()
                    elif self.currentScreen == "options":
                        self.options.movedMouse()
                    elif self.currentScreen == "login":
                        self.login.movedMouse()
                    elif self.currentScreen == "seleccionPartidas":
                        self.seleccionPartidas.movedMouse()
                    elif self.currentScreen == "configuracionPartida":
                        self.configuracionPartida.movedMouse()
                    elif self.currentScreen == "salaEspera":
                        self.salaEspera.movedMouse()
                    elif self.currentScreen == "joinPartida":
                        self.joinPartida.movedMouse()
                    elif self.currentScreen == "server_disc":
                        self.serverDisc.movedMouse()
                    elif self.currentScreen == "seleccionPersonaje":
                        self.seleccionPersonaje.movedMouse()
                    else:
                        pass
            #print("FPS = ",int(self.clock.get_fps()))
            #print("Dm a voz = ",self.dmvoz)
            self.clock.tick(self.configuration.fps)
        #antes de cerrar el simulador hay que guardar la configuración
        self.perfil.savePerfilToFile()
        try:
            self.salaEspera.escuchaTCP.closeSocketTCPServer()
        except:
            pass
        try:
            self.salaEspera.escuchaUDP.closeSocketUDPServer()
        except:
            pass
        try:
            self.joinPartida.escuchaTCPClient.closeSocketTCPServer()
        except:
            pass
        try:
            self.salaEspera.enviarEstadoUDP.desconectar()
        except:
            pass
        self.configuration.saveConfigurationToFile()
        try:
            self.s.close()
        except:
            pass
        pygame.quit()
    
    def change_music(self,volM,volE):
        #Los canales actúan como variables globales en pygame, así que si cambio aquí algo,
        #también cambia en el resto de ventanas
        mixer.music.set_volume(volM)
        self.ch1.set_volume(volE)
        self.ch2.set_volume(volE)
        self.ch3.set_volume(volE)
        self.ch4.set_volume(volE)
    def getLocalIP(self):
        #local_ip = socket.gethostbyname(socket.gethostname())
        #public_ip = requests.get('https://ident.me').text.strip()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #socket
        try:
            s.connect(("8.8.8.8", 80)) #conexión
            local_ip = s.getsockname()[0] #ip
            s.close() #cerramos
        except:
            local_ip = None
        return (local_ip)
        #return(local_ip,public_ip)
