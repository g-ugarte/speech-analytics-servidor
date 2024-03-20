from load.vectorizadores import Counter
import pandas as pd

class Texto_Clave():
    def __init__(self, ruta_export):
        try:
            self.counter: Counter = Counter(ruta_export=ruta_export)
            print("Obtener vectorizador Tf.")
        except Exception as e:
            print(e)

        try:
            self.analyzer = self.counter.count_vectorizer.build_analyzer()
            print("Función tokenizadora obtenida.")
        except Exception as e:
            print(e)

    def obtener_texto(self, texto: str):
        return ' '.join(self.analyzer(texto))

    def obtener_textos(self, df: pd.DataFrame):
        try:
            grupos = df.groupby(by='Usuario')['Contenido'].apply(lambda x:  ' '.join(self.analyzer(' '.join(x))))
            print("Mensajes de asosr & cliente tokenizados.")
        except Exception as e:
            print(e)
        return grupos.loc['asesor'], grupos.loc['cliente']
    
    def frecuencias(self, df: pd.DataFrame):
        try:
            mensajes = ' '.join(df['Contenido'].to_list())
            print("Cadena con toda la conversación.")
        except Exception as e:
            print(e)

        try:
            matriz = self.counter.count_vectorizer.transform([mensajes, ])
            print("Matriz de frecuencias generada")
        except Exception as e:
            print(e)

        try:
            palabras = self.counter.count_vectorizer.get_feature_names_out()
            print("Términos.")
        except Exception as e:
            print(e)
        
        try:
            frecs = {palabras[c]: matriz[0, c] for c in range(matriz.shape[1])}
            print("Diccionario de frecuencias generado.")
        except Exception as e:
            print(e)
            
        return frecs
    
if __name__ == "__main__":

    df = pd.DataFrame({
        'Usuario': ['cliente', 'cliente', 'asesor', 'asesor', 'cliente'],
        'Contenido': ['Buenos días', ' Gracias por llamar a Interbank', "Ayudanos a mejorar", "Hablame sobre la cuenta negocios", "gracias"]
    })

    tc = Texto_Clave()
    print(tc.obtener_textos(df))
