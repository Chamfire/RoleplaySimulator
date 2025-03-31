## Imports
#14s LLM MEJOR OPCIÓN
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

## Download the GGUF model
model_name = "bartowski/Llama-3.2-3B-Instruct-GGUF"
model_file = "Llama-3.2-3B-Instruct-Q4_K_M.gguf" # this is the specific model file we'll use in this example. It's a 4-bit quant, but other levels of quantization are available in the model repo if preferred
model_path = hf_hub_download(model_name, filename=model_file)

## Instantiate model from downloaded file
llm = Llama(
    model_path=model_path,
    n_ctx=128,  # Context length to use
    n_threads=32,            # Number of CPU threads to use
    n_gpu_layers=0        # Number of model layers to offload to GPU
)

## Generation kwargs
generation_kwargs = {
            "max_tokens":100,
            "stop":["</s>"],
            "echo":False, # Echo the prompt in the output
            "top_p": 0.85, #top_p y temperatura le da aleatoriedad
            "temperature": 0.8
}

## Run inference
prompt = "Describe la apariencia física de un elfo que es de clase bárbaro (65kg, 57 años de edad) en únicamente un párrafo corto. Sé creativo y divertido, y comienza tu respuesta con la frase 'Es un elfo bárbaro que...' "

res = llm(prompt, **generation_kwargs) # Res is a dictionary

## Unpack and the generated text from the LLM response dictionary and print it
response_good = res["choices"][0]["text"]
if "." in response_good:
    response_good = response_good.rsplit(".", 1)[0] + "."  # Para devolver un párrafo completo
response_good = response_good[2:] #quitamos los caracteres de espacio del pcpio
print(response_good)
# res is short for result