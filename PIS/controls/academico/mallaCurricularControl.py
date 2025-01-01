from controls.dao.daoAdapter import DaoAdapter
from models.mallaCurricular import Malla_Curricular

class MallaCurricularControl(DaoAdapter):
    def __init__(self):
        super().__init__(Malla_Curricular)
        self.__mallaCurricular = None

    @property
    def _mallaCurricular(self):
        if self.__mallaCurricular is None:
            self.__mallaCurricular = Malla_Curricular()
        return self.__mallaCurricular

    @_mallaCurricular.setter
    def _mallaCurricular(self, value):
        self.__mallaCurricular = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._mallaCurricular)
    
    def merge(self, pos):
        self._merge(self._mallaCurricular, pos)

