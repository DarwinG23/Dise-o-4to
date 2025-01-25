from controls.tda.linked.linkedList import Linked_List
from controls.tda.asignacionControl import AsignacionControl
from controls.tda.estudianteControl import EstudianteControl

class Curso:
    def __init__(self):
        self.__id = 0
        self.__nombre = ""
        self.__paralelo = ""
        self.__numParticipantes = 0
        self.__idDocente = 0
        self.__estudiantes = Linked_List()
        self.__asignaciones = Linked_List()

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
    def _nombre(self):
        return self.__nombre

    @_nombre.setter
    def _nombre(self, value):
        self.__nombre = value

    @property
    def _paralelo(self):
        return self.__paralelo

    @_paralelo.setter
    def _paralelo(self, value):
        self.__paralelo = value

    @property
    def _numParticipantes(self):
        return self.__numParticipantes

    @_numParticipantes.setter
    def _numParticipantes(self, value):
        self.__numParticipantes = value

    @property
    def _idDocente(self):
        return self.__idDocente

    @_idDocente.setter
    def _idDocente(self, value):
        self.__idDocente = value

    @property
    def _estudiantes(self):
        return self.__estudiantes

    @_estudiantes.setter
    def _estudiantes(self, value):
        self.__estudiantes = value

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
            "paralelo": self.__paralelo,
            "numParticipantes": self.__numParticipantes,
            "idDocente": self.__idDocente
        }
    
    @classmethod
    def deserializar(self, data):
        curso = Curso()
        curso._id = data["id"]
        curso._nombre = data["nombre"]
        curso._paralelo = data["paralelo"]
        curso._numParticipantes = data["numparticipantes"]
        curso._idDocente = data["iddocente"]
        
        ac = AsignacionControl()
        if ac._list().isEmpty:
            asignaciones = Linked_List()
        else:
            asignaciones = ac._list() 
            asignaciones = asignaciones.lineal_binary_search_models(str(curso._id),"_idCurso") 
        curso._asignaciones = asignaciones
        
        ec = EstudianteControl()
        if ec._list().isEmpty:
            estudiantes = Linked_List()
        else:
            estudiantes = ec._list()
            estudiantes = estudiantes.lineal_binary_search_models(str(curso._id),"_idCurso")
        
        return curso
    
    def __str__(self):
        return "Curso: " + self.__nombre + " Paralelo: " + self.__paralelo 
