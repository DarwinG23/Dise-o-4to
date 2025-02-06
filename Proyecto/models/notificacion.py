from controls.tda.linked.linkedList import Linked_List

class Notificacion:
    def __init__(self):
        self.__id = 0
        self.__titulo = ""
        self.__mensaje = ""
        self.__fechaCreacion = ""
        self.__horaEnvio = ""
        self.__idCuenta = 0

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value

    @property
    def _titulo(self):
        return self.__titulo

    @_titulo.setter
    def _titulo(self, value):
        self.__titulo = value

    @property
    def _mensaje(self):
        return self.__mensaje

    @_mensaje.setter
    def _mensaje(self, value):
        self.__mensaje = value

    @property
    def _fechaCreacion(self):
        return self.__fechaCreacion

    @_fechaCreacion.setter
    def _fechaCreacion(self, value):
        self.__fechaCreacion = value

    @property
    def _horaEnvio(self):
        return self.__horaEnvio

    @_horaEnvio.setter
    def _horaEnvio(self, value):
        self.__horaEnvio = value

    @property
    def _idCuenta(self):
        return self.__idCuenta

    @_idCuenta.setter
    def _idCuenta(self, value):
        self.__idCuenta = value
        
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "titulonotificacion": self.__titulo,
            "mensaje": self.__mensaje,
            "fechaCreacion": self.__fechaCreacion,
            "horaEnvio": self.__horaEnvio,
            "idCuenta": self.__idCuenta
        }
        
    @classmethod
    def deserializar(self, data):
        notificacion = Notificacion()
        notificacion._id = data['id']
        notificacion._titulo = data['titulonotificacion']
        notificacion._mensaje = data['mensaje']
        notificacion._fechaCreacion = data['fechacreacion']
        notificacion._horaEnvio = data['horaenvio']
        notificacion._idCuenta = data['idcuenta']
        return notificacion
