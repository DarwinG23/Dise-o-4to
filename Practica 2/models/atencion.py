class Atencion:
    def __init__(self):
        self.__id = 0
        self.__dia = ""
        self.__tiempo = ""
        self.__calificacion = ""
        self.__motivo = ""

    @property
    def _motivo(self):
        return self.__motivo

    @_motivo.setter
    def _motivo(self, value):
        self.__motivo = value

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value

    @property
    def _dia(self):
        return self.__dia

    @_dia.setter
    def _dia(self, value):
        self.__dia = value

    @property
    def _tiempo(self):
        return self.__tiempo

    @_tiempo.setter
    def _tiempo(self, value):
        self.__tiempo = value

    @property
    def _calificacion(self):
        return self.__calificacion

    @_calificacion.setter
    def _calificacion(self, value):
        self.__calificacion = value

    @property
    def serializable(self):
        return {
            "id": self.__id,
            "dia": self.__dia,
            "tiempo": self.__tiempo,
            "calificacion": self.__calificacion,
            "motivo": self.__motivo
        }
    
    @classmethod
    def deserializar(self, data):
        atencion = Atencion()
        atencion._id = data["id"]
        atencion._dia = data["dia"]
        atencion._tiempo = data["tiempo"]
        atencion._motivo = data["motivo"]
        atencion._calificacion = data["calificacion"]
        return atencion
    

    def __str__(self):
        return f"ID: {self.__id}, Dia: {self.__dia}, Tiempo: {self.__tiempo}, Calificacion: {self.__calificacion}, Motivo: {self.__motivo}"

    
    
