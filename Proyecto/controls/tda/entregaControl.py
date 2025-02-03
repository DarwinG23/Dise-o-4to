from controls.dao.daoAdapter import DaoAdapter
from models.entrega import Entrega

class EntregaControl(DaoAdapter):
    def __init__(self):
        super().__init__(Entrega)
        self.__entrega = None

    @property
    def _entrega(self):
        if self.__entrega is None:
            self.__entrega = Entrega()
        return self.__entrega

    @_entrega.setter
    def _entrega(self, value):
        self.__entrega = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._entrega)
    
    def crearEntrega(self, ruta_pdf, estado, calificacion, comentario, fecha, permiso, idAsignacion, idEstudiante):
        self._entrega._ruta_pdf = ruta_pdf
        self._entrega._estado = estado
        self._entrega._calificacion = calificacion
        self._entrega._comentario = comentario
        self._entrega._fecha = fecha
        self._entrega._permiso = permiso
        if idAsignacion is not None:
            self._entrega._idAsignacion = idAsignacion
        if idEstudiante is not None:
            self._entrega._idEstudiante = idEstudiante
        self.save
        
       