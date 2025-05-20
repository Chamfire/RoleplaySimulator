import pygame
import os
import random
import numpy as np
import sys
import heapq
import pickle
from Lista_Inventario import Lista_Inventario
import base64


# 0: Casilla sin determinar
# 1: 

class Cofre:
    def __init__(self, llave_puerta,llave_enlace):
        self.inventory = []
        lista = Lista_Inventario()
        if(llave_puerta != None):
            # Ya tenemos el objeto
            llave = lista.createLlave(llave_puerta,llave_enlace)
            self.inventory = ["Llave","Llave",llave,1]
        #rellenamos el cofre con loot
        else:
            # Hay que poner 1 objeto aleatorio
            armaduras_list = lista.getArmaduraList()
            armas_list = lista.getArmasList()
            objetos_list = lista.getObjetosList()
            escudos_list = lista.getEscudosList()

            opcion = random.randint(0,100)
            if(opcion <= 60):
                choosed = objetos_list
            elif(60 < opcion <= 80):
                choosed = armas_list
            elif(80 < opcion <= 90):
                choosed = armaduras_list
            else:
                choosed = escudos_list
            categorias_num = len(choosed)
            if(categorias_num == 1):
                categoria_choosed = 1
            else:
                categoria_choosed = random.randint(1,categorias_num)
            cont = 1
            for categoria,lista in choosed.items():
                if(cont == categoria_choosed):
                    # Es la categoría escogida
                    items_num =  len(lista)
                    if(items_num == 1):
                        item_escogido = 1
                    else:
                        item_escogido = random.randint(1,items_num)
                    cont2 = 1
                    for name, item in lista.items():
                        if(cont2 == item_escogido):
                            # Ya tenemos el objeto
                            self.inventory = [categoria,name,item,1]
                        cont2 +=1    
                    break
                cont+=1

    def getLoot(self):
        return self.inventory

            


class Sala:
    def __init__(self,i,size):
        self.id = i
        self.es_obligatoria = False #por defecto se marcan como opcionales. Luego, las obligatorias se marcarán como obligatorias
        self.esInicial = False
        self.daASalas = {}
        self.tienePortales = []
        self.contieneLlaves = [] #Lista de posiciones de las puertas que abre cada llave de aquí
        self.esFinal = False
        self.orden = None
        self.variableDeCheck = None
        self.tipo_mision = None
        self.contieneCofres = []
        self.size = size
        self.pos_x = None
        self.pos_y = None


class Map_generation:
    def __init__(self,eleccion,currentPartida,tipo_mision, variableDeCheck, numJugadores, NPC_imagen,id_host,width,height,load = False):
        if(not load):
            self.NPC_imagen = NPC_imagen
            self.id_host = id_host
            self.tile_cache = {}
            imagen = pygame.image.load(self.NPC_imagen)

            # Define el tamaño de cada frame
            ancho_frame = 64
            alto_frame = 64

            # Calcula el número de frames en cada fila y columna
            num_frames_x = imagen.get_width() // ancho_frame
            num_frames_y = imagen.get_height() // alto_frame

            # Lista para almacenar los frames
            self.frames = {}

            # Recorre la imagen y extrae cada frame
            for y in range(num_frames_y):
                self.frames[y] = []
                for x in range(num_frames_x):
                    # Extrae el frame actual
                    frame = imagen.subsurface(pygame.Rect(x * ancho_frame, y * alto_frame, ancho_frame, alto_frame))
                    # Añade el frame a la lista
                    self.frames[y] += [frame]


            sys.setrecursionlimit(5000)  
            config_dir = 'mapas/'+currentPartida
            config_file = 'mapa_'+currentPartida+".pickle"
            config_file2 = 'objetos_'+currentPartida+".pickle"
            self.eleccion = eleccion
            self.map_size = 100
            self.spawn = None
            self.centroides = {}
            self.salas = {}
            self.map_tileSize = [width/37.5000,height/21.8750]
            self.casillasVistas = np.zeros((self.map_size,self.map_size), dtype=int) #matriz de 0s de 100 x 100 -> es el mapa
            self.playersCurrentPos = {}

            self.grafos = {}
            self.adyacencias = None
            self.main_path = None
            self.matrix = np.zeros((self.map_size,self.map_size), dtype=int) #matriz de 0s de 100 x 100 -> es el mapa
            self.objetos = np.zeros((self.map_size,self.map_size), dtype=int) #matriz de 0s de 100 x 100 -> es el mapa
            if(self.eleccion == "mazmorra"):
                NUM_TILES = 121
                for i in range(NUM_TILES):  # el número total de IDs posibles
                    path = f"tiles/{self.eleccion}/{i}.png"
                    try:
                        self.tile_cache[i] = pygame.image.load(path)
                    except:
                        self.tile_cache[i] = None
                self.createMazmorra() 
                self.fillWithObjects(tipo_mision,variableDeCheck)
                self.createRandomThings(tipo_mision,variableDeCheck, eleccion,numJugadores)
                # for sala in self.salas: 
                #     print("Sala "+str(sala)+" acceso directo a:")
                #     print(self.salas[sala].daASalas)
                #     print("Llaves: ")
                #     print(self.salas[sala].contieneLlaves)
            elif(self.eleccion == "desierto"):
                pass
            elif(self.eleccion == "aldea medieval"):
                pass
            elif(self.eleccion == "ciudad moderna"):
                pass
            elif(self.eleccion == "bosque"):
                pass
            elif(self.eleccion == "barco"):
                pass
            
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
                        
            with open(config_dir+'/'+config_file, 'wb') as f:
                # for fila in self.matrix:
                #     f.write(' '.join(map(str, fila)) + '\n')
                pickle.dump(self.matrix, f)

            with open(config_dir+'/'+config_file2, 'wb') as f:
                pickle.dump(self.objetos, f)
            with open(config_dir+'/casillasVistas.pickle', 'wb') as f:
                pickle.dump(self.casillasVistas, f)
            with open(config_dir+'/salas.pickle', 'wb') as f:
                pickle.dump(self.salas, f)
            with open(config_dir+'/adyacencias.pickle', 'wb') as f:
                pickle.dump(self.adyacencias, f)
            with open(config_dir+'/pathNPC.pickle', 'wb') as f:
                pickle.dump(self.NPC_imagen, f)
            with open(config_dir+'/playersCurrentPost.pickle', 'wb') as f:
                pickle.dump(self.playersCurrentPos, f)
        else:
            config_dir = 'mapas/'+currentPartida
            config_file = 'mapa_'+currentPartida+".pickle"
            config_file2 = 'objetos_'+currentPartida+".pickle"
            with open(config_dir+'/'+config_file, "rb") as f:
                matrix = pickle.load(f)
            with open(config_dir+'/'+config_file2, "rb") as f:
                objetos = pickle.load(f)
            with open(config_dir+'/casillasVistas.pickle', "rb") as f:
                casillasVistas = pickle.load(f)
            with open(config_dir+'/salas.pickle', "rb") as f:
                salas = pickle.load(f)
            with open(config_dir+'/adyacencias.pickle', "rb") as f:
                adyacencias = pickle.load(f)
            with open(config_dir+'/pathNPC.pickle', "rb") as f:
                NPC_imagen = pickle.load(f)
            with open(config_dir+'/playersCurrentPost.pickle', "rb") as f:
                self.playersCurrentPos = pickle.load(f)


            self.reload(matrix,objetos,adyacencias,salas,casillasVistas,eleccion,width,height,NPC_imagen)

    def reload(self,matrix,objetos,adyacencias,salas,casillasVistas,eleccion,width,height,NPC_imagen):
        self.matrix = matrix
        self.objetos = objetos
        self.adyacencias = adyacencias
        self.salas = salas
        self.casillasVistas = casillasVistas
        self.eleccion = eleccion
        self.width = width
        self.height = height
        self.NPC_imagen = NPC_imagen
        self.tile_cache = {}
        imagen = pygame.image.load(self.NPC_imagen)

        # Define el tamaño de cada frame
        ancho_frame = 64
        alto_frame = 64

        # Calcula el número de frames en cada fila y columna
        num_frames_x = imagen.get_width() // ancho_frame
        num_frames_y = imagen.get_height() // alto_frame

        # Lista para almacenar los frames
        self.frames = {}

        # Recorre la imagen y extrae cada frame
        for y in range(num_frames_y):
            self.frames[y] = []
            for x in range(num_frames_x):
                # Extrae el frame actual
                frame = imagen.subsurface(pygame.Rect(x * ancho_frame, y * alto_frame, ancho_frame, alto_frame))
                # Añade el frame a la lista
                self.frames[y] += [frame]

        if(self.eleccion == "mazmorra"):
            NUM_TILES = 121
            for i in range(NUM_TILES):  # el número total de IDs posibles
                print(i)
                path = f"tiles/{self.eleccion}/{i}.png"
                try:
                    self.tile_cache[i] = pygame.image.load(path)
                except:
                    self.tile_cache[i] = None
        self.map_tileSize = [width/37.5000,height/21.8750]


    def createMazmorra(self):
        num_max_salas = 20
        num_min_salas = 15
        num_aleatorio_salas = random.randint(num_min_salas,num_max_salas)
        self.available_map_size = self.map_size - 2 #Le quitamos los bordes, que deben ser muro 
        walls_percentage = 0.2
        total_tiles = self.available_map_size**2
        aprox_wall_tiles = total_tiles*walls_percentage #número de casillas que preferiblemente serán muros
        aprox_room_tiles = total_tiles-aprox_wall_tiles #número de casillas que conformarán las salas
        max_size_room = aprox_room_tiles//num_max_salas #tamaño máximo por sala (si queremos que haya como mucho 10)
        min_size_room = 36 # tamaño mínimo para ser considerado habitación
        length_max_one_side = int(np.sqrt(max_size_room))
        length_min_one_side = 6 #lo mínimo sería 6 x 6 -> puede haber como mucho 12 mobs a matar, que deberían estar en la última sala (6x6 = 36 - bordes = 16)
        room_sizes = {}
        room_start_points = {}
        #De forma aleatoria determinamos el tamaño de las salas de la mazmorra, teniendo en cuenta las limitaciones de espacio
        for i in range(0,num_aleatorio_salas):
            room_sizes[i] = [random.randint(length_min_one_side,length_max_one_side),random.randint(length_min_one_side,length_max_one_side)]
            self.adyacencias = np.zeros((num_aleatorio_salas,num_aleatorio_salas), dtype=int)
            self.salas[i] = Sala(i,room_sizes[i])

        # print("Número total de salas: ", num_aleatorio_salas)
        # print("Tamaños de las salas: ")
        # print(room_sizes)
        # print("---------------------------")
        for i,room_size in room_sizes.items():
            #Determino cuál podría ser una posible posición para esa sala, teniendo en cuenta que debe printearse dentro del cuadro del mapa
            found_place_to_print = False
            count = 0
            while(not found_place_to_print):
                count +=1
                #print("intento "+str(count)+" en sala "+str(i))
                found_place_to_print = True
                x_start = random.randint(1,self.available_map_size-room_size[0]+1)
                y_start = random.randint(1,self.available_map_size-room_size[1]+1)
                room_start_points[i] = [x_start,y_start]
                    #Ejemplo de funcionamiento: mapa de 5 x 5, tamaño disponible= 3. Tamaño sala = 3 x 3. d = disponible. i = 1x1
                    # x_start = (i[0],3-3+1 = 1) = random(1,1) => x = 1 es la única posición donde podría empezar. Lo mismo con la i
                    #   0 1 2 3 4
                    # 0 - - - - -       - - - - -
                    # 1 - d d d -       - i x x -
                    # 2 - d d d -  -->  - x x x -
                    # 3 - d d d -       - x x x -
                    # 4 - - - - -       - - - - -

                    #Comprobamos que todas las casillas que ocupa la sala estén libres en el mapa (== 0)
                matrix_aux = self.matrix.copy()
                for pos_x in range(x_start,x_start + room_size[0]):
                    for pos_y in range(y_start,y_start + room_size[1]):
                        if(self.matrix[pos_y][pos_x] != 0):
                            found_place_to_print = False
                            break
                        if(pos_x == x_start and pos_y == y_start):
                            #esquina izqda arriba sala
                            matrix_aux[pos_y][pos_x] = 2
                        elif(pos_x == (x_start + room_size[0]-1) and pos_y == y_start):
                            #esquina dcha arriba sala
                            matrix_aux[pos_y][pos_x] = 3
                        elif(pos_x == (x_start + room_size[0]-1) and pos_y == (y_start + room_size[1] - 1)):
                            #esquina dcha abajo sala
                            matrix_aux[pos_y][pos_x] = 4
                        elif(pos_x == x_start and pos_y == (y_start + room_size[1] - 1)):
                            #esquina izqda abajo sala
                            matrix_aux[pos_y][pos_x] = 5
                        elif(pos_x == x_start):
                            #muro izqdo
                            matrix_aux[pos_y][pos_x] = 9
                        elif(pos_y == y_start):
                            #muro superior
                            matrix_aux[pos_y][pos_x] = 6
                        elif(pos_x == (x_start + room_size[0]-1)):
                            #muro derecho
                            matrix_aux[pos_y][pos_x] = 7
                        elif(pos_y == (y_start + room_size[1] - 1)):
                            #muro inferior
                            matrix_aux[pos_y][pos_x] = 8
                        else:
                            matrix_aux[pos_y][pos_x] = 1 #1 es suelo de baldosa de mazmorra
                    if(found_place_to_print == False):
                        break #se propaga el break
                                
                
            #Si llegamos aquí, quiere decir que hemos encontrado un lugar libre completo donde printear esa sala:
            self.matrix = matrix_aux
            #self.printSubMap(room_size,x_start,y_start,i)
            self.salas[i].pos_x = x_start
            self.salas[i].pos_y = y_start
            #calculamos el centro de la sala
            half_size_x = room_sizes[i][0]//2
            half_size_y = room_sizes[i][1]//2
            self.centroides[i] = [room_start_points[i][0]+half_size_x,room_start_points[i][1]+half_size_y]

        #ponemos a -1 los muros de los bordes
        for pos in range(0,self.map_size):
            self.matrix[0][pos] = -1 #fila de arriba a -1
            self.matrix[self.map_size-1][pos] = -1 #fila de abajo a -1
            self.matrix[pos][0] = -1
            self.matrix[pos][self.map_size-1] = -1



        self.createPasillosMazmorra(room_start_points,room_sizes)
        subarboles = []
        for sala in self.salas:
            subArbol = [self.getSubArbol(room_start_points,sala)]
            subarboles += subArbol
            if(len(subArbol[0]) == (len(self.salas)-1)):
                #todos están conectados
                break
            else:
                pass
        ##Conecto los subárboles que se hayan quedado aislados mediante portales
        exit_val = False
        while(len(subarboles) != 1):
            for subArbol in subarboles:
                for subArbol2 in subarboles:
                    if(subArbol != subArbol2):
                        for sala in subArbol:
                            for sala2 in subArbol2:
                                if(sala not in subArbol2 and sala2 not in subArbol2):
                                    [posx,posy] = room_start_points[sala]
                                    for currentx in range(posx,posx+room_sizes[sala]):
                                        for currenty in range(posy,posy+room_sizes[sala]):
                                            if(self.matrix[currenty][currentx] == 1 and self.matrix[currenty+1][currentx] != 13 and self.matrix[currenty-1][currentx] != 12 and self.matrix[currenty][currentx+1] != 11 and self.matrix[currenty][currentx-1] != 10):
                                                self.salas[sala].tienePortales += [currentx,currenty]
                                                self.salas[sala].daASalas[sala2] = [[currentx,currenty],None]
                                                self.objetos[currenty][currentx] = 32
                                                self.adyacencias[sala][sala2] = -1

                                    [posx,posy] = room_start_points[sala2]
                                    for currentx in range(posx,posx+room_sizes[sala2]):
                                        for currenty in range(posy,posy+room_sizes[sala2]):
                                            if(self.matrix[currenty][currentx] == 1 and self.matrix[currenty+1][currentx] != 13 and self.matrix[currenty-1][currentx] != 12 and self.matrix[currenty][currentx+1] != 11 and self.matrix[currenty][currentx-1] != 10):
                                                self.salas[sala2].tienePortales += [currentx,currenty]
                                                self.salas[sala2].daASalas[sala] = [[currentx,currenty],None]
                                                self.objetos[currenty][currentx] = 32
                                                self.adyacencias[sala2][sala] = -1
                                    newSubArbol = subArbol | subArbol2
                                    subarboles.remove(subArbol)
                                    subarboles.remove(subArbol2)
                                    subarboles +=newSubArbol
                                    exit_val = True
                                    break
                            if(exit_val):
                                break
                        if(exit_val):
                            break
                if(exit_val):
                    break
            if(exit_val):
                exit_val = False
                break

    def createRandomThings(self,tipo_mision,variableDeCheck, ubicacion,numJugadores):
        # Si la misión es de combate, recapitulamos los mobs que NO podemos incluir en encuentros aleatorios

        mobs_a_excluir = []
        if(tipo_mision == "combate"):
            for mob in variableDeCheck:
                mobs_a_excluir += [mob]

        # Ahora vamos a extraer la lista de mobs que podemos poner como encuentro aleatorio
        mobs_que_pueden_incluirse = []
        mobs_a_incluir = {}
        rooms_with_monsters = 0
        lista_mobs_disponibles = {"mazmorra": ["esqueleto","zombie","slime","beholder","troll"],# 33-38, 39, 40, 41, 42
                                  "ciudad moderna": ["droide","fantasma","objeto animado de silla", "mimic de cofre", "muñeca animada", "cyborg"], #38,39,40,41,42,43
                                  "bosque": ["lobo wargo", "vampiro", "oso", "hombre lobo"], 
                                  "desierto": ["serpiente","cocodrilo", "momia", "esfinge"], 
                                  "aldea medieval": ["goblin","cultista","gnoll","elemental de roca"],
                                  "barco": ["sirena","tiburón","hada","kraken"], 
                                  "raros": ["dragón","sombras","fénix"], #43-46,47,48
                                  "medio": ["ankheg","basilísco"], #49,50-56
                                  "comun": ["murciélago","rata","felino salvaje"]} #57,58,59-66
        for mob in lista_mobs_disponibles[ubicacion]:
            if(mob not in mobs_a_excluir):
                mobs_que_pueden_incluirse += [mob]
        for mob in lista_mobs_disponibles["comun"]:
            mobs_que_pueden_incluirse += [mob]
        prob = random.randint(0,100)
        #print(prob)
        if(70 < prob < 90):
            mobs_a_incluir[rooms_with_monsters] = [lista_mobs_disponibles["medio"][random.randint(0,1)]]
            rooms_with_monsters +=1
        elif(prob >= 90):
            mobs_a_incluir[rooms_with_monsters] = [lista_mobs_disponibles["raros"][random.randint(0,2)]]
            rooms_with_monsters +=1
        else:
            pass
        num_total_salas = len(self.salas)
        monsters_rooms = num_total_salas//3 #Un tercio tendrán monstruos

        while(rooms_with_monsters != monsters_rooms):
            n = random.randint(1,int(numJugadores*1.5))
            mobs_a_incluir[rooms_with_monsters] = []
            mob = random.randint(0,len(mobs_que_pueden_incluirse)-1)
            for i in range(0,n):
                mobs_a_incluir[rooms_with_monsters] += [mobs_que_pueden_incluirse[mob]]
            rooms_with_monsters +=1


        # Ya tenemos establecido el número de salas con monstruos, y los monstruos
        # De posibles salas, son todas menos la primera
        posibles_salas = []
        for i in range(0,len(self.salas)):
            posibles_salas += [i]
        posibles_salas.remove(self.main_path[0])


        #print(mobs_a_incluir)
        for i in range(0,rooms_with_monsters):
            l = random.randint(0,len(posibles_salas)-1)
            posiciones = []
            for pos_x in range(self.salas[posibles_salas[l]].pos_x+1,self.salas[posibles_salas[l]].pos_x+self.salas[posibles_salas[l]].size[0]-1):
                for pos_y in range(self.salas[posibles_salas[l]].pos_y+1,self.salas[posibles_salas[l]].pos_y+self.salas[posibles_salas[l]].size[1]-1):
                    if(self.matrix[pos_y-1][pos_x] != 12 and self.matrix[pos_y+1][pos_x] != 13 and self.matrix[pos_y][pos_x-1] != 10 and self.matrix[pos_y][pos_x+1] != 11):
                        posiciones += [[pos_x,pos_y]]
            mobs_selected = mobs_a_incluir[i] #el mob/mobs elegido para esa sala
            for mob in mobs_selected:
                found = False
                #print(mob)
                if(mob == "esqueleto"):
                    weapon = random.randint(0,5)
                    id = 33+weapon
                elif(mob == "zombie"):
                    id = 39
                elif(mob == "slime"):
                    id = 40
                elif(mob == "beholder"):
                    id = 41
                elif(mob == "troll"):
                    id = 42
                elif(mob == "dragón"):
                    tipo = random.randint(0,3)
                    id = 43+tipo
                elif(mob == "sombras"):
                    id = 47
                elif(mob == "fénix"):
                    id = 48
                elif(mob == "ankheg"):
                    id = 49
                elif(mob == "basilísco"):
                    tipo = random.randint(0,6)
                    id = 50+tipo
                elif(mob == "murciélago"):
                    id = 57
                elif(mob == "rata"):
                    id = 58
                elif(mob == "felino salvaje"):
                    tipo = random.randint(0,7)
                    id = 59+tipo
                while(not found and len(posiciones) >=1):
                    l2 = len(posiciones)
                    pos = random.randint(0,l2-1)
                    [pos_x,pos_y] = posiciones[pos]  
                    if(self.objetos[pos_y][pos_x] == 0):
                        self.objetos[pos_y][pos_x] = id
                        #print("Mob: "+mob+" en posición "+str(pos_x)+","+str(pos_y))
                        found = True
            # Ahora ubico un cofre de botín en esa sala
            s = posibles_salas[l]
            posiciones = []
            for pos_x in range(self.salas[s].pos_x+1,self.salas[s].pos_x+self.salas[s].size[0]-1):
                for pos_y in range(self.salas[s].pos_y+1,self.salas[s].pos_y+self.salas[s].size[1]-1):
                    if((pos_x == self.salas[s].pos_x + 1) or (pos_x == (self.salas[s].pos_x+self.salas[s].size[0])) or (pos_y == self.salas[s].pos_y+1 or (pos_y == self.salas[s].pos_y+self.salas[s].size[1]-1))):
                        if(self.matrix[pos_y-1][pos_x] != 12 and self.matrix[pos_y+1][pos_x] != 13 and self.matrix[pos_y][pos_x-1] != 10 and self.matrix[pos_y][pos_x+1] != 11):
                            posiciones += [[pos_x,pos_y]]
            found = False
            while(not found):
                l2 = len(posiciones)
                pos = random.randint(0,l2-1)
                [pos_x,pos_y] = posiciones[pos]   
                if(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y-1][pos_x] == 6)):
                    self.objetos[pos_y][pos_x] = 91
                    cofre = Cofre(None,None)
                    self.salas[s].contieneCofres += [[[pos_x,pos_y],cofre]]
                    found = True
                elif(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y+1][pos_x] == 8)):
                    self.objetos[pos_y][pos_x] = 93
                    cofre = Cofre(None,None)
                    self.salas[s].contieneCofres += [[[pos_x,pos_y],cofre]]
                    found = True
                elif(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y][pos_x-1] == 9)):
                    self.objetos[pos_y][pos_x] = 92
                    cofre = Cofre(None,None)
                    self.salas[s].contieneCofres += [[[pos_x,pos_y],cofre]]
                    found = True
                elif(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y][pos_x+1] == 7)):
                    self.objetos[pos_y][pos_x] = 94
                    cofre = Cofre(None,None)
                    self.salas[s].contieneCofres += [[[pos_x,pos_y],cofre]]
                    found = True
                else:
                    posiciones.remove(posiciones[pos])
            posibles_salas.remove(posibles_salas[l])

        # Lista de opciones aleatorias: 
        # 1. puertas cerradas con llave del camino pcpal
        num_salas = len(self.main_path) #número de salas del camino pcpal
        cerradas = random.randint(1,2) #1 o 2 puertas estarán cerradas con llave
        sala_elegida = self.main_path[random.randint(0,num_salas-1)]
        # Bloqueamos la puerta predecesora en el camino
        if(sala_elegida != self.main_path[0]):
            pred = self.getPredecesorInmediatoEnMainPath(sala_elegida)
            self.salas[pred].daASalas[sala_elegida][1] = "cerrado" #cerramos esa puerta
            resp = self.devolverLongitudCamino(self.main_path[0],sala_elegida,[],0,[])
            # Como está en el camino pcpal, sabemos que va a ser True
            length = resp[1]
            camino = resp[2]
            sala_con_llave = camino[random.randint(0,length-1)]
            coordenadas_puerta = self.salas[sala_elegida].daASalas[pred][0]
            self.salas[sala_con_llave].contieneLlaves += [coordenadas_puerta]
            s = sala_con_llave
            cofre1 = Cofre(sala_elegida,pred)
        else:
            # Si es la primera sala, se queda todo en la primera sala
            self.salas[sala_elegida].daASalas[self.main_path[1]][1] = "cerrado" #cerramos esa puerta
            coordenadas_puerta = self.salas[sala_elegida].daASalas[self.main_path[1]][0]
            self.salas[sala_elegida].contieneLlaves += [coordenadas_puerta]
            s = sala_elegida
            cofre1 = Cofre(sala_elegida,self.main_path[1])
        
        # Ubico un baúl en en la sala con llave 's', que es donde irá la llave
        posiciones = []
        for pos_x in range(self.salas[s].pos_x+1,self.salas[s].pos_x+self.salas[s].size[0]-1):
            for pos_y in range(self.salas[s].pos_y+1,self.salas[s].pos_y+self.salas[s].size[1]-1):
                if((pos_x == self.salas[s].pos_x + 1) or (pos_x == (self.salas[s].pos_x+self.salas[s].size[0])) or (pos_y == self.salas[s].pos_y+1 or (pos_y == self.salas[s].pos_y+self.salas[s].size[1]-1))):
                    if(self.matrix[pos_y-1][pos_x] != 12 and self.matrix[pos_y+1][pos_x] != 13 and self.matrix[pos_y][pos_x-1] != 10 and self.matrix[pos_y][pos_x+1] != 11):
                        posiciones += [[pos_x,pos_y]]
        found = False
        while(not found):
            l = len(posiciones)
            pos = random.randint(0,l-1)
            [pos_x,pos_y] = posiciones[pos]   
            if(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y-1][pos_x] == 6)):
                self.objetos[pos_y][pos_x] = 91
                self.salas[s].contieneCofres += [[[pos_x,pos_y],cofre1]]
                found = True
            elif(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y+1][pos_x] == 8)):
                self.objetos[pos_y][pos_x] = 93
                self.salas[s].contieneCofres += [[[pos_x,pos_y],cofre1]]
                found = True
            elif(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y][pos_x-1] == 9)):
                self.objetos[pos_y][pos_x] = 92
                self.salas[s].contieneCofres += [[[pos_x,pos_y],cofre1]]
                found = True
            elif(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y][pos_x+1] == 7)):
                self.objetos[pos_y][pos_x] = 94
                self.salas[s].contieneCofres += [[[pos_x,pos_y],cofre1]]
                found = True
            else:
                posiciones.remove(posiciones[pos])

        if(cerradas == 2):
            sala2 = sala_elegida
            while(sala2 == sala_elegida):
                sala2 = self.main_path[random.randint(0,num_salas-1)]
            # Tenemos 2 salas distintas aleatorias del camino pcpal
            # Recuperamos el camino pcpal desde el prinipio hasta esta sala
            if(sala2 != self.main_path[0]):
                pred = self.getPredecesorInmediatoEnMainPath(sala2)
                self.salas[pred].daASalas[sala2][1] = "cerrado" #cerramos esa puerta
                resp = self.devolverLongitudCamino(self.main_path[0],sala2,[],0,[])
                # Como está en el camino pcpal, sabemos que va a ser True
                length = resp[1]
                camino = resp[2]
                sala_con_llave = camino[random.randint(0,length-1)]
                coordenadas_puerta = self.salas[sala2].daASalas[pred][0]
                self.salas[sala_con_llave].contieneLlaves += [coordenadas_puerta]
                s = sala_con_llave
                cofre2 = Cofre(sala2,pred)
            else:
                # Si es la primera sala, se queda todo en la primera sala
                self.salas[sala2].daASalas[self.main_path[1]][1] = "cerrado" #cerramos esa puerta
                coordenadas_puerta = self.salas[sala2].daASalas[self.main_path[1]][0]
                self.salas[sala2].contieneLlaves += [coordenadas_puerta]
                s = sala2
                cofre2 = Cofre(sala2,self.main_path[1])

            # Ubico un baúl en en la sala con llave 's', que es donde irá la llave
            posiciones = []
            for pos_x in range(self.salas[s].pos_x+1,self.salas[s].pos_x+self.salas[s].size[0]-1):
                for pos_y in range(self.salas[s].pos_y+1,self.salas[s].pos_y+self.salas[s].size[1]-1):
                    if((pos_x == self.salas[s].pos_x + 1) or (pos_x == (self.salas[s].pos_x+self.salas[s].size[0])) or (pos_y == self.salas[s].pos_y+1 or (pos_y == self.salas[s].pos_y+self.salas[s].size[1]-1))):
                        if(self.matrix[pos_y-1][pos_x] != 12 and self.matrix[pos_y+1][pos_x] != 13 and self.matrix[pos_y][pos_x-1] != 10 and self.matrix[pos_y][pos_x+1] != 11):
                            posiciones += [[pos_x,pos_y]]
            found = False
            while(not found):
                l = len(posiciones)
                pos = random.randint(0,l-1)
                [pos_x,pos_y] = posiciones[pos]   
                if(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y-1][pos_x] == 6)):
                    self.objetos[pos_y][pos_x] = 91
                    self.salas[s].contieneCofres += [[[pos_x,pos_y],cofre2]]
                    found = True
                elif(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y+1][pos_x] == 8)):
                    self.objetos[pos_y][pos_x] = 93
                    self.salas[s].contieneCofres += [[[pos_x,pos_y],cofre2]]
                    found = True
                elif(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y][pos_x-1] == 9)):
                    self.objetos[pos_y][pos_x] = 92
                    self.salas[s].contieneCofres += [[[pos_x,pos_y],cofre2]]
                    found = True
                elif(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y][pos_x+1] == 7)):
                    self.objetos[pos_y][pos_x] = 94
                    self.salas[s].contieneCofres += [[[pos_x,pos_y],cofre2]]
                    found = True
                else:
                    posiciones.remove(posiciones[pos])
        # Ahora creo elementos de decoración
        for sala in self.salas:
            size = self.salas[sala].size
            num_tiles = (size[0]-1)*(size[1]-1)
            num_a_rellenar = int(num_tiles*0.2)

            posiciones = []
            for pos_x in range(self.salas[sala].pos_x+1,self.salas[sala].pos_x+self.salas[sala].size[0]-1):
                for pos_y in range(self.salas[sala].pos_y+1,self.salas[sala].pos_y+self.salas[sala].size[1]-1):
                    if(self.matrix[pos_y-1][pos_x] != 12 and self.matrix[pos_y+1][pos_x] != 13 and self.matrix[pos_y][pos_x-1] != 10 and self.matrix[pos_y][pos_x+1] != 11):
                        posiciones += [[pos_x,pos_y]]
            for i in range(0,num_a_rellenar):
                found = False
                while(not found and len(posiciones) >=1):
                    l = len(posiciones)
                    pos = random.randint(0,l-1)
                    [pos_x,pos_y] = posiciones[pos]   
                    if(self.objetos[pos_y][pos_x] == 0):
                        tipo = random.randint(0,100)
                        if(tipo < 80):
                            tipo2 = random.randint(1,100)
                            if(tipo2 >= 80):
                                rand_obj = random.randint(107,110)
                            else:
                                rand_obj = random.randint(118,121)
                        elif(80 < tipo <= 95):
                            rand_obj = random.randint(111,117)
                        else:
                            rand_obj = random.randint(95,106)
                        self.objetos[pos_y][pos_x] = rand_obj
                        posiciones.remove(posiciones[pos])
                        found = True





    def getPredecesorInmediatoEnMainPath(self,room):
        #print(room)
        for sala in range(1,len(self.main_path)):
            if(room == self.main_path[sala]):
                return self.main_path[sala-1]
        return self.main_path[0] #es la primera sala la que debe estar cerrada y con la llave                  

    def fillCasillasVistas(self,pos_x,pos_y):
        # Marcamos esa casilla como vista
        self.casillasVistas[pos_x][pos_y] = 1

        # Calculamos qué casillas podría ver:
        # Esfera de 10 pies: 
        # - - v - -
        # - v v v -
        # v v P v v
        # - v v v -
        # - - v - -

        # Condiciones: 
        # Si está dentro de una sala (1):
        # Si el adyacente es un muro/puerta[0;2-13], no puede ver más allá. (-1 no cuenta porque ya es borde de mapa)
        if(self.matrix[pos_y][pos_x] == 1):
            self.casillasVistas[pos_x][pos_y+1] = 1
            self.casillasVistas[pos_x][pos_y-1] = 1
            self.casillasVistas[pos_x+1][pos_y] = 1
            self.casillasVistas[pos_x-1][pos_y] = 1
            self.casillasVistas[pos_x+1][pos_y+1] = 1
            self.casillasVistas[pos_x-1][pos_y-1] = 1
            self.casillasVistas[pos_x+1][pos_y-1] = 1
            self.casillasVistas[pos_x-1][pos_y+1] = 1
            if(not (2 <=self.matrix[pos_y][pos_x+1]<=13)):
                self.casillasVistas[pos_x+2][pos_y] = 1
            if(not (2 <=self.matrix[pos_y][pos_x-1]<=13)):
                self.casillasVistas[pos_x-2][pos_y] = 1
            if(not (2 <=self.matrix[pos_y+1][pos_x]<=13)):
                self.casillasVistas[pos_x][pos_y+2] = 1
            if(not (2 <=self.matrix[pos_y-1][pos_x]<=13)):
                self.casillasVistas[pos_x][pos_y-2] = 1

        # Si está en un pasillo
        elif(self.matrix[pos_y][pos_x] == 22):
            if(self.matrix[pos_y-1][pos_x] == 22):
                self.casillasVistas[pos_x][pos_y-1] = 1
                if(pos_y-2 >= 0 and self.matrix[pos_y-2][pos_x] == 22):
                    self.casillasVistas[pos_x][pos_y-2] = 1
            
            elif(self.matrix[pos_y-1][pos_x] == 13):
                self.casillasVistas[pos_x][pos_y-1] = 1

            if(self.matrix[pos_y+1][pos_x] == 22):
                self.casillasVistas[pos_x][pos_y+1] = 1
                if(pos_y+2 <=99 and self.matrix[pos_y+2][pos_x] == 22):
                    self.casillasVistas[pos_x][pos_y+2] = 1
            
            elif(self.matrix[pos_y+1][pos_x] == 12):
                self.casillasVistas[pos_x][pos_y+1] = 1
            
            if(self.matrix[pos_y][pos_x-1] == 22):
                self.casillasVistas[pos_x-1][pos_y] = 1
                if(pos_x-2 >=0 and self.matrix[pos_y][pos_x-2] == 22):
                    self.casillasVistas[pos_x-2][pos_y] = 1
            
            elif(self.matrix[pos_y][pos_x-1] == 11):
                self.casillasVistas[pos_x-1][pos_y] = 1

            if(self.matrix[pos_y][pos_x+1] == 22):
                self.casillasVistas[pos_x+1][pos_y] = 1
                if(pos_x+2 <=99 and self.matrix[pos_y][pos_x+2] == 22):
                    self.casillasVistas[pos_x+2][pos_y] = 1
            
            elif(self.matrix[pos_y][pos_x+1] == 10):
                self.casillasVistas[pos_x+1][pos_y] = 1
           

    def fillWithObjects(self,tipo_mision,variableDeCheck):
        longest_path = self.getLongestPath()
        self.main_path = longest_path[3]
        # print("Longest path:")
        # print(longest_path[0])
        # print(longest_path[1])
        # print(longest_path[2])
        # print(longest_path[3])
        # print("pos last room: "+str(self.salas[longest_path[1]].pos_x)+","+str(self.salas[longest_path[1]].pos_y))
        self.salas[longest_path[0]].esInicial = True
        self.salas[longest_path[0]].orden = 0
        self.salas[longest_path[0]].esObligatoria = True
        #determinamos el punto de spawnpoint
        posiciones = []
        for pos_x in range(self.salas[longest_path[0]].pos_x+1,self.salas[longest_path[0]].pos_x+self.salas[longest_path[0]].size[0]-1):
            for pos_y in range(self.salas[longest_path[0]].pos_y+1,self.salas[longest_path[0]].pos_y+self.salas[longest_path[0]].size[1]-1):
                posiciones += [[pos_x,pos_y]]
        found = False
        while(not found):
            l = len(posiciones)
            pos = random.randint(0,l-1)
            [pos_x,pos_y] = posiciones[pos]
            if(self.objetos[pos_y][pos_x] == 0):
                self.objetos[pos_y][pos_x] = 80
                self.playersCurrentPos[self.id_host] = [pos_x,pos_y]
                self.fillCasillasVistas(pos_x,pos_y)
                print("spawn:")
                print(pos_x,pos_y)
                self.spawn = [pos_x,pos_y]
                #El jugador siempre empieza mirando hacia abajo
                found = True
                posiciones.remove(posiciones[pos])
            
        # Ubicamos al NPC, mirando en la dirección correcta
        posiciones = []
        for pos_x in range(self.salas[longest_path[0]].pos_x+1,self.salas[longest_path[0]].pos_x+self.salas[longest_path[0]].size[0]-1):
            for pos_y in range(self.salas[longest_path[0]].pos_y+1,self.salas[longest_path[0]].pos_y+self.salas[longest_path[0]].size[1]-1):
                if((pos_x == self.salas[longest_path[0]].pos_x + 1) or (pos_x == (self.salas[longest_path[0]].pos_x+self.salas[longest_path[0]].size[0])) or (pos_y == self.salas[longest_path[0]].pos_y+1 or (pos_y == self.salas[longest_path[0]].pos_y+self.salas[longest_path[0]].size[1]-1))):
                    if(self.matrix[pos_y-1][pos_x] != 12 and self.matrix[pos_y+1][pos_x] != 13 and self.matrix[pos_y][pos_x-1] != 10 and self.matrix[pos_y][pos_x+1] != 11):
                        posiciones += [[pos_x,pos_y]]
        found = False
        while(not found):
            l = len(posiciones)
            pos = random.randint(0,l-1)
            [pos_x,pos_y] = posiciones[pos]
            # Es una posición libre, y no tiene ninguna puerta adyacente
            if(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y-1][pos_x] == 6)):
                self.objetos[pos_y][pos_x] = 90 # NPC mirando hacia abajo
                print(pos_y,pos_x)
                found = True
            elif(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y+1][pos_x] == 8)):
                self.objetos[pos_y][pos_x] = 89 # NPC mirando hacia arriba
                found = True
                print(pos_y,pos_x)
            elif(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y][pos_x-1] == 9)):
                self.objetos[pos_y][pos_x] = 88 # NPC mirando hacia la dcha
                found = True
                print(pos_y,pos_x)
            elif(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y][pos_x+1] == 7)):
                self.objetos[pos_y][pos_x] = 87 # NPC mirando hacia la izqda
                found = True
                print(pos_y,pos_x)
            else:
                posiciones.remove(posiciones[pos])


        self.salas[longest_path[1]].esFinal = True
        cont = 0
        for sala in longest_path[3]:
            cont+=1
            self.salas[sala].esObligatoria = True
            self.salas[sala].orden = cont

        self.salas[longest_path[1]].tipo_mision = tipo_mision
        self.salas[longest_path[1]].variableDeCheck = variableDeCheck

        self.closeSomePaths(longest_path[3])

        if(tipo_mision == "combate"):
            mobsMision = []
            posiciones = []
            for pos_x in range(self.salas[longest_path[1]].pos_x+1,self.salas[longest_path[1]].pos_x+self.salas[longest_path[1]].size[0]-1):
                for pos_y in range(self.salas[longest_path[1]].pos_y+1,self.salas[longest_path[1]].pos_y+self.salas[longest_path[1]].size[1]-1):
                    if(self.matrix[pos_y-1][pos_x] != 12 and self.matrix[pos_y+1][pos_x] != 13 and self.matrix[pos_y][pos_x-1] != 10 and self.matrix[pos_y][pos_x+1] != 11):
                        posiciones += [[pos_x,pos_y]]
            for mob in variableDeCheck:
                mobsMision += [mob]
                for i in range(0,variableDeCheck[mob][0]):
                    #numero de mobs a matar de ese tipo -> hay que ubicarlos en esa sala
                    #4x4 = 16. Como mucho 12 mobs, caben de sobra. Se quitan los bordes de la sala
                    ubicado = False
                    while(not ubicado):
                        l = len(posiciones)
                        pos = random.randint(0,l-1)
                        [pos_x,pos_y] = posiciones[pos]
                        if(self.objetos[pos_y][pos_x] == 0):
                            posiciones.remove(posiciones[pos])
                            if(mob == "esqueleto"):
                                weapon = random.randint(0,5)
                                id = 33+weapon
                                self.objetos[pos_y][pos_x] = id #trampa de mob -> al dirigirte a esa casilla, antes de poder pasar, el DM introduce al mob, y aparece en la casilla. 
                                ubicado = True
                            elif(mob == "zombie"):
                                self.objetos[pos_y][pos_x] = 39
                                ubicado = True
                            elif(mob == "slime"):
                                self.objetos[pos_y][pos_x] = 40
                                ubicado = True
                            elif(mob == "beholder"):
                                self.objetos[pos_y][pos_x] = 41
                                ubicado = True
                            elif(mob == "troll"):
                                self.objetos[pos_y][pos_x] = 42
                                ubicado = True
                        else:
                            posiciones.remove(posiciones[pos])
                               

        elif(tipo_mision == "búsqueda"):
            for objeto in variableDeCheck: #solo hay 1, pero así lo sacamos
                #print(objeto)
                found = False
                if(objeto == "Árbol"):  #"Árbol","Cadáver de dragón","Parte de cadáver de Dragón","Cofre","Armario","Ruina"
                    posiciones = []
                    for pos_x in range(self.salas[longest_path[1]].pos_x+1,self.salas[longest_path[1]].pos_x+self.salas[longest_path[1]].size[0]-1):
                        for pos_y in range(self.salas[longest_path[1]].pos_y+1,self.salas[longest_path[1]].pos_y+self.salas[longest_path[1]].size[1]-1):
                            if(self.matrix[pos_y-1][pos_x] != 12 and self.matrix[pos_y+1][pos_x] != 13 and self.matrix[pos_y][pos_x-1] != 10 and self.matrix[pos_y][pos_x+1] != 11):
                                posiciones += [[pos_x,pos_y]]
                    while(not found):
                        l = len(posiciones)
                        pos = random.randint(0,l-1)
                        [pos_x,pos_y] = posiciones[pos]
                        if(self.objetos[pos_y][pos_x] == 0):
                            self.objetos[pos_y][pos_x] = 68
                            found = True
                        else:
                            posiciones.remove(posiciones[pos])
                                    
                elif(objeto == "Cadáver de dragón"):
                    posiciones = []
                    for pos_x in range(self.salas[longest_path[1]].pos_x+1,self.salas[longest_path[1]].pos_x+self.salas[longest_path[1]].size[0]-1):
                        for pos_y in range(self.salas[longest_path[1]].pos_y+1,self.salas[longest_path[1]].pos_y+self.salas[longest_path[1]].size[1]-1):
                            if(self.matrix[pos_y-1][pos_x] != 12 and self.matrix[pos_y+1][pos_x] != 13 and self.matrix[pos_y][pos_x-1] != 10 and self.matrix[pos_y][pos_x+1] != 11):
                                posiciones += [[pos_x,pos_y]]
                    while(not found):
                        l = len(posiciones)
                        pos = random.randint(0,l-1)
                        [pos_x,pos_y] = posiciones[pos]
                        if(self.objetos[pos_y][pos_x] == 0):
                            self.objetos[pos_y][pos_x] = 69
                            found = True
                        else:
                            posiciones.remove(posiciones[pos])
                                
                elif(objeto == "Parte de cadáver de Dragón"):
                    posiciones = []
                    for pos_x in range(self.salas[longest_path[1]].pos_x+1,self.salas[longest_path[1]].pos_x+self.salas[longest_path[1]].size[0]-1):
                        for pos_y in range(self.salas[longest_path[1]].pos_y+1,self.salas[longest_path[1]].pos_y+self.salas[longest_path[1]].size[1]-1):
                            if(self.matrix[pos_y-1][pos_x] != 12 and self.matrix[pos_y+1][pos_x] != 13 and self.matrix[pos_y][pos_x-1] != 10 and self.matrix[pos_y][pos_x+1] != 11):
                                posiciones += [[pos_x,pos_y]]
                    while(not found):
                        l = len(posiciones)
                        pos = random.randint(0,l-1)
                        [pos_x,pos_y] = posiciones[pos]
                        if(self.objetos[pos_y][pos_x] == 0):
                            self.objetos[pos_y][pos_x] = 70
                            found = True
                        else:
                            posiciones.remove(posiciones[pos])
                               
                elif(objeto == "Cofre"):
                    posiciones = []
                    for pos_x in range(self.salas[longest_path[1]].pos_x+1,self.salas[longest_path[1]].pos_x+self.salas[longest_path[1]].size[0]-1):
                        for pos_y in range(self.salas[longest_path[1]].pos_y+1,self.salas[longest_path[1]].pos_y+self.salas[longest_path[1]].size[1]-1):
                            if((pos_x == self.salas[longest_path[1]].pos_x + 1) or (pos_x == (self.salas[longest_path[1]].pos_x+self.salas[longest_path[1]].size[0])) or (pos_y == self.salas[longest_path[1]].pos_y+1 or (pos_y == self.salas[longest_path[1]].pos_y+self.salas[longest_path[1]].size[1]-1))):
                                if(self.matrix[pos_y-1][pos_x] != 12 and self.matrix[pos_y+1][pos_x] != 13 and self.matrix[pos_y][pos_x-1] != 10 and self.matrix[pos_y][pos_x+1] != 11):
                                    posiciones += [[pos_x,pos_y]]
                    while(not found):
                        l = len(posiciones)
                        pos = random.randint(0,l-1)
                        [pos_x,pos_y] = posiciones[pos]   
                        if(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y-1][pos_x] == 6)):
                            self.objetos[pos_y][pos_x] = 71
                            found = True
                        elif(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y+1][pos_x] == 8)):
                            self.objetos[pos_y][pos_x] = 73
                            found = True
                        elif(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y][pos_x-1] == 9)):
                            self.objetos[pos_y][pos_x] = 74
                            found = True
                        elif(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y][pos_x+1] == 7)):
                            self.objetos[pos_y][pos_x] = 72
                            found = True
                        else:
                            posiciones.remove(posiciones[pos])
                            

                elif(objeto == "Armario"):
                    posiciones = []
                    for pos_x in range(self.salas[longest_path[1]].pos_x+1,self.salas[longest_path[1]].pos_x+self.salas[longest_path[1]].size[0]-1):
                        for pos_y in range(self.salas[longest_path[1]].pos_y+1,self.salas[longest_path[1]].pos_y+self.salas[longest_path[1]].size[1]-1):
                            if((pos_x == self.salas[longest_path[1]].pos_x + 1) or (pos_x == (self.salas[longest_path[1]].pos_x+self.salas[longest_path[1]].size[0])) or (pos_y == self.salas[longest_path[1]].pos_y+1 or (pos_y == self.salas[longest_path[1]].pos_y+self.salas[longest_path[1]].size[1]-1))):
                                if(self.matrix[pos_y-1][pos_x] != 12 and self.matrix[pos_y+1][pos_x] != 13 and self.matrix[pos_y][pos_x-1] != 10 and self.matrix[pos_y][pos_x+1] != 11):
                                    posiciones += [[pos_x,pos_y]]
                    while(not found):
                        l = len(posiciones)
                        pos = random.randint(0,l-1)
                        [pos_x,pos_y] = posiciones[pos]
                        if(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y-1][pos_x] == 6)):
                            self.objetos[pos_y][pos_x] = 75
                            found = True
                        elif(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y+1][pos_x] == 8)):
                            self.objetos[pos_y][pos_x] = 76
                            found = True
                        elif(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y][pos_x-1] == 9)):
                            self.objetos[pos_y][pos_x] = 77
                            found = True
                        elif(self.objetos[pos_y][pos_x] == 0 and (self.matrix[pos_y][pos_x+1] == 7)):
                            self.objetos[pos_y][pos_x] = 78
                            found = True
                        else:
                            posiciones.remove(posiciones[pos])
                            
                elif(objeto == "Ruina"):
                    posiciones = []
                    for pos_x in range(self.salas[longest_path[1]].pos_x+1,self.salas[longest_path[1]].pos_x+self.salas[longest_path[1]].size[0]-1):
                        for pos_y in range(self.salas[longest_path[1]].pos_y+1,self.salas[longest_path[1]].pos_y+self.salas[longest_path[1]].size[1]-1):
                            if(self.matrix[pos_y-1][pos_x] != 12 and self.matrix[pos_y+1][pos_x] != 13 and self.matrix[pos_y][pos_x-1] != 10 and self.matrix[pos_y][pos_x+1] != 11):
                                posiciones += [[pos_x,pos_y]]
                    while(not found):
                        l = len(posiciones)
                        pos = random.randint(0,l-1)
                        [pos_x,pos_y] = posiciones[pos]
                        if(self.objetos[pos_y][pos_x] == 0):
                            self.objetos[pos_y][pos_x] = 79
                            found = True
                        else:
                            posiciones.remove(posiciones[pos])

        

    def closeSomePaths(self,path):
        #Una vez que están todas las salas conectadas, establezco los enlaces directos entre salas
        for sala in self.salas:
            self.setSalasLinked(sala,path)

                                

    def getLongestPath(self):
        current_inicial = None
        max_inicial = None
        max_final = None
        max_length = 0
        current_length = 0
        current_final = None
        longest_path = []
        for sala in self.salas:
            for sala2 in self.salas:
                current_inicial = sala
                current_final = sala2
                current_length = self.devolverLongitudCamino(current_inicial,current_final,[],0,[])
                if(max_length == None or current_length[1] > max_length):
                    max_length = current_length[1]
                    max_inicial = current_inicial
                    max_final = current_final
                    longest_path = current_length[2]
        return (max_inicial,max_final,max_length,longest_path)
                
    def devolverLongitudCamino(self,room_from,room_to,checked,long,path):
        num_sala = -1
        aux_path = path.copy()
        aux_path += [room_from]
        for conn in self.adyacencias[room_from]:
            num_sala +=1
            if(num_sala not in checked and num_sala != room_from):
                if(conn == 1 or conn == 2 or conn == -1):
                    #existe un túnel entre num_sala y room_from
                    if(num_sala == room_to):
                        #es la sala que buscábamos
                        aux_path += [num_sala]
                        return (True,long+1,aux_path)
                    else:
                        checked += [room_from]
                        resp = self.devolverLongitudCamino(num_sala,room_to,checked,long+1,aux_path)
                    if(resp[0]):
                        return (True,resp[1], resp[2])
        return (False,long,aux_path)

    def sucesor(self,sala,sala2,path):
        for sala3 in range(0,len(path)-1):
            for sala4 in range(0,len(path)):
                if (path[sala3] == sala and sala2 == path[sala4]):
                    return True
        return False
    
    def predecesor(self,sala,sala2,path):
        for sala3 in range(0,len(path)-1):
            for sala4 in range(0,len(path)):
                if (path[sala3] == sala2 and sala == path[sala4]):
                    return True
        return False
    
    def checkIfConnectsWithMainPath(self,sala,path,checked):
        for sala3,state in self.salas[sala].daASalas.items():
            estado = state[1] #abierto o cerrado
            checked_aux = checked.copy()
            checked_aux+= [sala3]
            if(estado == "abierto" and sala3 not in path and sala3 not in checked_aux): #no conecta con el path, seguimos buscando
                resp =  self.checkIfConnectsWithMainPath(sala3,path)
                if(resp):
                    return resp
            elif(estado == "abierto" and sala3 in path):
                return True #conecta con el camino pcpal
            else: 
                return False
        return False



    def setSalasLinked(self,room_from,path):
        num_sala = -1
        for conn in self.adyacencias[room_from]:
            num_sala +=1
            if(num_sala != room_from):
                if(conn == 1 or conn == 2 or conn == -1):
                    #print(str(answ)+" con "+str(num_sala))
                    #existe un túnel entre num_sala y room_from
                    if(self.sucesor(room_from,num_sala,path)):
                        #print(str(room_from)+" sucesor de "+str(num_sala))
                        self.salas[room_from].daASalas[num_sala][1] = "abierto" #en la posición 0 está la puerta
                    elif(self.predecesor(room_from,num_sala,path)):
                        #print(str(room_from)+" predecesor de "+str(num_sala))
                        self.salas[room_from].daASalas[num_sala][1] = "abierto"
                    elif(num_sala not in path and not self.checkIfConnectsWithMainPath(num_sala,path,[])):
                        #print(str(num_sala)+" no está en el path. Poniendo ese y  "+str(room_from)+" a abierto")
                        # Si el nodo de destino no se encuentra en el camino principal, el camino hacia ese nodo estará abierto
                        self.salas[room_from].daASalas[num_sala][1] = "abierto"
                        self.salas[num_sala].daASalas[room_from][1] = "abierto"
                    else:
                        if(self.salas[room_from].daASalas[num_sala][1] == None):
                            #print(str(room_from)+" a "+ str(num_sala)+" era None. Cerrando camino")
                            self.salas[room_from].daASalas[num_sala][1] = "cerrado" #en la posición 0 está la puerta. TODO: Modificar con nodos opcionales -> permitir los que vayan a otros nodos distintos del camino principal. Permitir a los que vayan a nodos anteriores al camino principal. Bloquear los que van al último, y permitir del final a todos. 
                        #self.salas[num_sala].daASalas[room_from][1] = "cerrado"
            
    def getSubArbol(self,room_start_points,num_sala):
        #cogemos, por ejemplo, la sala 0
        arbol = set()
        for i in room_start_points:
            if(i != num_sala):
                if(self.existeConexion(num_sala,i,[])):
                    arbol.add(i)
        return arbol

    def getRoomAtPoint(self,x,y,room_sizes,room_start_points):
        for i,size in room_sizes.items():
            start_x = room_start_points[i][0]
            start_y = room_start_points[i][1]
            dif = x - start_x
            dif2 = y - start_y
            if(dif >= 0 and dif <size[0] and dif2 >= 0 and dif2 < size[1]):
                return i
        return -1

    def existeConexion(self,room_from,room_to,checked):
        num_sala = -1
        for conn in self.adyacencias[room_from]:
            num_sala +=1
            if(num_sala not in checked and num_sala != room_from):
                if(conn == 1 or conn == 2 or conn == -1):
                    #existe un túnel entre num_sala y room_from
                    if(num_sala == room_to):
                        #es la sala que buscábamos
                        return True
                    else:
                        checked += [room_from]
                        resp = self.existeConexion(num_sala,room_to,checked)
                    if(resp):
                        return True
        return False


    def todasLasSalasAlcanzables(self,room_start_points,num_sala = 0):
        #cogemos, por ejemplo, la sala 0
        cont1 = 0
        cont2 = 0
        for i in room_start_points:
            cont1 +=1
            if(i != num_sala):
                if(self.existeConexion(num_sala,i,[])):
                    cont2 +=1
        #print(str(cont1)+" respecto a "+str(cont2))
        if((cont1-1) == cont2):
            return True
        else:
            return False


    def createPasillosMazmorra(self,room_start_points,room_sizes):
        room_end_points = {}
        for i in room_start_points:
            x_end = room_start_points[i][0]+room_sizes[i][0] - 1
            y_end = room_start_points[i][1]+room_sizes[i][1] - 1
            room_end_points[i] = [x_end, y_end]

        posibles_puertas_por_sala = {}
        for i in room_start_points:
            pos_y = room_start_points[i][1]
            posibles_puertas_por_sala[i] = {"arriba": None, "abajo": None, "derecha": None, "izquierda": None}
            for pos_x in range(room_start_points[i][0]+1,room_end_points[i][0]): #de 1 a n-1 (las esquinas no se pueden considerar puertas)
                #como es muro superior, compruebo si lo que tiene justo encima es un bloque de posible puerta(0 u 8: podría tener encima otra sala)
                #También compruebo si lo que hay a ambos lados de ese bloque disponible, es otro bloque posible de puerta, o es un muro esquina posible(5)
                if(self.matrix[pos_y-1][pos_x] == 0 or self.matrix[pos_y-1][pos_x] == 8):
                    if(self.matrix[pos_y-1][pos_x-1] == 0 or self.matrix[pos_y-1][pos_x-1] == 8 or self.matrix[pos_y-1][pos_x-1] == 5):
                        if(self.matrix[pos_y-1][pos_x+1] == 0 or self.matrix[pos_y-1][pos_x+1] == 8 or self.matrix[pos_y-1][pos_x+1] == 4):                        
                            room_to = self.getRoomAtPoint(pos_x,pos_y-1,room_sizes,room_start_points)
                            existe_conn = self.existeConexion(i,room_to,[])
                            #print("existe conn entre "+str(i)+" y "+str(room_to)+" = "+str(existe_conn))
                            if(room_to != -1 and not existe_conn):
                                if(self.matrix[pos_y-1][pos_x] == 8):
                                    #print("cambio en == 8")
                                    self.adyacencias[i][room_to] = 1
                                    self.salas[i].daASalas[room_to] = [[pos_x,pos_y],None]
                                    self.adyacencias[room_to][i] = 1
                                    self.salas[room_to].daASalas[i] = [[pos_x,pos_y-1],None]
                                    self.matrix[pos_y][pos_x] = 12
                                    self.matrix[pos_y-1][pos_x] = 13
                            else:
                                if(posibles_puertas_por_sala[i].get("arriba") != None):
                                    posibles_puertas_por_sala[i]["arriba"] += [[pos_x,pos_y]]
                                else:
                                    posibles_puertas_por_sala[i]["arriba"] = [[pos_x,pos_y]]

            pos_x = room_end_points[i][0]
            for pos_y in range(room_start_points[i][1]+1,room_end_points[i][1]):
                #como es muro dcho, compruebo si lo que tiene a su derecha es un bloque de posible puerta(0 o 9)
                if(self.matrix[pos_y][pos_x+1] == 0 or self.matrix[pos_y][pos_x+1] == 9):
                    if(self.matrix[pos_y-1][pos_x+1] == 0 or self.matrix[pos_y-1][pos_x+1] == 9 or self.matrix[pos_y-1][pos_x+1] == 2):
                        if(self.matrix[pos_y+1][pos_x+1] == 0 or self.matrix[pos_y+1][pos_x+1] == 9 or self.matrix[pos_y+1][pos_x+1] == 5):                        
                            room_to = self.getRoomAtPoint(pos_x+1,pos_y,room_sizes,room_start_points)
                            existe_conn = self.existeConexion(i,room_to,[])
                            #print("existe conn entre "+str(i)+" y "+str(room_to)+" = "+str(existe_conn))
                            if(room_to != -1 and not existe_conn):
                                #print("cambio en == 9")
                                if(self.matrix[pos_y][pos_x+1] == 9):
                                    self.adyacencias[i][room_to] = 1
                                    self.salas[i].daASalas[room_to] = [[pos_x,pos_y],None]
                                    self.adyacencias[room_to][i] = 1
                                    self.salas[room_to].daASalas[i] = [[pos_x+1,pos_y],None]
                                    self.matrix[pos_y][pos_x] = 11
                                    self.matrix[pos_y][pos_x+1] = 10
                            else:
                                if(posibles_puertas_por_sala[i].get("derecha") != None):
                                    posibles_puertas_por_sala[i]["derecha"] += [[pos_x,pos_y]]
                                else:
                                    posibles_puertas_por_sala[i]["derecha"] = [[pos_x,pos_y]]
                
            pos_y = room_end_points[i][1]
            for pos_x in range(room_start_points[i][0]+1,room_end_points[i][0]):  
                #como es muro inferior, compruebo si lo que tiene justo debajo es un bloque de posible puerta(0 o 6)
                if(self.matrix[pos_y+1][pos_x] == 0 or self.matrix[pos_y+1][pos_x] == 6):
                    if(self.matrix[pos_y+1][pos_x+1] == 0 or self.matrix[pos_y+1][pos_x+1] == 6 or self.matrix[pos_y+1][pos_x+1] == 3):
                        if(self.matrix[pos_y+1][pos_x-1] == 0 or self.matrix[pos_y+1][pos_x-1] == 6 or self.matrix[pos_y+1][pos_x-1] == 2):                        
                            room_to = self.getRoomAtPoint(pos_x,pos_y+1,room_sizes,room_start_points)
                            existe_conn = self.existeConexion(i,room_to,[])
                            #print("existe conn entre "+str(i)+" y "+str(room_to)+" = "+str(existe_conn))
                            if(room_to != -1 and not existe_conn):
                                if(self.matrix[pos_y+1][pos_x] == 6):
                                    #print("cambion en == 6")
                                    self.adyacencias[i][room_to] = 1
                                    self.salas[i].daASalas[room_to] = [[pos_x,pos_y],None]
                                    self.adyacencias[room_to][i] = 1
                                    self.salas[room_to].daASalas[i] = [[pos_x,pos_y+1],None]
                                    self.matrix[pos_y][pos_x] = 13
                                    self.matrix[pos_y+1][pos_x] = 12
                            else:
                                if(posibles_puertas_por_sala[i].get("abajo") != None):
                                    posibles_puertas_por_sala[i]["abajo"] += [[pos_x,pos_y]]
                                else:
                                    posibles_puertas_por_sala[i]["abajo"] = [[pos_x,pos_y]]

            pos_x = room_start_points[i][0]
            for pos_y in range(room_start_points[i][1]+1,room_end_points[i][1]):
                #como es muro izqdo, compruebo si lo que tiene a su izquierda es un bloque de posible puerta(0 o 7)
                if(self.matrix[pos_y][pos_x-1] == 0 or self.matrix[pos_y][pos_x-1] == 7):
                    if(self.matrix[pos_y+1][pos_x-1] == 0 or self.matrix[pos_y+1][pos_x-1] == 7 or self.matrix[pos_y+1][pos_x-1] == 4):
                        if(self.matrix[pos_y-1][pos_x-1] == 0 or self.matrix[pos_y-1][pos_x-1] == 7 or self.matrix[pos_y-1][pos_x-1] == 3):                        
                            room_to = self.getRoomAtPoint(pos_x-1,pos_y,room_sizes,room_start_points)
                            existe_conn = self.existeConexion(i,room_to,[])
                            #print("existe conn entre "+str(i)+" y "+str(room_to)+" = "+str(existe_conn))
                            if(room_to != -1 and not existe_conn):
                                if(self.matrix[pos_y][pos_x-1] == 7):
                                    #print("cambio en == 7")
                                    self.adyacencias[i][room_to] = 1
                                    self.salas[i].daASalas[room_to] = [[pos_x,pos_y],None]
                                    self.adyacencias[room_to][i] = 1
                                    self.salas[room_to].daASalas[i] = [[pos_x-1,pos_y],None]
                                    self.matrix[pos_y][pos_x] = 10
                                    self.matrix[pos_y][pos_x-1] = 11
                            else:
                                if(posibles_puertas_por_sala[i].get("izquierda") != None):
                                    posibles_puertas_por_sala[i]["izquierda"] += [[pos_x,pos_y]]
                                else:
                                    posibles_puertas_por_sala[i]["izquierda"] = [[pos_x,pos_y]]

        
        #self.printPosiblesPuertas(posibles_puertas_por_sala)  
        #el orden será en el sentido de las agujas del reloj
        heuristicas_por_sala = self.calculateHeuristics()
        #print(heuristicas_por_sala)
        # print("-------------------")
        # print(self.adyacencias)

        for salas in heuristicas_por_sala:
            i = heuristicas_por_sala[salas][2]
            num_sala = heuristicas_por_sala[salas][3]
            orden = heuristicas_por_sala[salas][1]
            orden2 = heuristicas_por_sala[str(num_sala)+"_"+str(i)][1]
            for direccion in orden:
                for direccion2 in orden2:
                    #calculamos cuál es la mejor puerta y puerta2 para las 2 direcciones dadas
                    heuristicas_por_puerta = {}
                    if(posibles_puertas_por_sala[i][direccion] != None):
                        for puerta in posibles_puertas_por_sala[i][direccion]:
                            if(posibles_puertas_por_sala[num_sala][direccion2] != None):
                                for puerta2 in posibles_puertas_por_sala[num_sala][direccion2]:
                                    distancia_x =  puerta[0]-puerta2[0]
                                    distancia_y = puerta[1]-puerta2[1]
                                    d = np.sqrt(distancia_x**2 + distancia_y**2)
                                    heuristicas_por_puerta[str(puerta)+"_"+str(puerta2)] = [d,puerta,puerta2]
                    heuristicas_por_puerta = dict(sorted(heuristicas_por_puerta.items(), key=lambda x: x[1][0]))
                    for pair_of_doors in heuristicas_por_puerta.items():
                        #intentamos unir las 2 puertas con mejor heurística, y si no, se prueba con las siguientes.
                        #Si encuentra camino, marcamos las 2 salas como conectadas. 
                        door_from = pair_of_doors[1][1]
                        door_to = pair_of_doors[1][2]
                        camino = []
                        conn = self.existeConexion(i,num_sala,[])
                        if(not conn):
                            #print("No existe camino entre la sala "+str(i)+" y "+str(num_sala))
                            #sabemos que el +1 en la dirección indicada cumple los requisitos. Ahora hay que trazar el camino desde ese +1
                            if(direccion == "arriba"):
                                current_x = door_from[0] 
                                current_y = door_from[1]-1
                                camino += ["arriba"]
                            elif(direccion == "derecha"):
                                current_x = door_from[0]+1 
                                current_y = door_from[1]
                                camino += ["derecha"]
                            elif(direccion == "abajo"):
                                current_x = door_from[0] 
                                current_y = door_from[1]+1
                                camino += ["abajo"]
                            elif(direccion == "izquierda"):
                                current_x = door_from[0]-1 
                                current_y = door_from[1]
                                camino += ["izquierda"]
                            #proceso de crear camino
                            camino_final = self.caminoPosible(current_x,current_y,door_from,door_to,camino,i,num_sala,set())
                            
                            if(camino_final[0] == True):
                                #cambiar las casillas en la matriz
                                #print("Camino creado entre salas "+str(i)+" y "+str(num_sala)+" y puertas "+str(door_from)+" - "+str(door_to))
                                self.modifyMapWithCamino(door_from,door_to,camino_final)
                                self.salas[i].daASalas[num_sala] = [[door_from[0],door_from[1]],None]
                                self.salas[num_sala].daASalas[i] = [[door_to[0],door_to[1]],None]
                            else:
                                #no existe un camino entre esas 2 puertas, pasamos a la siguiente combinación de puertas por si hubiera más suerte
                                continue
                            #al terminar:
                            if(self.todasLasSalasAlcanzables(room_start_points)):
                                return 
                            
    def modifyMapWithCamino(self,door_from,door_to,camino):
        current_x = door_from[0]
        current_y = door_from[1]
        #print(camino)
        if(camino[1][0] == "arriba"):
            self.matrix[current_y][current_x] = 12
        elif(camino[1][0] == "abajo"):
            self.matrix[current_y][current_x] = 13
        elif(camino[1][0] == "derecha"):
            self.matrix[current_y][current_x] = 11
        elif(camino[1][0] == "izquierda"):
            self.matrix[current_y][current_x] = 10
        for next_direccion in camino[1][0:]:
            if(next_direccion == "arriba"):
                current_y -=1
                if(current_x == door_to[0] and current_y == door_to[1]):
                    self.matrix[current_y][current_x] = 13
                else:
                    self.matrix[current_y][current_x] = 22
            elif(next_direccion == "abajo"):
                current_y +=1
                if(current_x == door_to[0] and current_y == door_to[1]):
                    self.matrix[current_y][current_x] = 12
                else:
                    self.matrix[current_y][current_x] = 22
            elif(next_direccion == "izquierda"):
                current_x -=1
                if(current_x == door_to[0] and current_y == door_to[1]):
                    self.matrix[current_y][current_x] = 11
                else:
                    self.matrix[current_y][current_x] = 22
            elif(next_direccion == "derecha"):
                current_x +=1
                if(current_x == door_to[0] and current_y == door_to[1]):
                    self.matrix[current_y][current_x] = 10
                else:
                    self.matrix[current_y][current_x] = 22
                            
    def caminoPosible(self,current_x,current_y,door_from,door_to,camino,s1,s2,currentCasillasPasadas):
        start = (current_x, current_y)
        goal = (door_to[0], door_to[1])
        
        open_set = []
        heapq.heappush(open_set, (0, start, camino))
        closed_set = set() 


        g_score = {start: 0}
        
        while open_set:
            f_score, (x, y), path = heapq.heappop(open_set)
            if (x, y) == goal:
                self.adyacencias[s1][s2] = 2
                self.adyacencias[s2][s1] = 2
                return [True, path]


            if (x, y) in closed_set:
                continue
            closed_set.add((x, y))


            direcciones = {
                "arriba": (0, -1),
                "abajo": (0, 1),
                "izquierda": (-1, 0),
                "derecha": (1, 0)
            }
            for direccion, (dx, dy) in direcciones.items():
                nx, ny = x + dx, y + dy
                new_pos = (nx, ny)

                # Verificamos si la nueva posición está dentro de los límites
                if not (0 <= ny < len(self.matrix) and 0 <= nx < len(self.matrix[0])):
                    continue

                tile = self.matrix[ny][nx]

                # Condición de validez: el tile no debe ser un obstáculo (0 o valores fuera de rango)
                if not(tile == 0 or 14 <= tile <= 22 or (nx == door_to[0] and ny == door_to[1])):
                    continue

                # Calculamos el coste g y f del nuevo nodo
                tentative_g_score = g_score[(x, y)] + 1
                if new_pos not in g_score or tentative_g_score < g_score[new_pos]:
                    g_score[new_pos] = tentative_g_score
                    h_score = np.sqrt((goal[0] - nx) ** 2 + (goal[1] - ny) ** 2)  # Heurística: distancia euclidiana
                    f_score = tentative_g_score + h_score
                    heapq.heappush(open_set, (f_score, new_pos, path + [direccion]))
        return [False, None]

    def calculateHeuristics(self):
        heuristicas_por_sala = {}
        for sala,centroide in self.centroides.items():
            for sala_2,centroide2 in self.centroides.items():
                if(sala_2 != sala):
                    heuristicas_por_sala[str(sala)+"_"+str(sala_2)] = {} 
                    distance_x = centroide[0]-centroide2[0]
                    distance_y = centroide[1]-centroide2[1]
                    if(abs(distance_x) >= abs(distance_y)):
                        #está más cerca en el eje y que en el x: arriba-abajo
                        if(distance_y < 0):
                            #si y es negativa, quiere decir que se encuentra hacia abajo del recuadro actual
                            if(distance_x < 0): 
                                #si es negativo quiere decir que se encuentra hacia la derecha
                                orden = ["abajo","derecha","arriba","izquierda"]
                            else:
                                orden = ["abajo","izquierda","arriba","derecha"]
                        else:
                            if(distance_x < 0): 
                                orden = ["arriba","derecha","abajo","izquierda"]
                            else:
                                orden = ["arriba","izquierda","abajo","derecha"]
                    else:
                        #está más cerca en el eje x: derecha-izqda
                        if(distance_x < 0):
                            if(distance_y < 0): 
                                orden = ["derecha","abajo","izquierda","arriba"]
                            else:
                                orden = ["derecha","arriba","izquierda","abajo"]
                        else:
                            if(distance_y < 0): 
                                orden = ["izquierda","abajo","derecha","arriba"]
                            else:
                                orden = ["izquierda","arriba","derecha","abajo"]


                    d = np.sqrt(distance_x**2 + distance_y**2)
                    heuristicas_por_sala[str(sala)+"_"+str(sala_2)] = [int(d),orden,sala,sala_2] # sala 0: [sala 1, 58], donde 58 es la distancia entre los centroides
        #las ordeno de menor a mayor valor de heurística
        heuristicas_por_sala = dict(sorted(heuristicas_por_sala.items(), key=lambda item: item[1][0]))
        return heuristicas_por_sala
                    
    def printPosiblesPuertas(self,posibles_puertas_por_sala):
        print("------------------")
        for i,direccion in posibles_puertas_por_sala.items():
            print("Sala "+str(i)+":")
            print("     - arriba: "+str(direccion["arriba"]))
            print("     - abajo: "+str(direccion["abajo"]))
            print("     - izquierda: "+str(direccion["izquierda"]))
            print("     - derecha: "+str(direccion["derecha"]))

    def printSubMap(self,room_size,x_start,y_start,i):
        print("----------")
        print("Sala "+str(i))
        print("----------")
        print("Tamaño: "+str(room_size))
        print("pos_x, pos_y: "+str(x_start)+","+str(y_start))
        print("matrix of sala:")
        end_subm_x = x_start + room_size[0]
        end_subm_y = y_start + room_size[1] 
        submatriz = self.matrix[y_start:end_subm_y,x_start:end_subm_x]
        print(submatriz)

    def paintMap(self,ubicacion):
        #printeo de casillas        
        pygame.init()
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) 
        #self.screen = pygame.display.set_mode((1500,600)) #para pruebas de tamaño 1
        self.screen = pygame.display.set_mode((974,550)) #para pruebas de tamaño 2
        info = pygame.display.Info()
        # --------------SEMILLA ----------------------
        #seed_random = 33
        seed_random = random.randint(0,10000) #por defecto es aleatoria, pero se puede poner la de arriba
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
        self.screen.fill((0,0,0))
        for i in range(0,26):
            for j in range(0,10):
                try:
                    tile = pygame.image.load("tiles/"+ubicacion+"/"+str(self.matrix[j][i])+".png")
                    self.screen.blit(pygame.transform.scale(tile, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*i, (self.height/87.5000)+(self.height/21.8750)*j)) #32 32 8 8
                except:
                    pass
                try:
                    id = self.objetos[j][i]
                    if(not (87 <= id <= 90)):
                        object = pygame.image.load("tiles/"+ubicacion+"/"+str(id)+".png")
                        self.screen.blit(pygame.transform.scale(object, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*i, (self.height/87.5000)+(self.height/21.8750)*j)) #32 32 8 8
                    else:
                        if(id == 87):
                            self.screen.blit(pygame.transform.scale(self.frames[1][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*i, (self.height/87.5000)+(self.height/21.8750)*j)) #32 32 8 8
                        elif(id== 88):
                            self.screen.blit(pygame.transform.scale(self.frames[3][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*i, (self.height/87.5000)+(self.height/21.8750)*j)) #32 32 8 8
                        elif(id==89):
                            self.screen.blit(pygame.transform.scale(self.frames[0][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*i, (self.height/87.5000)+(self.height/21.8750)*j)) #32 32 8 8
                        elif(id==90):
                            self.screen.blit(pygame.transform.scale(self.frames[2][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*i, (self.height/87.5000)+(self.height/21.8750)*j)) #32 32 8 8
                except:
                    pass
        current_tiles = [0,0]

        # self.screen.blit(pygame.transform.scale(self.map, (self.width/1.4252, self.height/1.5837)), (self.width/150.0000, self.height/87.5000)) #842 442 8 8
        pygame.display.update() 

        while(True):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if(event.key == pygame.K_UP):
                        if(current_tiles[1] > 0):
                            current_tiles[1] -=1
                            cont_x = 0
                            cont_y = 0
                            self.screen.fill((0,0,0))
                            for i in range(current_tiles[0],current_tiles[0]+26):
                                cont_x = 0
                                for j in range(current_tiles[1],current_tiles[1]+10):
                                    try:
                                        tile = pygame.image.load("tiles/"+ubicacion+"/"+str(self.matrix[j][i])+".png")
                                        self.screen.blit(pygame.transform.scale(tile, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                    except:
                                        pass
                                    try:
                                        id = self.objetos[j][i]
                                        if(not (87 <= id <= 90)):
                                            object = pygame.image.load("tiles/"+ubicacion+"/"+str(id)+".png")
                                            self.screen.blit(pygame.transform.scale(object, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                        else:
                                            if(id == 87):
                                                self.screen.blit(pygame.transform.scale(self.frames[1][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                            elif(id== 88):
                                                self.screen.blit(pygame.transform.scale(self.frames[3][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                            elif(id==89):
                                                self.screen.blit(pygame.transform.scale(self.frames[0][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                            elif(id==90):
                                                self.screen.blit(pygame.transform.scale(self.frames[2][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                    except Exception as e:
                                        print(e)
                                        pass
                                    cont_x +=1
                                cont_y +=1
                            pygame.display.update()
                    elif(event.key == pygame.K_DOWN):
                        if(current_tiles[1] < self.map_size):
                            current_tiles[1] +=1
                            cont_x = 0
                            cont_y = 0
                            self.screen.fill((0,0,0))
                            for i in range(current_tiles[0],current_tiles[0]+26):
                                cont_x = 0
                                for j in range(current_tiles[1],current_tiles[1]+10):
                                    try:
                                        tile = pygame.image.load("tiles/"+ubicacion+"/"+str(self.matrix[j][i])+".png")
                                        self.screen.blit(pygame.transform.scale(tile, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                    except:
                                        pass
                                    try:
                                        id = self.objetos[j][i]
                                        if(not (87 <= id <= 90)):
                                            object = pygame.image.load("tiles/"+ubicacion+"/"+str(id)+".png")
                                            self.screen.blit(pygame.transform.scale(object, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                        else:
                                            if(id == 87):
                                                self.screen.blit(pygame.transform.scale(self.frames[1][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                            elif(id== 88):
                                                self.screen.blit(pygame.transform.scale(self.frames[3][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                            elif(id==89):
                                                self.screen.blit(pygame.transform.scale(self.frames[0][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                            elif(id==90):
                                                self.screen.blit(pygame.transform.scale(self.frames[2][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                    except Exception as e:
                                        print(e)
                                        pass
                                    cont_x +=1
                                cont_y +=1
                            pygame.display.update()
                    elif(event.key == pygame.K_LEFT):
                        if(current_tiles[0] > 0):
                            current_tiles[0] -=1
                            cont_x = 0
                            cont_y = 0
                            self.screen.fill((0,0,0))
                            for i in range(current_tiles[0],current_tiles[0]+26):
                                cont_x = 0
                                for j in range(current_tiles[1],current_tiles[1]+10):
                                    try:
                                        tile = pygame.image.load("tiles/"+ubicacion+"/"+str(self.matrix[j][i])+".png")
                                        self.screen.blit(pygame.transform.scale(tile, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                    except:
                                        pass
                                    try:
                                        id = self.objetos[j][i]
                                        if(not (87 <= id <= 90)):
                                            object = pygame.image.load("tiles/"+ubicacion+"/"+str(id)+".png")
                                            self.screen.blit(pygame.transform.scale(object, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                        else:
                                            if(id == 87):
                                                self.screen.blit(pygame.transform.scale(self.frames[1][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                            elif(id== 88):
                                                self.screen.blit(pygame.transform.scale(self.frames[3][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                            elif(id==89):
                                                self.screen.blit(pygame.transform.scale(self.frames[0][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                            elif(id==90):
                                                self.screen.blit(pygame.transform.scale(self.frames[2][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                    except Exception as e:
                                        print(e)
                                        pass
                                    cont_x +=1
                                cont_y +=1
                            pygame.display.update()
                    elif(event.key == pygame.K_RIGHT):
                        if(current_tiles[0] < self.map_size):
                            current_tiles[0] +=1
                            cont_x = 0
                            cont_y = 0
                            self.screen.fill((0,0,0))
                            for i in range(current_tiles[0],current_tiles[0]+26):
                                cont_x = 0
                                for j in range(current_tiles[1],current_tiles[1]+10):
                                    try:
                                        tile = pygame.image.load("tiles/"+ubicacion+"/"+str(self.matrix[j][i])+".png")
                                        self.screen.blit(pygame.transform.scale(tile, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                    except:
                                        pass
                                    try:
                                        id = self.objetos[j][i]
                                        if(not (87 <= id <= 90)):
                                            object = pygame.image.load("tiles/"+ubicacion+"/"+str(id)+".png")
                                            self.screen.blit(pygame.transform.scale(object, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                        else:
                                            if(id == 87):
                                                self.screen.blit(pygame.transform.scale(self.frames[1][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                            elif(id== 88):
                                                self.screen.blit(pygame.transform.scale(self.frames[3][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                            elif(id==89):
                                                self.screen.blit(pygame.transform.scale(self.frames[0][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                            elif(id==90):
                                                self.screen.blit(pygame.transform.scale(self.frames[2][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                    except Exception as e:
                                        print(e)
                                        pass
                                    cont_x +=1
                                cont_y +=1
                            pygame.display.update()


    def drawMapInGame(self,ubicacion,width,height,screen,player_pos):
        currentTilePlayer = player_pos
        if((currentTilePlayer[0] >=13) and (currentTilePlayer[0] < 87)):
            #se puede printear normal
            i_start = currentTilePlayer[0]-13
        elif((currentTilePlayer[0] >=13) and (currentTilePlayer[0] >= 87)):
            i_start = currentTilePlayer[0]-26+(99-currentTilePlayer[0])
        else:
            i_start = 0
        if((currentTilePlayer[1] < 93) and (currentTilePlayer[1] >=6)):
            j_start = currentTilePlayer[1]-6
        elif((currentTilePlayer[1] <93) and (currentTilePlayer[1] <6)):
            j_start = 0
        else:
            j_start = currentTilePlayer[1]-13+(99-currentTilePlayer[1])
        cont_x = 0
        cont_y = 0
        #el tamaño de la pantalla es de 26 x 10, y la casilla actual del jugador debe ser la del medio
        blackScreen = pygame.Rect(width/150.0000, height/87.5000, width/1.4252, height/1.5837) #25 470 810 124
        pygame.draw.rect(screen, pygame.Color(0,0,0), blackScreen, 0)
        for i in range(i_start,i_start+26):
            cont_x = 0
            for j in range(j_start,j_start+13):
                if(int(self.casillasVistas[i][j]) == 1):
                    try:
                        integ = int(self.matrix[j][i])
                        tile = self.tile_cache[integ]
                        if tile is not None:
                            screen.blit(pygame.transform.scale(tile, (self.map_tileSize[0],self.map_tileSize[1])), ((width/150.0000)+(self.map_tileSize[0])*cont_y, (height/87.5000)+(self.map_tileSize[1])*cont_x)) #32 32 8 8
                    except:
                        pass
                    try:
                        id = int(self.objetos[j][i])
                        if(not (87 <= id <= 90)):
                            object = self.tile_cache[id]
                            if object is not None:
                                screen.blit(pygame.transform.scale(object, (self.map_tileSize[0],self.map_tileSize[1])), ((width/150.0000)+(self.map_tileSize[0])*cont_y, (height/87.5000)+(self.map_tileSize[1])*cont_x)) #32 32 8 8
                        else:
                            if(id == 87):
                                screen.blit(pygame.transform.scale(self.frames[1][0], ((self.map_tileSize[0],self.map_tileSize[1]))), ((width/150.0000)+(self.map_tileSize[0])*cont_y, (height/87.5000)+(self.map_tileSize[1])*cont_x)) #32 32 8 8
                            elif(id== 88):
                                screen.blit(pygame.transform.scale(self.frames[3][0], ((self.map_tileSize[0],self.map_tileSize[1]))), ((width/150.0000)+(self.map_tileSize[0])*cont_y, (height/87.5000)+(self.map_tileSize[1])*cont_x)) #32 32 8 8
                            elif(id==89):
                                screen.blit(pygame.transform.scale(self.frames[0][0], ((self.map_tileSize[0],self.map_tileSize[1]))), ((width/150.0000)+(self.map_tileSize[0])*cont_y, (height/87.5000)+(self.map_tileSize[1])*cont_x)) #32 32 8 8
                            elif(id==90):
                                screen.blit(pygame.transform.scale(self.frames[2][0], ((self.map_tileSize[0],self.map_tileSize[1]))), ((width/150.0000)+(self.map_tileSize[0])*cont_y, (height/87.5000)+(self.map_tileSize[1])*cont_x)) #32 32 8 8
                    except:
                        pass
                cont_x +=1
            cont_y +=1
        return screen

    def drawMapOutGame(self,ubicacion):
        #printeo de casillas        
        pygame.init()
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) 
        #self.screen = pygame.display.set_mode((1500,600)) #para pruebas de tamaño 1
        self.screen = pygame.display.set_mode((974,550)) #para pruebas de tamaño 2
        info = pygame.display.Info()
        # --------------SEMILLA ----------------------
        #seed_random = 33
        seed_random = random.randint(0,10000) #por defecto es aleatoria, pero se puede poner la de arriba
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
        self.screen.fill((0,0,0))

        currentTilePlayer = self.spawn
        print(currentTilePlayer)
        if(currentTilePlayer[0] >=13 and currentTilePlayer[0] < 87):
            #se puede printear normal
            i_start = currentTilePlayer[0]-13
        elif(currentTilePlayer[0] >=13 and currentTilePlayer[0] >= 87):
            i_start = currentTilePlayer[0]-26+(99-currentTilePlayer[0])
        else:
            i_start = 0
        if(currentTilePlayer[1] < 93 and currentTilePlayer[1] >=6):
            j_start = currentTilePlayer[1]-6
        elif(currentTilePlayer[1] <93 and currentTilePlayer[1] <6):
            j_start = 0
        else:
            j_start = currentTilePlayer[1]-13+(99-currentTilePlayer[1])
        cont_x = 0
        cont_y = 0
        width = self.width
        height = self.height
        screen = self.screen
        #el tamaño de la pantalla es de 26 x 10, y la casilla actual del jugador debe ser la del medio
        for i in range(i_start,i_start+26):
            cont_x = 0
            for j in range(j_start,j_start+13):
                if(self.casillasVistas[i][j] == 1):
                    try:
                        tile = pygame.image.load("tiles/"+ubicacion+"/"+str(self.matrix[j][i])+".png")
                        screen.blit(pygame.transform.scale(tile, (self.map_tileSize)), ((width/150.0000)+(self.map_tileSize[0])*cont_y, (height/87.5000)+(self.map_tileSize[1])*cont_x)) #32 32 8 8
                    except:
                        pass
                    try:
                        id = self.objetos[j][i]
                        if(not (87 <= id <= 90)):
                            object = pygame.image.load("tiles/"+ubicacion+"/"+str(id)+".png")
                            screen.blit(pygame.transform.scale(object, (self.map_tileSize)), ((width/150.0000)+(self.map_tileSize[0])*cont_y, (height/87.5000)+(self.map_tileSize[1])*cont_x)) #32 32 8 8
                        else:
                            if(id == 87):
                                screen.blit(pygame.transform.scale(self.frames[1][0], (self.map_tileSize)), ((width/150.0000)+(self.map_tileSize[0])*cont_y, (height/87.5000)+(self.map_tileSize[1])*cont_x)) #32 32 8 8
                            elif(id== 88):
                                screen.blit(pygame.transform.scale(self.frames[3][0], (self.map_tileSize)), ((width/150.0000)+(self.map_tileSize[0])*cont_y, (height/87.5000)+(self.map_tileSize[1])*cont_x)) #32 32 8 8
                            elif(id==89):
                                screen.blit(pygame.transform.scale(self.frames[0][0], (self.map_tileSize)), ((width/150.0000)+(self.map_tileSize[0])*cont_y, (height/87.5000)+(self.map_tileSize[1])*cont_x)) #32 32 8 8
                            elif(id==90):
                                screen.blit(pygame.transform.scale(self.frames[2][0], (self.map_tileSize)), ((width/150.0000)+(self.map_tileSize[0])*cont_y, (height/87.5000)+(self.map_tileSize[1])*cont_x)) #32 32 8 8
                    except:
                        pass
                cont_x +=1
            cont_y +=1
            pygame.display.update()
        while(True):
            pass

        
    def drawNPC(self,id,i,j):
        #printeo de casillas        
        pygame.init()
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) 
        #self.screen = pygame.display.set_mode((1500,600)) #para pruebas de tamaño 1
        self.screen = pygame.display.set_mode((974,550)) #para pruebas de tamaño 2
        info = pygame.display.Info()
        # --------------SEMILLA ----------------------
        #seed_random = 33
        seed_random = random.randint(0,10000) #por defecto es aleatoria, pero se puede poner la de arriba
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
        self.screen.fill((0,0,0))
        try:
            for i in range(0,9):
                self.screen.blit(pygame.transform.scale(self.frames[0][i], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*i, (self.height/87.5000)+(self.height/21.8750)*j)) #32 32 8 8
            # if(id == 87):
            #     self.screen.blit(pygame.transform.scale(self.frames[1][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*i, (self.height/87.5000)+(self.height/21.8750)*j)) #32 32 8 8
            # elif(id== 88):
            #     self.screen.blit(pygame.transform.scale(self.frames[3][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*i, (self.height/87.5000)+(self.height/21.8750)*j)) #32 32 8 8
            # elif(id==89):
            #     self.screen.blit(pygame.transform.scale(self.frames[0][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*i, (self.height/87.5000)+(self.height/21.8750)*j)) #32 32 8 8
            # elif(id==90):
            #     self.screen.blit(pygame.transform.scale(self.frames[2][0], ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*i, (self.height/87.5000)+(self.height/21.8750)*j)) #32 32 8 8
        except Exception as e:
            print(e)
        pygame.display.update()
        while(True):
            pass
        
# #zona de pruebas
# tipo_mapa = ["mazmorra","barco","desierto","bosque","aldea medieval","ciudad moderna"]
# currentPartida = "p1"
# lista_mobs_disponibles = {"mazmorra": ["esqueleto","zombie","slime","beholder","troll"],# 33, 34, 35, 36, 37
#                                   "ciudad moderna": ["droide","fantasma","objeto animado de silla", "mimic de cofre", "muñeca animada", "cyborg"], #38,39,40,41,42,43
#                                   "bosque": ["lobo wargo", "vampiro", "oso", "hombre lobo"], #44,45,46,47
#                                   "desierto": ["serpiente","cocodrilo", "momia", "esfinge"], #48,49,50,51
#                                   "aldea medieval": ["goblin","cultista","gnoll","elemental de roca"], #52,53,54,55
#                                   "barco": ["sirena","tiburón","hada","kraken"], #56,57,58,59
#                                   "raros": ["dragón","sombras","fénix"], #60,61,62
#                                   "medio": ["ankheg","basilísco"], #63,64
#                                   "comun": ["murciélago","rata","felino salvaje"]} #65,66,67

# ubicacion = tipo_mapa[0]
# tipo_mision_num =2 #random.randint(1,2)
# if(tipo_mision_num == 1):
#     tipo_mision = "combate"
#      # tipo_mobs = random.randint(0,100)
#     mobs = {}
#     num_mobs = random.randint(1,2)
#     n = len(lista_mobs_disponibles[ubicacion])-1
#     for i in range(0,num_mobs):
#         seleccion = random.randint(0,n)
#         if mobs.get(lista_mobs_disponibles[ubicacion][seleccion]) != None:
#             mobs[lista_mobs_disponibles[ubicacion][seleccion]] +=1
#         else:
#             mobs[lista_mobs_disponibles[ubicacion][seleccion]] = 1
            
#     mision = "Hay que matar "
#     variableDeCheck = {}
#     for mob_name,num in mobs.items():
#         mision += str(num)+" "+mob_name+","
#         variableDeCheck[mob_name] = [num,0] #5,0 -> 5 de ese tipo a matar, 0 matados
            
# elif(tipo_mision_num == 2):
#     tipo_mision = "búsqueda"
#     lugar_posible = ["Árbol","Cadáver de dragón","Parte de cadáver de Dragón","Cofre","Armario","Ruina"] #68,69,70,71-74,75-78,79
#     n = len(lugar_posible)-1
#     lugar = random.randint(0,n)
#     mision = "Hay que encontrar lo siguiente: "+lugar_posible[lugar]
#     variableDeCheck = {}
#     variableDeCheck[lugar_posible[lugar]] = False #ninguno de los jugadores lo ha encontrado
# carpeta = "animations/NPCs/elfo_vive en el bosque_75_430_de piel verde/walk.png"
# Mapa = Map_generation(ubicacion,currentPartida,tipo_mision,variableDeCheck,1,carpeta,1234,1200,700) #que genere el mapa de una mazmorra
# #Mapa.paintMap(ubicacion)
# #Mapa.drawMapOutGame("mazmorra")
# Mapa.drawNPC(87,3,3)