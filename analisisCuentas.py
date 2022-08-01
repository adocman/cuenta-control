import pandas as pd
import os
import numpy as np
from openpyxl.styles import PatternFill

def color_boolean(val):
    color =''
    if val == True:
        color = 'red'
    elif val == False:
        color = 'green'
    return 'background-color: %s' % color

carpeta_objetivo = "descargas"

archivos = os.listdir(carpeta_objetivo)
archivos = sorted(archivos, key=lambda s: s.lower())

cuentas = [archivo.replace(".csv", "") for archivo in archivos]

columnas = []
columnas.append(cuentas)
df = pd.DataFrame(columns = columnas)

for cuenta in cuentas:
    datos = pd.read_csv(carpeta_objetivo + "/" + cuenta + ".csv", header = 0)
    datos = datos.sort_values(by='usuario_objetivo', key=lambda col: col.str.lower())

    siguiendo = []
    for dato in datos["following"].items():
        siguiendo.append(dato[1])
        
    df = df.append(pd.DataFrame([siguiendo], columns = columnas))

df.insert(0, 'Cuenta', cuentas)
    
df.to_csv('resultadosAnalisis/analisisCuentas.csv', index = False) 

df = pd.read_csv('resultadosAnalisis/analisisCuentas.csv', header = 0)

with pd.ExcelWriter("resultadosAnalisis/analisisCuentas.xlsx", engine="openpyxl") as writer:
    sheet_name = "Seguidos"
    # Export DataFrame content
    df.to_excel(writer, sheet_name=sheet_name)
    # Set backgrund colors depending on cell values
    sheet = writer.sheets[sheet_name]


    