from controls.tda.linked.linkedList import Linked_List

class Tarea:
    def __init__(self):
        self.__id = 0
        self.__titulo = ""
        self.__descripcion = ""
        self.__estado = ""
        self.__idAsignacion = 0

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
    def _descripcion(self):
        return self.__descripcion

    @_descripcion.setter
    def _descripcion(self, value):
        self.__descripcion = value

    @property
    def _estado(self):
        return self.__estado

    @_estado.setter
    def _estado(self, value):
        self.__estado = value

    @property
    def _idAsignacion(self):
        return self.__idAsignacion

    @_idAsignacion.setter
    def _idAsignacion(self, value):
        self.__idAsignacion = value
        
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "titulo": self.__titulo,
            "descripcion": self.__descripcion,
            "estado": self.__estado,
            "idAsignacion": self.__idAsignacion
        }
    
    @classmethod
    def deserializar(self, data):
        tarea = Tarea()
        tarea._id = data["id"]
        tarea._titulo = data["titulo"]
        tarea._descripcion = data["descripcion"]
        tarea._estado = data["estado"]
        tarea._idAsignacion = data["idasignacion"]
        return tarea

        
    
    