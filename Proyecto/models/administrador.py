from controls.tda.linked.linkedList import Linked_List
#COMPLETAR
class Administrador:
    def __init__(self):
        self.__id = 0
        self.__idUsuario = 0
        self.__recomendaciones = Linked_List()
        self.__tests = Linked_List()

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value

    @property
    def _idUsuario(self):
        return self.__idUsuario

    @_idUsuario.setter
    def _idUsuario(self, value):
        self.__idUsuario = value

    @property
    def _recomendaciones(self):
        return self.__recomendaciones

    @_recomendaciones.setter
    def _recomendaciones(self, value):
        self.__recomendaciones = value

    @property
    def _tests(self):
        return self.__tests

    @_tests.setter
    def _tests(self, value):
        self.__tests = value
        
    @property
    def serializar(self):
        return {
            "id": self.__id,
            "idUsuario": self.__idUsuario
        }
    
    @classmethod
    def deserializar(self, data):
        administrador = Administrador()
        administrador._id = data["id"]
        administrador._idUsuario = data["idusuario"]
        #COMPLETAR
        return administrador

