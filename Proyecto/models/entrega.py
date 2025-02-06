


class Entrega:
    def __init__(self):
        self.__id = 0
        self.__ruta_pdf = "Sin ruta"
        self.__estado = "Sin estado"
        self.__calificacion = 0
        self.__comentario = "Sin comentario"
        self.__fecha = "Sin fecha"
        self.__permiso = 0
        self.__idAsignacion = 0
        self.__idEstudiante = 0

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value

    @property
    def _ruta_pdf(self):
        return self.__ruta_pdf

    @_ruta_pdf.setter
    def _ruta_pdf(self, value):
        self.__ruta_pdf = value

    @property
    def _estado(self):
        return self.__estado

    @_estado.setter
    def _estado(self, value):
        self.__estado = value

    @property
    def _calificacion(self):
        return self.__calificacion

    @_calificacion.setter
    def _calificacion(self, value):
        self.__calificacion = value

    @property
    def _comentario(self):
        return self.__comentario

    @_comentario.setter
    def _comentario(self, value):
        self.__comentario = value

    @property
    def _fecha(self):
        return self.__fecha

    @_fecha.setter
    def _fecha(self, value):
        self.__fecha = value

    @property
    def _permiso(self):
        return self.__permiso

    @_permiso.setter
    def _permiso(self, value):
        self.__permiso = value

    @property
    def _idAsignacion(self):
        return self.__idAsignacion

    @_idAsignacion.setter
    def _idAsignacion(self, value):
        self.__idAsignacion = value

    @property
    def _idEstudiante(self):
        return self.__idEstudiante

    @_idEstudiante.setter
    def _idEstudiante(self, value):
        self.__idEstudiante = value


    
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "ruta_pdf": self.__ruta_pdf,
            "estado": self.__estado,
            "calificacion": self.__calificacion,
            "comentario": self.__comentario,
            "permiso": self.__permiso,
            "idAsignacion": self.__idAsignacion,
            "idEstudiante": self.__idEstudiante,
            "fecha": self.__fecha
        }
        
    @classmethod
    def deserializar(self, data):
        entrega = Entrega()
        entrega._id = data["id"]
        entrega._ruta_pdf = data["ruta_pdf"]
        entrega._estado = data["estado"]
        entrega._calificacion = data["calificacion"]
        entrega._comentario = data["comentario"]
        entrega._permiso = data["permiso"]
        entrega._idAsignacion = data["idasignacion"]
        entrega._idEstudiante = data["idestudiante"]
        entrega._fecha = data["fecha"]
        return entrega
