import pyodbc
from datetime import datetime
import json 

with open("./res/bd.json") as f:
    CREDS_BD = json.load(f)

class Database():
    SERVER = CREDS_BD['SERVER']
    DATABASE = CREDS_BD['DATABASE']
    USERNAME = CREDS_BD['USERNAME']
    PASSWORD = CREDS_BD['PASSWORD']

    connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

    SQL_QUERY_FETCH_S1 = """
    EXEC SP_TEXT_ANALYTICS_FETCH_S1 @Ticket = ?;
    """
    SQL_QUERY_FETCH_IVR = """
    EXEC SP_TEXT_ANALYTICS_FETCH_IVR @Ticket = ?;
    """

    SQL_QUERY_INSERT_S1 = """
    EXEC SP_TEXT_ANALYTICS_UPLOAD_S1
        @caso_id = ?,
        @espera_prom = ?,
        @sentimiento_pos = ?,
        @sentimiento_neu = ?,
        @sentimiento_neg = ?,
        @mensaje_asesor = ?,
        @mensaje_cliente = ?,
        @producto_prediccion = ?,
        @espera_min = ?,
        @espera_max = ?,
        @grupo = ?,
        @asesor = ?,
        @fecha_analisis = ?;
    """
    SQL_QUERY_INSERT_IVR = """
    EXECUTE SP_TEXT_ANALYTICS_UPLOAD_IVR
        @caso_id = ?,
        @tiempo_activo = ?,
        @tiempo_total = ?,
        @sentimiento_pos = ?,
        @sentimiento_neu = ?,
        @sentimiento_neg = ?,
        @mensaje_tokenizado = ?,
        @producto_prediccion = ?,
        @grupo = ?,
        @asesor = ?,
        @fecha_analisis = ?;
    """

    def obtener_producto_asesor_grupo_IVR(self, caso_id):
        conn = pyodbc.connect(self.connectionString)
        cursor = conn.cursor()
        cursor.execute(self.SQL_QUERY_FETCH_IVR, str(caso_id))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def obtener_producto_asesor_grupo_S1(self, caso_id):
        conn = pyodbc.connect(self.connectionString)
        cursor = conn.cursor()
        cursor.execute(self.SQL_QUERY_FETCH_S1, int(caso_id))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    
    def subir_datos_S1(self, caso_id, espera_min, espera_prom, espera_max, sentimiento_pos, sentimiento_neu, sentimiento_neg, mensaje_asesor, mensaje_cliente, producto_prediccion, grupo, asesor):
        conn = pyodbc.connect(self.connectionString)
        cursor = conn.cursor()
        cursor.execute(self.SQL_QUERY_INSERT_S1, caso_id, espera_prom, sentimiento_pos, sentimiento_neu, sentimiento_neg, mensaje_asesor, mensaje_cliente, producto_prediccion, espera_min, espera_max, grupo, asesor, datetime.now())
        conn.commit()
        cursor.close()
        conn.close()
    
    def subir_datos_IVR(self, caso_id, tiempo_activo, tiempo_total, sentimiento_pos, sentimiento_neu, sentimiento_neg, mensaje_tokenizado, producto_prediccion, grupo, asesor):
        conn = pyodbc.connect(self.connectionString)
        cursor = conn.cursor()
        cursor.execute(self.SQL_QUERY_INSERT_IVR, caso_id,  tiempo_activo, tiempo_total, sentimiento_pos, sentimiento_neu, sentimiento_neg, mensaje_tokenizado, producto_prediccion, grupo, asesor, datetime.now())
        conn.commit()
        cursor.close()
        conn.close()