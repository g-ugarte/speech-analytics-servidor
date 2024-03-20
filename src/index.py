import os
import json


with open(os.path.join(os.getcwd(), "res/rutas.json"), "r") as f:
    rutas = json.load(f)

# Habilitar la ruta de ffmpeg para las librerías que analicen archivos MP3
current_path = os.environ.get('PATH', '')
directory_to_add = f'{rutas["export"]}/ffmpeg'
new_path = current_path + os.pathsep + directory_to_add
os.environ['PATH'] = new_path

import re
from glob import glob
from time import sleep
import pandas as pd
import numpy as np
from utils.wait import obtener_tiempos, tiempo_muerto
from load.sentimientos import Sentimientos
from load.maquina import Maquina
from utils.texto_clave import Texto_Clave
from load.vectorizadores import limpiar_tokenizar
from utils.graficos import *
from utils.fragmentar import Fragmentar
from load.transcripcion import Transcripcion
import shutil
import json
import os
from tqdm import tqdm
from download.chat import Descargar_Reportes, PATRONES_REPORTES
from download.call import Descargar_Llamada
from utils.database import Database
import argparse


for v in rutas.values():
    os.makedirs(v, exist_ok=True)

SENT = Sentimientos(ruta_export=rutas['export'])
TC = Texto_Clave(ruta_export=rutas['export'])
MAQ = Maquina(ruta_export=rutas['export'])
TRANS = Transcripcion(ruta_export=rutas['export'])
DB = Database()

def obtener_caso_id(df: pd.DataFrame):
    return np.unique(df.index.levels[0])

def funcion_excel(ruta):
    # Filtra, Limpia y Agrupa conversaciones por cada Ticket
    try:
        df = pd.read_excel(ruta)
        df['Usuario'] = df['Usuario'].fillna('cliente')
        df = df[df['Grupo'] != 'Bot Anfitrion']
        df = df[df['Usuario'].str.startswith('bot.').fillna(False) == False]
        df['Caso ID'] = df['Caso ID'].astype(str)
        df = df[df['Usuario'].str.startswith('S1').fillna(False) == False]
        df = df.groupby(by='Caso ID').apply(lambda x: x)
        filter_single_word = lambda r: len(str(r['Contenido']).split()) > 1
        df = df[~df['Contenido'].astype(str).str.isnumeric()]
        df = df.dropna(subset=['Caso ID'])
        df["Usuario"][df["Usuario"] != 'cliente'] = 'asesor'
        df = df[df.apply(filter_single_word, axis=1)]    
        df = df.reset_index(drop=True)
        df = df.groupby(by='Caso ID', group_keys=True).apply(lambda x: x)
        print("DataFrame reajustado por id de los tickets.")
    except Exception as e:
        print(e)

    try:
        for caso_id in df['Caso ID'].unique():
            for index, row in df.loc[caso_id,:].iterrows():
                if 'cliente' == row['Usuario']:
                    df = df.drop(index=(caso_id, index))
                else:
                    break
        print("Obtener mensajes de cliente")
    except Exception as e:
        print(e)

    casos_ids = obtener_caso_id(df)

    # Iterar por los tickets
    for caso_id in tqdm(casos_ids):
        try:
            # Obtener el producto, asesor y grupo registrado en la base de datos
            producto, asesor, grupo = DB.obtener_producto_asesor_grupo_S1(caso_id)
            # Obtener los tiempos de espera del cliente
            espera_min, espera_max, espera_prom = obtener_tiempos(df.loc[caso_id])
            # Obtener las métricas de sentimientos
            pos, neu, neg = SENT.obtener_sentimientos(df.loc[caso_id])
            # Obtener la predicción del producto
            pred_producto = MAQ.clasificar(df.loc[caso_id])
            # Limpiar y tokenizar el texto de la conversación
            texto_asesor, texto_cliente = TC.obtener_textos(df.loc[caso_id])
            # Obtener las frecuencias de cada token
            frecuencias_diccionario = TC.frecuencias(df.loc[caso_id])
            
            # Nombre de la carpeta donde se almacenarán los resultados
            carpeta = caso_id

            #Si se activo la bandera de producción, se suben los resultados a la base de datos
            DB.subir_datos_S1(
                caso_id, espera_min, espera_prom, espera_max, pos, neu, neg,
                texto_asesor, texto_cliente, pred_producto, grupo,
                asesor
            )

            # Crear la carpeta con los resultados
            try:
                os.makedirs(f"{rutas['salida']}/{carpeta}", exist_ok=True)
            except Exception as e1:
                print(e1)

            df.loc[caso_id][['Contenido', 'Usuario', 'Fecha']].to_excel(f"{rutas['salida']}/{carpeta}/conversacion.xlsx", index=False)

            # Exportar gráficos de cada análisis
            grafico_barras_sentimientos(pos, neu, neg, carpeta, rutas['salida'], caso_id)
            grafico_barras_espera(espera_min, espera_max, espera_prom, caso_id, carpeta, rutas['salida'])
            graficos_palabras(frecuencias_diccionario, carpeta, rutas['salida'])

        except Exception as e:
            print(e)


def funcion_audio(ruta):

    # Nombre de la carpeta con análisis
    carpeta = os.path.splitext(os.path.basename(ruta))[0]
    # Extraer el ID del ticket en el nombre del archivo
    uuid_pattern = re.compile(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$')
    uuid_match = uuid_pattern.search(carpeta)
    caso_id = None
    if uuid_match:
        caso_id = uuid_match.group(1)
    else:
        raise Exception("Archivo de llamada debe tener el uuid")
    
    # Obtener parámetros adicionales de la base de datos
    producto, asesor, grupo = DB.obtener_producto_asesor_grupo_IVR(caso_id)

    # Fragmentoar los audios en audios más pequeños para su análisis
    rutas_fragmentos = Fragmentar(ruta, carpeta, 120)

    print(rutas_fragmentos)

    texto = []
    bloques = []

    # Transcribir cada fragmento de audio
    for ruta_f in rutas_fragmentos:
        print(ruta_f)
        t_frag = TRANS.transcribir(ruta_f)
        texto.append(t_frag['text'])
        bloque = pd.DataFrame(t_frag['chunks'])
        bloques.append(bloque)
    texto = ' '.join(texto)
    tiempo_activo, tiempo_total = tiempo_muerto(bloques)
    bloques = pd.concat(bloques)
    bloques = bloques.rename(columns={'text':'Contenido'})


    pos, neu, neg = SENT.obtener_sentimientos(bloques)
                                              
    texto_tokenizado = TC.obtener_texto(texto)
    frecuencias_diccionario = TC.frecuencias(bloques)

    pred_producto = MAQ.clasificar_texto(texto)

    DB.subir_datos_IVR(caso_id, tiempo_activo, tiempo_total, pos, neu, neg, texto_tokenizado, pred_producto, grupo, asesor)
    print("Subido a BD IVR")

    try:
        os.makedirs(f"{rutas['salida']}/{carpeta}", exist_ok=True)
        with open(f"{rutas['salida']}/{carpeta}/transcripcion.txt", 'w', encoding='utf-8') as f:
            f.write(texto)
        print("Carpeta de salida creada")
    except Exception as e:
        print(e)
    
    try:
        graficos_palabras(frecuencias_diccionario, carpeta, rutas['salida'])
        grafico_barras_sentimientos(pos, neu, neg, carpeta, rutas['salida'])
        grafico_barras_activo(tiempo_activo, tiempo_total, carpeta, rutas['salida'])
        print("Gráficos creados")
    except Exception as e:
        print(e)

    shutil.rmtree(f"{rutas['fragmentos']}")

parser = argparse.ArgumentParser()
parser.add_argument('-x', '--excel', action='store_true', help="Descarga y Análisis de Conversaciones en Excel")
parser.add_argument("-m", '--mp3', type=str, help="Descarga y Análisis de Conversación en MP3 (proveer id)")
parser.add_argument('-c', '--ruta_excel', type=str, help="Análisis de Conversaciones en Excel")
parser.add_argument("-l", '--ruta_llamada', type=str, help="Análisis de Conversación en MP3")

args = parser.parse_args()

print(args.excel)
print(args.mp3)
print(args.ruta_excel)
print(args.ruta_llamada)

if args.excel:
    print("Descargar y analizar mensajes del día anterior")
    obj = Descargar_Reportes()
    obj.descargar(PATRONES_REPORTES['Detalle de Mensajes'])
    ruta_excel = obj.validar()
    funcion_excel(ruta_excel)

    if os.path.exists(ruta_excel):
        os.remove(ruta_excel)

elif args.mp3:
    print("Descargar y analizar llamada")
    obj = Descargar_Llamada()
    obj.descargar(args.mp3)
    ruta_audio = obj.validar(args.mp3)
    funcion_audio(ruta_audio)

    if os.path.exists(ruta_audio):
        os.remove(ruta_audio)

elif args.ruta_excel:
    if not os.path.isfile(args.ruta_excel):
        raise Exception("No es una ruta de archivo excel")
    print("Analizar mensajes")
    funcion_excel(args.ruta_excel)
elif args.ruta_llamada:
    if not os.path.isfile(args.ruta_llamada):
        raise Exception("No es una ruta de archivo excel")
    print("Analizar llamada")
    funcion_audio(args.ruta_llamada)

