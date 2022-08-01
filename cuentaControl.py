from tkinter.ttk import Progressbar
from tokenize import String
import tweepy
import configparser
import pandas as pd
import json
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading

def abrir_archivo():
    global ruta_archivo 
    ruta_archivo = filedialog.askopenfilename(
                                            parent = root,
                                            title = "Seleccionar archivo",
                                            filetypes = (("Archivos csv", "*.csv"),
                                                ("Todos los archivos","*.*"))    
                                            )
    if ruta_archivo:
        archivo = open(ruta_archivo, 'r')
        contenido = archivo.read()
        text_box = tk.Text(root, height = 10, width = 48, padx = 10, pady = 10)
        text_box.insert(1.0, contenido)
        text_box.grid(column = 1, row = 4)
        text_box.configure(state='disabled')

def consultar_usuario(username, lista_usuarios):
    usuario = api.get_user(screen_name = username)

    columnas = ["screen_name", "following", "followed_by", "usuario_objetivo"]
    df = pd.DataFrame(columns = columnas)

    for usuario_objetivo in lista_usuarios:
        str = " "
        str_usuario_objetivo = str.join(usuario_objetivo)
        nexos = api.get_friendship(source_screen_name = username, target_screen_name = str_usuario_objetivo)
        json_usuario_1 = json.loads(json.dumps(nexos[0]._json, indent=2))

        # Le pasamos los valores
        for key, value in json_usuario_1.items():
            if key == columnas[0]:
                screen_name = value
            if key == columnas[1]:
                following = value
            if key == columnas[2]:
                followed_by = value
                lista = [screen_name, following, followed_by, str_usuario_objetivo]
                df = df.append(pd.DataFrame([lista], columns = columnas))
    
    df.to_csv('descargas/' + usuario.screen_name + '.csv', index = False) 

def ejecutar_consulta():
    txt_consulta.set("Descargando...")
    # Cargamos los usuarios que deseamos consultar
    df_usuarios = pd.read_csv(ruta_archivo)
    lista_usuarios = df_usuarios.values.tolist()

    # Obtenemos el largo de la lista de usuarios de twitter para la barra de tareas:
    tareas = len(lista_usuarios)
    progreso = 0
    tarea_actual = 1

    # Consultamos
    for username in lista_usuarios:
        # Ejecutamos la consulta
        str = " "
        consultar_usuario(str.join(username), lista_usuarios)

        # Actualizamos la barra de tareas
        barra_progreso['value'] += (tarea_actual/tareas)*100
        progreso += tarea_actual

        root.update_idletasks()

    txt_consulta.set("Ejecutar")
    tk.messagebox.showinfo("", "Consulta finalizada")
    

def descargar():
    t = threading.Thread(target=ejecutar_consulta).start()


# Obtenemos la configuración del archivo
config = configparser.ConfigParser()
config.read('config.ini')

# Nos conectamos con la API
api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

# Interfaz gráfica
root = tk.Tk()
root.title("Cuenta Control")
root.resizable(False, False)

# Ventana
canvas = tk.Canvas(root, bg = "#ded1b1",width = 720, height = 540)
canvas.grid(columnspan = 3, rowspan = 8)

# Logo
logo = Image.open('componentes_ui/logo_ucen_color.png')
logo = logo.resize((100,100), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image = logo)
logo_label.image = logo
logo_label.grid(columnspan = 1, column = 1, row = 0)

# Instrucciones
instrucciones = tk.Label(root, text = "Seleccione un archivo csv con las cuentas que desee consultar", font = "Montserrat", bg = "#ded1b1", fg = "#1c2632")
instrucciones.grid(columnspan = 1, column = 1, row = 1)

# Boton buscar archivo
btn_archivo = tk.Button(root, text = "Seleccionar archivo", font = "Montserrat", bg = "#1c2632", fg = "white", height = 2, width = 15, command = abrir_archivo)
btn_archivo.grid(columnspan = 1, column = 1, row = 2)

# Boton ejecutar programa
txt_consulta = tk.StringVar()
btn_consulta = tk.Button(root, textvariable = txt_consulta, font = "Montserrat", bg = "#1c2632", fg = "white", height = 2, width = 15, command = descargar)
txt_consulta.set("Ejecutar")
btn_consulta.grid(columnspan = 1, column = 1, row = 3)

# Barra de descarga
barra_progreso = Progressbar(root, orient = HORIZONTAL, length = 300)
barra_progreso.grid(columnspan = 1, column = 1, row = 5)

# Label Universidad
lbl_universidad = tk.Label(root, text = "Universidad Central de Chile", font = "Montserrat", bg = "#ded1b1", fg = "#1c2632")
lbl_universidad.grid(columnspan = 1, column = 1, row = 6)

# Label Departamento
lbl_departamento = tk.Label(root, text = "Observatorio de Política y Redes Sociales", font = "Montserrat", bg = "#ded1b1", fg = "#1c2632")
lbl_departamento.grid(columnspan = 1, column = 1, row = 7)

root.mainloop()