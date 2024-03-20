import torch
import os
import pandas as pd
import numpy as np
os.environ['CURL_CA_BUNDLE']=''
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

class Sentimientos():
    def __init__(self, ruta_export):

        self.task = "sentiment-analysis"
        try:
            self.tokenizer =  AutoTokenizer.from_pretrained(f"{ruta_export}/tokenizer-sentiment")
            print("Tokenizador cargado")
        except Exception as e:
            print(e)
        
        try:
            self.model = AutoModelForSequenceClassification.from_pretrained(f"{ruta_export}/model-sentiment")
            print("Modelo cargado")
        except Exception as e:
            print(e)

        try:
            self.pipeline = pipeline(self.task, tokenizer=self.tokenizer, model=self.model, return_all_scores=True)
            print("Flujo creado.")
        except Exception as e:
            print(e)
    
    def obtener_sentimientos(self, df):
        positivo = []
        negativo = []
        neutral = []

        for index, row in df.iterrows():
            resultado = self.pipeline(row['Contenido'])[0]
            resultado = pd.DataFrame(resultado)
            resultado.set_index('label', inplace=True)

            positivo.append(float(resultado.T.loc['score','positive']))
            negativo.append(float(resultado.T.loc['score','negative']))
            neutral.append(float(resultado.T.loc['score','neutral']))
            
        return float(np.mean(positivo)), float(np.mean(neutral)), float(np.mean(negativo))


if __name__ == '__main__':
    s = Sentimientos()
    s_df = pd.DataFrame(s.pipeline("Hola buenas tardes")[0])
    s_df.set_index('label', inplace=True)
    print(s_df.T.loc["score", 'positive'])