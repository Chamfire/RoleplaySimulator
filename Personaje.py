class Personaje:
    def __init__(self,isNPC,partida_id,id_jugador_or_NPC):
        self.name = ' ' #lo modifica el jugador
        self.sm1 = True
        self.sm2 = True
        self.sm3 = True
        self.nivel = 1
        self.inspiracion = 0
        self.esta_muerto = False
        self.bpc = None #cambiar al escoger personaje
        self.cons = None
        self.fu = None
        self.des = None
        self.sab = None
        self.car = None
        self.coordenadas_actuales = None #se calcula con el mapa
        self.vida_temp = None #cambiar al escoger la clase
        self.ca = None #cambiar al escoger personaje
        self.edad = None #lo escoge el jugador
        self.peso = None #lo escoge el jugador
        self.velocidad = None #cambiar al escoger la raza
        self.descripcion_fisica = None #la debe proporcionar el jugador
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
        if(isNPC):
            self.id_jugador = None
            self.num_npc_partida = id_jugador_or_NPC
        else:
            self.id_jugador = id_jugador_or_NPC
            self.num_npc_partida = None
        



