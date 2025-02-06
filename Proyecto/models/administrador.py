from controls.tda.linked.linkedList import Linked_List
from controls.tda.testControl import TestControl

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
    def serializable(self):
        return {
            "id": self.__id,
            "idUsuario": self.__idUsuario
        }
    
    @classmethod
    def deserializar(self, data):
        administrador = Administrador()
        administrador._id = data["id"]
        administrador._idUsuario = data["idusuario"]
        tc = TestControl()
        
        if tc._list().isEmpty:
            tests = Linked_List()
        else:
            tests = tc._list() 
            tests = tests.lineal_binary_search_models(str(administrador._id),"_idAdministrador") 
        administrador._tests = tests
        return administrador

