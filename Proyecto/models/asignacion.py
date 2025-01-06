from controls.tda.linked.linkedList import Linked_List

class Asignacion:
    def __init__(self):
        self.__id = 0
        self.__fechaInicio = ""
        self.__fechaFin = ""
        self.__asignado = ""
        self.__estado = ""
        self.__idEstudiante = 0
        self.__idCurso = 0
        self.__idDocente = 0
        self.__idNotificacion = 0

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value

    @property
    def _fechaInicio(self):
        return self.__fechaInicio

    @_fechaInicio.setter
    def _fechaInicio(self, value):
        self.__fechaInicio = value

    @property
    def _fechaFin(self):
        return self.__fechaFin

    @_fechaFin.setter
    def _fechaFin(self, value):
        self.__fechaFin = value

    @property
    def _asignado(self):
        return self.__asignado

    @_asignado.setter
    def _asignado(self, value):
        self.__asignado = value

    @property
    def _estado(self):
        return self.__estado

    @_estado.setter
    def _estado(self, value):
        self.__estado = value

    @property
    def _idEstudiante(self):
        return self.__idEstudiante

    @_idEstudiante.setter
    def _idEstudiante(self, value):
        self.__idEstudiante = value

    @property
    def _idCurso(self):
        return self.__idCurso

    @_idCurso.setter
    def _idCurso(self, value):
        self.__idCurso = value

    @property
    def _idDocente(self):
        return self.__idDocente

    @_idDocente.setter
    def _idDocente(self, value):
        self.__idDocente = value

    @property
    def _idNotificacion(self):
        return self.__idNotificacion

    @_idNotificacion.setter
    def _idNotificacion(self, value):
        self.__idNotificacion = value
        
    @property
    def serializar(self):
        return {
            "id": self.__id,
            "fechaInicio": self.__fechaInicio,
            "fechaFin": self.__fechaFin,
            "asignado": self.__asignado,
            "estado": self.__estado,
            "idEstudiante": self.__idEstudiante,
            "idCurso": self.__idCurso,
            "idDocente": self.__idDocente,
            "idNotificacion": self.__idNotificacion
        }
    
    @classmethod
    def deserializar(self, data):
        asignacion = Asignacion()
        asignacion._id = data["id"]
        asignacion._fechaInicio = data["fechainicio"]
        asignacion._fechaFin = data["fechafin"]
        asignacion._asignado = data["asignado"]
        asignacion._estado = data["estado"]
        asignacion._idEstudiante = data["idestudiante"]
        asignacion._idCurso = data["idcurso"]
        asignacion._idDocente = data["iddocente"]
        asignacion._idNotificacion = data["idnotificacion"]
        return asignacion
