import pygame
import os
import random
import numpy as np

# 0: Casilla sin determinar
# 1: 


class Map_generation:
    def __init__(self,eleccion,currentPartida):
        config_dir = 'mapas'
        config_file = 'mapa_'+currentPartida+".txt"
        self.eleccion = eleccion
        self.map_size = 100
        self.centroides = {}
        self.salas = {}
        self.matrix = np.zeros((self.map_size,self.map_size), dtype=int) #matriz de 0s de 500 x 500 -> es el mapa
        if(self.eleccion == "mazmorra"):
            self.createMazmorra() 
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
        length_min_one_side = 5 #lo mínimo sería 5 x 5
        room_sizes = {}
        room_start_points = {}
        #De forma aleatoria determinamos el tamaño de las salas de la mazmorra, teniendo en cuenta las limitaciones de espacio
        for i in range(0,num_aleatorio_salas):
            room_sizes[i] = [random.randint(length_min_one_side,length_max_one_side),random.randint(length_min_one_side,length_max_one_side)]
        self.salas[0] = ["inicial","obligatoria"]
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
                            if(posibles_puertas_por_sala[i].get("arriba") != None):
                                posibles_puertas_por_sala[i]["arriba"] += [[pos_y,pos_x]]
                            else:
                                posibles_puertas_por_sala[i]["arriba"] = [[pos_y,pos_x]]

            pos_x = room_end_points[i][0]
            for pos_y in range(room_start_points[i][1]+1,room_end_points[i][1]):
                #como es muro dcho, compruebo si lo que tiene a su derecha es un bloque de posible puerta(0 o 9)
                if(self.matrix[pos_y][pos_x+1] == 0 or self.matrix[pos_y][pos_x+1] == 8):
                    if(self.matrix[pos_y-1][pos_x+1] == 0 or self.matrix[pos_y-1][pos_x+1] == 8 or self.matrix[pos_y-1][pos_x+1] == 2):
                        if(self.matrix[pos_y+1][pos_x+1] == 0 or self.matrix[pos_y+1][pos_x+1] == 8 or self.matrix[pos_y+1][pos_x+1] == 5):                        
                            if(posibles_puertas_por_sala[i].get("derecha") != None):
                                posibles_puertas_por_sala[i]["derecha"] += [[pos_y,pos_x]]
                            else:
                                posibles_puertas_por_sala[i]["derecha"] = [[pos_y,pos_x]]
                
            pos_y = room_end_points[i][1]
            for pos_x in range(room_start_points[i][0]+1,room_end_points[i][0]):  
                #como es muro inferior, compruebo si lo que tiene justo debajo es un bloque de posible puerta(0 o 6)
                if(self.matrix[pos_y+1][pos_x] == 0 or self.matrix[pos_y+1][pos_x] == 8):
                    if(self.matrix[pos_y+1][pos_x+1] == 0 or self.matrix[pos_y+1][pos_x+1] == 8 or self.matrix[pos_y+1][pos_x+1] == 3):
                        if(self.matrix[pos_y+1][pos_x-1] == 0 or self.matrix[pos_y+1][pos_x-1] == 8 or self.matrix[pos_y+1][pos_x-1] == 2):                        
                            if(posibles_puertas_por_sala[i].get("abajo") != None):
                                posibles_puertas_por_sala[i]["abajo"] += [[pos_y,pos_x]]
                            else:
                                posibles_puertas_por_sala[i]["abajo"] = [[pos_y,pos_x]]

            pos_x = room_start_points[i][0]
            for pos_y in range(room_start_points[i][1]+1,room_end_points[i][1]):
                #como es muro izqdo, compruebo si lo que tiene a su izquierda es un bloque de posible puerta(0 o 7)
                if(self.matrix[pos_y][pos_x-1] == 0 or self.matrix[pos_y][pos_x-1] == 8):
                    if(self.matrix[pos_y+1][pos_x-1] == 0 or self.matrix[pos_y+1][pos_x-1] == 8 or self.matrix[pos_y+1][pos_x-1] == 4):
                        if(self.matrix[pos_y-1][pos_x-1] == 0 or self.matrix[pos_y-1][pos_x-1] == 8 or self.matrix[pos_y-1][pos_x-1] == 3):                        
                            if(posibles_puertas_por_sala[i].get("izquierda") != None):
                                posibles_puertas_por_sala[i]["izquierda"] += [[pos_y,pos_x]]
                            else:
                                posibles_puertas_por_sala[i]["izquierda"] = [[pos_y,pos_x]]
        #self.printPosiblesPuertas(posibles_puertas_por_sala)  
        #el orden será en el sentido de las agujas del reloj
        heuristicas_por_sala = self.calculateHeuristics()
        print(heuristicas_por_sala)

        for i in room_start_points:
            salas_no_conectables = {}
            for sala in heuristicas_por_sala[i]:
                nearest_sala = sala
                num_sala = nearest_sala[0]
                orden = nearest_sala[2]
                #TODO: Arreglar orden2
                orden2 = heuristicas_por_sala[num_sala][2]
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
                            print(pair_of_doors)
                                         

                                        


                
                



    def calculateHeuristics(self):
        heuristicas_por_sala = {}
        for sala,centroide in self.centroides.items():
            heuristicas_por_sala[sala] = {} 
            for sala_2,centroide2 in self.centroides.items():
                if(sala_2 != sala):
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
                    if(heuristicas_por_sala[sala] == {}):
                        heuristicas_por_sala[sala] = [[sala_2, int(d),orden]] # sala 0: [sala 1, 58], donde 58 es la distancia entre los centroides
                    else:
                        heuristicas_por_sala[sala] += [[sala_2, int(d),orden]]
            #las ordeno de menor a mayor valor de heurística
            heuristicas_por_sala[sala] = sorted(heuristicas_por_sala[sala], key=lambda x: x[1])
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
        #self.screen.blit(pygame.transform.scale(self.map, (self.width/1.4252, self.height/1.5837)), (self.width/150.0000, self.height/87.5000)) #842 442 8 8
        pygame.init()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) 
        #self.screen = pygame.display.set_mode((1500,600)) #para pruebas de tamaño 1
        #self.screen = pygame.display.set_mode((974,550)) #para pruebas de tamaño 2
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
        pygame.display.update() 


    

#zona de pruebas
tipo_mapa = ["mazmorra","barco","desierto","bosque","aldea medieval","ciudad moderna"]
currentPartida = "p1"
Mapa = Map_generation(tipo_mapa[0],currentPartida) #que genere el mapa de una mazmorra
#Mapa.paintMap()