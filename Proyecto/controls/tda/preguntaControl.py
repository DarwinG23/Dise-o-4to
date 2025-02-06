from controls.dao.daoAdapter import DaoAdapter
from models.pregunta import Pregunta

class PreguntaControl(DaoAdapter):
    def __init__(self):
        super().__init__(Pregunta)
        self.__pregunta = None

    @property
    def _pregunta(self):
        if self.__pregunta is None:
            self.__pregunta = Pregunta()
        return self.__pregunta

    @_pregunta.setter
    def _rol(self, value):
        self.__pregunta = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._pregunta)
    
    def merge(self, pos):
        self._merge(self._pregunta, pos)
        
    def crearPregunta(self, pregunta, estado, respuesta, idTest):
        self._pregunta._pregunta = pregunta
        self._pregunta._estado = estado
        self._pregunta._respuesta = respuesta
        self._pregunta._idTest = idTest
        self.save
    