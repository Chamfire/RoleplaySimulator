## Imports
#14s LLM MEJOR OPCIÓN
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
import random
import os 
import json


config_dir = 'descripciones'
config_file = 'Monsters.json'

## Download the GGUF model
model_name = "bartowski/Llama-3.2-3B-Instruct-GGUF"
model_file = "Llama-3.2-3B-Instruct-Q4_K_M.gguf" 
model_path = hf_hub_download(model_name, filename=model_file)
#semilla = 70853
## Instantiate model from downloaded file

## Run inference
prompts = []
descripciones = {}
monstruos = {"no-muerto", "slime", "beholder","troll", "droide","fantasma","objeto animado","cyborg", "lobo wargo","vampiro","oso","hombre lobo","serpiente","cocodrilo","momia","esfinge","goblin","cultista","gnoll","sirena","tiburón","hada","elemental de fuego","elemental de aire","elemental de tierra","elemental de agua","elemental de caos","elemental de planta","kraken","dragón","sombra","fénix","ankheg","basilisco","murciélago","rata","felino salvaje"}
#2 descripciones por cada tipo de monstruo, y luego me quedo con la mejor de las 2 descripciones. 
for monstruo in monstruos:
    for i in range(0,2):
        prompts+= [("""{Eres un dungeon master de Dnd 5e y tienes que generar descripciones para monstruos.}<|eot_id|><|start_header_id|>user<|end_header_id|>
                    {Describe la apariencia física de un """+monstruo+ """. Limítate a ser creativo y divertido, y genéralo directamente como texto en forma de párrafo. Omite cualquier frase inicial de ¡Claro, aquí lo tienes! y cosas parecidas. Comienza tu descripción con "Se trata de un ser/monstruo/animal/etc..."}
                    <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",str(monstruo+"_"+str(i)))]
            
for prompt in prompts:
    semilla = random.randint(1,100000)
    llm = Llama(
            model_path=model_path,
            n_ctx=500,  # Context length to use
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
    res = llm(prompt[0], **generation_kwargs) # Res is a dictionary

        ## Unpack and the generated text from the LLM response dictionary and print it
    response_good = res["choices"][0]["text"]
    if "." in response_good:
        response_good = response_good.rsplit(".", 1)[0] + "."  # Para devolver un párrafo completo
    response_good = response_good.lstrip()
    print(response_good)
    # res is short for result
    descripciones[prompt[1]] = [response_good]

    
if not os.path.exists(config_dir):
     os.makedirs(config_dir)
        
with open(config_dir+'/'+config_file, 'w',encoding='utf8') as f:
     json.dump(descripciones, f,ensure_ascii=False)
