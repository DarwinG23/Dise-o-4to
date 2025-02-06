from controls.dao.daoAdapter import DaoAdapter
from models.test import Test

class TestControl(DaoAdapter):
    def __init__(self):
        super().__init__(Test)
        self.__test = None

    @property
    def _test(self):
        if self.__test is None:
            self.__test = Test()
        return self.__test

    @_test.setter
    def _test(self, value):
        self.__test = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._test)
    
    def merge(self, pos):
        self._merge(self._test, pos)
        
    
    def crearTest(self, nombre, descripcion, resultado, idAsignacion, idAdministrador):
        
        self._test._nombre = nombre
        self._test._descripcion = descripcion
        self._test._resultado = resultado
        self._test._idAsignacion = idAsignacion
        self._test._idAdministrador = idAdministrador
        self.save
    