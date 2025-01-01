from controls.dao.daoAdapter import DaoAdapter
from models.reporte import Reporte

class ReporteControl(DaoAdapter):
    def __init__(self):
        super().__init__(Reporte)
        self.__reporte = None

    @property
    def _reporte(self):
        if self.__reporte is None:
            self.__reporte = Reporte()
        return self.__reporte

    @_reporte.setter
    def _reporte(self, value):
        self.__reporte = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._reporte)
    
    def merge(self, pos):
        self._merge(self._reporte, pos)

