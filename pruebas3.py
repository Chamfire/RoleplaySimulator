from vllm import LLM
llm = LLM(model="NousResearch/Hermes-3-Llama-3.2-3B")
output = llm.generate("Describe the physical appearance of an elf barbarian (65kg, 57 years old) in just one short paragraph.")
print(output)