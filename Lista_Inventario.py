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

class Arma:
    def __init__(self,dado,cantidad_dados,damage_adicional,pc,pp,pe,po,ppt,tipo_de_uso,rango,tipo_damage,arrojadizo,rango_arrojadizo,modificador,ligera,recarga,pesada,versatil, peso,dado_versatil = None,cantidad_dados_versatil = None):
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
        self.peso = peso

class Objeto_de_Espacio:
    def __init__(self,num_objetos_max,tipo):
        self.num_objetos_max = num_objetos_max
        tipo = tipo
        self.peso_actual = 0
        self.objetos = {}
        for i in range(0,self.num_objetos_max):
            self.objetos[str("slot_"+str(i))] = None

    def addObject(objeto):
        pass 
    def removeObject(self): #devolverá el objeto que se ha sacado de la mochila, y se pasará al inventario
        pass
    


class Objeto:
    def __init__(self):
        pass

class Armadura:
    def __init__(self,pc,pp,pe,po,ppt,nueva_ca,modificador,maximo_mod,requisito_fu,desventaja_sigilo,peso):
        self.pc = pc
        self.pp = pp
        self.pe = pe
        self.po = po
        self.ppt = ppt
        self.nueva_ca = nueva_ca
        self.modificador = modificador
        self.maximo_mod = maximo_mod
        self.requisito_fu = requisito_fu
        self.desventaja_sigilo = desventaja_sigilo
        self.peso = peso

class Escudo:
    def __init__(self,pc,pp,pe,po,ppt,addToCA,peso):
        self.pc = pc
        self.pp = pp
        self.pe = pe
        self.po = po
        self.ppt = ppt
        self.addToCA = addToCA
        self.peso = peso

class Equipo:
    def __init__(self,fu):
        self.num_objetos_max = 9 #como objetos cuenta la mochila, y en la mochila puedes meter más objetos
        self.num_objetos_actual = 0
        self.peso_max = fu*15 #fu x 15
        self.peso_actual = 0
        self.objetos = {}
        for i in range(0,self.num_objetos_max):
            self.objetos[str("slot_"+str(i))] = None
        self.armadura_actual = None
        self.objeto_equipado_mano_derecha = None
        self.objeto_equipado_mano_izquierda = None #aquí iría un escudo en caso de tenerlo

    def passArmorFromInventoryToArmorEquipment(self):
        pass
    def passArmorEquipmentToInventory(self):
        pass
    def passObjectFromInventoryToLeftHand(self):
        pass
    def passObjectFromInventoryToRightHand(self):
        pass
    def passObjectFromLeftHandToInventory(self):
        pass
    def passObjectFromRightHandToInventory(self):
        pass
        
    def find_free_slot(self):
        for (elem,i) in self.objetos.keys():
            if(elem == None):
                return i

    def addObjectToInventory(self,objeto,categoria,nombre):
        if(self.peso_actual + objeto.peso > self.peso_max):
            return -1 #no puede llevar tanto peso
        elif(self.num_objetos_actual + 1 > self.num_objetos_max):
            return -2
        else:
            self.peso_actual += objeto.peso
            self.num_objetos_actual +=1
            slot_libre = self.find_free_slot()
            self.objetos[str("slot_"+str(slot_libre))] = (categoria,nombre,objeto) #Añado el objeto al inventario: self.objetos[slot_1] = (categoria,nombre,objeto)
            return 1
        
    def removeObjectFromInventory(self,slot):
        if(self.objetos[slot] != None):
            peso_a_quitar = self.objetos[slot][2].peso
            self.peso_actual -= peso_a_quitar
            self.num_objetos_actual -=1
            self.objetos[str("slot_"+str(slot))] = None
            return 1
        else:
            return -1

class Lista_Inventario:
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
        self.armas["Armas c/c simples"]["Bastón"] = Arma(6,1,0,0,2,0,0,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CONTUNDENTE,False,None,modificador.Fuerza,False,False,False,True,4,8,1)
        self.armas["Armas c/c simples"]["Daga"] = Arma(4,1,0,0,0,0,2,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.PERFORANTE,True,20,modificador.Destreza,True,False,1) #Arrojadiza, rango de 20 pies (no se aplica lo de desventaja para mayor rango. Se implementará en un futuro)
        #Todos tendrán golpe desarmado por defecto, además de las armas que se indiquen en la ficha de personaje
        self.armas["Armas c/c simples"]["Golpe desarmado"] = Arma(0,0,1,0,0,0,0,0,tipo_uso.A_2_Manos,(5,5),tipo_damage.CONTUNDENTE,False,None,modificador.Fuerza,False,False,False,False,0)
        self.armas["Armas c/c simples"]["Gran clava"] = Arma(8,1,0,0,2,0,0,0,tipo_uso.A_2_Manos,(5,5),tipo_damage.CONTUNDENTE,False,None,modificador.Fuerza,False,False,False,False,10)
        self.armas["Armas c/c simples"]["Hacha de mano"] = Arma(6,1,0,0,0,0,5,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CORTANTE,True,20,modificador.Fuerza,True,False,False,False,2)
        self.armas["Armas c/c simples"]["Hoz"] = Arma(4,1,0,0,0,0,1,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CORTANTE,False,None,modificador.Destreza,True,False,False,False,2)
        self.armas["Armas c/c simples"]["Jabalina"] = Arma(6,1,0,0,5,0,0,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.PERFORANTE,True,30,modificador.Destreza,False,False,False,False,2)
        self.armas["Armas c/c simples"]["Lanza"] = Arma(6,1,0,0,0,0,1,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.PERFORANTE,True,20,modificador.Destreza,False,False,False,True,3,8,1)
        self.armas["Armas c/c simples"]["Martillo ligero"] = Arma(4,1,0,0,0,0,2,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CONTUNDENTE,True,20,modificador.Fuerza,True,False,False,False,2)
        self.armas["Armas c/c simples"]["Maza"] = Arma(6,1,0,0,0,0,5,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CONTUNDENTE,False,None,modificador.Fuerza,False,False,False,False,4)
        self.armas["Armas c/c simples"]["Clava"] = Arma(4,1,0,0,1,0,0,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CONTUNDENTE,False,None,modificador.Fuerza,True,False,False,False,2)
        #---------Armas a distancia simples -----------
        self.armas["Armas a distancia simples"]["Arco corto"] = Arma(6,1,0,0,0,0,25,0,tipo_uso.A_2_Manos,(10,80),tipo_damage.PERFORANTE,False,None,modificador.Destreza,False,False,False,False,2)
        self.armas["Armas a distancia simples"]["Ballesta ligera"] = Arma(8,1,0,0,0,0,25,0,tipo_uso.A_2_Manos,(10,80),tipo_damage.PERFORANTE,False,None,modificador.Destreza,False,True,False,False,5)
        self.armas["Armas a distancia simples"]["Dardo"] = Arma(4,1,0,5,0,0,0,0,tipo_uso.A_1_Mano,(0,0),tipo_damage.PERFORANTE,True,(10,20),modificador.Fuerza,False,False,False,False,0.25) #este objeto no se puede usar, salvo que se arroje (es como una flecha)
        self.armas["Armas a distancia simples"]["Honda"] = Arma(4,1,0,0,1,0,0,0,tipo_uso.A_1_Mano,(10,30),tipo_damage.CONTUNDENTE, False,None,modificador.Fuerza,False,False,False,False,0.25)
        #--------- Armas c/c marciales ----------------
        self.armas["Armas c/c marciales"]["Alabarda"] = Arma(10,1,0,0,0,0,20,0,tipo_uso.A_2_Manos,(10,10),tipo_damage.CORTANTE,False,None,modificador.Fuerza,False,False,True,False,6)
        self.armas["Armas c/c marciales"]["Atarraga"] = Arma(6,2,0,0,0,0,10,0,tipo_uso.A_2_Manos,(5,5),tipo_damage.CONTUNDENTE,False,None,modificador.Fuerza,False,False,True,False,10)
        self.armas["Armas c/c marciales"]["Cimitarra"] = Arma(6,1,0,0,0,0,25,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CORTANTE,False,None,modificador.Destreza,True,False,False,False,3)
        self.armas["Armas c/c marciales"]["Espada corta"] = Arma(6,1,0,0,0,0,10,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CORTANTE,False,None,modificador.Fuerza,True,False,False,False,2)
        self.armas["Armas c/c marciales"]["Espada larga"] = Arma(8,1,0,0,0,0,15,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CORTANTE,False,None,modificador.Fuerza,False,False,False,True,3,10,1)
        self.armas["Armas c/c marciales"]["Espadón"] = Arma(6,2,0,0,0,0,50,0,tipo_uso.A_2_Manos,(5,5),tipo_damage.CORTANTE,False,None,modificador.Fuerza,False,False,True,False,6)
        self.armas["Armas c/c marciales"]["Estoque"] = Arma(8,1,0,0,0,0,25,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.PERFORANTE,False,None,modificador.Destreza,False,False,False,False,2)
        self.armas["Armas c/c marciales"]["Hacha de batalla"] = Arma(8,1,0,0,0,0,10,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CORTANTE,False,None,modificador.Fuerza,False,False,False,True,4,10,1)
        self.armas["Armas c/c marciales"]["Gran hacha"] = Arma(12,1,0,0,0,0,30,0,tipo_uso.A_2_Manos,(5,5),tipo_damage.CORTANTE,False,None,modificador.Fuerza,False,False,True,False,7)
        self.armas["Armas c/c marciales"]["Guja"] = Arma(10,1,0,0,0,0,20,0,tipo_uso.A_2_Manos,(10,10),tipo_damage.CORTANTE,False,None,modificador.Fuerza,False,False,True,False,6)
        #No se va a modelar la desventaja y la necesidad de estar a caballo con lanza de caballería
        self.armas["Armas c/c marciales"]["Lanza de caballería"] = Arma(12,1,0,0,0,0,10,0,tipo_uso.A_2_Manos,(10,10),tipo_damage.PERFORANTE,False,None,modificador.Fuerza,False,False,False,False,6)
        self.armas["Armas c/c marciales"]["Látigo"] = Arma(4,1,0,0,0,0,2,0,tipo_uso.A_1_Mano,(10,10),tipo_damage.CORTANTE,False,None,modificador.Fuerza,False,False,False,False,3)
        self.armas["Armas c/c marciales"]["Lucero del alba"] = Arma(8,1,0,0,0,0,15,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.PERFORANTE,False,None,modificador.Fuerza,False,False,False,False,4)
        self.armas["Armas c/c marciales"]["Martillo de guerra"] = Arma(8,1,0,0,0,0,15,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CONTUNDENTE,False,None,modificador.Fuerza,False,False,False,True,2,10,1)
        self.armas["Armas c/c marciales"]["Mayal"] = Arma(8,1,0,0,0,0,10,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.CONTUNDENTE,False,None,modificador.Fuerza,False,False,False,False,2)
        self.armas["Armas c/c marciales"]["Pica"] = Arma(10,1,0,0,0,0,5,0,tipo_uso.A_2_Manos,(10,10),tipo_damage.PERFORANTE,False,None,modificador.Fuerza,False,False,True,False,18)
        self.armas["Armas c/c marciales"]["Pica de guerra"] = Arma(8,1,0,0,0,0,5,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.PERFORANTE,False,None,modificador.Fuerza,False,False,False,False,2)
        self.armas["Armas c/c marciales"]["Tridente"] = Arma(6,1,0,0,0,0,5,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.PERFORANTE,True,(10,20),modificador.Destreza,False,False,False,True,4,6,1)
        self.armas["Armas a distancia marciales"]["Arco largo"] = Arma(8,1,0,0,0,0,50,0,tipo_uso.A_2_Manos,(10,150),tipo_damage.PERFORANTE,False,None,modificador.Destreza,False,False,True,False,2)
        self.armas["Armas a distancia marciales"]["Ballesta de mano"] = Arma(6,1,0,0,0,0,75,0,tipo_uso.A_1_Mano,(10,30),tipo_damage.PERFORANTE,False,None,modificador.Destreza,True,True,False,False,3)
        self.armas["Armas a distancia marciales"]["Ballesta pesada"] = Arma(10,1,0,0,0,0,50,0,tipo_uso.A_2_Manos,(10,100),tipo_damage.PERFORANTE,False,None,modificador.Fuerza,False,True,True,False,18)
        self.armas["Armas a distancia marciales"]["erbatana"] = Arma(0,0,1,0,0,0,10,0,tipo_uso.A_1_Mano,(10,25),tipo_damage.PERFORANTE,False,None,modificador.Fuerza,False,True,False,False,1)
        #La red, como solo es de tipo especial, y no hace daño, no la voy a modelar por ahora

        self.objeto = {"Comida": {}, "Bebida": {}, "Mecanico": {}, "Refugio": {},"Libro": {}, "Kit": {}, "Iluminación": {}, "Otros": {}, "Almacenaje": {}}
        
        self.objeto["Refugio"]["Saco de dormir"] = Objeto()
        self.objeto["Mecanico"]["Palanca"] = Objeto()
        self.objeto["Otros"]["Piton"] = Objeto() #palos de escalada
        self.objeto["Iluminación"]["Antorcha"] = Objeto()
        self.objeto["Otros"]["Yesquero"] = Objeto()
        self.objeto["Comida"]["Ración"] = Objeto()
        self.objeto["Bebida"]["Odre de agua"] = Objeto() #definir en el futuro: 4.84,"liquido"
        self.objeto["Otros"]["Cuerda de cáñamo"] = Objeto()

        self.objeto["Almacenaje"]["Mochila"] = Objeto_de_Espacio(30,"sólido")
        self.objeto["Kit"]["De cocina"] = Objeto() #permitirá en sus funciones cocinar, pero se registrará como un único objeto por ahora
        
        #Armaduras
        self.armadura = {"Armaduras ligeras": {},"Armaduras medias": {},"Armaduras pesadas": {}}
        self.armadura["Armaduras ligeras"]["Acolchada"] = Armadura(0,0,0,5,0,11,modificador.Destreza,None,0,True,8)
        self.armadura["Armaduras ligeras"]["Cuero"] = Armadura(0,0,0,10,0,11,modificador.Destreza,None,0,False,10)
        self.armadura["Armaduras ligeras"]["Cuero tachonado"] = Armadura(0,0,0,45,0,12,modificador.Destreza,None,0,False,13)
        self.armadura["Armaduras medias"]["Pieles"] = Armadura(0,0,0,10,0,12,modificador.Destreza,2,0,False,12)
        self.armadura["Armaduras medias"]["Camisote de mallas"] = Armadura(0,0,0,50,0,13,modificador.Destreza,2,0,False,12)
        self.armadura["Armaduras medias"]["Cota de escamas"] = Armadura(0,0,0,50,0,14,modificador.Destreza,2,0,False,20)
        self.armadura["Armaduras medias"]["Coraza"] = Armadura(0,0,0,400,0,14,modificador.Destreza,2,0,True,45)
        self.armadura["Armaduras medias"]["Semiplacas"] = Armadura(0,0,0,750,0,14,modificador.Destreza,2,False,True,40)
        self.armadura["Armaduras pesadas"]["Cota de anillas"] = Armadura(0,0,0,30,0,14,None,None,0,True,40)
        self.armadura["Armaduras pesadas"]["Cota de mallas"] = Armadura(0,0,0,75,0,16,None,None,13,True,55)
        self.armadura["Armaduras pesadas"]["Bandas"] = Armadura(0,0,0,200,0,16,None,None,15,True,60)
        self.armadura["Armaduras pesadas"]["Placas"] = Armadura(0,0,0,1500,0,18,None,None,15,True,65)
        self.escudo = {"Escudo":{}}
        self.escudo["Escudo"]["Escudo básico"] = Escudo(0,0,0,10,0,2,6)