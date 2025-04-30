
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
from Consulta_RAG_musica import Consulta_RAG_musica

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

class Evaluacion_musica:
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
    
    prompts_prueba = ["¿Cuál es la mejor o mejores canciones para reproducir cuando el DM está dando la introducción para la aventura, y los jugadores empiezan desde barco?",
                      "¿Cuál es la mejor o mejores canciones para reproducir cuando el DM está dando la introducción para la aventura, y los jugadores empiezan desde mazmorra?",
                      "¿Cuál es la mejor o mejores canciones para reproducir cuando el DM está dando la introducción para la aventura, y los jugadores empiezan desde desierto?",
                      "¿Cuál es la mejor o mejores canciones para reproducir cuando el DM está dando la introducción para la aventura, y los jugadores empiezan desde ciudad moderna?",
                      "¿Cuál es la mejor o mejores canciones para reproducir cuando el DM está dando la introducción para la aventura, y los jugadores empiezan desde aldea medieval?",
                      "¿Cuál es la mejor o mejores canciones para reproducir cuando el DM está dando la introducción para la aventura, y los jugadores empiezan desde bosque?"]
    RAG_musica = Consulta_RAG_musica()
    cancion = []
    for prompt in prompts_prueba:
        canciones = RAG_musica.consultar_cancion(prompt)
        try:
            canciones_list = canciones.split("\n")
            print(canciones_list)
            cancion += [canciones_list] #Tomamos la primera de las canciones -> Mejor coincidencia
        except:
            cancion += ["error"]
    print(cancion)
    # [['intro_corta/Land_of_Pirates', 'intro_corta/Seven_Seas'], ['intro_corta/Our Story Begins', 'intro_corta/Red_Barons_Theme', 'intro_corta/Arcadia'], 
    #  ['intro_corta/Adventure_remaster', 'intro_corta/Return of the Mummy', 'intro_corta/Ibn Al-Noor'], ['intro_corta/Neverwhere_-_320bit', 'intro_corta/Nightclub_Two', 'intro_corta/Part_A'], 
    #  ['intro_corta/Call_to_Adventure', 'intro_corta/William_Tell_Overture_orchestral_version'], ['intro_corta/Adventure_remaster', 'intro_corta/Enchantment', 'intro_corta/William_Tell_Overture_orchestral_version']]