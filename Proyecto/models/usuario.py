from flask_login import UserMixin
class Usuario(UserMixin):
    def __init__(self):
        self.__id = 0
        self.__nombre = ""
        self.__apellido = ""
        self.__ci = ""
        self.__fechaNacimiento = ""
        self.__direccion = ""
        self.__telefono = ""
        
    def get_id(self):
        return str(self.__id)  


    def get_nombre(self):
        return self.__nombre

    def get_apellido(self):
        return self.__apellido

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
    def _apellido(self):
        return self.__apellido

    @_apellido.setter
    def _apellido(self, value):
        self.__apellido = value

    @property
    def _ci(self):
        return self.__ci

    @_ci.setter
    def _ci(self, value):
        self.__ci = value

    @property
    def _fechaNacimiento(self):
        return self.__fechaNacimiento

    @_fechaNacimiento.setter
    def _fechaNacimiento(self, value):
        self.__fechaNacimiento = value

    @property
    def _direccion(self):
        return self.__direccion

    @_direccion.setter
    def _direccion(self, value):
        self.__direccion = value

    @property
    def _telefono(self):
        return self.__telefono

    @_telefono.setter
    def _telefono(self, value):
        self.__telefono = value
        
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "apellido": self.__apellido,
            "ci": self.__ci,
            "fechaNacimiento": self.__fechaNacimiento,
            "direccion": self.__direccion,
            "telefono": self.__telefono
        }
        
    @classmethod
    def deserializar(self, data):
        usuario = Usuario()
        usuario._id = data["id"]
        usuario._nombre = data["nombre"]
        usuario._apellido = data["apellido"]
        usuario._ci = data["ci"]
        usuario._fechaNacimiento = data["fechanacimiento"]
        usuario._direccion = data["direccion"]
        usuario._telefono = data["telefono"]
        return usuario 
    
    def __str__(self):
        return str(self._nombre) + " " + str(self._apellido) + " " + str(self._id)
        

        
    
        