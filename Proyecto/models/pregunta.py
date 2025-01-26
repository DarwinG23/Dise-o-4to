from controls.tda.linked.linkedList import Linked_List
from controls.tda.opcionControl import OpcionControl

class Pregunta:
    def __init__(self):
        self.__id = 0
        self.__pregunta = ""
        self.__estado = ""
        self.__respuesta = ""
        self.__idTest = 0
        self.__opciones = Linked_List()

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value

    @property
    def _pregunta(self):
        return self.__pregunta

    @_pregunta.setter
    def _pregunta(self, value):
        self.__pregunta = value

    @property
    def _estado(self):
        return self.__estado

    @_estado.setter
    def _estado(self, value):
        self.__estado = value

    @property
    def _respuesta(self):
        return self.__respuesta

    @_respuesta.setter
    def _respuesta(self, value):
        self.__respuesta = value

    @property
    def _idTest(self):
        return self.__idTest

    @_idTest.setter
    def _idTest(self, value):
        self.__idTest = value

    @property
    def _opciones(self):
        return self.__opciones

    @_opciones.setter
    def _opciones(self, value):
        self.__opciones = value
        
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "pregunta": self.__pregunta,
            "estado": self.__estado,
            "respuesta": self.__respuesta,
            "idTest": self.__idTest
        }
        
    @classmethod
    def deserializar(self, data):
        pregunta = Pregunta()
        pregunta._id = data['id']
        pregunta._pregunta = data['pregunta']
        pregunta._estado = data['estado']
        pregunta._respuesta = data['respuesta']
        pregunta._idTest = data['idtest']
        oc = OpcionControl()
        opciones = oc._list()
        if not opciones.isEmpy:
            opciones = opciones.lineal_binary_search_models(str(pregunta._id),"_idPregunta")
        pregunta._opciones = opciones
        return pregunta
