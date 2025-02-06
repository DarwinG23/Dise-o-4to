from controls.tda.linked.linkedList import Linked_List

class Tarea:
    def __init__(self):
        self.__id = 0
        self.__titulo = ""
        self.__descripcion = ""
        self.__estado = ""
        self.__idAsignacion = 0
        self.__ruta_pdf = ""

    @property
    def _ruta_pdf(self):
        return self.__ruta_pdf

    @_ruta_pdf.setter
    def _ruta_pdf(self, value):
        self.__ruta_pdf = value


    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value

    @property
    def _titulo(self):
        return self.__titulo

    @_titulo.setter
    def _titulo(self, value):
        self.__titulo = value

    @property
    def _descripcion(self):
        return self.__descripcion

    @_descripcion.setter
    def _descripcion(self, value):
        self.__descripcion = value

    @property
    def _estado(self):
        return self.__estado

    @_estado.setter
    def _estado(self, value):
        self.__estado = value

    @property
    def _idAsignacion(self):
        return self.__idAsignacion

    @_idAsignacion.setter
    def _idAsignacion(self, value):
        self.__idAsignacion = value
        
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "titulo": self.__titulo,
            "descripcion": self.__descripcion,
            "estado": self.__estado,
            "idAsignacion": self.__idAsignacion,
            "ruta_pdf": self.__ruta_pdf
        }
    
    @classmethod
    def deserializar(self, data):
        tarea = Tarea()
        tarea._id = data["id"]
        tarea._titulo = data["titulo"]
        tarea._descripcion = data["descripcion"]
        tarea._estado = data["estado"]
        tarea._idAsignacion = data["idasignacion"]
        tarea._ruta_pdf = data["ruta_pdf"]
        return tarea

        
    def __str__(self):
        return "ID: " + str(self.__id) + " Titulo: " + str(self.__titulo) + " Descripcion: " + str(self.__descripcion) + " Estado: " + str(self.__estado) + " ID Asignacion: " + str(self.__idAsignacion) + " Ruta PDF: " + str(self.__ruta_pdf)
    