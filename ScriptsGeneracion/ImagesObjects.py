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


objetos = {"Bastón","Daga","Gran clava","Hacha de mano","Hoz","Jabalina","Lanza","Martillo ligero","Maza","Clava","Arco corto","Ballesta ligera","Dardo","Honda","Alabarda","Atarraga","Cimitarra","Espada corta","Espada larga","Espadón","Estoque","Hacha de batalla","Gran hacha","Guja","Lanza de caballería","Látigo","Lucero del alba","Martillo de guerra","Mayal","Pica","Pica de guerra","Tridente","Arco largo","Ballesta de mano","Ballesta pesada","Cerbatana","Saco de dormir","Palanca","Piton","Antorcha","Yesquero","Ración","Odre de agua","Cuerda de cáñamo","Flecha","Mochila","Kit de cocina","Martillo","Armadura acolchada","Armadura de cuero","Armadura de cuero tachonado","Armadura de pieles","Camisote de mallas","Cota de escamas","Coraza","Semiplacas","Cota de anillas","Cota de mallas","Bandas","Placas","Escudo"}
for objeto in objetos:
    prompt = "pixel, transparent background. "+  "Genera la siguiente arma: "+objeto

    translator = GoogleTranslator(source='auto', target='en')
    translated = False    
    while(translated == False):
        try:
            prompt = translator.translate(prompt)
            translated = True
        except Exception as e:
            print(e)
            
    #Generación de las imágenes
    for i in range(0,16):
        img = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=8,
            guidance_scale=1.5,
        ).images[0]
            
        img.save(f""+objeto+"_"+str(i)+".png")


