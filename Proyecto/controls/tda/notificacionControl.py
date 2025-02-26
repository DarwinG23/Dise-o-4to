from controls.dao.daoAdapter import DaoAdapter
from models.notificacion import Notificacion

class NotificacionControl(DaoAdapter):
    def __init__(self):
        super().__init__(Notificacion)
        self.__notificacion = None

    @property
    def _notificacion(self):
        if self.__notificacion is None:
            self.__notificacion = Notificacion()
        return self.__notificacion

    @_notificacion.setter
    def _notificacion(self, value):
        self.__notificacion = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._notificacion)
    
    def merge(self, pos):
        self._merge(self._notificacion, pos)
        
    def crearNotificacion(self, titulo, mensaje, fechaCreacion, horaEnvio, idCuenta):
        self._notificacion._titulo = titulo
        self._notificacion._mensaje = mensaje
        self._notificacion._fechaCreacion = fechaCreacion
        self._notificacion._horaEnvio = horaEnvio
        if idCuenta is not None:
            self._notificacion._idCuenta = idCuenta
        self.save

    