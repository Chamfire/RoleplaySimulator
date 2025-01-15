class Partida:
    def __init__(self):
        self.num_jugadores = 1 #valor por defecto -> tú mismo 
        self.ubicacion_historia = None 
        self.server_code = None
        self.server_port = None #se establece por defecto
        self.horas_jugadas = 0
        self.ultima_conexion = None # se establecerá justo cuando se le de al botón de crear partida
        self.numPartida = None
        self.nombre = None

    def setNombrePartida(self,nombre):
        self.nombre = nombre
    def getNombrePartida(self):
        return self.nombre
    def setNumJugadores(self,numJugadores):
        self.num_jugadores = numJugadores
    def getNumJugadores(self):
        return self.num_jugadores
    
    def setUbicacionHistoria(self,uh):
        self.ubicacion_historia = uh
    def getUbicacionHistoria(self):
        return self.ubicacion_historia
    
    def setServerCode(self,sc):
        self.server_code = sc
    def getServerCode(self):
        return self.server_code
    
    def setServerPort(self,sp):
        self.server_port = sp
    def getServerPort(self):
        return self.server_port
    
    def setHorasJugadas(self,hj):
        self.horas_jugadas = hj
    def getHorasJugadas(self):
        return self.horas_jugadas
    
    def setUltimaConexion(self,uc):
        self.ultima_conexion = uc
    def getUltimaConexion(self):
        return self.ultima_conexion
    
    def setNumPartida(self,np):
        self.numPartida = np
    def getNumPartida(self):
        return self.numPartida

    