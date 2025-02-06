from controls.dao.daoAdapter import DaoAdapter
from models.curso import Curso

class CursoControl(DaoAdapter):
    def __init__(self):
        super().__init__(Curso)
        self.__curso = None

    @property
    def _curso(self):
        if self.__curso is None:
            self.__curso = Curso()
        return self.__curso

    @_curso.setter
    def _curso(self, value):
        self.__curso = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._curso)
    
    def merge(self, pos):
        self._merge(self._curso, pos)
        
    def crearCurso(self, nombre, paralelo, idDocente):
        self._curso._nombre = nombre
        self._curso._paralelo = paralelo
        self._curso._numParticipantes = 0
        self._curso._idDocente = idDocente
        self.save