from Lista_Inventario import Lista_Inventario
import numpy as np

class Patata:
    def __init__(self,var):
        self.var = var


s = "patata123:Chamfire:1:4c62140c-a27c-4b39-86f3-8d4d18b5b792"
[password,nombre,pic,id] = s.split(':')
print(password,nombre,pic,id)

s2 = "ok:4:id1;pepe;1:id2;juan;4"
resp = s2.split(':')
jugadores = {}
for i in range(0,len(resp)-2):
    [id_j,name,pic] = resp[i+2].split(';')
    jugadores[i] = (id_j,(name,int(pic))) 
print((True,int(resp[1]),jugadores))
#{0: ('id1', ('pepe', 1)), 1: ('id2', ('juan', 4))}

a = {1,2,3}
print(len(a))

s3 = "hola"
resp2 = s3.split(":")
print(resp2[0])

f = '-34'
print(int(f))
n = 5
objetos = {}
for i in range(0,n):
     #definimos los slots para cada posible objeto
    objetos[str("slot_"+str(i))] = None # self.objetos = {"slot_0": None, "slot_1": None, etc etc}
print(objetos)

lista_inv = Lista_Inventario()
armaduras = lista_inv.getArmaduraList()
armadura_1 = armaduras["Armaduras ligeras"]["Acolchada"]
tipo = str(type(armadura_1))
print(tipo[25:-2])

a = []
a.append('a')
a[0]+= 'b'
print(a)


p1 = Patata(1)
p2 = Patata(2)

array = [p1,p2,p1]

p1.var = 4

for i in array:
    print(i.var)

patata = "patata"
print(len(patata))
print(patata[3:])
matrix = np.zeros((5,5))
matrix[0][0] = 1
matrix[1][2] = 2
print(matrix)
aux_matrix = matrix.copy()
aux_matrix[1][2] = 3
print(matrix)
for n in matrix[1]:
    print(n)

a = [1,4,5,6]
print(a[-1])
print(a[1:])
print(2<=-1<=4)
r = {}
for i in r:
    print(i)
f = set()
f.add((3,4))
f.add((3,4))
print(f)
print((3,4) in f)
a2 = {1: [23,"abcd"],2: [24,"lkj"]}
a3 = a2
a3[2] = [25,"lkj"]
print(a2)
a4 = [3,[2,4]]
print(a4[0])
print(a4[1][0])

