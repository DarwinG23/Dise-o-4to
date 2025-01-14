from controls.tda.linked.linkedList import Linked_List

class Recomendacion:
    def __init__(self):
        self.__id = 0
        self.__titulo = ""
        self.__descripcion = ""
        self.__estado = ""
        self.__idDocente = 0
        self.__idAdministrador = 0
        self.__idEstudiante = 0

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
    def _idDocente(self):
        return self.__idDocente

    @_idDocente.setter
    def _idDocente(self, value):
        self.__idDocente = value

    @property
    def _idAdministrador(self):
        return self.__idAdministrador

    @_idAdministrador.setter
    def _idAdministrador(self, value):
        self.__idAdministrador = value

    @property
    def _idEstudiante(self):
        return self.__idEstudiante

    @_idEstudiante.setter
    def _idEstudiante(self, value):
        self.__idEstudiante = value
        
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "titulo": self.__titulo,
            "descripcion": self.__descripcion,
            "estado": self.__estado,
            "idDocente": self.__idDocente,
            "idAdministrador": self.__idAdministrador,
            "idEstudiante": self.__idEstudiante
        }
    
    @classmethod
    def deserializar(self, data):
        recomendacion = Recomendacion()
        recomendacion._id = data['id']
        recomendacion._titulo = data['titulo']
        recomendacion._descripcion = data['descripcion']
        recomendacion._estado = data['estado']
        recomendacion._idDocente = data['iddocente']
        recomendacion._idAdministrador = data['idadministrador']
        recomendacion._idEstudiante = data['idestudiante']
        return recomendacion

        