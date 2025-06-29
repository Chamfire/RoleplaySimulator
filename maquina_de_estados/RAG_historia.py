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

class RAG_historia:
    def __init__(self,currentPartida):
        self.currentPartida = currentPartida
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
        model_name="bartowski/Llama-3.2-3B-Instruct-GGUF"
        model_file = "Llama-3.2-3B-Instruct-Q4_K_M.gguf"
        model_path = hf_hub_download(model_name, filename=model_file)
        with suppress_stdout_stderr():
            llm = Llama(
                model_path=model_path,
                n_ctx=3000,  # Context length to use
                n_threads=32,            # Number of CPU threads to use
                n_gpu_layers=0,        # Number of model layers to offload to GPU
                seed= random.randint(1,100000)
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
        query_context = "Teniendo en cuenta que un NPC está hablando conmigo, y ese NPC me dijo: "+lastTexto+". Luego, yo le contesté: "+contexto_estado+". ¿Qué información o diálogos sucedidos pueden ser de utilidad para fundamentar una respuesta a lo que yo le he dicho a ese NPC?"
        context = self.devolver_contexto(query_context, embedding_model, index, document_texts)
        contexto_formato = "\n".join(context)

        pregunta = "Acabo de decirle esto al NPC: "+contexto_estado+". Teniendo en cuenta que un NPC estaba hablando conmigo, y lo último que me dijo el NPC fue esto: "+lastTexto+".Pregunta: ¿Qué me responde el NPC a lo que yo acabo de decir? Emplea información del contexto siguiente dado para elaborar una respuesta, o inventante una respuesta que podría dar el NPC si el contexto no fuera suficiente."
        query = f"""
                Eres un dungeon master de DnD 5e y debes responder únicamente como el NPC, usando solo el contexto proporcionado. Tu respuesta debe ser parte del diálogo, como si estuvieras hablando directamente con el jugador.

                **Reglas importantes**:
                - Comienza cada respuesta con frases como: 'Así, ves que te mira fijamente y te dice...', 'Tras decir eso, ves que se queda pensativo, y empieza a decir...', 'Kaelin desvía la mirada por un instante antes de decir...', etc.
                - No puedes usar frases de apertura que ya se hayan dicho antes, ni repetir ninguna parte del diálogo anterior.
                - Si el jugador repite una pregunta o contradice lo que dijo antes, responde con ironía, impaciencia, sospecha o desconfianza, pero **sin decir lo mismo que antes**.
                - Si el jugador dice algo ilegible (como 'asdasdf'), respóndele en voz baja diciendo que no eleve la voz, porque podría despertar a algún monstruo.
                - Nunca expliques cosas fuera del personaje. No des descripciones meta como: 'Este diálogo te será útil' o 'Esta información podría ayudarte...'
                - Reacciona emocionalmente al tono del jugador: si se muestra hostil, sospechoso, insistente o confuso, haz que Kaelin actúe en consecuencia y muestre una evolución emocional (más firmeza, más sospecha, más resignación, etc.)

                {pregunta}

                Contexto adicional para responder:
                {contexto_formato}

                <|eot_id|><|start_header_id|>user<|end_header_id|>
                Pregunta: {pregunta}
                <|eot_id|><|start_header_id|>assistant<|end_header_id|>
                """
        res = llm(query, **generation_kwargs) # Res is a dictionary
        ## Unpack and the generated text from the LLM response dictionary and print it
        response_good = res["choices"][0]["text"]
        if "." in response_good:
            response_good = response_good.rsplit(".", 1)[0] + "."  # Para devolver un párrafo completo
        response_good = response_good.lstrip()
        response_good.replace("\\n", " ")
        response_good = ''.join(c for c in response_good if c.isprintable())
        print("\n=== RESPUESTA ===")
        print(response_good)
        print("\n=== CONTEXTO ===")
        print(query)
        return response_good