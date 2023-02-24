import pandas as pd
def tabla(nombre):
    return pd.read_parquet(f'../bases-ganancias-2022/middle/{nombre}.parquet')