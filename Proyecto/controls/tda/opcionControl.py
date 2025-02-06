from controls.dao.daoAdapter import DaoAdapter
from models.opcion import Opcion

class OpcionControl(DaoAdapter):
    def __init__(self):
        super().__init__(Opcion)
        self.__opcion = None

    @property
    def _opcion(self):
        if self.__opcion is None:
            self.__opcion = Opcion()
        return self.__opcion

    @_opcion.setter
    def _opcion(self, value):
        self.__opcion = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._opcion)
    
    def merge(self, pos):
        self._merge(self._opcion, pos)
        
    def crearOpcion(self, opcion, estado, valor, idPregunta):
        print("Creando opcion")
        print(opcion)
        self._opcion._opcion = opcion
        self._opcion._estado = estado
        self._opcion._valor = valor
        self._opcion._idPregunta = idPregunta
        self.save
        
    