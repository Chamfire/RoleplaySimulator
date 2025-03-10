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
        self.stackeable = False

class Objeto_de_Espacio:
    def __init__(self,num_objetos_max,tipo,peso_base):
        self.num_objetos_max = num_objetos_max
        self.actual_num_objetos = 0
        tipo = tipo
        self.peso = peso_base
        self.stackeable = False
        self.objetos = {}
        for i in range(0,self.num_objetos_max):
            self.objetos[str("slot_"+str(i))] = None

    def find_free_slot(self):
        for i,elem in self.objetos.items():
            if(elem == None):
                return i
        else:
            return -1
        
    def addObject(self,categoria,nombre,objeto,max_capacidad):
        if(self.peso + objeto.peso > max_capacidad):
            return -2 #pesa demasiado
        if(objeto.stackeable):
            slot_objeto = self.findSameObject(nombre)
            if(slot_objeto == - 1):
                pass #que siga
            else:
                q = self.objetos[slot_objeto][3]
                self.peso += objeto.peso
                self.objetos[slot_objeto][3] = q+1
                #no añadimos nada a número actual de objetos, porque no estamos ocupando un slot nuevo
                return 1
        if(self.actual_num_objetos +1 > self.num_objetos_max):
            return -1 #no hay slots libres
        else:
            slot_libre = self.find_free_slot()
            self.objetos[slot_libre] = [categoria,nombre,objeto,1]
            self.peso += objeto.peso
            self.actual_num_objetos +=1
            return 1
            
    def removeObject(self,slot): #devolverá el objeto que se ha sacado de la mochila, y se pasará al inventario
        if(self.objetos[str("slot_"+str(slot))] != None):
            peso_a_quitar = (self.objetos[str("slot_"+str(slot))][2].peso / self.objetos[str("slot_"+str(slot))][3])
            self.objetos[str("slot_"+str(slot))][3] -=1
            if(self.objetos[slot][3] == 0):
                self.objetos[str("slot_"+str(slot))][3] = None
                self.num_objetos_actual -=1 
            self.peso -= peso_a_quitar
            self.objetos[str("slot_"+str(slot))] = None
            return 1 #proceso correcto
        else:
            return -1 #no había nada en ese slot
    


class Objeto:
    def __init__(self,pc,pp,pe,po,ppt,peso,stackeable):
        self.pc = pc
        self.pp = pp
        self.pe = pe
        self.po = po
        self.ppt = ppt
        self.peso = peso
        self.stackeable = stackeable

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
        self.stackeable = False

class Escudo:
    def __init__(self,pc,pp,pe,po,ppt,addToCA,peso):
        self.pc = pc
        self.pp = pp
        self.pe = pe
        self.po = po
        self.ppt = ppt
        self.addToCA = addToCA
        self.peso = peso
        self.stackeable = False

class Equipo:
    def __init__(self,fu):
        self.num_objetos_max = 20 #como objetos cuenta la mochila, y en la mochila puedes meter más objetos
        self.num_objetos_actual = 0
        self.peso_max = fu*15 #fu x 15
        self.peso_actual = 0
        self.objetos = {}
        for i in range(0,self.num_objetos_max):
            self.objetos[str("slot_"+str(i))] = None
        self.armadura_actual = None
        self.objeto_equipado_mano_derecha = None
        self.objeto_equipado_mano_izquierda = None #aquí iría un escudo en caso de tenerlo
        self.listaInventario = Lista_Inventario()

    def findSameObject(self,nombre): #[categoria,nombre,objeto,1]
        for i,slot in self.objetos.items():
            if(slot != None and slot[1] == nombre):
                return i #devuelve el slot donde ha encontrado que está el objeto
        return -1


    def printEquipoConsolaDebugSuperficial(self):
        print("# --------------- Equipo ------------------")
        for i in range(0,self.num_objetos_max):
            if(self.objetos[str("slot_"+str(i))] != None):
                print("slot_"+str(i)+": "+self.objetos[str("slot_"+str(i))][0]+"; "+self.objetos[str("slot_"+str(i))][1]+"; "+str(self.objetos[str("slot_"+str(i))][3]))

    def passArmorFromInventoryToArmorEquipment(self,categoria,nombre,armor):
        if(self.armadura_actual != None):
            self.armadura_actual = (categoria,nombre,armor)
            slot_libre = self.find_free_slot()
            if(slot_libre == -1):
                return -1
            else:
                #hay un slot libre
                self.objetos[str("slot_"+str(slot_libre))] = [self.armadura_actual[0],self.armadura_actual[1],self.armadura_actual[2],self.armadura_actual[3]]
        self.num_objetos_actual -=1
        #el peso se mantiene, pues lo sigue llevando
        self.armadura_actual = (categoria,nombre,armor)
        return 1
    

    def passArmorEquipmentToInventory(self):
        if(self.armadura_actual != None):
            slot_libre = self.find_free_slot()
            if(slot_libre == -1):
                return -1 #no hay slots libres
            else:
                #hay un slot libre
                self.objetos[slot_libre] = [self.armadura_actual[0],self.armadura_actual[1],self.armadura_actual[2],self.armadura_actual[3]]
                self.num_objetos_actual +=1
                return 1
        else:
            return -2 #no se ha podido pasar, porque la armadura estaba vacía
    
    def passObjectFromInventoryToLeftHand(self,categoria,nombre,object):
        if(self.objeto_equipado_mano_izquierda != None):
            slot_libre = self.find_free_slot()
            if(slot_libre == -1):
                return -1 #no hay slots libres
            else:
                #hay un slot libre
                self.objetos[slot_libre] = [self.objeto_equipado_mano_izquierda[0],self.objeto_equipado_mano_izquierda[1],self.objeto_equipado_mano_izquierda[2],self.objeto_equipado_mano_izquierda[3]]
        self.num_objetos_actual -=1
        self.objeto_equipado_mano_izquierda = (categoria,nombre,object)
        return 1

    def passObjectFromInventoryToRightHand(self,categoria,nombre,object):
        if(self.objeto_equipado_mano_derecha != None):
            slot_libre = self.find_free_slot()
            if(slot_libre == -1):
                return -1 #no hay slots libres
            else:
                #hay un slot libre
                self.objetos[slot_libre] = [self.objeto_equipado_mano_derecha[0],self.objeto_equipado_mano_derecha[1],self.objeto_equipado_mano_derecha[2],self.objeto_equipado_mano_derecha[3]]
        self.num_objetos_actual -=1
        self.objeto_equipado_mano_izquierda = (categoria,nombre,object)
        return 1
    
    def passObjectFromLeftHandToInventory(self):
        if(self.objeto_equipado_mano_izquierda != None):
            slot_libre = self.find_free_slot()
            if(slot_libre == -1):
                return -1 #no hay slots libres
            else:
                #hay un slot libre
                self.objetos[slot_libre] = [self.objeto_equipado_mano_izquierda[0],self.objeto_equipado_mano_izquierda[1],self.objeto_equipado_mano_izquierda[2],self.objeto_equipado_mano_izquierda[3]]
                self.objeto_equipado_mano_izquierda = None
                self.num_objetos_actual +=1
                return 1
        else:
            return -2 #no había ningún objeto en la mano izquierda
    def passObjectFromRightHandToInventory(self): #se pasa todo el stack entero a la mano
        if(self.objeto_equipado_mano_derecha != None):
            slot_libre = self.find_free_slot()
            if(slot_libre == -1):
                return -1
            else:
                self.objetos[slot_libre] = [self.objeto_equipado_mano_derecha[0],self.objeto_equipado_mano_derecha[1],self.objeto_equipado_mano_derecha[2],self.objeto_equipado_mano_derecha[3]]
                self.objeto_equipado_mano_derecha = None
                self.num_objetos_actual +=1
                return 1
        else:
            return -2

    def passObjectFromRightHandToLeftHand(self):
        if(self.objeto_equipado_mano_derecha != None):
            if(self.objeto_equipado_mano_izquierda != None):
                aux = self.objeto_equipado_mano_derecha
                self.objeto_equipado_mano_derecha = self.objeto_equipado_mano_izquierda
                self.objeto_equipado_mano_izquierda = aux
                return 1
            else:
                self.objeto_equipado_mano_izquierda = self.objeto_equipado_mano_derecha
                return 1
        elif(self.objeto_equipado_mano_izquierda != None):
            self.objeto_equipado_mano_derecha = self.objeto_equipado_mano_izquierda
            return 1
        else:
            return -1
        
    def find_free_slot(self):
        for i,elem in self.objetos.items():
            if(elem == None):
                return i
        else:
            return -1

    def addObjectToInventory(self,objeto,categoria,nombre):
        if(self.peso_actual + objeto.peso > self.peso_max):
            #print("return -1")
            return -1 #no puede llevar tanto peso
        
        if(objeto.stackeable):
            slot_objeto = self.findSameObject(nombre)
            if(slot_objeto == - 1):
                #print("no lo ha encontrado")
                pass #que siga
            else:
                q = self.objetos[slot_objeto][3]
                self.peso_actual += objeto.peso
                self.objetos[slot_objeto][3] = q+1
                #no añadimos nada a número actual de objetos, porque no estamos ocupando un slot nuevo
                #print("return 1")
                return 1
        #si estamos aquí, es que el objeto no era stackeable, o bien no teníamos ningún objeto de ese tipo
        if(self.num_objetos_actual + 1 > self.num_objetos_max):
            #print("return -2")
            return -2 #no hay slots libres
        else:
            slot_libre = self.find_free_slot()
            if(slot_libre == -1):
                #print("return -2")
                return -2 #no hay slots libres
            else:
                self.peso_actual += objeto.peso
                self.num_objetos_actual +=1
                self.objetos[slot_libre] = [categoria,nombre,objeto,1] #Añado el objeto al inventario: self.objetos[slot_1] = (categoria,nombre,objeto,1) --> el 1 es la cantidad de ese objeto
                #print("return 1")
                return 1 #proceso correcto
        
    def removeObjectFromInventory(self,slot): #solo eliminará 1 objeto de ese slot. Si es el único, lo vaciará, pero si hay más le restará 1
        if(self.objetos[str("slot_"+str(slot))] != None):
            peso_a_quitar = (self.objetos[str("slot_"+str(slot))][2].peso / self.objetos[str("slot_"+str(slot))][3])
            self.objetos[str("slot_"+str(slot))][3] -=1
            if(self.objetos[slot][3] == 0):
                self.objetos[str("slot_"+str(slot))][3] = None
                self.num_objetos_actual -=1 
            self.peso_actual -= peso_a_quitar
            self.objetos[str("slot_"+str(slot))] = None
            return 1 #proceso correcto
        else:
            return -1 #no había nada en ese slot

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
        self.armas["Armas c/c simples"]["Daga"] = Arma(4,1,0,0,0,0,2,0,tipo_uso.A_1_Mano,(5,5),tipo_damage.PERFORANTE,True,20,modificador.Destreza,True,False,False,False,1) #Arrojadiza, rango de 20 pies (no se aplica lo de desventaja para mayor rango. Se implementará en un futuro)
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
        self.armas["Armas a distancia marciales"]["Cerbatana"] = Arma(0,0,1,0,0,0,10,0,tipo_uso.A_1_Mano,(10,25),tipo_damage.PERFORANTE,False,None,modificador.Fuerza,False,True,False,False,1)
        #La red, como solo es de tipo especial, y no hace daño, no la voy a modelar por ahora
        
        self.objeto = {"Comida": {}, "Bebida": {}, "Mecanico": {}, "Refugio": {},"Libro": {}, "Kit": {}, "Iluminación": {}, "Otros": {}, "Almacenaje": {}, "Munición": {}}
        
        self.objeto["Refugio"]["Saco de dormir"] = Objeto(0,0,0,1,0,7,False)
        self.objeto["Mecanico"]["Palanca"] = Objeto(0,0,0,2,0,5,True)
        self.objeto["Otros"]["Piton"] = Objeto(5,0,0,0,0,0.25,True) #palos de escalada
        self.objeto["Iluminación"]["Antorcha"] = Objeto(1,0,0,0,0,1,True)
        self.objeto["Otros"]["Yesquero"] = Objeto(0,5,0,0,0,1,False)
        self.objeto["Comida"]["Ración"] = Objeto(0,5,0,0,0,2,True)
        self.objeto["Bebida"]["Odre de agua"] = Objeto(0,2,0,0,0,5,False) #definir en el futuro: 4.84,"liquido"
        self.objeto["Otros"]["Cuerda de cáñamo"] = Objeto(0,0,0,1,0,10,False)
        self.objeto["Munición"]["Flecha"] = Objeto(0,0,0,1,0,1,True)
        self.objeto["Almacenaje"]["Mochila"] = Objeto_de_Espacio(30,"sólido",5)
        self.objeto["Kit"]["De cocina"] = Objeto(0,0,0,2,0,5,False) #permitirá en sus funciones cocinar, pero se registrará como un único objeto por ahora
        self.objeto["Mecanico"]["Martillo"] = Objeto(0,0,0,1,0,3,False)

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

    def getArmasList(self):
        return self.armas
    def getArmaduraList(self):
        return self.armadura
    def getEscudosList(self):
        return self.escudo
    def getObjetosList(self):
        return self.objeto