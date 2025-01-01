from controls.tda.linked.linkedList import Linked_List
from models.asignacion import Asignacion
from controls.seguimiento.asignacionControl import AsignacionDaoControl
from controls.academico.cicloControl import CicloControl


class Materia:
    def __init__(self):
        self.__id = 0
        self.__nombre = ""
        self.__codigo = ""
        self.__horas = 0
        self.__asignaciones =  Linked_List()
        self.__id_ciclo = 0

    @property
    def _id_ciclo(self):
        return self.__id_ciclo

    @_id_ciclo.setter
    def _id_ciclo(self, value):
        self.__id_ciclo = value


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
    def _codigo(self):
        return self.__codigo

    @_codigo.setter
    def _codigo(self, value):
        self.__codigo = value

    @property
    def _horas(self):
        return self.__horas

    @_horas.setter
    def _horas(self, value):
        self.__horas = value

    @property
    def _asignaciones(self):
        return self.__asignaciones

    @_asignaciones.setter
    def _asignaciones(self, value):
        self.__asignaciones = value
        
        
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "codigo": self.__codigo,
            "horas": self.__horas,
            "idCiclo": self.__id_ciclo
            #"asignaciones": self.__asignaciones.serializable,
            #"id_ciclo": self.__id_ciclo
        }
        
    @classmethod
    def deserializar(self, dic):
        materia = Materia()
        materia._id = dic["id"]
        materia._nombre = dic["nombre"]
        materia._codigo = dic["codigo"]
        materia._horas = dic["horas"]
        ac = AsignacionDaoControl()
        if ac._list().isEmpty:
            asignaciones = Linked_List()
        else:
            asignaciones = ac._list()
            asignaciones = asignaciones.lineal_binary_search_models(str(materia._id), "_id_materia")
        
        cc = CicloControl()
        if cc._list().isEmpty:
            ciclo = "s/n"
        else:
            ciclos = cc._list()
            ciclo = ciclos.binary_search_models(materia._id_ciclo, "_id")
        
        materia._id_ciclo = ciclo
        return materia
    
    def __str__(self):
        return self.__nombre

    
    
    