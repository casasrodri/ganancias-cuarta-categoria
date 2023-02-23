from os.path import exists
import pandas as pd
BASE_PRORRATEOS = 'bases-ganancias-2022/prorrateos.parquet.brotli'

class Prorrateos:
    def __init__(self) -> None:
      if exists(BASE_PRORRATEOS):
        self.data = pd.read_parquet(BASE_PRORRATEOS)
      else:
        self.generar_data()

    def generar_data(self):
      self.data = pd.DataFrame(columns=['legajo', 'CCn', 'nombre', 'importe', 'mes', 'mes_pago', 'origen'])
      self._records = []

      from data import CWTR
      from parametrizacion.conceptos import ParamConceptos
      import numpy as np

      conceptos = ParamConceptos()
      cwtr_a_prorratear = CWTR[CWTR['CC-n.'].isin(conceptos.prorrateables)]

      for i, row in cwtr_a_prorratear.iterrows():
          dic = {
              'legajo':       row['Nº pers.'],
              'CCn':          row['CC-n.'],
              'nombre':       row['Texto expl.CC-nómina'],
              'importe':      row['Importe'],
              'mes':          row['Mes'],
              'mes_pago':     row['Mes'],
              'origen':       'CWTR'
          }

          # Elemento de CWTR
          self._records.append(dic)

          # Elementos prorrateados
          self.prorratear(dic)

      # Se carga en el dataframe
      self.data = pd.DataFrame.from_records(self._records)
      del self._records

      # Control integridad
      self.data['control'] = np.where(self.data['origen']=='CWTR', -1, 1) * self.data['importe']

      if round(self.data['control'].sum(), 2) != 0:
          raise ValueError('La suma del total de conceptos prorrateados, no da. Existen problemas de integridad.')

      self.data.drop('control', axis=1, inplace=True)

      # Se guarda la data en un .parquet
      self.data.to_parquet(BASE_PRORRATEOS, compression='brotli')

      return self.data

    def prorratear(self, dic):
      meses_a_prorratear = 12 - dic['mes'] + 1
      importe_prorrateado = dic['importe'] / meses_a_prorratear

      for i in range(0, meses_a_prorratear):
          self._records.append({
              'legajo':       dic['legajo'],
              'CCn':          "#" + dic['CCn'],
              'nombre':       "[Proporcional] " + dic['nombre'],
              'importe':      importe_prorrateado,
              'mes':          dic['mes'] + i,
              'mes_pago':     dic['mes'],
              'origen':       'Calculado',
          })

    def filtrar(self, legajo, mes, origen):
      df = self.data
      filtro =  df['legajo'].eq(legajo) & \
                df['mes'].eq(mes) & \
                df['origen'].str.upper().eq(origen.upper())

      out = df[filtro].reset_index()
      return out
