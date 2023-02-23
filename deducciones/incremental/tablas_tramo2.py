import pandas as pd

class TablasTramo2:
    def __init__(self) -> None:
        self.data = pd.read_excel('./bases-ganancias-2022/tablas_afip.xlsx')

    def deduccion(self, mes, sueldo):
        df = self.data
        filtro_mes = df['ini'].le(mes) & df['fin'].ge(mes)
        filtro_rem = df['sueldo'].ge(sueldo)
        primer_row = df[filtro_mes & filtro_rem].head(1)
        if len(primer_row) == 0:
            raise ValueError(f'No es posible obtener una deducción en la tabla para el importe {sueldo} en el mes {mes}.')
        else:
            return primer_row.iloc[0].at['deduccion']

# tabla_tramo2 = TablasTramo2()
# tabla_tramo2.deduccion(5, 226_539.00)