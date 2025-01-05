from controls.tda.linked.linkedList import Linked_List
#COMPLETAR

class Test:
    def __init__(self):
        self.__id = 0
        self.__nombre = ""
        self.__descripcion = ""
        self.__resultado = 0
        self.__idAsignacion = 0
        self.__preguntas = Linked_List()

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value

    @property
    def _nombre(self):
        return self.__nombre

    @_nombre.setter
    def _nombre(self, value):
        self.__nombre = value

    @property
    def _descripcion(self):
        return self.__descripcion

    @_descripcion.setter
    def _descripcion(self, value):
        self.__descripcion = value

    @property
    def _resultado(self):
        return self.__resultado

    @_resultado.setter
    def _resultado(self, value):
        self.__resultado = value

    @property
    def _idAsignacion(self):
        return self.__idAsignacion

    @_idAsignacion.setter
    def _idAsignacion(self, value):
        self.__idAsignacion = value

    @property
    def _preguntas(self):
        return self.__preguntas

    @_preguntas.setter
    def _preguntas(self, value):
        self.__preguntas = value
        
        
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "descripcion": self.__descripcion,
            "resultado": self.__resultado,
            "idAsignacion": self.__idAsignacion
        }
        
    @classmethod
    def deserializar(self, data):
        test = Test()
        test._id = data['id']
        test._nombre = data['nombre']
        test._descripcion = data['descripcion']
        test._resultado = data['resultado']
        test._idAsignacion = data['idasignacion']
        #COMPLETAR
        return test

        

        
        