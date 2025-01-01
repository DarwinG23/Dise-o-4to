from controls.tda.linked.linkedList import Linked_List
from models.ciclo import Ciclo

class Malla_Curricular:
    def __init__(self):
        self.__id = 0
        self.__nombre = ""
        self.__descripcion = ""
        self.__vigencia = True
        self.__ciclos = Linked_List()

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
    def _vigencia(self):
        return self.__vigencia

    @_vigencia.setter
    def _vigencia(self, value):
        self.__vigencia = value

    @property
    def _ciclos(self):
        return self.__ciclos

    @_ciclos.setter
    def _ciclos(self, value):
        self.__ciclos = value
        
    
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "descripcion": self.__descripcion,
            "vigencia": self.__vigencia,
            #"ciclos": self.__ciclos.serializable
            #quitamos los ciclos, por que no existe en la base
        }
    
    @classmethod
    def deserializar(cls, dict):
        malla = Malla_Curricular()
        malla._id = dict["id"]
        malla._nombre = dict["nombre"]
        malla._descripcion = dict["descripcion"]
        malla._vigencia = dict["vigencia"]

        #Hacer una consulta
        clase = Ciclo()
        #malla._ciclos = Linked_List().deserializar(dict["ciclos"], clase)
        return malla
    
    def __str__(self):
        return self.__nombre

        
        

   