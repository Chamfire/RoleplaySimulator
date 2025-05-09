import Lista_Inventario
import pygame 

class Personaje:
    def __init__(self,isNPC,partida_id,id_jugador_or_NPC):
        self.name = ' ' #lo modifica el jugador
        self.sm1 = False
        self.sm2 = False
        self.sm3 = False
        self.nivel = 1
        self.inspiracion = 0
        self.esta_muerto = False
        self.bpc = None #cambiar al escoger personaje
        self.cons = None
        self.fu = None
        self.des = None
        self.sab = None
        self.car = None
        self.int = None
        #Dinero
        self.pc = 0
        self.pp = 0
        self.pe = 0
        self.po = 0
        self.ppt = 0
        self.genero = None
        self.coordenadas_actuales = '(0,0)' #de momento serán esas
        self.coordenadas_actuales_r = [None,None]
        self.vida_temp = None #cambiar al escoger la clase
        self.max_vida = None
        self.ca = None #cambiar al escoger personaje
        self.edad = ' ' #lo escoge el jugador
        self.peso = None #lo escoge el jugador
        self.velocidad = None #cambiar al escoger la raza
        self.descripcion_fisica = None #la genera la ia
        self.tipo_raza = None #la escoge el jugador
        self.tipo_clase = None #la escoge el jugador
        self.tipo_alineamiento = None #lo escoge el jugador
        self.id_trasfondo = None #lo escoge el jugador
        self.vinculo = None #lo escoge el jugador
        self.defecto = None #lo escoge el jugador
        self.rasgo_personalidad = None #lo escoge el jugador
        self.ideal = None #lo escoge el jugador
        self.tipo_size = None #en función de la raza, será uno u otro
        self.partida_id = partida_id
        self.idiomas_competencia = {"Común":False,"Enano":False,"Éflico":False,"Infernal":False,"Celestial":False,"Abisal":False,"Dracónido":False,"Habla Profunda":False,"Primordial":False,"Silvano":False,"Infracomún":False}
        self.salvaciones_comp = {"des":False,"cons":False,"sab":False,"int":False,"car":False,"fu":False}
        self.habilidades_comp = {"Acrobacias":False,"Atletismo":False,"Conocimiento Arcano":False,"Engaño":False,"Historia":False,"Interpretacion":False,"Intimidación":False,"Investigación":False,"Juego de Manos":False, "Medicina":False,"Naturaleza":False,"Percepción":False,"Perspicacia":False,"Persuasión":False,"Religión":False,"Sigilo":False,"Supervivencia":False,"Trato con Animales":False}
        self.equipo = None
        #iniciativa, percepción pasiva y dados de golpe, se extraen solo con un if de la clase
        if(isNPC):
            self.id_jugador = None
            self.num_npc_partida = id_jugador_or_NPC
        else:
            self.id_jugador = id_jugador_or_NPC
            self.num_npc_partida = None


        # Esto es a efectos de movimiento
        self.right = False
        self.up = False
        self.down = False
        self.left = False
        self.moving = False
        self.lastMoving = False
        self.needsToChange = False
        self.actualMovement = ["DOWN","UP","LEFT","RIGHT", "NOTHING"]
        self.move = self.actualMovement[4]
        self.lastMove = self.actualMovement[4]
        self.x = None
        self.y = None
        self.speed = None
        self.actions = {"IDLE": 1, "WALK":2}
        self.playerAction = 1 #Idle
        self.animations = {}
        self.aniTick = 0
        self.aniIndex = 0
        self.difX = None
        self.difY = None
        self.maxX = None
        self.maxY = None
        self.mapa = None
        self.tileSize = None

    def setUp(self,up):
        self.up = up

    def setRight(self,r):
        self.right = r

    def setDown(self,down):
        self.down = down

    def setLeft(self,left):
        self.left = left

    def initEquipo(self):
        self.equipo = Lista_Inventario.Equipo(self.fu) #creo el inventario vacío

    def setFPS(self,fps):
        if(fps == 60):
            self.speed = 2
        elif(fps == 120):
            self.speed = 1
        elif(fps == 90):
            self.speed = 1.5
        elif(fps == 144):
            self.speed = 0.93


    def setCurrentPos(self,pos,tileSize,width,height):
        self.coordenadas_actuales_r[0] = pos[0] #xTile
        self.coordenadas_actuales_r[1] = pos[1] #yTile
        self.tileSize = tileSize
        currentTilePlayer = self.coordenadas_actuales_r
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
        
        calc_x = currentTilePlayer[0] - i_start #número de casillas de diferencia
        calc_y = currentTilePlayer[1] - j_start 
        self.difX = self.tileSize[0]*i_start #Los píxeles que nos estamos comiendo de mapa, que no aparecen. Para el cálculo después de las tiles
        self.difY = self.tileSize[1]*j_start

        self.x = calc_x*tileSize[0]
        self.y = calc_y*tileSize[1]
        self.maxX = (width/150.0000)+(self.tileSize[0])*25
        self.maxY = (height/87.5000)+(self.tileSize[1])*12
        self.coordenadas_actuales = "("+str(self.coordenadas_actuales_r[0])+","+str(self.coordenadas_actuales_r[1])+")"


    def setPlayerAction(self,a):
        self.playerAction = a

    def getImage(self,ubicacion):
        images = {"bosque,elfo,0":("elfo_vive en el bosque_75_430_de piel verde",75,430,"mujer"),
                "bosque,Elfo,1":("elfo_vive en el bosque_78_420_de piel verde",78,420,"hombre"),
                "desierto,Elfo,0":("elfo_vive en el desierto_61_465_de piel clara",61,465,"hombre"),
                "desierto,Elfo,1": ("elfo_vive en el desierto_80_80_de piel verde",80,80,"mujer"),
                "barco,Elfo,0":("elfo_vive en un barco_69_354_de piel verde",69,354,"mujer"),
                "barco,Elfo,1":("elfo_vive en un barco_79_493_de piel verde",79,493,"hombre"),
                "aldea medieval,Elfo,0":("elfo_vive en una aldea medieval_68_196_de piel clara",68,196,"mujer"),
                "aldea medieval,Elfo,1":("elfo_vive en una aldea medieval_80_303_de piel clara",80,303,"hombre"),
                "mazmorra,Elfo,0":("elfo_vive en una ciudad antigua subterránea_64_739_de piel clara",64,739,"mujer"),
                "mazmorra,Elfo,1":("elfo_vive en una ciudad antigua subterránea_80_649_de piel verde",80,649,"hombre"),
                "ciudad moderna,Elfo,0":("elfo_vive en una ciudad moderna_61_257_de piel verde",61,257,"hombre"),
                "ciudad moderna,Elfo,1":("elfo_vive en una ciudad moderna_80_326_de piel clara",80,326,"mujer"),
                "bosque,Enano,0":("enano_vive en el bosque_45_127_omite referencias al color de piel",45,127,"mujer"),
                "bosque,Enano,1":("enano_vive en el bosque_47_255_omite referencias al color de piel",47,255,"hombre"),
                "desierto,Enano,0":("enano_vive en el desierto_45_329_omite referencias al color de piel",45,329,"mujer"),
                "desierto,Enano,1":("enano_vive en el desierto_59_188_omite referencias al color de piel",59,188,"hombre"),
                "barco,Enano,0":("enano_vive en un barco_46_321_omite referencias al color de piel",46,321,"hombre"),
                "barco,Enano,1":("enano_vive en un barco_57_237_omite referencias al color de piel",57,237,"mujer"),
                "aldea medieval,Enano,0":("enano_vive en una aldea medieval_51_71_omite referencias al color de piel",51,71,"mujer"),
                "aldea medieval,Enano,1":("enano_vive en una aldea medieval_60_278_omite referencias al color de piel",60,278,"hombre"),
                "mazmorra,Enano,0":("enano_vive en una ciudad antigua subterránea_52_349_omite referencias al color de piel",52,349,"mujer"),
                "mazmorra,Enano,1":("enano_vive en una ciudad antigua subterránea_58_212_omite referencias al color de piel",58,212,"hombre"),
                "ciudad moderna,Enano,0":("enano_vive en una ciudad moderna_45_103_omite referencias al color de piel",45,103,"hombre"),
                "ciudad moderna,Enano,1":("enano_vive en una ciudad moderna_62_81_omite referencias al color de piel",62,81,"mujer")}
        if(ubicacion == "mazmorra"):
            #Solo tenemos definida la mazmorra
            tipo = "mazmorra,"+self.tipo_raza
            for i in range(0,2):
                if(images[tipo+","+str(i)][3] == self.genero):
                    string = "animations\\NPCs\\"
                    return string+images[tipo+","+str(i)][0]+"\\walk.png"
        else:
            pass

    def loadAnimations(self,ubicacion):
        imagen = pygame.image.load(self.getImage(ubicacion))

        # Define el tamaño de cada frame
        ancho_frame = 64
        alto_frame = 64

        # Calcula el número de frames en cada fila y columna
        num_frames_x = int(imagen.get_width() // ancho_frame)
        num_frames_y = int(imagen.get_height() // alto_frame)

        # Lista para almacenar los frames

        # Recorre la imagen y extrae cada frame
        for y in range(num_frames_y):
            self.animations[y] = []
            for x in range(num_frames_x):
                # Extrae el frame actual
                frame = imagen.subsurface(pygame.Rect(x * ancho_frame, y * alto_frame, ancho_frame, alto_frame))
                # Añade el frame a la lista
                self.animations[y] += [frame]

    
    def isLegalAction(self,x,y):
        real_p_x = x+self.difX
        real_p_y = y+self.difY
        XinGrid = int(real_p_x//self.tileSize[0])
        YinGrid = int(real_p_y//self.tileSize[1])
        tile_id = self.mapa.matrix[YinGrid][XinGrid]
        print(tile_id)
        print("next casilla: "+str(XinGrid)+","+str(YinGrid))
        if(tile_id == 1 or tile_id == 22):
            # Es una casilla andable
            #TODO: es una puerta
            #El objeto/NPC/monstruo no impide su paso
            print(self.mapa.objetos[YinGrid][XinGrid])
            if(self.mapa.objetos[YinGrid][XinGrid] != 32 and (not(33 <= self.mapa.objetos[YinGrid][XinGrid] <=106) or self.mapa.objetos[YinGrid][XinGrid] == 80)and (not (111 <= self.mapa.objetos[YinGrid][XinGrid] <=117))):
                print("True")
                return True
        return False

    def updatePos(self):
        self.moving = False
        self.move = self.actualMovement[4] #NOTHING
        if(self.left and not self.right):
            print(self.x-self.speed)
            if(self.x-self.speed >=0 and self.isLegalAction(self.x-self.speed,self.y)):
                print(self.coordenadas_actuales)
                self.x -= self.speed
                self.move = self.actualMovement[2] #left
                self.moving = True
        elif(self.right and not self.left):
            print(self.x+self.speed)
            if((self.x + self.speed) <=(self.maxX) and self.isLegalAction(self.x+self.speed,self.y)):
                print(self.coordenadas_actuales)
                self.x+=self.speed
                self.move = self.actualMovement[3] #RIGHT
                self.moving = True
        if(self.up and not self.down):
            print(self.y-self.speed)
            if((self.y-self.speed >=0) and self.isLegalAction(self.x,self.y-self.speed)):
                print(self.coordenadas_actuales)
                self.y -= self.speed
                self.move = self.actualMovement[1] #UP
                self.moving = True
        elif(self.down and not self.up):
            print(self.y+self.speed)
            if((self.y+self.speed <=self.maxY) and self.isLegalAction(self.x,self.y+self.speed)):
                print(self.coordenadas_actuales)
                self.y +=self.speed
                self.move = self.actualMovement[0] #DOWN
                self.moving = True
        if(self.move != self.lastMove and (self.move != self.actualMovement[4])):
            self.lastMove = self.move
        if(self.lastMoving != self.moving):
            self.lastMoving = self.moving
            self.needsToChange = True
        if(self.needsToChange and self.moving):
            self.needsToChange = False
        self.updateTile()

    def updateTile(self):
        real_p_x = self.x+self.difX
        real_p_y = self.y+self.difY
        self.coordenadas_actuales_r[0] = int(real_p_x // self.tileSize[0])
        self.coordenadas_actuales_r[1] = int(real_p_y // self.tileSize[1])

        currentTilePlayer = self.coordenadas_actuales_r
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
        
        calc_x = currentTilePlayer[0] - i_start #número de casillas de diferencia
        calc_y = currentTilePlayer[1] - j_start 
        self.difX = self.tileSize[0]*i_start #Los píxeles que nos estamos comiendo de mapa, que no aparecen. Para el cálculo después de las tiles
        self.difY = self.tileSize[1]*j_start
        self.x = calc_x*self.tileSize[0]
        self.y = calc_y*self.tileSize[1]

        self.coordenadas_actuales = "("+str(self.coordenadas_actuales_r[0])+","+str(self.coordenadas_actuales_r[1])+")"
        self.mapa.fillCasillasVistas(self.coordenadas_actuales_r[0],self.coordenadas_actuales_r[1])

    def getSpriteAmount(self):
        if(self.playerAction == "WALK_DOWN" or self.playerAction == "WALK_UP" or self.playerAction == "WALK_LEFT" or self.playerAction == "WALK_RIGHT"):
            return 4
        else:
            return 1
        
    def updateAnimationTick(self,fps):
        self.aniTick+=1
        if(self.aniTick >= (fps*0.1)):
            self.aniTick=0
            self.aniIndex +=1
            if(self.aniIndex >= self.getSpriteAmount()):
                self.aniIndex=0

    def getCurrentFrame(self):
        if(self.playerAction == "WALK_DOWN" or self.playerAction == "IDLE_DOWN"):
            return 2
        elif(self.playerAction == "WALK_UP" or self.playerAction == "IDLE_UP"):
            return 0
        elif(self.playerAction == "WALK_LEFT" or self.playerAction == "IDLE_LEFT"):
            return 1
        else:
            return 2 #RIGHT
                
    def setAnimation(self):
        startAni = self.playerAction
        if(self.moving and self.move == self.actualMovement[0]):
            self.playerAction = "WALK_DOWN"
        elif(self.moving and self.move == self.actualMovement[1]):
            self.playerAction = "WALK_UP"
        elif(self.moving and self.move == self.actualMovement[2]):
            self.playerAction = "WALK_LEFT"
        elif(self.moving and self.move == self.actualMovement[3]):
            self.playerAction = "WALK_RIGHT"
        elif(self.move == self.actualMovement[4] and self.lastMove == self.actualMovement[1]):
            self.playerAction = "IDLE_UP"
        elif(self.move == self.actualMovement[4] and self.lastMove == self.actualMovement[2]):
            self.playerAction = "IDLE_LEFT"
        elif(self.move == self.actualMovement[4] and self.lastMove == self.actualMovement[3]):
            self.playerAction = "IDLE_RIGHT"
        else:
            self.playerAction = "IDLE_DOWN"
        
        if(startAni != self.playerAction):
            self.resetAniTick(); #to reset the index if the animation has not finished and we change to another
    
    def resetAniTick(self):
        self.aniTick=0
        self.aniIndex=0


    def render(self,fps,mapa,ubicacion,width,height,screen):
        #primero actualizo la situación del personaje y veo si puedo renderizar otra cosa
        self.updatePos()
        self.updateAnimationTick(fps)
        self.setAnimation()
        # cont = self.getCurrentYX()
        # cont_y = cont[0]
        # cont_x = cont[1]
        self.mapa = mapa
        self.mapa.drawMapInGame(ubicacion,width,height,screen,self.coordenadas_actuales_r)
        #print(self.getCurrentFrame(),self.aniIndex,self.tileSize[0],self.tileSize[1])
        screen.blit(pygame.transform.scale(self.animations[self.getCurrentFrame()][self.aniIndex], ((self.tileSize[0],self.tileSize[1]))), ((width/150.0000)+self.x, (height/87.5000)+self.y))
        return screen
    
    def renderLast(self,mapa,ubicacion,width,height,screen):
    
        self.mapa = mapa
        #print(self.getCurrentFrame(),self.aniIndex,self.tileSize[0],self.tileSize[1])
        screen.blit(pygame.transform.scale(self.animations[self.getCurrentFrame()][self.aniIndex], ((self.tileSize[0],self.tileSize[1]))), ((width/150.0000)+self.x, (height/87.5000)+self.y))
        return screen



