import Lista_Inventario
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
    def initEquipo(self):
        self.equipo = Lista_Inventario.Equipo(self.fu) #creo el inventario vacío
        



