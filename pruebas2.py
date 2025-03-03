import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, LlamaForCausalLM, LlamaTokenizer, BitsAndBytesConfig
import bitsandbytes

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    llm_int8_enable_fp32_cpu_offload=True
)

#modelos descargados: ai-forever/mGPT y NousResearch/Hermes-3-Llama-3.2-3B
#Hermes 3: Tarda aprox 9 min con 750 tokens, temperature=0.8, repetition_penalty=1.1, do_sample=True
#Hermes 3: Tarda aprox 3 min 19s con 100 tokens, temperature=0.8, repetition_penalty=1.1, do_sample=True
#Hermes 3: Tarda aprox 3 min 17s con 100 tokens, temperature=0.8, repetition_penalty=1.1, do_sample=True y con añadido de prompt "in just 1 paragraph"
#Hermes 3: Tarda aprox 2 min 7s con 60 tokens, temperature=0.8, repetition_penalty=1.1 y con añadido de prompt "in just 1 paragraph"
#Hermes 3: Tarda aprox 2 min 12s con 60 tokens, temperature=0.8, repetition_penalty=1.1 y con añadido de prompt "in just 1 paragraph" y cogiendo solo un párrafo completo
#--output correcto
#prueba modificando la penalty a 1.05, temperatura a 0.7, añadiendo limite en top k 50 y top p 0.9: mismo tiempo
#--output correcto
#Hermes 3: Tarda aprox 2 min 8s con 60 tokens, y con añadido de prompt "in just 1 paragraph" y cogiendo solo un párrafo completo
#--output correcto
#MEJOR: Hermes 3: Tarda aprox 1 min 53s con 60 tokens, con añadido de prompt "in just 1 paragraph" y cogiendo solo un párrafo completo. 4 bits en vez de 8
#--output correcto
#Hermes 3: Tarda aprox 1 min 56s con 60 tokens, con añadido de prompt "in just 1 paragraph" y cogiendo solo un párrafo completo. 4 bits y prompt con introducción de rol eliminada
#--output correcto
#Hermes 3: Tarda aprox 2 min con 60 tokens, con añadido de prompt "in just 1 paragraph" y cogiendo solo un párrafo completo. 4 bits y double quant parameter en quantization
#--output correcto
# Hermes 3 GGUF: Tarda aprox  con 60 tokens, con añadido de prompt "in just 1 paragraph" y cogiendo solo un párrafo completo. 4 bits 



#tokenizer = AutoTokenizer.from_pretrained('NousResearch/Hermes-3-Llama-3.2-3B', trust_remote_code=True)
tokenizer = LlamaTokenizer.from_pretrained('', trust_remote_code=True)
model = LlamaForCausalLM.from_pretrained(
    "NousResearch/Hermes-3-Llama-3.2-3B-GGUF",
    torch_dtype=torch.float16,
    quantization_config = quantization_config,
    device_map= "cuda"
    )



prompts = [
    """<|im_start|>system
            You are a dungeon master, of Dnd 5th generation, and you are helping me to create a character.<|im_end|>
        <|im_start|>user
            Describe the physical appearance of an elf barbarian (65kg, 57 years old) in just one short paragraph.<|im_end|>
        <|im_start|>assistant""",
    ]

for chat in prompts:
    print(chat)
    encoding = tokenizer(chat, return_tensors="pt")
    input_ids = encoding.input_ids.to("cuda")
    attention_mask = encoding.attention_mask.to("cuda")
    generated_ids = model.generate(input_ids, attention_mask=attention_mask,max_new_tokens=60, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(generated_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    if "." in response:
        response = response.rsplit(".", 1)[0] + "."  # Para devolver un párrafo completo
    print(f"Response: {response}")

