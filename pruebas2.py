import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, LlamaForCausalLM, GPT2LMHeadModel, BitsAndBytesConfig
import bitsandbytes
from optimum.bettertransformer import BetterTransformer

torch._dynamo.config.suppress_errors = True  # Evita errores en torch.compile

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)

#modelos descargados: ai-forever/mGPT y NousResearch/Hermes-3-Llama-3.2-3B
#Hermes 3: Tarda aprox 3 min en generar una respuesta. Problema: es en inglés. 
#ai-forever: 9 s es bazofia
tokenizer = AutoTokenizer.from_pretrained('NousResearch/Hermes-3-Llama-3.2-3B', trust_remote_code=True)
model = LlamaForCausalLM.from_pretrained(
#model = GPT2LMHeadModel.from_pretrained(
    "NousResearch/Hermes-3-Llama-3.2-3B",
    torch_dtype=torch.float16,
    quantization_config = quantization_config,
    device_map= "cuda"
)

#device = "cuda" if torch.cuda.is_available() else "cpu"  # Asegurarse de que se use la GPU si está disponible
#model = model.to(device)

# Texto de entrada
input_text = "Generate the physical description of an elf in Dnd 5th, who is a barbarian, weights 64 kg and is 36 years old."

# Tokenizar el texto
inputs = tokenizer(input_text, return_tensors="pt")
inputs = {key: value.to("cuda") for key, value in inputs.items()}

# Generar el texto
output = model.generate(
    inputs['input_ids'],
    attention_mask=inputs['attention_mask'],  # Asegúrate de que el attention_mask esté definido
    pad_token_id=tokenizer.eos_token_id,  # Establece el pad_token_id si es necesario
    max_length=256
)

# Decodificar y mostrar el resultado
print(tokenizer.decode(output[0], skip_special_tokens=True))