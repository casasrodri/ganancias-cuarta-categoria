# Importación y carga de la CWTR
from data import CWTR, CWTR_SUM, DOTACION

class Empleado:
    def __init__(self, legajo) -> None:
        self.legajo = legajo
        self.nombre = DOTACION[DOTACION['legajo'].eq(legajo)].iloc[0].at['nombre']
        # self.mejor_sueldo = {}
    
    def __str__(self) -> str:
        return f"< {type(self).__name__} - {self.legajo} - {self.nombre} >"

class NominasCWTR:
    def __init__(self, legajo, mes) -> None:
        self.legajo = legajo
        self.mes = mes
        self.cargar_nominas()

    def __getitem__(self, key):
        return self.importes.get(key, 0)

    def cargar_nominas(self):
        filtro = CWTR_SUM['legajo'].eq(self.legajo) & CWTR['mes'].eq(self.mes)
        filtrado = CWTR_SUM[filtro]
        filtrado = filtrado[['CCn','importe']]

        sumarizado = filtrado.groupby('CCn').sum()

        self.importes = {}
        for i,row in sumarizado.iterrows():
            self.importes[i] = round(row['importe'],2)

class LiquidacionMensualEmpleado:
    def __init__(self, empleado, mes) -> None:
        self.empleado = empleado
        self.mes = mes
        self.nominas = NominasCWTR(empleado.legajo, mes)

    def logicaLiquidacion(self):

        # Paso 1: Determinación de Ganancia Imponible
        self.gananciaImponible = 0

        # Paso 1.1: Base bruta
        self.gananciaImponible += self.determinacionBaseBruta()

        # Paso 1.2: Conceptos Exentos
        self.gananciaImponible -= self.determinacionConceptosExentos()

    def determinacionBaseBruta(self):
        self.baseBruta = 0
        self.baseBruta += self.nominas['/111'] # Total Haberes con aportes
        self.baseBruta += self.nominas['/124'] # Haberes no remun.SIJP

        return self.baseBruta

    def determinacionConceptosExentos(self):
        self.conceptosExentos = 0
        self.conceptosExentos += self.nominas['409A'] # Reintegro gastos HO
        self.conceptosExentos += self.nominas['/146'] # Rem. Hora Ext. Exenta
        self.conceptosExentos += self.nominas['1239'] # Enfermedad Profesional
        self.conceptosExentos += self.nominas['1235'] # Accidente-Primeros 10d
        self.conceptosExentos += self.nominas['1236'] # Accidente - Mas 10d
        self.conceptosExentos += self.nominas['1237'] # Accid. In Itiner-Prim.1
        self.conceptosExentos += self.nominas['1238'] # Accid. In Itiner-Mas 10
        self.conceptosExentos += self.nominas['1262'] # Lic.por enf.COVID19

        return self.conceptosExentos


# _______________________________________________________________
# LEGAJO_PAU = 6066825
# LEGAJO_LUDU = 6002385

# empleado = Empleado(LEGAJO_PAU)
# liq = LiquidacionMensualEmpleado(empleado, 1)

# print(empleado.legajo, empleado.nombre)
# print('Mes: ', liq.mes)
# print('Nómina total de haberes (/111):', liq.nominas['/111'])
# print('Nominas:')
# print(liq.nominas.importes)

# liq.logicaLiquidacion()
# print(liq.baseBruta)
# print(liq.conceptosExentos)
# print(liq.gananciaImponible)


# import paramconceptos as pc

# conceptos = pc.ParamConceptos()

# print(conceptos.prorrateables)