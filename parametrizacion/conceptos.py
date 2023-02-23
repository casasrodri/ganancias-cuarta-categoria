import pandas as pd

PARAM_CONCEPTOS = './bases-ganancias-2022/conceptos.xlsx'

class ParamConceptos:
    def __init__(self) -> None:
        self.data = pd.read_excel(PARAM_CONCEPTOS)
    
        self.prorrateables = self.listar('Prorrateable','si')

        
    def listar(self, columna, valor):
        return list(map(lambda x: str(x), self.data[self.data[columna].eq(valor)]['CCn'].tolist()))

