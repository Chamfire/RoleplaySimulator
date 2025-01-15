import os
import json

class Configuracion:
    def __init__(self):
        self.volMusica = 0.5
        self.volEffects = 1.0
        self.fps = 60
        self.dmVoice = False
        self.config_dir = 'configuration'
        self.config_file = 'config.json'
        self.badFile = False

    def getConfiguration(self):
        return [self.volMusica, self.volEffects,self.fps,self.dmVoice]

    def loadConfigurationFromFile(self):
        # Create the assets directory if it doesn't exist
        if os.path.exists(self.config_dir+'/'+self.config_file):
            #cargar la configuración
            with open(self.config_dir+'/'+self.config_file) as f:
                try:
                    data = json.load(f)
                except:
                    print("El archivo 'configuration' no tiene una estructura de json, por lo que se reseteará la configuración del jugador...")
                    self.badFile = True
            if(not self.badFile):
                volMusica = None
                volEffects = None
                dmVoice = None
                fps = None
                #comprobaremos cada parte de la configuración, para que si se ha corrompido algo, el resto se pueda rescatar
                try:
                    volMusica = data["volMusica"]
                except:
                    print("Archivo 'configuration' corrupto en atributo -volMusica-: estableciendo volumen de música a valor por defecto...")
                try:
                    volEffects = data["volEffects"]
                except:
                    print("Archivo 'configuration' corrupto en atributo -volEffects-: estableciendo volumen de efectos de sonido a valor por defecto...")
                try:
                    dmVoice = data["dmVoice"]
                except:
                    print("Archivo 'configuration' corrupto en atributo -dmVoice-: estableciendo configuración del speech-to-text del DM a valor por defecto...")
                try:
                    fps = data["fps"]
                except:
                    #en caso de que se haya corrompido alguna cosa, se dejará la configuración por defecto
                    print("Archivo 'configuration' corrupto en atributo -fps-: estableciendo configuración de fps a valor por defecto...")
                #antes de asignarlo vamos a comprobar que no haya ninguna corrupción dentro de cada campo:
                if(volMusica is not None and (type(volMusica)==float or type(volMusica)==int) and 0 <= volMusica <=1):
                    self.volMusica = volMusica
                else:
                    print("En el archivo 'configuration' el valor de -volMusica- se ha visto alterado. Regresando a la configuración por defecto...")
                if(volEffects is not None and (type(volEffects)==float or type(volEffects)==int) and 0 <= volEffects <=1):
                    self.volEffects = volEffects
                else:
                    print("En el archivo 'configuration' el valor de -volEffects- se ha visto alterado. Regresando a la configuración por defecto...")
                if(dmVoice is not None and type(dmVoice)==bool):
                    self.dmVoice = dmVoice
                else:
                    print("En el archivo 'configuration' el valor de -dmVoice- se ha visto alterado. Regresando a la configuración por defecto...")
                if(fps is not None and type(fps)==int and (fps == 60 or fps == 90 or fps == 120 or fps == 144)):
                    self.fps = fps
                else:
                    print("En el archivo 'configuration' el valor de -fps- se ha visto alterado. Regresando a la configuración por defecto...")

        else:
            #Configuración por defecto -> es la que se pone en el init
            pass 

    def saveConfigurationToFile(self):
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        data = {"volMusica":self.volMusica,"volEffects":self.volEffects,"dmVoice":self.dmVoice,"fps":self.fps}

        # Save the data to a JSON file
        with open(self.config_dir+'/'+self.config_file, 'w') as f:
            json.dump(data, f)
                    

