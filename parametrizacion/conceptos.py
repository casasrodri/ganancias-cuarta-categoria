from helpers.bases import tabla

class ParamConceptos:
    '''
    Permite obtener las parametrizaciones definidas para cada concepto.
    '''
    def __init__(self) -> None:
        self.data = tabla('conceptos')
    
        self.prorrateables = self.listar('Prorrateable','si')

        
    def listar(self, columna, valor):
        return list(map(lambda x: str(x), self.data[self.data[columna].eq(valor)]['CCn'].tolist()))
    
    def __getitem__(self, key):
        data = self.data
        return data[data['CCn'].eq(key)].to_dict('records')[0]

