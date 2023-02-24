import pandas as pd
def tabla(nombre):
    return pd.read_parquet(ruta_tabla(nombre))

from os.path import exists
def existe_tabla(nombre):
    return exists(ruta_tabla(nombre))

def ruta_tabla(nombre):
    return f'../bases-ganancias-2022/middle/{nombre.lower()}.parquet'