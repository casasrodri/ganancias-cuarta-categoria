from helpers.bases import tabla

CWTR = tabla('cwtr')
CWTR_SUM = CWTR.groupby(['Nº pers.','CC-n.','Mes'])['Importe'].sum().reset_index().rename(columns={"Nº pers.": "legajo", "CC-n.": "CCn", "Mes": "mes", "Importe": "importe"})
DOTACION = tabla('dotacion')

