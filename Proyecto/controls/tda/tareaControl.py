from controls.dao.daoAdapter import DaoAdapter
from models.tarea import Tarea

class TareaControl(DaoAdapter):
    def __init__(self):
        super().__init__(Tarea)
        self.__tarea = None

    @property
    def _tarea(self):
        if self.__tarea is None:
            self.__tarea = Tarea()
        return self.__tarea

    @_tarea.setter
    def _tarea(self, value):
        self.__tarea = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._tarea)
    
    def merge(self, pos):
        self._merge(self._tarea, pos)
        
    
    def crearTarea(self, titulo, descripcion, estado, idAsignacion, ruta_pdf):
        self._tarea._titulo = titulo
        self._tarea._descripcion = descripcion
        self._tarea._estado = estado
        if idAsignacion is not None:
            self._tarea._idAsignacion = idAsignacion
        if ruta_pdf is not None:
            self._tarea._ruta_pdf = ruta_pdf
        self.save
        
    