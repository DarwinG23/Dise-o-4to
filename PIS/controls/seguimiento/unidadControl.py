from controls.dao.daoAdapter import DaoAdapter
from models.unidad import Unidad

class UnidadControl(DaoAdapter):
    def __init__(self):
        super().__init__(Unidad)
        self.__unidad = None

    @property
    def _unidad(self):
        if self.__unidad is None:
            self.__unidad = Unidad()
        return self.__unidad

    @_unidad.setter
    def _unidad(self, value):
        self.__unidad = value

    def _lista(self):
        return self._list()

    @property
    def save(self):
        self._save(self._unidad)

    def merge(self, pos):
        self._merge(self._unidad, pos)