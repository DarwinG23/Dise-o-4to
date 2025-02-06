from controls.tda.linked.linkedList import Linked_List  
from controls.tda.recomendacionControl import RecomendacionControl
from controls.tda.asignacionControl import AsignacionControl

class Estudiante:
    def __init__(self):
        self.__id = 0
        self.__matricula = ""
        self.__contactoEmergencia = ""
        self.__idCurso = 0
        self.__idUsuario = 0
        self.__asignaciones = Linked_List()
        self.__recomendaciones = Linked_List()

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value

    @property
    def _matricula(self):
        return self.__matricula

    @_matricula.setter
    def _matricula(self, value):
        self.__matricula = value

    @property
    def _contactoEmergencia(self):
        return self.__contactoEmergencia

    @_contactoEmergencia.setter
    def _contactoEmergencia(self, value):
        self.__contactoEmergencia = value

    @property
    def _idCurso(self):
        return self.__idCurso

    @_idCurso.setter
    def _idCurso(self, value):
        self.__idCurso = value

    @property
    def _idUsuario(self):
        return self.__idUsuario

    @_idUsuario.setter
    def _idUsuario(self, value):
        self.__idUsuario = value

    @property
    def _asignaciones(self):
        return self.__asignaciones

    @_asignaciones.setter
    def _asignaciones(self, value):
        self.__asignaciones = value

    @property
    def _recomendaciones(self):
        return self.__recomendaciones

    @_recomendaciones.setter
    def _recomendaciones(self, value):
        self.__recomendaciones = value
        
        
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "matricula": self.__matricula,
            "contactoEmergencia": self.__contactoEmergencia,
            "idCurso": self.__idCurso,
            "idUsuario": self.__idUsuario
        }
    
    @classmethod
    def deserializar(self, data):
        estudiante = Estudiante()
        estudiante._id = data["id"]
        estudiante._matricula = data["matricula"]
        estudiante._contactoEmergencia = data["contactoemergencia"]
        estudiante._idCurso = data["idcurso"]
        estudiante._idUsuario = data["idusuario"]
        rc= RecomendacionControl()
        ac = AsignacionControl()
        recomendaciones = rc._list()
        if not recomendaciones.isEmpty:
            recomendaciones = recomendaciones.lineal_binary_search_models(str(estudiante._id),"_idEstudiante")
        estudiante._recomendaciones = recomendaciones
        asignaciones = ac._list()
        if not asignaciones.isEmpty:
            asignaciones = asignaciones.lineal_binary_search_models(str(estudiante._id),"_idEstudiante")
        estudiante._asignaciones = asignaciones
        
        return estudiante
    
    


    