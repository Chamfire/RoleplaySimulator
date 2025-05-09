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
        self.playerSpeed = 2.0
        self.moving = False
        self.actions = {"IDLE": 1, "WALK":2}
        self.playerAction = 1 #Idle
        self.animations = {}
        self.aniTick = 0
        self.aniIndex = 0


    # def getLookingPos(self):
    #     if(self.lookingDir == "DOWN"):
    #         return 2
    #     elif(self.lookingDir == "UP"):
    #         return 0
    #     elif(self.lookingDir == "LEFT"):
    #         return 1
    #     elif(self.lookingDir == "RIGHT"):
    #         return 3

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

    def loadAnimations(self):
        imagen = pygame.image.load(self.NPC_imagen)

        # Define el tamaño de cada frame
        ancho_frame = 64
        alto_frame = 64

        # Calcula el número de frames en cada fila y columna
        num_frames_x = imagen.get_width() // ancho_frame
        num_frames_y = imagen.get_height() // alto_frame

        # Lista para almacenar los frames

        # Recorre la imagen y extrae cada frame
        for y in range(num_frames_y):
            self.animations[y] = []
            for x in range(num_frames_x):
                # Extrae el frame actual
                frame = imagen.subsurface(pygame.Rect(x * ancho_frame, y * alto_frame, ancho_frame, alto_frame))
                # Añade el frame a la lista
                self.animations[y] += [frame]
    
    def updatePos(self):
        self.moving = False
        if(self.left and not self.right):
            x-= self.playerSpeed
            self.moving = True
        elif(self.right and not self.left):
            x+=self.playerSpeed
            self.moving = True
        if(self.up and not self.down):
            y-= self.playerSpeed
            self.moving = True
        elif(self.down and not self.up):
            y+=self.playerSpeed
            self.moving = True

    def getSpriteAmount(self):
        if(self.playerAction == 1):
            return 1
        elif(self.playerAction == 2):
            return 4
        
    def updateAnimationTick(self,fps):
        self.aniTick+=1
        if(self.aniTick >= (fps*0.2)):
            self.aniTick=0
            self.aniIndex +=1
            if(self.aniIndex >= self.getSpriteAmount()):
                self.aniIndex=0
                
    def setAnimation(self):
        startAni = self.playerAction

        if(self.moving):
            self.playerAction= 2
        else:
            self.playerAction = 1
        
        if(startAni != self.playerAction):
            self.resetAniTick(); #to reset the index if the animation has not finished and we change to another
    
    def resetAniTick(self):
        self.aniTick=0
        self.aniIndex=0


    def render(self,tile_w,tile_h,screen,width,heigth,fps):
        #primero actualizo la situación del personaje y veo si puedo renderizar otra cosa
        self.updatePos()
        self.updateAnimationTick(fps)
        self.setAnimation()
        screen.blit(pygame.transform.scale(, (tile_w,tile_h)), ((width/150.0000)+(self.map_tileSize[0])*cont_y, (height/87.5000)+(self.map_tileSize[1])*cont_x))
    
        



