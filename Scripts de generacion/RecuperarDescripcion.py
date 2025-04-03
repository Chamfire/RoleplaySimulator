import os 
import json

config_dir = 'descripciones'
config_file = 'NPCs.json'
with open(config_dir+'/'+config_file,encoding='utf8') as f:
    data = json.load(f)

for elem,i in data.items():
    print(elem)
    print("------------------------------------------------------------------------------")
    print(i[0]+"\n")