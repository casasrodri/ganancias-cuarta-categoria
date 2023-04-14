import sys
sys.path.append('..')

# Creación del dataframe de trabajo para las deducciones incrementales
import pandas as pd
from data import CWTR_SUM, DOTACION

# Se crea una copia del df
df = CWTR_SUM.copy()

# Se agregan valores vacíos
df_vacio = []

# crea un df vacio para que ningun legajo quede sin valor en algun mes, por defecto le va poner cero
for empleado in DOTACION['legajo'].tolist():
    for mes in range(1,13):
        df_vacio.append({
            'legajo': empleado,
            'CCn': 'VACIO',
            'mes': mes,
            'importe': 0.00
        })

df_vacio = pd.DataFrame.from_records(df_vacio)


df = pd.concat([df_vacio, CWTR_SUM])

# Se importan la parametrización de los conceptos:
from parametrizacion.conceptos import ParamConceptos
conceptos = ParamConceptos()

# Se determinan los valores individuales a sumar y restar para obtener la REMUN. BRUTA MENSUAL:
import numpy as np
df['Suma'] = np.where(df['CCn'].isin(conceptos.listar('BaseTramos', '+')), df['importe'], 0)
df['Resta'] = np.where(df['CCn'].isin(conceptos.listar('BaseTramos', '-')), df['importe'], 0)
df['BaseTramos'] = df['Suma'] - df['Resta']

# Se crea un df que contenga sumado por legajo y por mes, la REMUN. BRUTA MENSUAL:
BASES_DEDUC_INCREM = df.groupby(['legajo', 'mes'])['BaseTramos'].sum().reset_index()

# Se declaran los tramos según la normativa en cada epoca:
AFIP_DEDUC_INCREM = [
    {'epoca': 1, 'ini': 1, 'fin': 5, 'tope1': 225_937, 'tope2': 260_580,},
    {'epoca': 2, 'ini': 6, 'fin': 10, 'tope1': 280_792, 'tope2': 324_182},
    {'epoca': 3, 'ini': 11, 'fin': 12, 'tope1': 330_000, 'tope2': 431_988},
]

class DeduccionEspecial:

    @staticmethod
    def norma_aplicable(mes):
        '''
        Recibe por parametro un mes y devuelve un diccionario con información del tramo aplicable
        '''
        for norma in AFIP_DEDUC_INCREM:
            if norma['ini'] <= mes <= norma['fin']:
                return norma

    @staticmethod
    def obtener_rem_mes(legajo, mes):
        filtro =    BASES_DEDUC_INCREM['legajo'].eq(legajo) & \
                    BASES_DEDUC_INCREM['mes'].eq(mes)
        return BASES_DEDUC_INCREM[filtro].iloc[0].at['BaseTramos']
    
    @staticmethod
    def obtener_promedio_rem(legajo, mes, norma):
        filt_min = min(norma['ini'], mes)
        filt_max = min(norma['fin'], mes)

        filtro_periodos =   BASES_DEDUC_INCREM['mes'].ge(filt_min) & \
                            BASES_DEDUC_INCREM['mes'].le(filt_max)

        filtrado_fechas = BASES_DEDUC_INCREM[filtro_periodos]
        promediado = filtrado_fechas.groupby(['legajo'])['BaseTramos'].mean().reset_index()
        valor = promediado[promediado['legajo'].eq(legajo)].iloc[0].at['BaseTramos']
        return round(valor, 2)
    
    @staticmethod
    def obtener_promedio_rem_df(legajo, mes, norma, df):
        filt_min = min(norma['ini'], mes)
        filt_max = min(norma['fin'], mes)

        filtro_periodos =   df['Mes'].ge(filt_min) & \
                            df['Mes'].le(filt_max)

        filtrado_fechas = df[filtro_periodos]
        promediado = filtrado_fechas.groupby(['legajo'])['Importe'].mean().reset_index()
        valor = promediado[promediado['legajo'].eq(legajo)].iloc[0].at['Importe']
        return round(valor, 2)

    @staticmethod
    def obtener_base_para_tramos(empleado, mes, norma):
        legajo = int(empleado.legajo)

        # Se filtra la remuneración del mes:
        rem_bruta_mes = DeduccionEspecial.obtener_rem_mes(legajo, mes)

        # Se obtiene la remuneración promedio:
        rem_promedio = DeduccionEspecial.obtener_promedio_rem(legajo, mes, norma)

        # Se determina la mínima
        return min(rem_bruta_mes, rem_promedio)

    @staticmethod
    def obtener_tramo(base_tramo, mes):
        # Se determina la norma aplicable
        norma = DeduccionEspecial.norma_aplicable(mes)
    
        # Determinación tramo:
        if base_tramo <= norma['tope1']:
            tramo = 1
        elif base_tramo <= norma['tope2']:
            tramo = 2
        else:
            tramo = 3
        
        return tramo
