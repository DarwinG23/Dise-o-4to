

class Unidad:
    def __init__(self):
        self.__id = 0
        self.__codigo = ' '
        self.__estado = False
        self.__fecha_inicio = ''
        self.__fecha_limite = ''
        self.__asignacion = 0
        self.__nombre = ''
        self.__numero = 0

    @property
    def _numero(self):
        return self.__numero

    @_numero.setter
    def _numero(self, value):
        self.__numero = value


    @property
    def _nombre(self):
        return self.__nombre

    @_nombre.setter
    def _nombre(self, value):
        self.__nombre = value


    @property
    def _asignacion(self):
        return self.__asignacion

    @_asignacion.setter
    def _asignacion(self, value):
        self.__asignacion = value


    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value

    @property
    def _codigo(self):
        return self.__codigo

    @_codigo.setter
    def _codigo(self, value):
        self.__codigo = value

    @property
    def _estado(self):
        return self.__estado

    @_estado.setter
    def _estado(self, value):
        self.__estado = value

    @property
    def _fecha_inicio(self):
        return self.__fecha_inicio

    @_fecha_inicio.setter
    def _fecha_inicio(self, value):
        self.__fecha_inicio = value

    @property
    def _fecha_limite(self):
        return self.__fecha_limite

    @_fecha_limite.setter
    def _fecha_limite(self, value):
        self.__fecha_limite = value


    
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "codigo": self.__codigo,
            "estado": self.__estado,
            "fecha_inicio": self.__fecha_inicio,
            "fecha_limite": self.__fecha_limite,
            "idAsignacion": self.__asignacion,
            "nombre": self.__nombre,
            "numero": self.__numero,
        }
        
    @classmethod
    def deserializar(self, data):
        unidad = Unidad()
        unidad._id = data["id"]
        unidad._codigo = str(data["codigo"])
        unidad._estado = data["estado"]
        unidad._fecha_inicio = data["fecha_inicio"]
        unidad._fecha_limite = data["fecha_limite"]
        unidad._asignacion = data["idasignacion"]
        unidad._nombre = data["nombre"]
        unidad._numero = data["numero"]         
        return unidad
    
    def __str__(self) -> str:
        return self.__nombre + " Codigo " + self.__codigo