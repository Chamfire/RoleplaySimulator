import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, LlamaForCausalLM, GPT2LMHeadModel, BitsAndBytesConfig
import bitsandbytes

quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,
    bnb_8bit_compute_dtype=torch.float16
)

#modelos descargados: ai-forever/mGPT y NousResearch/Hermes-3-Llama-3.2-3B
#Hermes 3: Tarda aprox 9 min con 750 tokens, temperature=0.8, repetition_penalty=1.1, do_sample=True
#ai-forever: 9 s es bazofia
tokenizer = AutoTokenizer.from_pretrained('NousResearch/Hermes-3-Llama-3.2-3B', trust_remote_code=True)
model = LlamaForCausalLM.from_pretrained(
#model = GPT2LMHeadModel.from_pretrained(
    "NousResearch/Hermes-3-Llama-3.2-3B",
    torch_dtype=torch.float16,
    quantization_config = quantization_config,
    device_map= "cuda"
)


prompts = [
    """<|im_start|>system
            You are a dungeon master, of Dnd 5th generation, and you are helping me to create a character.<|im_end|>
        <|im_start|>user
            Generate a physical description of an elf, which is barbarian, weights 65kg and is 57 years old.<|im_end|>
        <|im_start|>assistant""",
    ]

for chat in prompts:
    print(chat)
    encoding = tokenizer(chat, return_tensors="pt")
    input_ids = encoding.input_ids.to("cuda")
    attention_mask = encoding.attention_mask.to("cuda")
    generated_ids = model.generate(input_ids, attention_mask=attention_mask,max_new_tokens=100, temperature=0.8, repetition_penalty=1.1, do_sample=True, eos_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(generated_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    print(f"Response: {response}")