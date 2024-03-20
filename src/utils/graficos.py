from matplotlib import pyplot as plt
from wordcloud import WordCloud
from json import load
import argparse

def grafico_barras_sentimientos(pos, neu, neg, carpeta, ruta_salida, caso_id = None):
    labels = ['Positivo', 'Neutral', 'Negativo']
    scores = [pos, neu, neg]

    plt.bar(labels, scores, color=['green', 'blue', 'red'])
    plt.xlabel('Sentimiento')
    plt.ylabel('Score')
    if caso_id:
        plt.title(f'Análisis de sentimientos en el caso {caso_id}')
    else: 
        plt.title(f'Análisis de sentimientos')
    plt.ylim(0, 1)  

    try:
        plt.savefig(f'{ruta_salida}/{carpeta}/sentimientos.png')  
        print("Grafico de sentimiento guardado.")
    except Exception as e:
        print(e)
    plt.clf()

def grafico_barras_espera(espera_min, espera_max, espera_prom, caso_id, carpeta, ruta_salida):
    labels = ['Mínimo', 'Promedio', 'Máximo']
    scores = [espera_min, espera_prom, espera_max]

    plt.bar(labels, scores, color=['green', 'blue', 'red'])
    plt.ylabel('Tiempo muerto (min)')
    plt.title(f'Análisis de tiempo muerto en el caso {caso_id}')
    try:
        plt.savefig(f'{ruta_salida}/{carpeta}/espera.png')  
        print("Grafico de tiempo guardado.")
    except Exception as e:
        print(e)
    plt.clf()

def grafico_barras_activo(tiempo_activo, tiempo_total, carpeta, ruta_salida):
    labels = ['Tiempo Activo', 'Tiempo Total']
    scores = [tiempo_activo / 60 , tiempo_total / 60]

    plt.bar(labels, scores, color=['blue', 'red'])
    plt.ylabel('Tiempo (min)')
    plt.title(f'Análisis de tiempo')
    try:
        plt.savefig(f'{ruta_salida}/{carpeta}/activo.png')  
        print("Gráfico de tiempo guardado.")
    except Exception as e:
        print(e)
    plt.clf()



def graficos_palabras(diccionario, carpeta,ruta_salida):
    try:
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(diccionario)
        print("Objeto de nube de palabras")
    except Exception as e:
        print(e)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    try:
        plt.savefig(f'{ruta_salida}/{carpeta}/nube.png')
        print("Nube de palabras guardada")
    except Exception as e:
        print(e)
    plt.clf()