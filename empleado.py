# Importación y carga de la CWTR
import pandas as pd
CWTR = pd.read_parquet('./cwtr.parquet.brotli')

class Empleado:
    def __init__(self, legajo) -> None:
        self.legajo = legajo
        self.nombre = CWTR[CWTR['Nº pers.'].eq(legajo)].iloc[0].at['Apellido Nombre']
        self.mejor_sueldo = {}

class NominasCWTR:
    def __init__(self, legajo, mes) -> None:
        self.legajo = legajo
        self.mes = mes
        self.cargar_nominas()

    def __getitem__(self, key):
        return self.importes[key]

    def cargar_nominas(self):
        filtro = CWTR['Nº pers.'].eq(self.legajo) & CWTR['Mes'].eq(self.mes)
        filtrado = CWTR[filtro]
        filtrado = filtrado[['CC-n.','Importe']]

        sumarizado = filtrado.groupby('CC-n.').sum()

        self.importes = {}
        for i,row in sumarizado.iterrows():
            self.importes[i] = round(row['Importe'],2)

class LiquidacionMensualEmpleado:
    def __init__(self, empleado, mes) -> None:
        self.empleado = empleado
        self.mes = mes
        self.nominas = NominasCWTR(empleado.legajo, mes)

    def logicaLiquidacion(self):
        pass

# _______________________________________________________________
LEGAJO_PAU = 6066825
LEGAJO_LUDU = 6002385

empleado = Empleado(LEGAJO_LUDU)
liq = LiquidacionMensualEmpleado(empleado, 1)

print(empleado.legajo, empleado.nombre)
print('Mes: ', liq.mes)
print('Nómina total de haberes (/111):', liq.nominas['/111'])
print('Nominas:')
print(liq.nominas.importes)
