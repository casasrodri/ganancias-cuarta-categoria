import pandas as pd
def tabla(nombre):
    return pd.read_parquet(f'../bases-ganancias-2022/middle/{nombre}.parquet')

from os.path import exists
def existe_tabla(nombre):
    return exists(f'../bases-ganancias-2022/middle/{nombre}.parquet')