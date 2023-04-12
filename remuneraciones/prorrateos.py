from helpers.bases import *
import pandas as pd

class Prorrateos:
    def __init__(self) -> None:
      if existe_tabla('prorrateos'):
        self.data = tabla('prorrateos')
      else:
        self.generar_data()

    def generar_data(self):
      self._records = []

      from data import CWTR_SUM
      from parametrizacion.conceptos import ParamConceptos
      import numpy as np

      conceptos = ParamConceptos()
      cwtr_a_prorratear = CWTR_SUM[CWTR_SUM['CCn'].isin(conceptos.prorrateables)]

      for i, row in cwtr_a_prorratear.iterrows():
          ccn = row['CCn']
          dic = {
              'legajo':       row['legajo'],
              'CCn':          row['CCn'],
              'nombre':       conceptos[ccn]['descripcion'],
              'importe':      row['importe'],
              'mes':          row['mes'],
              'mes_pago':     row['mes'],
              'origen':       conceptos[ccn]['origen'],
          }

          # Elemento de CWTR
          self._records.append(dic)

          # Elementos prorrateados
          self.prorratear(dic)

      # Se carga en el dataframe
      self.data = pd.DataFrame.from_records(self._records)
      del self._records

      # Control integridad
      self.data['control'] = np.where(self.data['origen']=='cwtr', -1, 1) * self.data['importe']

      if round(self.data['control'].sum(), 2) != 0:
          raise ValueError('La suma del total de conceptos prorrateados, no da. Existen problemas de integridad.')

      self.data.drop('control', axis=1, inplace=True)

      # Se guarda la data en un .parquet
      self.data.to_parquet(ruta_tabla('prorrateos'), compression='brotli')

      # return self.data

    def prorratear(self, dic):
      meses_a_prorratear = 12 - dic['mes'] + 1 #12 menos el mes en el que estoy + 1 (11 para el bav por ejemplo)
      importe_prorrateado = dic['importe'] / meses_a_prorratear # defino el importe que voy a prorratear por mes

      for i in range(0, meses_a_prorratear):
          self._records.append({
              'legajo':       dic['legajo'],
              'CCn':          "#" + dic['CCn'],
              'nombre':       "[Proporcional] " + dic['nombre'],
              'importe':      importe_prorrateado,
              'mes':          dic['mes'] + i,
              'mes_pago':     dic['mes'],
              'origen':       'fx',
          })

    def filtrar(self, legajo, mes, origen):
      df = self.data
      filtro =  df['legajo'].eq(legajo) & \
                df['mes'].eq(mes) & \
                df['origen'].str.upper().eq(origen.upper())

      out = df[filtro].reset_index()
      return out

    def prorrateados(self):
      df = self.data
      filtro = df['origen'].eq("fx")  
                    
      out = df[filtro].reset_index()
      return out