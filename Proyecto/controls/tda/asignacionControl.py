from controls.dao.daoAdapter import DaoAdapter
from models.asignacion import Asignacion

class AsignacionControl(DaoAdapter):
    def __init__(self):
        super().__init__(Asignacion)
        self.__asignacion = None

    @property
    def _asignacion(self):
        if self.__asignacion is None:
            self.__asignacion = Asignacion()
        return self.__asignacion

    @_asignacion.setter
    def _asignacion(self, value):
        self.__asignacion = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._asignacion)
    
    def merge(self, pos):
        self._merge(self._asignacion, pos)
    

    def obtener_asignaciones(self):
        """Obtiene todas las asignaciones en formato serializado."""
        asignaciones = self._list()  
        return [asignacion.serializar for asignacion in asignaciones]
    
    def crearAsignacion(self, fechaInicio, fechaFin, asignado ,estado, idEstudiante, idCurso, idDocente, idNotificacion):
        self._asignacion._fechaInicio = fechaInicio
        self._asignacion._fechaFin = fechaFin
        self._asignacion._asignado = asignado
        self._asignacion._estado = estado
        if idEstudiante is not None:
            self._asignacion._idEstudiante = idEstudiante
        self._asignacion._idCurso = idCurso
        self._asignacion._idDocente = idDocente
        self._asignacion._idNotificacion = idNotificacion
        return self.save