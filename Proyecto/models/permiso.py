class Permiso: 
    def __init__(self):
        self.__id = 0
        self.__nombre = ""
        self.__detalle = ""
        self.__estado = ""
        self.__idRol = 0

    @property
    def _idRol(self):
        return self.__idRol

    @_idRol.setter
    def _idRol(self, value):
        self.__idRol = value

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
    def _detalle(self):
        return self.__detalle

    @_detalle.setter
    def _detalle(self, value):
        self.__detalle = value

    @property
    def _estado(self):
        return self.__estado

    @_estado.setter
    def _estado(self, value):
        self.__estado = value
        
    
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "detalle": self.__detalle,
            "estado": self.__estado,
            "idRol": self.__idRol
        }
    
    @classmethod
    def deserializar(self, data):
        permiso = Permiso()
        permiso._id = data["id"]
        permiso._nombre = data["nombre"]
        permiso._detalle = data["detalle"]
        permiso._estado = data["estado"]
        permiso._idRol = data["idRol"]
        return permiso


    