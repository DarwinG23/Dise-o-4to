
class Cuenta:
    def __init__(self):
        self.__id = 0
        self.__correo = ""
        self.__contrasenia = ""
        self.__estado = False
        self.__idPersona = 0

    @property
    def _idPersona(self):
        return self.__idPersona

    @_idPersona.setter
    def _idPersona(self, value):
        self.__idPersona = value


    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value

    @property
    def _correo(self):
        return self.__correo

    @_correo.setter
    def _correo(self, value):
        self.__correo = value

    @property
    def _contrasenia(self):
        return self.__contrasenia

    @_contrasenia.setter
    def _contrasenia(self, value):
        self.__contrasenia = value

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
            "correo": self.__correo,
            "contrasenia": self.__contrasenia,
            "estado": self.__estado,
            "idPersona": self.__idPersona
        }
    
    @classmethod
    def deserializar(cls, dic):
        cuenta = Cuenta()
        cuenta._id = dic["id"]
        cuenta._correo = dic["correo"]
        cuenta._contrasenia = dic["contrasenia"]
        cuenta._estado = dic["estado"]
        #PONER EN LA BASE   
        cuenta._idPersona = dic["idpersona"]
        return cuenta
    
    
    def __str__(self):
        return self.__correo


        

