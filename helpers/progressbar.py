import sys
import math
from IPython.display import clear_output

class ProgressBar:
    vacio = '░'
    lleno = '█'

    def __init__(self, total, segmentos=50) -> None:
        self.total = total
        self.actual = 0
        self.progreso_actual = 0
        self.segmentos = segmentos
        self.unidad_segmento = total / segmentos

    def next(self):
        self.show(self.actual + 1)

    def show(self, valor):
        self.actual = valor
        completado = math.floor(valor / self.unidad_segmento)

        if completado > self.progreso_actual:
            print(completado, self.progreso_actual)
            self.progreso_actual = completado

            progreso = round(valor * 100 / self.total, 2)
            self.bar(completado, progreso)

    def bar(self, avance, progreso):

        porc_lleno = self.lleno * avance
        porc_vacio = self.vacio * (self.segmentos - avance)

        clear_output()
        print(f'|{porc_lleno}{porc_vacio}| {progreso} %')
        sys.stdout.flush()
