from controls.tda.linked.linkedList import Linked_List
#from controls.academico.materiaControl import MateriaControl

class Ciclo:
    def __init__(self):
        self.__id = 0
        self.__descripcion = ""
        self.__vigencia = True
        self.__malla_curricular = 0
        self.__materias = Linked_List()

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value

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
    def _malla_curricular(self):
        return self.__malla_curricular

    @_malla_curricular.setter
    def _malla_curricular(self, value):
        self.__malla_curricular = value

    @property
    def _materias(self):
        return self.__materias

    @_materias.setter
    def _materias(self, value):
        self.__materias = value
        
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "descripcion": self.__descripcion,
            "vigencia": self.__vigencia,
            "malla_curricular": self.__malla_curricular,
           # "materias": self.__materias.serializable
        }
        
    @classmethod
    def deserializar(cls, dic):
        ciclo = Ciclo()
        ciclo._id = dic["id"]
        ciclo._descripcion = dic["descripcion"]
        ciclo._vigencia = dic["vigencia"]
        ciclo._malla_curricular = dic["malla_curricular"]
        
        # mc = MateriaControl()
        # if mc._list().isEmpty:
        #     materias = Linked_List()
        # else:
        #     materias = mc._list()
        #     materias = materias.lineal_binary_search_models(ciclo._id, "_idCiclo")
        materias = Linked_List()
        ciclo._materias = materias
        
        return ciclo
    
    def __str__(self):
        return self.__descripcion + " " + self.__vigencia

        
