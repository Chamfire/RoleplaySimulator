
from langchain.chains.retrieval_qa.base import RetrievalQA
import faiss
from sentence_transformers import SentenceTransformer
from huggingface_hub import hf_hub_download
from langchain_core.runnables import Runnable
from llama_cpp import Llama
from langchain.schema import Document
import random
import numpy as np
import contextlib
import os
import sys

@contextlib.contextmanager
def suppress_stdout_stderr():
    with open(os.devnull, "w") as fnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = fnull
        sys.stderr = fnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

class Consulta_RAG_musica:
    def __init__(self):
        with open('RAG_music/Descripciones_canciones.txt','r',encoding='utf-8') as file:
            text = file.read()
            file.close()
        self.documentos = text.split('\n\n')
        #print(self.documentos)

    def crear_vectores(self): #all-MiniLM-L6-v2
        embedding_model = SentenceTransformer('all-MiniLM-L12-v2') 
        embeddings = embedding_model.encode(self.documentos)

        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings.astype(np.float32))
        return index, self.documentos, embedding_model

    def devolver_contexto(self,query, embedding_model, index, documents, k=2):
        query_embedding = embedding_model.encode([query])
        distances, indices = index.search(query_embedding.astype(np.float32), k)
        return [documents[i] for i in indices[0]]

    def consultar_cancion(self,contexto_estado):
        model_name="bartowski/Llama-3.2-3B-Instruct-GGUF"
        model_file = "Llama-3.2-3B-Instruct-Q4_K_M.gguf"
        model_path = hf_hub_download(model_name, filename=model_file)
        with suppress_stdout_stderr():
            llm = Llama(
                model_path=model_path,
                n_ctx=2048,  # Context length to use
                n_threads=32,            # Number of CPU threads to use
                n_gpu_layers=0,        # Number of model layers to offload to GPU
                seed = 55555
            )
        ## Generation kwargs
        generation_kwargs = {
            "max_tokens":300,
            "stop":["</s>"],
            "echo":False, # Echo the prompt in the output
            "top_p": 0.85, #top_p y temperatura le da aleatoriedad
            "temperature": 0.8
        }

        index, document_texts, embedding_model = self.crear_vectores()
        # Retrieve context
        query_context = contexto_estado
        context = self.devolver_contexto(query_context, embedding_model, index, document_texts)
        contexto_formato = "\n".join(context)

        # Consulta de ejemplo
        # query = """{Eres un dungeon master de Dnd 5e y tienes que escoger la mejor canción para un momento específico de una aventura.}<|eot_id|><|start_header_id|>user<|end_header_id|>
        #                 {¿Cuál es la mejor canción para una situación que tiene los siguientes atributos: algo tenso, sigilo y tribal? Responde únicamente con el nombre de la canción elegida, sin dar ningún detalle adicional.}
        #                 <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
        #query = f"Use just the following context for answering the question: \n Taking into account that all the songs have this format: \"carpet/name\": \n{contexto_formato} \n<|eot_id|><|start_header_id|>user<|end_header_id|> \nQuestion: {query_context} \nAnswer just with the content above, and giving just the carpet/name or several carpet/names of the songs choosed, separated in different lines and whithout giving any additional detail.\n<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
        query = f"Usa únicamente el siguiente contexto para responder a la pregunta: \n Teniendo en cuenta que todas las canciones tienen este formato: nombre carpeta/nombre cancion, y que: \n{contexto_formato} \n<|eot_id|><|start_header_id|>user<|end_header_id|> \nPregunta: {query_context} \nResponde únicamente basandote en el contexto anterior, y devolviendo únicamente la carpeta/canción o varias carpeta/canción escogidas, separadas en líneas diferentes, sin dar ningún detalle adicional.\n<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
        res = llm(query, **generation_kwargs) # Res is a dictionary
        ## Unpack and the generated text from the LLM response dictionary and print it
        response_good = res["choices"][0]["text"]
        if "." in response_good:
            response_good = response_good.rsplit(".", 1)[0] + "."  # Para devolver un párrafo completo
        response_good = response_good.lstrip()
        # print("\n=== RESPUESTA ===")
        # print(response_good)
        # print("\n=== CONTEXTO ===")
        # print(query)
        return response_good


#consulta = Consulta_RAG_musica()
#consulta.consultar_cancion("¿Cuál es la mejor o mejores canciones para reproducir cuando el DM está dando la introducción para la aventura, y los jugadores empiezan desde Barco?")



#consulta.consultar_cancion("What is the best or bests songs to reproduce when the players are in combat?")

#Ejemplos de ejecución:
#Resultado de lista de canciones que coinciden con la descripción: 

#consulta.consultar_cancion("What is the best song to reproduce when the players are in a tense environment?")
#------------------ RESPUESTA -------------------------------
# === RESPUESTA ===
# tension_corta/Countdown
# tension_corta/Bloodlust
# tension_corta/Black Vortex
# tribal/Big Mojo
# tension_corta/Constance

# === CONTEXTO ===
# Use just the following context for answering the question:
# When players are exploring a dungeon, or any dark or gloomy zone (it could for example be night), the best
# songs to reproduce are "tension_corta/Constance" or "tension_corta/Countdown". If we also know that they are
# outdoors, you can also reproduce "tension_corta/Bloodlust". These songs can also be reproduced in a tense environment.
# When the players are talking to an evil NPC, the best song to play is "tension_corta/Black Vortex". This song can
# also be reproduced in a tense environment.
# When the players are in a tribe, indigenous villages or any unhappy culture, in a cheerful environment,
# the song to be reproduced is "tribal/tribal_joy". However, if the environment is tense, the best
# song is tribal/Big Mojo". When the environment is not tense, but neutral, it will be "tribal/ambient_bongos".
# <|eot_id|><|start_header_id|>user<|end_header_id|>
# Question: What is the best song to reproduce when the players are in a tense environment?
# Answer just with the content above, and giving just the name of the song choosed, whithout giving any additional detail.
# <|eot_id|><|start_header_id|>assistant<|end_header_id|>




#Resultado de canción que coincide: 
 #What is the best song to reproduce when the players are talking to an evil NPC?

# tension_corta/Black Vortex

# === CONTEXTO ===
# Use just the following context for answering the question:
# When the players are talking to an evil NPC, the best song to play is "tension_corta/Black Vortex".
# When players are exploring a dungeon, or any dark or gloomy zone (it could for example be night), the best
# songs to reproduce are "tension_corta/Constance" or "tension_corta/Countdown". If we also know that they are
# outdoors, you can also reproduce "tension_corta/Bloodlust".
# When several monsters are being seen in an area by the players for the first time, to prepare a possible combat, the song to
# reproduce is "tension_corta/Evil March".
# <|eot_id|><|start_header_id|>user<|end_header_id|>
# Question: What is the best song to reproduce when the players are talking to an evil NPC?
# Answer just with the content above, and giving just the name of the song choosed, whithout giving any additional detail.
# <|eot_id|><|start_header_id|>assistant<|end_header_id|>
# ---------------------------------------------------------------------



#Resultado de la canción más parecida que coincide, pues la que más coincide no es posible: 

#consulta.consultar_cancion("Taking into account that tension_corta/Black Vortex cannot be the answer, what is the best song to reproduce when the players are talking to an evil NPC?")
# === RESPUESTA ===
# tension_corta/Constance

# === CONTEXTO ===
# Use just the following context for answering the question:
# When the players are talking to an evil NPC, the best song to play is "tension_corta/Black Vortex".
# When players are exploring a dungeon, or any dark or gloomy zone (it could for example be night), the best
# songs to reproduce are "tension_corta/Constance" or "tension_corta/Countdown". If we also know that they are
# outdoors, you can also reproduce "tension_corta/Bloodlust".
# When several monsters are being seen in an area by the players for the first time, to prepare a possible combat, the song to
# reproduce is "tension_corta/Evil March".
# <|eot_id|><|start_header_id|>user<|end_header_id|>
# Question: Taking into account that tension_corta/Black Vortex cannot be the answer, what is the best song to reproduce when the players are talking to an evil NPC?
# Answer just with the content above, and giving just the name of the song choosed, whithout giving any additional detail.
# <|eot_id|><|start_header_id|>assistant<|end_header_id|>