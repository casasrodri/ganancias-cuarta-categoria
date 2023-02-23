import pandas as pd

CWTR = pd.read_parquet('./bases-ganancias-2022/cwtr.parquet.brotli')
CWTR_SUM = CWTR.groupby(['Nº pers.','CC-n.','Mes'])['Importe'].sum().reset_index().rename(columns={"Nº pers.": "legajo", "CC-n.": "CCn", "Mes": "mes", "Importe": "importe"})
EMPLEADOS = CWTR_SUM['legajo'].unique().tolist()

