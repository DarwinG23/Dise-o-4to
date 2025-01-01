class Cursa:
    def __init__(self):
        self.__id = 0
        self.__paralelo = ''
        self.__idEstudiante = 0
        self.__asignacion = 0
        self.__periodoAcademico = 0


    @property
    def _idEstudiante(self):
        return self.__idEstudiante

    @_idEstudiante.setter
    def _idEstudiante(self, value):
        self.__idEstudiante = value

    @property
    def _asignacion(self):
        return self.__asignacion

    @_asignacion.setter
    def _asignacion(self, value):
        self.__asignacion = value

    @property
    def _periodoAcademico(self):
        return self.__periodoAcademico

    @_periodoAcademico.setter
    def _periodoAcademico(self, value):
        self.__periodoAcademico = value


    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value

    @property
    def _paralelo(self):
        return self.__paralelo

    @_paralelo.setter
    def _paralelo(self, value):
        self.__paralelo = value

    
    @property
    def serializable(self):
        return{
            "id": self.__id,
            "paralelo": self.__paralelo,
            "idEstudiante": self.__idEstudiante,
            "idAsignacion": self.__asignacion,
            "periodoAcademico": self.__periodoAcademico
        }
        
    @classmethod
    def deserializar(self, data):
        cursa = Cursa()
        cursa._id = data["id"]
        cursa._paralelo = data["paralelo"]
        cursa.__idEstudiante = data["idestudiante"]
        cursa.__asignacion = data["idasignacion"]
        cursa.__periodoAcademico = data["periodoacademico"]
        return cursa
    
    def __str__(self):
        return "Paralelo: " + self.__paralelo + " Asignacion: " + str(self.__asignacion) + " Estudiante: " + str(self.__idEstudiante)
    
        