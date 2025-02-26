from controls.dao.daoAdapter import DaoAdapter
from models.estudiante import Estudiante

class EstudianteControl(DaoAdapter):
    def __init__(self):
        super().__init__(Estudiante)
        self.__estudiante = None

    @property
    def _estudiante(self):
        if self.__estudiante is None:
            self.__estudiante = Estudiante()
        return self.__estudiante

    @_estudiante.setter
    def _estudiante(self, value):
        self.__estudiante = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._estudiante)
    
    def merge(self, pos):
        self._merge(self._estudiante, pos)
        
    def agregarDatos(self, matricula, contacto, idUsuario):
        self._estudiante._matricula = matricula
        self._estudiante._contactoEmergencia = contacto
        self._estudiante._idUsuario = idUsuario
        self.save
        
    