
class Opcion:
    def __init__(self):
        self.__opcion = ""
        self.__estado = ""
        self.__valor = 0
        self.__idPregunta = 0
        self.__id = 0

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value


    @property
    def _opcion(self):
        return self.__opcion

    @_opcion.setter
    def _opcion(self, value):
        self.__opcion = value

    @property
    def _estado(self):
        return self.__estado

    @_estado.setter
    def _estado(self, value):
        self.__estado = value

    @property
    def _valor(self):
        return self.__valor

    @_valor.setter
    def _valor(self, value):
        self.__valor = value

    @property
    def _idPregunta(self):
        return self.__idPregunta

    @_idPregunta.setter
    def _idPregunta(self, value):
        self.__idPregunta = value
        
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "opcion": self.__opcion,
            "estado": self.__estado,
            "valor": self.__valor,
            "idPregunta": self.__idPregunta
        }
    @classmethod
    def deserializar(self, data):
        opcion = Opcion()
        opcion._opcion = data["id"]
        opcion._opcion = data["opcion"]
        opcion._estado = data["estado"]
        opcion._valor = data["valor"]
        opcion._idPregunta = data["idpregunta"]
        return opcion
    
    
    def __str__(self):
        return str(self._opcion) + " " + str(self._idPregunta)
