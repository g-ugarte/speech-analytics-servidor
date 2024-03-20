from pydub import AudioSegment
import os
import shutil
from json import load
from glob import glob
import json

with open(os.path.join(os.getcwd(), "res/rutas.json"), 'r') as f:
    rutas_json = load(f)

def Fragmentar(ruta_audio: str, carpeta_salida: str, tiempo_fragmento: int = 300):
    audio = None
    try:
        audio = AudioSegment.from_mp3(ruta_audio)
        print("Obtener audio.")
    except Exception as e:
            print(e)

    tiempo_total = len(audio) / 1000

    numero_fragmentos = int(tiempo_total / tiempo_fragmento)

    try:
        os.makedirs(f'{rutas_json["fragmentos"]}/{carpeta_salida}', exist_ok=True)
        print("Carpeta de fragmentos de audio creada")
    except Exception as e:
        print(e)

    for i in range(numero_fragmentos + 1):
        tiempo_inicio = i * tiempo_fragmento * 1000
        tiempo_fin = min((i+1)*tiempo_fragmento*1000, len(audio))

        fragmento_audio = audio[tiempo_inicio: tiempo_fin]

        try:
            archivo_fragmento = os.path.join(f'{rutas_json["fragmentos"]}/{carpeta_salida}', f'fragmento_{i+1}.mp3')
            print(f"Framgento {i+1} creado.")
        except Exception as e:
            print(e)

        try:
            fragmento_audio.export(archivo_fragmento, format='mp3')
            print(f"Framgento {i+1} exportado.")
        except Exception as e:
            print(e)

    return glob(f'{rutas_json["fragmentos"]}/{carpeta_salida}/*.mp3')