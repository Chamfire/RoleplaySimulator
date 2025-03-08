from enum import Enum
class tipo_uso(Enum):
    A_2_Manos = 1
    A_1_Mano = 2
    NO_REQUIERE_SUJECCION = 3

class tipo_damage(Enum):
    ACIDO = 1
    CONTUNDENTE = 2
    FRIO = 3
    FUEGO = 4
    FUERZA = 5
    RELAMPAGO = 6
    NECROTICO = 7
    PERFORANTE = 8
    VENENO = 9
    PSIQUICO = 10
    RADIANTE = 11
    CORTANTE = 12
    TRUENO = 13

class modificador(Enum):
    Sabiduria = 1
    Constitucion = 2
    Destreza = 3
    Fuerza = 4
    Carisma = 5
    Inteligencia = 6

# functional syntax
Color = Enum('Color', [('RED', 1), ('GREEN', 2), ('BLUE', 3)])

class arma:
    def __init__(self,dado,cantidad_dados,damage_adicional,pc,pp,pe,po,ppt,tipo_de_uso,rango,tipo_damage,arrojadizo,rango_arrojadizo,modificador,ligera,recarga,pesada,versatil, dado_versatil = None,cantidad_dados_versatil = None):
        self.coste = {"pc":pc,"pp":pp,"pe":pe,"po":po,"ppt":ppt}
        self.dado = dado #4,6,8,10,12,20,100
        self.cantidad_dados = cantidad_dados
        self.damage_adicional = damage_adicional
        self.tipo_de_uso = tipo_de_uso
        self.tipo_damage = tipo_damage
        self.image = None #por ahora se quedará en None
        self.arrojadizo = arrojadizo #todas las que sean arrojadizas, usarán destreza al lanzar
        self.rango_arrojazido = rango_arrojadizo #por defecto es None, si pasas None
        self.modificador = modificador #modificador cuando no se usan como arrojadizas
        self.versatil = versatil
        if(self.versatil): #también puede usarse a 2 manos
            self.dado_versatil = dado_versatil
            self.cantidad_dados_versatil = cantidad_dados_versatil
        self.rango = rango
        self.ligera = ligera #si es True, al tener dos armas de este tipo, se podrá usar una en cada mano. Si no, no.
        self.recarga = recarga #si es True, solo podrá usarla 1 vez por turno, independientemente del número de ataques que pueda usar
        self.pesada = pesada
class Objeto_Inventario:
    def __init__(self):
        #Tabla de equivalencias:
        #1self.pc = moneda de menor valor
        #self.pp = 10 self.pp
        #self.pe = 10 self.pp
        #self.po = 10 self.pe
        #1 self.ppt = 10 self.po
        #Coste: (pc,pp,pe,po,ppt)
        #Inicialización de armas, objetos, y equipos de dnd
        self.armas = {"Armas c/c simples": {}, "Armas a distancia simples":{},"Armas c/c marciales":{},"Armas a distancia marciales":{}}
        
        #-------- Armas c/c simples ---------
        self.armas["Armas c/c simples"]["Bastón"] = arma(6,1,0,0,2,0,0,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CONTUNDENTE,False,None,modificador.Fuerza,False,False,False,True,8,1)
        self.armas["Armas c/c simples"]["Daga"] = arma(4,1,0,0,0,0,2,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.PERFORANTE,True,20,modificador.Destreza,True,False) #Arrojadiza, rango de 20 pies (no se aplica lo de desventaja para mayor rango. Se implementará en un futuro)
        #Todos tendrán golpe desarmado por defecto, además de las armas que se indiquen en la ficha de personaje
        self.armas["Armas c/c simples"]["Golpe desarmado"] = arma(0,0,1,0,0,0,0,0,tipo_uso.A_2_Manos,(5,5),tipo_damage.CONTUNDENTE,False,None,modificador.Fuerza,False,False,False,False)
        self.armas["Armas c/c simples"]["Gran clava"] = arma(8,1,0,0,2,0,0,0,tipo_uso.A_2_Manos,(5,5),tipo_damage.CONTUNDENTE,False,None,modificador.Fuerza,False,False,False,False)
        self.armas["Armas c/c simples"]["Hacha de mano"] = arma(6,1,0,0,0,0,5,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CORTANTE,True,20,modificador.Fuerza,True,False,False,False)
        self.armas["Armas c/c simples"]["Hoz"] = arma(4,1,0,0,0,0,1,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CORTANTE,False,None,modificador.Destreza,True,False,False,False)
        self.armas["Armas c/c simples"]["Jabalina"] = arma(6,1,0,0,5,0,0,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.PERFORANTE,True,30,modificador.Destreza,False,False,False,False)
        self.armas["Armas c/c simples"]["Lanza"] = arma(6,1,0,0,0,0,1,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.PERFORANTE,True,20,modificador.Destreza,False,False,False,True,8,1)
        self.armas["Armas c/c simples"]["Martillo ligero"] = arma(4,1,0,0,0,0,2,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CONTUNDENTE,True,20,modificador.Fuerza,True,False,False,False)
        self.armas["Armas c/c simples"]["Maza"] = arma(6,1,0,0,0,0,5,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CONTUNDENTE,False,None,modificador.Fuerza,False,False,False,False)
        self.armas["Armas c/c simples"]["Clava"] = arma(4,1,0,0,1,0,0,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CONTUNDENTE,False,None,modificador.Fuerza,True,False,False,False)
        #---------Armas a distancia simples -----------
        self.armas["Armas a distancia simples"]["Arco corto"] = arma(6,1,0,0,0,0,25,0,tipo_uso.A_2_Manos,(10,80),tipo_damage.PERFORANTE,False,None,modificador.Destreza,False,False,False,False)
        self.armas["Armas a distancia simples"]["Ballesta ligera"] = arma(8,1,0,0,0,0,25,0,tipo_uso.A_2_Manos,(10,80),tipo_damage.PERFORANTE,False,None,modificador.Destreza,False,True,False,False)
        self.armas["Armas a distancia simples"]["Dardo"] = arma(4,1,0,5,0,0,0,0,tipo_uso.A_1_Mano,(0,0),tipo_damage.PERFORANTE,True,(10,20),modificador.Fuerza,False,False,False,False) #este objeto no se puede usar, salvo que se arroje (es como una flecha)
        self.armas["Armas a distancia simples"]["Honda"] = arma(4,1,0,0,1,0,0,0,tipo_uso.A_1_Mano,(10,30),tipo_damage.CONTUNDENTE, False,None,modificador.Fuerza,False,False,False,False)
        #--------- Armas c/c marciales ----------------
        self.armas["Armas c/c marciales"]["Alabarda"] = arma(10,1,0,0,0,0,20,0,tipo_uso.A_2_Manos,(10,10),tipo_damage.CORTANTE,False,None,modificador.Fuerza,False,False,True,False)
        self.armas["Armas c/c marciales"]["Atarraga"] = arma(6,2,0,0,0,0,10,0,tipo_uso.A_2_Manos,(5,5),tipo_damage.CONTUNDENTE,False,None,modificador.Fuerza,False,False,True,False)
        self.armas["Armas c/c marciales"]["Cimitarra"] = arma(6,1,0,0,0,0,25,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CORTANTE,False,None,modificador.Destreza,True,False,False,False)
        self.armas["Armas c/c marciales"]["Espada corta"] = arma(6,1,0,0,0,0,10,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CORTANTE,False,None,modificador.Fuerza,True,False,False,False)
        self.armas["Armas c/c marciales"]["Espada larga"] = arma(8,1,0,0,0,0,15,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CORTANTE,False,None,modificador.Fuerza,False,False,False,True,10,1)
        self.armas["Armas c/c marciales"]["Espadón"] = arma(6,2,0,0,0,0,50,0,tipo_uso.A_2_Manos,(5,5),tipo_damage.CORTANTE,False,None,modificador.Fuerza,False,False,True,False)
        self.armas["Armas c/c marciales"]["Estoque"] = arma(8,1,0,0,0,0,25,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.PERFORANTE,False,None,modificador.Destreza,False,False,False,False)
        self.armas["Armas c/c marciales"]["Hacha de batalla"] = arma(8,1,0,0,0,0,10,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CORTANTE,False,None,modificador.Fuerza,False,False,False,True,10,1)
        self.armas["Armas c/c marciales"]["Gran hacha"] = arma(12,1,0,0,0,0,30,0,tipo_uso.A_2_Manos,(5,5),tipo_damage.CORTANTE,False,None,modificador.Fuerza,False,False,True,False)
        self.armas["Armas c/c marciales"]["Guja"] = arma(10,1,0,0,0,0,20,0,tipo_uso.A_2_Manos,(10,10),tipo_damage.CORTANTE,False,None,modificador.Fuerza,False,False,True,False)
        #No se va a modelar la desventaja y la necesidad de estar a caballo con lanza de caballería
        self.armas["Armas c/c marciales"]["Lanza de caballería"] = arma(12,1,0,0,0,0,10,0,tipo_uso.A_2_Manos,(10,10),tipo_damage.PERFORANTE,False,None,modificador.Fuerza,False,False,False,False)
        self.armas["Armas c/c marciales"]["Látigo"] = arma(4,1,0,0,0,0,2,0,tipo_uso.A_1_Mano,(10,10),tipo_damage.CORTANTE,False,None,modificador.Fuerza,False,False,False,False)
        self.armas["Armas c/c marciales"]["Lucero del alba"] = arma(8,1,0,0,0,0,15,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.PERFORANTE,False,None,modificador.Fuerza,False,False,False,False)
        self.armas["Armas c/c marciales"]["Martillo de guerra"] = arma(8,1,0,0,0,0,15,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CONTUNDENTE,False,None,modificador.Fuerza,False,False,False,True,10,1)
        self.armas["Armas c/c marciales"]["Mayal"] = arma(8,1,0,0,0,0,10,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CONTUNDENTE,False,None,modificador.Fuerza,False,False,False,False)
        self.armas["Armas c/c marciales"]["Pica"] = arma(10,1,0,0,0,0,5,0,tipo_uso.A_2_Manos,(10,10),tipo_damage.PERFORANTE,False,None,modificador.Fuerza,False,False,True,False)
        self.armas["Armas c/c marciales"]["Pica de guerra"] = arma(8,1,0,0,0,0,5,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.PERFORANTE,False,None,modificador.Fuerza,False,False,False,False)
        self.armas["Armas c/c marciales"]["Tridente"] = arma(6,1,0,0,0,0,5,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.PERFORANTE,True,(10,20),modificador.Destreza,False,False,False,True,6,1)
        self.armas["Armas a distancia marciales"]["Arco largo"] = arma(8,1,0,0,0,0,50,0,tipo_uso.A_2_Manos,(10,150),tipo_damage.PERFORANTE,False,None,modificador.Destreza,False,False,True,False)
        self.armas["Armas a distancia marciales"]["Ballesta de mano"] = arma(6,1,0,0,0,0,75,0,tipo_uso.A_1_Mano,(10,30),tipo_damage.PERFORANTE,False,None,modificador.Destreza,True,True,False,False)
        self.armas["Armas a distancia marciales"]["Ballesta pesada"] = arma(10,1,0,0,0,0,50,0,tipo_uso.A_2_Manos,(10,100),tipo_damage.PERFORANTE,False,None,modificador.Fuerza,False,True,True,False)
        self.armas["Armas a distancia marciales"]["Cerbatana"] = arma(0,0,1,0,0,0,10,0,tipo_uso.A_1_Mano,(10,25),tipo_damage.PERFORANTE,False,None,modificador.Fuerza,False,True,False,False)
        #La red, como solo es de tipo especial, y no hace daño, no la voy a modelar por ahora