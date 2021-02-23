
import json
import ast

f = open('prodotti_deco.txt', 'r')
products = f.read().splitlines()
f.close()

list_of_diz=[]
list_errors=[]
for i in products:
    try:
        elem=ast.literal_eval(i.replace('  ', '').replace('\r', ''))

        print(elem)
        #if barcode ha un numero, aggiungi, altrimenti continue
        if elem['barcode'].startswith('80') and len(elem)==5:
            #if ingredienti=='ingredienti', .replace('ingredienti', '')
            list_of_diz.append(elem)
    except:
        print("errore-> ", elem)
        list_errors.append(elem)
        continue

import pandas as pd
df = pd.DataFrame(list_of_diz)
df.to_excel("output.xlsx", encoding='utf-8')
