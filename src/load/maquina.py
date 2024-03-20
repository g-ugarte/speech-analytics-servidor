from sklearn.svm import SVC
import joblib
import pandas as pd

from load.vectorizadores import TfIdf

class Maquina():
    def __init__(self, ruta_export) -> None:
        try:
            self.svc: SVC = joblib.load(f'{ruta_export}/instance/modelo_productos.pkl')
            print("Clasificador cargado.")
        except Exception as e:
            print(e)

        try:
            self.vectorizer: TfIdf = TfIdf(ruta_export=ruta_export)
            print("Vectorizador TfIdf cargado")
        except Exception as e:
            print(e)

    def clasificar(self, df: pd.DataFrame):
        try:
            texto = ' '.join(df['Contenido'].to_list())
            print("Excel hecho una cadena de texto.")
        except Exception as e:
            print(e)

        try:
            tf_idf_texto = self.vectorizer.tfidf_vectorizer.transform([texto,])
            print("Vector de TfIdf obtenido")
        except Exception as e:
            print(e)
        
        try:
            pred_producto = self.svc.predict(X=tf_idf_texto)
            print("Clasificación hecha")
        except Exception as e:
            print(e)

        return pred_producto[0]
    
    def clasificar_texto(self, texto: str):
        try: 
            tf_idf_texto = self.vectorizer.tfidf_vectorizer.transform([texto,])
            print("Vector de TfIdf obtenido")
        except Exception as e:
            print(e)

        
        try:
            pred_producto = self.svc.predict(X=tf_idf_texto)
            print("Clasificación hecha")
        except Exception as e:
            print(e)

        return pred_producto[0]






