import pygame
import os
import random
import numpy as np
import sys
import heapq


# 0: Casilla sin determinar
# 1: 

class Sala:
    def __init__(self,i,size):
        self.id = i
        self.es_obligatoria = False
        self.esInicial = False
        self.daASalas = []
        self.tienePortales = []
        self.requiereLlave = False
        self.esFinal = False
        self.orden = None
        self.variableDeCheck = None
        self.tipo_mision = None
        self.size = size
        self.pos_x = None
        self.pos_y = None


class Map_generation:
    def __init__(self,eleccion,currentPartida,tipo_mision, variableDeCheck):
        sys.setrecursionlimit(5000)  
        config_dir = 'mapas/'+currentPartida
        config_file = 'mapa_'+currentPartida+".txt"
        self.eleccion = eleccion
        self.map_size = 100
        self.centroides = {}
        self.salas = {}
        self.grafos = {}
        self.adyacencias = None
        self.matrix = np.zeros((self.map_size,self.map_size), dtype=int) #matriz de 0s de 500 x 500 -> es el mapa
        self.objetos = np.zeros((self.map_size,self.map_size), dtype=int) #matriz de 0s de 500 x 500 -> es el mapa
        if(self.eleccion == "mazmorra"):
            self.createMazmorra() 
            self.fillWithObjects(tipo_mision,variableDeCheck)
        elif(self.eleccion == "barco"):
            pass
        elif(self.eleccion == "aldea medieval"):
            pass
        elif(self.eleccion == "ciudad moderna"):
            pass
        elif(self.eleccion == "bosque"):
            pass
        elif(self.eleccion == "desierto"):
            pass
        
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
                    
        with open(config_dir+'/'+config_file, 'w',encoding='utf8') as f:
            for fila in self.matrix:
                f.write(' '.join(map(str, fila)) + '\n')

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
        min_size_room = 25 # tamaño mínimo para ser considerado habitación
        length_max_one_side = int(np.sqrt(max_size_room))
        length_min_one_side = 6 #lo mínimo sería 6 x 6 -> puede haber como mucho 12 mobs a matar, que deberían estar en la última sala (6x6 = 36 - bordes = 16)
        room_sizes = {}
        room_start_points = {}
        #De forma aleatoria determinamos el tamaño de las salas de la mazmorra, teniendo en cuenta las limitaciones de espacio
        for i in range(0,num_aleatorio_salas):
            room_sizes[i] = [random.randint(length_min_one_side,length_max_one_side),random.randint(length_min_one_side,length_max_one_side)]
            self.adyacencias = np.zeros((num_aleatorio_salas,num_aleatorio_salas), dtype=int)
            self.salas[i] = Sala(i,room_sizes[i])

        print("Número total de salas: ", num_aleatorio_salas)
        print("Tamaños de las salas: ")
        print(room_sizes)
        print("---------------------------")
        for i,room_size in room_sizes.items():
            #Determino cuál podría ser una posible posición para esa sala, teniendo en cuenta que debe printearse dentro del cuadro del mapa
            found_place_to_print = False
            count = 0
            while(not found_place_to_print):
                count +=1
                print("intento "+str(count)+" en sala "+str(i))
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
            self.printSubMap(room_size,x_start,y_start,i)
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
                                                self.objetos[currentx][currenty] = 32
                                                self.adyacencias[sala][sala2] = -1

                                    [posx,posy] = room_start_points[sala2]
                                    for currentx in range(posx,posx+room_sizes[sala2]):
                                        for currenty in range(posy,posy+room_sizes[sala2]):
                                            if(self.matrix[currenty][currentx] == 1 and self.matrix[currenty+1][currentx] != 13 and self.matrix[currenty-1][currentx] != 12 and self.matrix[currenty][currentx+1] != 11 and self.matrix[currenty][currentx-1] != 10):
                                                self.salas[sala2].tienePortales += [currentx,currenty]
                                                self.objetos[currentx][currenty] = 32
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

        #Una vez que están todas las salas conectadas, establezco los enlaces directos entre salas
        for sala in self.salas:
            self.setSalasLinked(sala)
            print("Sala "+str(sala)+" acceso directo a:")
            print(self.salas[sala].daASalas)

    def fillWithObjects(self,tipo_mision,variableDeCheck):
        longest_path = self.getLongestPath()
        print("Longest path:")
        print(longest_path[0])
        print(longest_path[1])
        print(longest_path[2])
        print(longest_path[3])
        self.salas[longest_path[0]].esInicial = True
        self.salas[longest_path[0]].orden = 0
        self.salas[longest_path[0]].esObligatoria = True
        self.salas[longest_path[1]].esFinal = True
        cont = 0
        for sala in longest_path[3]:
            cont+=1
            self.salas[sala].esObligatoria = True
            self.salas[sala].orden = cont

        self.salas[longest_path[1]].tipo_mision = tipo_mision
        self.salas[longest_path[1]].variableDeCheck = variableDeCheck

        if(tipo_mision == "combate"):
            mobsMision = []
            for mob in variableDeCheck:
                mobsMision += [mob]
                for i in range(0,variableDeCheck[mob][0]):
                    #numero de mobs a matar de ese tipo -> hay que ubicarlos en esa sala
                    #4x4 = 16. Como mucho 12 mobs, caben de sobra. Se quitan los bordes de la sala
                    ubicado = False
                    for pos_x in range(self.salas[longest_path[1].pos_x+1,self.salas[longest_path[1]].pos_x+self.salas[longest_path[1]].size[0]]-1):
                        for pos_y in range(self.salas[longest_path[1].pos_y+1,self.salas[longest_path[1]].pos_y+self.salas[longest_path[1]].size[1]]-1):
                            if(self.objetos[pos_x][pos_y] == 0):
                                if(mob == "esqueleto"):
                                    self.objetos[pos_x][pos_y] = 33 #trampa de mob -> al dirigirte a esa casilla, antes de poder pasar, el DM introduce al mob, y aparece en la casilla. 
                                elif(mob == "zombie"):
                                    self.objetos[pos_x][pos_y] = 34
                                elif(mob == "slime"):
                                    self.objetos[pos_x][pos_y] = 35
                                elif(mob == "beholder"):
                                    self.objetos[pos_x][pos_y] = 36
                                elif(mob == "troll"):
                                    self.objetos[pos_x][pos_y] = 37
                                ubicado = True
                            if(ubicado):
                                break
                        if(ubicado):
                            break
                    ubicado = False

        elif(tipo_mision == "búsqueda"):
            for objeto in variableDeCheck: #solo hay 1, pero así lo sacamos
                if(objeto == "Árbol"):  #"Árbol","Cadáver de dragón","Parte de cadáver de Dragón","Cofre","Armario","Ruina"
                    for pos_x in range(self.salas[longest_path[1].pos_x+1,self.salas[longest_path[1]].pos_x+self.salas[longest_path[1]].size[0]]-1):
                        for pos_y in range(self.salas[longest_path[1].pos_y+1,self.salas[longest_path[1]].pos_y+self.salas[longest_path[1]].size[1]]-1):
                            if(self.objetos[pos_x][pos_y] == 0):
                    self.objetos[pos_x][pos_y] = 68
                elif(objeto == "Cadáver de dragón"):
                    self.objetos[pos_x][pos_y] = 69
                elif(objeto == "Parte de cadáver de Dragón"):
                    self.objetos[pos_x][pos_y] = 70
                elif(objeto == "Cofre"):
                    self.objetos[pos_x][pos_y] = 71
                elif(objeto == "Armario"):
                    self.objetos[pos_x][pos_y] = 72
                elif(objeto == "Ruina"):
                    self.objetos[pos_x][pos_y] = 73

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



    def setSalasLinked(self,room_from):
        num_sala = -1
        for conn in self.adyacencias[room_from]:
            num_sala +=1
            if(num_sala != room_from):
                if(conn == 1 or conn == 2 or conn == -1):
                    #existe un túnel entre num_sala y room_from
                    self.salas[room_from].daASalas += [num_sala]
            
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
        print(str(cont1)+" respecto a "+str(cont2))
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
                                    self.adyacencias[room_to][i] = 1
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
                                    self.adyacencias[room_to][i] = 1
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
                                    self.adyacencias[room_to][i] = 1
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
                                    self.adyacencias[room_to][i] = 1
                                    self.matrix[pos_y][pos_x] = 10
                                    self.matrix[pos_y][pos_x-1] = 11
                            else:
                                if(posibles_puertas_por_sala[i].get("izquierda") != None):
                                    posibles_puertas_por_sala[i]["izquierda"] += [[pos_x,pos_y]]
                                else:
                                    posibles_puertas_por_sala[i]["izquierda"] = [[pos_x,pos_y]]

        
        self.printPosiblesPuertas(posibles_puertas_por_sala)  
        #el orden será en el sentido de las agujas del reloj
        heuristicas_por_sala = self.calculateHeuristics()
        #print(heuristicas_por_sala)
        print("-------------------")
        print(self.adyacencias)

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
                                print("Camino creado entre salas "+str(i)+" y "+str(num_sala)+" y puertas "+str(door_from)+" - "+str(door_to))
                                self.modifyMapWithCamino(door_from,door_to,camino_final)
                            else:
                                #no existe un camino entre esas 2 puertas, pasamos a la siguiente combinación de puertas por si hubiera más suerte
                                continue
                            #al terminar:
                            if(self.todasLasSalasAlcanzables(room_start_points)):
                                return 
                            
    def modifyMapWithCamino(self,door_from,door_to,camino):
        current_x = door_from[0]
        current_y = door_from[1]
        print(camino)
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

    def paintMap(self):
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
                    tile = pygame.image.load("tiles/dungeon/"+str(self.matrix[j][i])+".png")
                    self.screen.blit(pygame.transform.scale(tile, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*i, (self.height/87.5000)+(self.height/21.8750)*j)) #32 32 8 8
                except:
                    pass
                try:
                    object = pygame.image.load("tiles/dungeon/"+str(self.objetos[j][i])+".png")
                    self.screen.blit(pygame.transform.scale(object, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*i, (self.height/87.5000)+(self.height/21.8750)*j)) #32 32 8 8
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
                                        tile = pygame.image.load("tiles/dungeon/"+str(self.matrix[j][i])+".png")
                                        self.screen.blit(pygame.transform.scale(tile, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                    except:
                                        pass
                                    try:
                                        object = pygame.image.load("tiles/dungeon/"+str(self.objetos[j][i])+".png")
                                        self.screen.blit(pygame.transform.scale(object, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                    except:
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
                                        tile = pygame.image.load("tiles/dungeon/"+str(self.matrix[j][i])+".png")
                                        self.screen.blit(pygame.transform.scale(tile, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                    except:
                                        pass
                                    try:
                                        object = pygame.image.load("tiles/dungeon/"+str(self.objetos[j][i])+".png")
                                        self.screen.blit(pygame.transform.scale(object, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                    except:
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
                                        tile = pygame.image.load("tiles/dungeon/"+str(self.matrix[j][i])+".png")
                                        self.screen.blit(pygame.transform.scale(tile, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                    except:
                                        pass
                                    try:
                                        object = pygame.image.load("tiles/dungeon/"+str(self.objetos[j][i])+".png")
                                        self.screen.blit(pygame.transform.scale(object, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                    except:
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
                                        tile = pygame.image.load("tiles/dungeon/"+str(self.matrix[j][i])+".png")
                                        self.screen.blit(pygame.transform.scale(tile, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                    except:
                                        pass
                                    try:
                                        object = pygame.image.load("tiles/dungeon/"+str(self.objetos[j][i])+".png")
                                        self.screen.blit(pygame.transform.scale(object, ((self.width/37.5000, self.height/21.8750))), ((self.width/150.0000)+(self.width/37.5000)*cont_y, (self.height/87.5000)+(self.height/21.8750)*cont_x)) #32 32 8 8
                                    except:
                                        pass
                                    cont_x +=1
                                cont_y +=1
                            pygame.display.update()



    

#zona de pruebas
tipo_mapa = ["mazmorra","barco","desierto","bosque","aldea medieval","ciudad moderna"]
currentPartida = "p1"
lista_mobs_disponibles = {"mazmorra": ["esqueleto","zombie","slime","beholder","troll"],# 33, 34, 35, 36, 37
                                  "ciudad moderna": ["droide","fantasma","objeto animado de silla", "mimic de cofre", "muñeca animada", "cyborg"], #38,39,40,41,42,43
                                  "bosque": ["lobo wargo", "vampiro", "oso", "hombre lobo"], #44,45,46,47
                                  "desierto": ["serpiente","cocodrilo", "momia", "esfinge"], #48,49,50,51
                                  "aldea medieval": ["goblin","cultista","gnoll","elemental de roca"], #52,53,54,55
                                  "barco": ["sirena","tiburón","hada","kraken"], #56,57,58,59
                                  "raros": ["dragón","sombras","fénix"], #60,61,62
                                  "medio": ["ankheg","basilísco"], #63,64
                                  "comun": ["murciélago","rata","felino salvaje"]} #65,66,67

ubicacion = tipo_mapa[0]
tipo_mision_num = random.randint(1,2)
if(tipo_mision_num == 1):
    tipo_mision = "combate"
     # tipo_mobs = random.randint(0,100)
    mobs = {}
    num_mobs = random.randint(1,2)
    n = len(lista_mobs_disponibles[ubicacion])-1
    for i in range(0,num_mobs):
        seleccion = random.randint(0,n)
        if mobs.get(lista_mobs_disponibles[ubicacion][seleccion]) != None:
            mobs[lista_mobs_disponibles[ubicacion][seleccion]] +=1
        else:
            mobs[lista_mobs_disponibles[ubicacion][seleccion]] = 1
            
    mision = "Hay que matar "
    variableDeCheck = {}
    for mob_name,num in mobs.items():
        mision += str(num)+" "+mob_name+","
        variableDeCheck[mob_name] = [num,0] #5,0 -> 5 de ese tipo a matar, 0 matados
            
elif(tipo_mision_num == 2):
    tipo_mision = "búsqueda"
    lugar_posible = ["Árbol","Cadáver de dragón","Parte de cadáver de Dragón","Cofre","Armario","Ruina"] #68,69,70,71,72,73
    n = len(lugar_posible)-1
    lugar = random.randint(0,n)
    mision = "Hay que encontrar lo siguiente: "+lugar_posible[lugar]
    variableDeCheck = {}
    variableDeCheck[lugar_posible[lugar]] = False #ninguno de los jugadores lo ha encontrado
Mapa = Map_generation(ubicacion,currentPartida,tipo_mision,variableDeCheck) #que genere el mapa de una mazmorra
Mapa.paintMap()