from controls.tda.linked.linkedList import Linked_List
from models.unidad import Unidad
from models.reporte import Reporte
from models.cursa import Cursa

from controls.administrativo.cursaControl import CursaControl
from controls.seguimiento.reporteControl import ReporteControl
from controls.seguimiento.unidadControl import UnidadControl

class Asignacion:
    def __init__(self):
        self.__id = 0
        self.__numero_unidades = 0
        self.__cedula_docente = ""
        self.__id_materia = 0
        self.__cursas = Linked_List()
        self.__unidades = Linked_List()
        self.__reportes = Linked_List()
        

    @property
    def _reportes(self):
        return self.__reportes

    @_reportes.setter
    def _reportes(self, value):
        self.__reportes = value


    @property
    def _unidades(self):
        return self.__unidades

    @_unidades.setter
    def _unidades(self, value):
        self.__unidades = value


    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value

    @property
    def _numero_unidades(self):
        return self.__numero_unidades

    @_numero_unidades.setter
    def _numero_unidades(self, value):
        self.__numero_unidades = value

    @property
    def _cedula_docente(self):
        return self.__cedula_docente

    @_cedula_docente.setter
    def _cedula_docente(self, value):
        self.__cedula_docente = value

    @property
    def _id_materia(self):
        return self.__id_materia

    @_id_materia.setter
    def _id_materia(self, value):
        self.__id_materia = value

    @property
    def _cursas(self):
        return self.__cursas

    @_cursas.setter
    def _cursas(self, value):
        self.__cursas = value


    @property
    def serializable(self):
        return {
            "id": self.__id,
            "numero_unidades": self.__numero_unidades,
            "cedula_docente": self.__cedula_docente,
            "id_materia": self.__id_materia,
            #"cursas": self.__cursas.serializable,
            #"unidades": self.__unidades.serializable, 
            #"reportes": self.__reportes.serializable
        }

    @classmethod
    def deserializar(self, data):
        asignacion = Asignacion()
        asignacion._id = data["id"]        
        asignacion._cedula_docente = data["cedula_docente"]
        asignacion._id_materia = data["id_materia"]
        #CONSULTAS
        cc = CursaControl()
        if cc._list().isEmpty:
            cursas = Linked_List()
        else:
            cursas = cc._list()
            cursas = cursas.lineal_binary_search_models(str(asignacion._id),"_asignacion")        
        asignacion._cursas = cursas
        
        uc = UnidadControl()
        if uc._list().isEmpty:
            unidades = Linked_List()
        else:
            unidades = uc._list()
            unidades = unidades.lineal_binary_search_models(str(asignacion._id),"_asignacion")
        asignacion._unidades = unidades
        asignacion._numero_unidades = unidades._length
        rc = ReporteControl()
        if rc._list().isEmpty:
            reportes = Linked_List()
        else:
            reportes = rc._list()
            reportes = reportes.lineal_binary_search_models(str(asignacion._id),"_idAsignacion")
        asignacion._reportes = reportes
        
        return asignacion
    
    
    
    
    def __str__(self):
        return "docente: " + str(self._cedula_docente) + " id: " + str(self._id) 