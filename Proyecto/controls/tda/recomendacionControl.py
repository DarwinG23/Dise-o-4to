from controls.dao.daoAdapter import DaoAdapter
from models.recomendacion import Recomendacion

class RecomendacionControl(DaoAdapter):
    def __init__(self):
        super().__init__(Recomendacion)
        self.__recomendacion = None

    @property
    def _recomendacion(self):
        if self.__recomendacion is None:
            self.__recomendacion = Recomendacion()
        return self.__recomendacion

    @_recomendacion.setter
    def _recomendacion(self, value):
        self.__recomendacion = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._recomendacion)
    
    def merge(self, pos):
        self._merge(self._recomendacion, pos)
    