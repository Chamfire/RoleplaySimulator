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
#prompt5 = "pixel, transparent background. Front view. "+"Es un enano con una sonrisa cónica, y con arrugas sobretodo alrededor de sus ojos. Su cabello es corto y espeso, y tiene bara muy larga."
#prompt6 = "pixel, transparent background. Front view. "+"Es una enana, mujer, de sonrisa crítica y de cabello con mechas blancas y grisáceas. Lleva un sombrero con talismanes."
#prompt7 = "pixel, transparent background. Front view. "+ "Es una enana mujer delgada y ágil, de cabello gris y rostro arrugado. Sonrisa amable. Lleva una camiseta de manga corta y unos pantalones de deporte."
#prompt8 = "pixel, transparent background. Front view. "+ "Es una enana mujer anciana sabia de sonrisa pícara y cabello espeso y oscuro, y llama la atención, que tiene barba, y esta es larga y bien cuidada. Tiene arrugas."
#prompt9 = "pixel, transparent background. Front view. "+ "Es una mujer de piel oscura, cabello negro rizado y lleva ropa de marinera."
#prompt10 = "pixel, transparent background. Front view. "+ "Es un elfo viejo de tono de piel verde, gordo, de ojos de color verde intenso y cabello negro. Tiene una barba larga y bien cuidada"
prompt = "pixel, transparent background. Portrait view. "+  "Es una elfa mujer de piel verde y pelo azul, con ojos azules. Lleva un sombrero de copa."

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
        
    img.save(f"elfo_vive en una ciudad antigua subterránea_64_739_de piel verde_"+str(i)+".png")
