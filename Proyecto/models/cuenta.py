from controls.tda.linked.linkedList import Linked_List
from controls.tda.rolContol import RolControl
from controls.tda.notificacionControl import NotificacionControl
#COMPLETAR

class Cuenta:
    def __init__(self):
        self.__id = 0
        self.__correo = ""
        self.__contrasena = ""
        self.__estado = ""
        self.__idUsuario = 0
        self.__roles = Linked_List()
        self.__notificaciones = Linked_List()

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value

    @property
    def _correo(self):
        return self.__correo

    @_correo.setter
    def _correo(self, value):
        self.__correo = value

    @property
    def _contrasena(self):
        return self.__contrasena

    @_contrasena.setter
    def _contrasena(self, value):
        self.__contrasena = value

    @property
    def _estado(self):
        return self.__estado

    @_estado.setter
    def _estado(self, value):
        self.__estado = value

    @property
    def _idUsuario(self):
        return self.__idUsuario

    @_idUsuario.setter
    def _idUsuario(self, value):
        self.__idUsuario = value

    @property
    def _roles(self):
        return self.__roles

    @_roles.setter
    def _roles(self, value):
        self.__roles = value

    @property
    def _notificaciones(self):
        return self.__notificaciones

    @_notificaciones.setter
    def _notificaciones(self, value):
        self.__notificaciones = value

        

   
        
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "correo": self.__correo,
            "contrasena": self.__contrasena,
            "estado": self.__estado,
            "idUsuario": self.__idUsuario
        }
        
    @classmethod
    def deserializar(self, dic):
        cuenta = Cuenta()
        cuenta._id = dic["id"]
        cuenta._correo = dic["correo"]
        cuenta._contrasena = dic["contrasena"]
        cuenta._estado = dic["estado"]
        cuenta._idUsuario = dic["idusuario"]
        rc = RolControl()
        print("Estamos aqui")
        print(rc._list())
        if rc._list().isEmpty:
            print("Estamos aqui")
            roles = Linked_List()
        else:
            print("Else")
            roles = rc._list()
            print(roles)
            print(cuenta._id)
            roles = roles.lineal_binary_search_models(str(cuenta._id),"_idCuenta")
            print(roles)
        cuenta._roles = roles
        print(cuenta._roles)
        print("############")
        nc = NotificacionControl()
        if nc._list().isEmpty:
            notificaciones = Linked_List()
        else:
            notificaciones = nc._list()
            notificaciones = notificaciones.lineal_binary_search_models(str(cuenta._id),"_idCuenta")
        cuenta._notificaciones = notificaciones
        return cuenta

        