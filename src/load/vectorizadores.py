import joblib
import re
import string
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

def limpiar_tokenizar(texto):
    
    nuevo_texto = texto.lower()
    #
    nuevo_texto = re.sub(":\w+:", '', nuevo_texto)
    #
    nuevo_texto = re.sub('http\S+', ' ', nuevo_texto)
    regex = '[\\!\\¿\\"\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\^_\\`\\{\\|\\}\\~]'
    nuevo_texto = re.sub(regex , ' ', nuevo_texto)
    nuevo_texto = re.sub("\d+", ' ', nuevo_texto)
    nuevo_texto = re.sub(" oci ", '', nuevo_texto)
    nuevo_texto = re.sub("\\s+", ' ', nuevo_texto)
    nuevo_texto = re.sub('\[.*?¿\]', '', nuevo_texto)
    nuevo_texto = re.sub('[%s]' % re.escape(string.punctuation), '', nuevo_texto)
    nuevo_texto = re.sub('\w*\d\w*', '', nuevo_texto)
    
    nuevo_texto = nuevo_texto.split(sep = ' ')
    nuevo_texto = [token for token in nuevo_texto if len(token) > 2]

    return nuevo_texto 

class Counter():
    def __init__(self, ruta_export):
        try:
            self.count_vectorizer: CountVectorizer = joblib.load(f"{ruta_export}/instance/vector_conteo.pkl")
            print("Vectorizador de tf cargado.")
        except Exception as e:
            print(e)

class TfIdf():
    def __init__(self, ruta_export):
        try:
            self.tfidf_vectorizer: TfidfVectorizer = joblib.load(f"{ruta_export}/instance/vector_tfidf.pkl")
            print("Vectorizador de TfIdf.")
        except Exception as e:
            print(e)

