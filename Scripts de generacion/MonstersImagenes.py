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




for monster,description in data.items():
    prompt = "pixel, transparent background. "+  "Genera una imagen del siguiente ser de fantasía: "+monster

    #Generación de las imágenes
    translator = GoogleTranslator(source='auto', target='en')
    translated = False    
    while(translated == False):
        try:
            prompt = translator.translate(prompt)
            translated = True
        except Exception as e:
            print(e)
    for i in range(0,8):
        img = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=8,
            guidance_scale=1.5,
        ).images[0]
            
        img.save(f""+monster+"_"+str(i)+".png")