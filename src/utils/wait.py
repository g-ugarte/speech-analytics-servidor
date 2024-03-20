from datetime import datetime
import pandas as pd
import numpy as np


def obtener_tiempos(df):
    prev_row = None
    tiempos = []
    for index, row in df.iterrows():
        if type(prev_row) != pd.Series:
            prev_row = row
        elif "asesor" == row.Usuario and prev_row.Usuario=='cliente':
            tiempos.append({'cliente': prev_row.Fecha, 'asesor': row.Fecha})
        prev_row = row

    df_tiempos = pd.DataFrame(tiempos)
    df_tiempos['cliente_seg'] = df_tiempos['cliente'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').timestamp()) 
    df_tiempos['asesor_seg'] = df_tiempos['asesor'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').timestamp()) 
    df_tiempos['espera'] = ((df_tiempos['asesor_seg'] - df_tiempos['cliente_seg'])/60).round().astype(int)

    return int(np.min(df_tiempos['espera'])), int(np.max(df_tiempos['espera'])), int(round(np.mean(df_tiempos['espera'])))

def tiempo_muerto(dfs: list[pd.DataFrame]):

    tiempo_total = 0
    tiempo_activo = 0

    for df in dfs:
        df['tiempo_inicio'] = df['timestamp'].apply(lambda x: x[0] if x[0] != None else x[1])
        df['tiempo_fin'] = df['timestamp'].apply(lambda x: x[1] if x[1] != None else x[0])

        tiempo_final = np.max(df['tiempo_fin'].to_numpy())
        tiempo_inicio = np.min(df['tiempo_inicio'].to_numpy())

        tiempo_total += tiempo_final - tiempo_inicio
        tiempo_activo += np.sum(df['tiempo_fin'] - df['tiempo_inicio'])

    return tiempo_activo, tiempo_total