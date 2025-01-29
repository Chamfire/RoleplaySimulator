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