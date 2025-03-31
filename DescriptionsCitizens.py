## Imports
#14s LLM MEJOR OPCIÓN
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
import random
import os 
import json


config_dir = 'descripciones'
config_file = 'NPCs.json'

## Download the GGUF model
model_name = "bartowski/Llama-3.2-3B-Instruct-GGUF"
model_file = "Llama-3.2-3B-Instruct-Q4_K_M.gguf" 
model_path = hf_hub_download(model_name, filename=model_file)
semilla = random.randint(1,100000)
print(semilla)
random.seed = semilla
## Instantiate model from downloaded file

## Run inference
prompts = []
descripciones = {}
razas = {"enano", "elfo"}
generos = {"hombre","mujer"}
escenarios = {"vive en un barco", "vive en el desierto", "vive en una ciudad moderna","vive en una aldea medieval", "vive en una ciudad antigua subterránea","vive en el bosque"}

for raza in razas:
    for genero in generos:
        for escenario in escenarios:
            if(raza == "elfo"):
                piel = "de piel verde"
                peso = random.randint(60,80)
                edad = random.randint(60,750)
            elif(raza == "enano"):
                piel = "omite referencias al color de piel"
                peso = random.randint(45,67)
                edad = random.randint(18,350)
            prompts+= ["""{Eres un dungeon master de Dnd 5e y me estás ayudando a hacerme la ficha de personaje.}<|eot_id|><|start_header_id|>user<|end_header_id|>
                        {Describe la apariencia física de un """+raza+ """que """ +escenario+ """ y pesa """+str(peso)+"""kg, tiene """+str(edad)+ """ años de edad, y """+piel+""") en únicamente un párrafo. Limítate a ser creativo y divertido, y comienza directamente tu respuesta con la frase "Es un """+raza+""" que..." }
                        <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""]
            
for prompt in prompts:
    llm = Llama(
            model_path=model_path,
            n_ctx=400,  # Context length to use
            n_threads=32,            # Number of CPU threads to use
            n_gpu_layers=0,        # Number of model layers to offload to GPU
            seed= semilla
    )

        ## Generation kwargs
    generation_kwargs = {
                    "max_tokens":400,
                    "stop":["</s>"],
                    "echo":False, # Echo the prompt in the output
                    "top_p": 0.85, #top_p y temperatura le da aleatoriedad
                    "temperature": 0.8
    }
    res = llm(prompt, **generation_kwargs) # Res is a dictionary

        ## Unpack and the generated text from the LLM response dictionary and print it
    response_good = res["choices"][0]["text"]
    if "." in response_good:
        response_good = response_good.rsplit(".", 1)[0] + "."  # Para devolver un párrafo completo
    response_good = response_good[1:] #quitamos los caracteres de espacio del pcpio
    print(response_good)
    # res is short for result
    descripciones[prompt] = [response_good]

    
if not os.path.exists(config_dir):
    os.makedirs(config_dir)
        
with open(config_dir+'/'+config_file, 'w') as f:
    json.dump(descripciones, f)

print("semilla: ",semilla)