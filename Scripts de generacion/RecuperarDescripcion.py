import os 
import json
from diffusers import DiffusionPipeline, LCMScheduler
import torch
from deep_translator import GoogleTranslator

config_dir = 'descripciones'
config_file = 'NPCs.json'
with open(config_dir+'/'+config_file,encoding='utf8') as f:
    data = json.load(f)

# ------- Imágenes ---------- #

base_model_id = "stabilityai/stable-diffusion-xl-base-1.0"
pipe = DiffusionPipeline.from_pretrained(base_model_id, variant="fp16", torch_dtype=torch.float16).to("cuda")
pipe.load_lora_weights("nerijs/pixel-art-xl", weight_name="pixel-art-xl.safetensors")

negative_prompt = "3d render, realistic"

#prompt1 = "pixel, transparent background. "+"Es un enano anciano, de cabello blanco, que cae en forma de mechón sobre su frente, y sus ojos brillan. Su rostro está lleno de arrugas y su cuerpo es delgado pero fuerte, y su mirada sigue siendo aguda y su sonrisa, cálida y acogedora. Su ropa, sencilla pero cómoda, está hecha de telas que se han vuelto transparentes con el paso del tiempo, con cinturón."

#prompt2 = "pixel, transparent background. Front view. "+"Es un enano  de 103 años, con un sombrero de fieltro que le da un toque de elegancia. Solo pesa 45 kg, y su cabello es un poco canoso y se le notan las arrugas en su rostro, pero su mirada sigue siendo brillante y astuta. Viste como si fuera futurista."

#prompt3 = "pixel, transparent background. Front view. "+"Es un enano musculoso y anciano con arrugas finas. Lleva vestimenta de cuero y telas oscuras, y tiene 212 años. Su cabello es canoso y ondulado, y le cae sobre su frente en una mecha larga y desordenada, y tiene una larga barba"
prompt = "pixel, transparent background. Front view. "+" Es un enano pequeño con 321 años de edad, delgado, muy feo pero con ojos que brillan y una sonrisa."


#Generación de las imágenes
translator = GoogleTranslator(source='auto', target='en')
translated = False    
while(translated == False):
    try:
        prompt = translator.translate(prompt)
        translated = True
    except Exception as e:
        print(e)

img = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=8,
    guidance_scale=1.5,
).images[0]
        
img.save(f"NPC_enano_vive en un barco_46_321_omite referencias al color de piel.png")
