import os 
import json
from diffusers import DiffusionPipeline, LCMScheduler
import torch
from deep_translator import GoogleTranslator

config_dir = 'descripciones'
config_file = 'Monsters.json'
with open(config_dir+'/'+config_file,encoding='utf8') as f:
    data = json.load(f)

# ------- Imágenes ---------- #

base_model_id = "stabilityai/stable-diffusion-xl-base-1.0"
pipe = DiffusionPipeline.from_pretrained(base_model_id, variant="fp16", torch_dtype=torch.float16).to("cuda")
pipe.load_lora_weights("nerijs/pixel-art-xl", weight_name="pixel-art-xl.safetensors")

negative_prompt = "3d render, realistic"


#monstruos = {"no-muerto", "slime", "beholder","troll", "droide","fantasma","objeto animado","cyborg", "lobo wargo","vampiro","oso","hombre lobo","serpiente","cocodrilo","momia","esfinge","goblin","cultista","gnoll","sirena","tiburón","hada","elemental de roca","kraken","dragón","sombra","fénix","ankheg","basilisco","murciélago","rata","felino salvaje"}
monstruos = {"ship_background"}

for monster in monstruos:
    prompt = "pixel,  "+  "forest full of trees, and a river across it"

    #Generación de las imágenes
    for i in range(0,16):
        img = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=8,
            guidance_scale=1.5,
        ).images[0]
            
        img.save(f"bosque_"+str(i)+".png")