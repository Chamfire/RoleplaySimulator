import os
import json
import uuid

class Jugador:
    def __init__(self):
        self.name = ' '
        self.avatarPicPerfil = None
        self.partidasEnProgreso = 0 #al pcpio serán 0
        self.partidasCompletadas = 0 #al pcpio serán 0
        self.numMuertes = 0 #al pcpio serán 0
        self.logged = False #se calcula con otras variables
        self.perfil_dir = 'perfil'
        self.perfil_file = 'perfil.json'
        self.badFile = False
        self.max_len_name = 13
        self.numIconos = 6
        self.id = None

    def loadPerfilFromFile(self):
        # Create the assets directory if it doesn't exist
        if os.path.exists(self.perfil_dir+'/'+self.perfil_file):
            #cargar la configuración
            with open(self.perfil_dir+'/'+self.perfil_file) as f:
                try:
                    data = json.load(f)
                except:
                    print("El archivo 'perfil' no tiene una estructura de json, por lo que se reseteará el perfil del jugador...")
                    self.badFile = True
                    #ignorará el if, y se quedarán los valores por defecto
            if(not self.badFile):
                name = None
                avatarPicPerfil = None
                partidasEnProgreso = None
                partidasCompletadas = None
                numMuertes = None
                id = None
                try:
                    name = data["name"]
                except:
                    print("Archivo 'perfil' corrupto en atributo -name-: estableciendo nombre del jugador a valor por defecto...")
                try:
                    avatarPicPerfil = data["avatarPicPerfil"]
                except:
                    print("Archivo 'perfil' corrupto en atributo -avatarPicPerfil-: estableciendo icono del jugador a valor por defecto...")
                try:
                    partidasEnProgreso = data["partidasEnProgreso"]
                except:
                    print("Archivo 'perfil' corrupto en atributo -partidasEnProgreso-: estableciendo contador de partidas en progreso del jugador a valor por defecto...")
                try:
                    partidasCompletadas = data["partidasCompletadas"]
                except:
                    print("Archivo 'perfil' corrupto en atributo -partidasCompletadas-: estableciendo contador de partidas completadas del jugador a valor por defecto...")
                try:
                    numMuertes = data["numMuertes"]
                except:
                    print("Archivo 'perfil' corrupto en atributo -numMuertes-: estableciendo contador de muertes del jugador a valor por defecto...")
                try:
                    id = data["id"]
                except:
                    print("Arhivo 'perfil' corrupto en atributo -id-: reasignando id...")
                    id = str(uuid.uuid4())
                
                #vamos a comprobar que no haya corrupción en el valor de los atributos
                if(name is not None and len(name) <= self.max_len_name):
                    self.name = name
                else:
                     print("En el archivo 'perfil' el valor de -name- se ha visto alterado. Regresando a la configuración por defecto...")
                if(avatarPicPerfil is not None and type(avatarPicPerfil)==int and 0<=avatarPicPerfil<=(self.numIconos-1) ):
                    self.avatarPicPerfil = avatarPicPerfil
                else:
                    print("En el archivo 'perfil' el valor de -avatarPicPerfil- se ha visto alterado. Regresando a la configuración por defecto...")
                if(partidasEnProgreso is not None and type(partidasEnProgreso)==int and partidasEnProgreso>=0):
                    self.partidasEnProgreso = partidasEnProgreso
                else:
                    print("En el archivo 'perfil' el valor de -partidasEnProgreso- se ha visto alterado. Regresando a la configuración por defecto...")
                if(partidasCompletadas is not None and type(partidasCompletadas)==int and partidasCompletadas>=0):
                    self.partidasCompletadas = partidasCompletadas
                else:
                    print("En el archivo 'perfil' el valor de -partidasCompletadas- se ha visto alterado. Regresando a la configuración por defecto...")
                if(numMuertes is not None and type(numMuertes)==int and numMuertes>=0):
                    self.numMuertes = numMuertes
                else:
                    print("En el archivo 'perfil' el valor de -numMuertes- se ha visto alterado. Regresando a la configuración por defecto...")
                if(self.name != " " and self.avatarPicPerfil is not None):
                    self.logged = True
                else:
                    #no está loggeado -> dejamos selg.logged a false, que es su valor por defecto
                    pass
                if(id != " " and id is not None):
                    self.id = id
                else:
                    print("En el archivo 'perfil' el valor de -id- se ha visto alterado. Reasignando id...")
                    self.id = str(uuid.uuid4())
        else:
            #Configuración por defecto -> es la que se pone en el init
            self.id = str(uuid.uuid4()) #le asignamos por primera vez una id al jugador

    def savePerfilToFile(self):
        if not os.path.exists(self.perfil_dir):
            os.makedirs(self.perfil_dir)
        data = {"name":self.name,"avatarPicPerfil":self.avatarPicPerfil,"partidasEnProgreso":self.partidasEnProgreso,"partidasCompletadas":self.partidasCompletadas,"numMuertes":self.numMuertes,"id":self.id}

        # Save the data to a JSON file
        with open(self.perfil_dir+'/'+self.perfil_file, 'w') as f:
            json.dump(data, f)
    