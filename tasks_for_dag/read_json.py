#in questo file calcoliamo la differenza tra quelle che ho messo nel json di claudio e le mie
import yaml

a_file = open("da passare a Claudio1.json", "r")
all_lines_of_file = a_file.read()
all_lines_of_file=all_lines_of_file.replace('[[','[').replace(']]','')
all_lines_of_file=all_lines_of_file.split('}')
errors=''
list_of_diz=[]
for idx, i in enumerate(all_lines_of_file):
    if i=='':
        continue
    if i[:2]=='[[':
        i=i.replace('[[', '')
        i+=']'
        i='['+i
        x = yaml.load(i)
        if len(x) > 1:
            list_of_diz.append(x)
        else:
            continue
    if i[:2]=='[{':
        i=i.replace('[','')
        i+='}'
        x = yaml.load(i)
        if len(x) > 1:
            list_of_diz.append(x)
        else:
            continue

    else:
        try:
            lista_i=i.split('}')
            for acca in lista_i:
                if '[' in acca or ']' in acca:
                    acca=acca.replace('[','').replace(']','')
                acca=acca+'}'
                if acca.startswith(', {'):
                    acca=acca.replace(', {', '{')

                x = yaml.load(acca)
                if len(x) > 1:
                    list_of_diz.append(x)
                else:
                    continue
        except:
            errors+=i
            f = open("errors.txt", "a")
            f.write(i)
            f.close()
            continue

print(len(list_of_diz))

import pandas as pd
df = pd.DataFrame(list_of_diz)

df.to_csv("dati_15_febbrario.csv", sep=';', encoding='utf-8')