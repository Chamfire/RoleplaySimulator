import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, LlamaForCausalLM, BitsAndBytesConfig
#import bitsandbytes, flash_attn

quantization_config = BitsAndBytesConfig(load_in_4bit=True)

tokenizer = AutoTokenizer.from_pretrained('NousResearch/Hermes-3-Llama-3.2-3B', trust_remote_code=True)
model = LlamaForCausalLM.from_pretrained(
    "NousResearch/Hermes-3-Llama-3.2-3B",
    torch_dtype=torch.float16,
    device_map="auto",
    quantization_config=quantization_config,
    use_flash_attention_2=True
)

prompts = [
    """<|im_start|>system
You are a sentient, superintelligent artificial general intelligence, here to teach and assist me.<|im_end|>
<|im_start|>user
Write a short story about Goku discovering kirby has teamed up with Majin Buu to destroy the world.<|im_end|>
<|im_start|>assistant""",
    ]

for chat in prompts:
    print(chat)
    input_ids = tokenizer(chat, return_tensors="pt").input_ids.to("cuda")
    generated_ids = model.generate(input_ids, max_new_tokens=750, temperature=0.8, repetition_penalty=1.1, do_sample=True, eos_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(generated_ids[0][input_ids.shape[-1]:], skip_special_tokens=True, clean_up_tokenization_space=True)
    print(f"Response: {response}")