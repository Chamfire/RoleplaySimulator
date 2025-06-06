Pasos a seguir para ejecutar la plataforma de Roleplay Simulator en su dispositivo:

Requisitos previos:
- La ejecución de la plataforma se puede realizar en cualquier dispositivo windows 10 y 11 que cuente con al menos 8 GB de RAM
- Para ejecutar el script de generación de imágenes es necesario disponer de al menos 16 GB de RAM (es independiente de la plataforma)
- No se garantiza que la plataforma pueda ser ejecutada correctamente en un dispositivo con menor capacidad RAM. 


1. Instalar visual studio code: https://code.visualstudio.com/
2. Instalar el paquete c/c++ en vs code
3. Instalar el paquete de Python en vs code
4. Instalar Github desktop: https://github.com/apps/desktop?locale=es
5. Descargar e instalar la versión 3.10.10 de python: https://www.python.org/downloads/release/python-31010/

6. Comprobar que se posee la siguiente versión de pip en la cmd:  22.3.1

7. Descargar pygame en la cmd con el comando:

pip install pygame

8. Descargar CUDA: https://developer.nvidia.com/cuda-11-8-0-download-archive
(recomendada para mi versión de gráfica, que es antigua). Comprobar qué versión de CUDA es más apropiada para su tarjeta gráfica.
9. Reiniciar pc: ¡¡¡IMPORTANTE!!!

Para ver si cuda está bien instalado, introduzca el siguiente comando en la cmd:

nvcc --version

El resultado que debería obtener es el siguiente, o algo parecido:

nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2022 NVIDIA Corporation
Built on Wed_Sep_21_10:41:10_Pacific_Daylight_Time_2022
Cuda compilation tools, release 11.8, V11.8.89
Build cuda_11.8.r11.8/compiler.31833905_0


10. Descargar la librería transformers en la cmd con el comando: 

pip install Transformers 

11. Descargar la versión adecuada de torch, torchvision y torchaudio. 
Recomendable visitar la página siguiente para averiguar cuál es la más apropiada: https://pytorch.org/get-started/locally/

En mi caso, la versión empleada era esta: 

pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118



Para comprobar que PyTorch ha sido correctamente instalado, creese un script que contenga el siguiente código:

import torch
print(torch.cuda.is_available())  # Debería devolver True si CUDA está disponible
print(torch.cuda.current_device())  # Debería devolver el índice de la GPU
print(torch.cuda.get_device_name(0))  # Debería devolver el nombre de la GPU, como "NVIDIA GeForce GTX 1050"

El resultado que debería obtener es el siguiente, o algo parecido. 

True
0
NVIDIA GeForce GTX 1050



12. Descargase la librería de huggingface_hub empleando el siguiente comando en la cmd:

pip install huggingface_hub

13. Descargarse la librería de wheel empleando el siguiente comando en la cmd:

pip install wheel

14. Descargarse la librería cmake empleando el siguiente comando en la cmd:

pip install cmake

15. Descargar Build Tools para Visual Studio: (visual-cpp-tools) 
https://visualstudio.microsoft.com/es/downloads/


16. Reiniciar windows


17. Descargar git y añadirla al path: https://git-scm.com/downloads

18. Si se tienen terminales abiertos, cerrarlos todos y abrir uno nuevo


19. Instalar librería de llama-cpp-Python con el siguiente comando en la cmd: 

pip install llama-cpp-Python

20. Instalar librería del traductor con el siguiente comando en la cmd:

pip install deep_translator


21. Instalar las librerías necesarias para generar las imágenes con el modelo de IA de Pixel Art, usando estos 2 comandos en la cmd:

pip install diffusers
pip install peft


22. Instalar las librerías necesarias para hacer funcionar el RAG, usando los siguientes comandos en la cmd:

pip install faiss-cpu 
pip install langchain_community langchain-huggingface langchain 
pip install chromadb
pip install pytest

23. Instalar la librería necesaria para hacer funcionar el text-to-speech, usando este comando en la cmd:

pip install pyttsx3

24. Instalar pandas para poder ejecutar el script del análisis de los datos

pip install pandas

24. Ejecutar el archivo Main.py




-- Listado de las versiones --
Si tuviera cualquier problema durante la instalación de alguno de los paquetes indicados, las versiones actuales empleadas
para que funcione la plataforma de cada librería es la siguiente:

accelerate                               1.6.0
aiohappyeyeballs                         2.6.1
aiohttp                                  3.11.16
aiosignal                                1.3.2
annotated-types                          0.7.0
anyio                                    4.9.0
asgiref                                  3.8.1
async-timeout                            4.0.3
attrs                                    25.3.0
backoff                                  2.2.1
bcrypt                                   4.3.0
beautifulsoup4                           4.13.3
bitsandbytes                             0.45.5
build                                    1.2.2.post1
cachetools                               5.5.2
certifi                                  2025.1.31
charset-normalizer                       3.4.1
chroma-hnswlib                           0.7.6
chromadb                                 1.0.4
click                                    8.1.8
cmake                                    3.31.6
colorama                                 0.4.6
coloredlogs                              15.0.1
comtypes                                 1.4.10
dataclasses-json                         0.6.7
deep-translator                          1.11.4
Deprecated                               1.2.18
diffusers                                0.33.1
diskcache                                5.6.3
distro                                   1.9.0
durationpy                               0.9
exceptiongroup                           1.2.2
faiss-cpu                                1.10.0
fastapi                                  0.115.9
filelock                                 3.18.0
flatbuffers                              25.2.10
frozenlist                               1.5.0
fsspec                                   2025.3.0
google-auth                              2.38.0
googleapis-common-protos                 1.69.2
greenlet                                 3.1.1
grpcio                                   1.71.0
h11                                      0.14.0
httpcore                                 1.0.8
httptools                                0.6.4
httpx                                    0.28.1
httpx-sse                                0.4.0
huggingface-hub                          0.30.2
humanfriendly                            10.0
idna                                     3.10
importlib_metadata                       8.6.1
importlib_resources                      6.5.2
iniconfig                                2.1.0
Jinja2                                   3.1.6
joblib                                   1.4.2
jsonpatch                                1.33
jsonpointer                              3.0.0
jsonschema                               4.23.0
jsonschema-specifications                2024.10.1
kubernetes                               32.0.1
langchain                                0.3.23
langchain-community                      0.3.21
langchain-core                           0.3.51
langchain-huggingface                    0.1.2
langchain-text-splitters                 0.3.8
langsmith                                0.3.30
llama_cpp_python                         0.3.8
markdown-it-py                           3.0.0
MarkupSafe                               3.0.2
marshmallow                              3.26.1
mdurl                                    0.1.2
mmh3                                     5.1.0
monotonic                                1.6
mpmath                                   1.3.0
multidict                                6.4.3
mypy-extensions                          1.0.0
networkx                                 3.3
numpy                                    2.2.4
oauthlib                                 3.2.2
onnxruntime                              1.21.0
opentelemetry-api                        1.32.0
opentelemetry-exporter-otlp-proto-common 1.32.0
opentelemetry-exporter-otlp-proto-grpc   1.32.0
opentelemetry-instrumentation            0.53b0
opentelemetry-instrumentation-asgi       0.53b0
opentelemetry-instrumentation-fastapi    0.53b0
opentelemetry-proto                      1.32.0
opentelemetry-sdk                        1.32.0
opentelemetry-semantic-conventions       0.53b0
opentelemetry-util-http                  0.53b0
orjson                                   3.10.16
overrides                                7.7.0
packaging                                24.2
peft                                     0.15.2
pillow                                   11.0.0
pip                                      22.3.1
pluggy                                   1.5.0
posthog                                  3.24.1
propcache                                0.3.1
protobuf                                 5.29.4
psutil                                   7.0.0
pyasn1                                   0.6.1
pyasn1_modules                           0.4.2
pydantic                                 2.11.3
pydantic_core                            2.33.1
pydantic-settings                        2.8.1
pygame                                   2.6.1
Pygments                                 2.19.1
PyPika                                   0.48.9
pypiwin32                                223
pyproject_hooks                          1.2.0
pyreadline3                              3.5.4
pytest                                   8.3.5
python-dateutil                          2.9.0.post0
python-dotenv                            1.1.0
pyttsx3                                  2.98
pywin32                                  310
PyYAML                                   6.0.2
referencing                              0.36.2
regex                                    2024.11.6
requests                                 2.32.3
requests-oauthlib                        2.0.0
requests-toolbelt                        1.0.0
rich                                     14.0.0
rpds-py                                  0.24.0
rsa                                      4.9
safetensors                              0.5.3
scikit-learn                             1.6.1
scipy                                    1.15.2
sentence-transformers                    4.0.2
setuptools                               65.5.0
shellingham                              1.5.4
six                                      1.17.0
sniffio                                  1.3.1
soupsieve                                2.6
SQLAlchemy                               2.0.40
starlette                                0.45.3
sympy                                    1.13.1
tenacity                                 9.1.2
threadpoolctl                            3.6.0
tokenizers                               0.21.1
tomli                                    2.2.1
torch                                    2.5.1+cu121
torchaudio                               2.5.1+cu121
torchvision                              0.20.1+cu121
tqdm                                     4.67.1
transformers                             4.51.2
typer                                    0.15.2
typing_extensions                        4.12.2
typing-inspect                           0.9.0
typing-inspection                        0.4.0
urllib3                                  2.3.0
uvicorn                                  0.34.1
watchfiles                               1.0.5
websocket-client                         1.8.0
websockets                               15.0.1
wheel                                    0.45.1
wrapt                                    1.17.2
yarl                                     1.19.0
zipp                                     3.21.0
zstandard                                0.23.0


Compare las versiones que se indican aquí con las suyas empleando el siguiente comando en la cmd:

pip list



