from llama_cpp import Llama
from Global import Global
import threading

class ConsultaDescripcion:
    def __init__(self):
        self.prompt = None
        self.generation_kwargs = None
        self.llm = None
        self.GLOBAL = Global()
        self.response_good = None

    def clear(self):
        self.prompt = None
        self.generation_kwargs = None
        self.llm = None
        self.response_good = None
        self.model_path = None
    
    def initialize(self,personaje,model_path):
        self.personaje = personaje
        self.model_path = model_path

    def getResponse(self):
        return self.response_good
    
    def cambiarScreenThread(self): #tiene que ser un hilo, puesto que Lock() es de threading
        self.GLOBAL.setRefreshScreen("seleccionPersonaje2")

    def consultaDescripcion(self):
        ## Instantiate model from downloaded file
        print("en consulta descripcion")
        self.llm = Llama(
            model_path=self.model_path,
            n_ctx=128,  # Context length to use
            n_threads=32,            # Number of CPU threads to use
            n_gpu_layers=0        # Number of model layers to offload to GPU
        )
        ## Generation kwargs
        self.generation_kwargs = {
            "max_tokens":60,
            "stop":["</s>"],
            "echo":False, # Echo the prompt in the output
            "top_k":1 # This is essentially greedy decoding, since the model will always return the highest-probability token. Set this value > 1 for sampling decoding
        }
        if(self.personaje.tipo_raza == "Elfo"):
            raza = "elf"
        elif(self.personaje.tipo_raza == "Enano"):
            raza = "dwarf"
        if(self.personaje.tipo_clase == "Bárbaro"):
            clase = "barbarian"
        elif(self.personaje.tipo_clase == "Explorador"):                    
            clase = "explorer"
                
        ## Run inference
        self.prompt = """<|im_start|>system
                    You are a dungeon master, of Dnd 5th generation, and you are helping me to create a character.<|im_end|>
                <|im_start|>user
                    Describe the physical appearance of an"""+raza+ """ """+clase+""" ("""+self.personaje.peso+"""kg, """+self.personaje.edad+""" years old) in just one short paragraph.<|im_end|>
                <|im_start|>assistant"""
        res = self.llm(self.prompt, **self.generation_kwargs) # Res is a dictionary
        ## Unpack and the generated text from the LLM response dictionary and print it
        self.response_good = res["choices"][0]["text"]
        if "." in self.response_good:
            self.response_good = self.response_good.rsplit(".", 1)[0] + "."  # Para devolver un párrafo completo
        self.response_good = self.response_good[2:] #quitamos los caracteres de espacio del pcpio
        hiloCambiaScreen = threading.Thread(target=self.cambiarScreenThread)
        hiloCambiaScreen.start()

