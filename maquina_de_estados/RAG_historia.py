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
import time
import cohere

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

class RAG_historia:
    def __init__(self,currentPartida):
        self.currentPartida = currentPartida
        self.co = cohere.Client('')
        if os.path.exists('maquina_de_estados/'+currentPartida):
            #Cargamos el trasfondo del NPC de la partida, si existe
            if os.path.exists('maquina_de_estados/'+currentPartida+'/info_NPC.txt'):
                with open('maquina_de_estados/'+currentPartida+'/info_NPC.txt','r',encoding='utf-8') as file:
                    text = file.read()
                    file.close()
                self.documentos = text.split('\n\n')
            if os.path.exists('maquina_de_estados/'+currentPartida+'/dialogos_NPC.txt'):
                with open('maquina_de_estados/'+currentPartida+'/dialogos_NPC.txt','r',encoding='utf-8') as file:
                    text = file.read()
                    file.close()
                self.documentos += text.split('\n\n')
            if os.path.exists('maquina_de_estados/'+currentPartida+'/info_mision.txt'):
                with open('maquina_de_estados/'+currentPartida+'/info_mision.txt','r',encoding='utf-8') as file:
                    text = file.read()
                    file.close()
                self.documentos += text.split('\n\n')

        else:
            #no existe el path -> hay que crearlo (la carpeta p1,p2,p3)
            if not os.path.exists('maquina_de_estados/'+currentPartida):
                os.makedirs('maquina_de_estados/'+currentPartida)

    def crear_vectores(self): #all-MiniLM-L6-v2
        embedding_model = SentenceTransformer('all-MiniLM-L12-v2') 
        embeddings = embedding_model.encode(self.documentos)

        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings.astype(np.float32))
        return index, self.documentos, embedding_model

    def devolver_contexto(self,query, embedding_model, index, documents, k=5):
        query_embedding = embedding_model.encode([query])
        distances, indices = index.search(query_embedding.astype(np.float32), k)
        return [documents[i] for i in indices[0]]
    
    #Escribimos en un archivo .txt el nombre, la descripción física, el trasfondo y el motivo de 
    #que el NPC esté donde esté, para ser recuperado por el RAG
    def escribirInfoNPC(self,nombreNPC,descripcionFisica,infoTrasfondo,motivoUbicacion):
        with open('maquina_de_estados/'+self.currentPartida+'/info_NPC.txt','w',encoding='utf-8') as f:
            info_a_escribir = "El nombre del NPC es "+nombreNPC+". "+descripcionFisica+" \n\n"
            info_a_escribir += infoTrasfondo+"\n\n"
            info_a_escribir += motivoUbicacion
            f.write(info_a_escribir)

    def escribirCurrentDialogoNPCYPregunta(self,msg_jugador,respuestaNPC,lastText):
        for word in respuestaNPC.split(' '):
            if(word == "metajuego"):
                return -1
        with open('maquina_de_estados/'+self.currentPartida+'/dialogos_NPC.txt','a',encoding='utf-8') as f:
            info_a_escribir = "\n\nCuando él me dijo: '"+lastText+"'. Yo le respondí con lo siguiente: '"+msg_jugador+"'. A esa respuesta, él me respondió: "+respuestaNPC
            f.write(info_a_escribir)
        return 1

    def escribirInfoMision(self,mision_basica,dialogos,nombreNPC):
        with open('maquina_de_estados/'+self.currentPartida+'/info_mision.txt','w',encoding='utf-8') as f:
            info_a_escribir = "Misión actual para mí: "+mision_basica+"\n\n"
            info_a_escribir += "Diálogo que empleó "+nombreNPC+" para proponerme la misión: "+dialogos+"\n\n"
            info_a_escribir += "Pistas para completar la misión: se necesita abrir una o varias puertas que bloquean el camino entre las galerías. Para abrir las puertas, se debe emplear su llave. Las llaves se pueden encontrar dentro de algunos sarcófagos que hay en las galerías de las mazmorras.\n\n"
            info_a_escribir += "Detalles sobre la mazmorra en la que se encuentra aquello que hay que encontrar: Solo contiene galerías vacías, conectadas por puertas y pasillos. En las galerías puede haber sarcófagos, y algunos animales o monstruos peligrosos."
            f.write(info_a_escribir)
    def escribirInfoSala(self,sala,frases_puertas,descripcion):
        with open('maquina_de_estados/'+self.currentPartida+'/'+str(sala)+'.txt','w',encoding='utf-8') as f:
            info_a_escribir = "La descripción de la sala "+str(sala)+"Es la siguiente: "+descripcion+"\n\n"
            for i in frases_puertas[sala]:
                if(frases_puertas[sala][i][0] != None):
                    info_a_escribir += "Diálogo del Dungeon Master cuando un jugador intenta abrir la puerta que conecta la sala "+str(sala)+" con la sala "+str(i)+", pero está cerrada: "+str(frases_puertas[sala][i][0])+"\n\n"
                info_a_escribir += "Diálogo del Dungeon Master cuando un jugador intenta abrir la puerta que conecta la sala "+str(sala)+" con la sala "+str(i)+", y está abierta: "+str(frases_puertas[sala][i][1])+"\n\n"
                info_a_escribir += "Diálogo del Dungeon Master cuando un jugador regresa a la sala "+str(sala)+": "+str(frases_puertas[sala][i][1])+"\n\n"
            f.write(info_a_escribir)

    def escribirDialogosNPC(self,dialogos, nombreNPC):
        with open('maquina_de_estados/'+self.currentPartida+'/dialogos_NPC.txt','w',encoding='utf-8') as f:
            info_a_escribir = "Esta es la presentación que ha hecho "+nombreNPC+" de sí mismo: "+dialogos
            f.write(info_a_escribir)

    def consultar_NPC(self,contexto_estado,lastTexto):
        # model_name="bartowski/Llama-3.2-3B-Instruct-GGUF"
        # model_file = "Llama-3.2-3B-Instruct-Q4_K_M.gguf"
        # model_path = hf_hub_download(model_name, filename=model_file)
        # with suppress_stdout_stderr():
        #     llm = Llama(
        #         model_path=model_path,
        #         n_ctx=3000,  # Context length to use
        #         n_threads=32,            # Number of CPU threads to use
        #         n_gpu_layers=0,        # Number of model layers to offload to GPU
        #         seed= random.randint(1,100000)
        #     )
        # ## Generation kwargs
        # generation_kwargs = {
        #     "max_tokens":300,
        #     "stop":["</s>"],
        #     "echo":False, # Echo the prompt in the output
        #     "top_p": 0.85, #top_p y temperatura le da aleatoriedad
        #     "temperature": 0.8
        # }

        index, document_texts, embedding_model = self.crear_vectores()
        # Retrieve context
        query_context = "Teniendo en cuenta que un NPC está hablando conmigo, y ese NPC me dijo: "+lastTexto+". Luego, yo le contesté: "+contexto_estado+". ¿Qué información o diálogos sucedidos pueden ser de utilidad para fundamentar una respuesta a lo que yo le he dicho a ese NPC?"
        context = self.devolver_contexto(query_context, embedding_model, index, document_texts)
        contexto_formato = "\n".join(context)

        preamble = f"""Eres un dungeon master de DnD 5e. Debes responder únicamente como el NPC Kaelin.
        Tu respuesta debe ser parte del diálogo, hablando directamente con el jugador.

        Reglas de comportamiento:
        - Comienza cada respuesta con una descripción narrativa (ej: 'Te mira fijamente...', 'Se queda pensativo...', 'Desvía la mirada...').
        - No uses frases de apertura repetidas ni digas lo mismo que en turnos anteriores.
        - Si el jugador es repetitivo o se contradice, responde con ironía, impaciencia o sospecha.
        - Si el jugador dice algo ilegible (ej: 'asdfg'), dile en voz baja que no grite para no despertar monstruos.
        - PROHIBIDO el lenguaje meta: No expliques utilidades del diálogo ni digas 'esta información te ayudará'.
        - Reacciona al tono: si el jugador es hostil o confuso, Kaelin debe mostrar evolución emocional (firmeza, resignación, etc.)."""

        # 3. Configuración del MESSAGE (Los datos dinámicos)
        prompt_usuario = f"""
            Contexto histórico/aventura:
            {contexto_formato}

            Diálogo actual:
            - Lo último que dijo el NPC: "{lastTexto}"
            - Lo que el jugador acaba de decir: "{contexto_estado}"

            Pregunta: ¿Qué le responde el NPC al jugador exactamente ahora? Usa el contexto para dar una respuesta coherente o invéntala si es necesario, pero siempre siguiendo las reglas de personalidad.
            """

        # 4. Llamada a la API de Cohere
        try:
                res = self.co.chat(
                    model='command-a-03-2025', # Ideal para RAG y rol
                    message=prompt_usuario,
                    preamble=preamble,
                    max_tokens=300,
                    temperature=0.8,
                    p=0.85
                )

                response_good = res.text

                # 5. Limpieza y formateo
                if "." in response_good:
                    response_good = response_good.rsplit(".", 1)[0] + "."
                
                response_good = response_good.lstrip().replace("\n", " ")
                response_good = ''.join(c for c in response_good if c.isprintable())

                time.sleep(1)

                print("\n=== RESPUESTA COHERE ===")
                print(response_good)
                return response_good

        except Exception as e:
            print(f"Error en la API: {e}")
            return "Kaelin te mira confundido, parece que el destino se ha fragmentado... (Error de conexión)."