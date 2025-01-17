from controls.tda.linked.linkedList import Linked_List
#En este caso importamos permisos porque es un atributo de la clase Rol
from controls.tda.permisoControl import PermisoControl
  

class Rol:
    #Constructor de la clase
    def __init__(self):
        #Atributos de la clase
        self.__id = 0
        self.__nombre = ""
        self.__detalle = ""
        self.__estado = ""
        self.__idCuenta = 0
        self.__permisos = Linked_List()
        
    #Getters y Setters de los atributos
    @property
    def _idCuenta(self):
        return self.__idCuenta

    @_idCuenta.setter
    def _idCuenta(self, value):
        self.__idCuenta = value
        
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
    def _permisos(self):
        return self.__permisos

    @_permisos.setter
    def _permisos(self, value):
        self.__permisos = value
        
    #Aqui van los metodos
    
    #Agregar,Modificar,Eliminar etc
    
    #Serializamos para subir a la base sin el atributo permisos porque no es necesario
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "detalle": self.__detalle,
            "estado": self.__estado,
            "idCuenta": self.__idCuenta
        }
    
    #Al deserializar si es necesario hacer una consulta a la bdd para obtener los permisos del rol
    @classmethod
    def deserializar(self, data):
        rol = Rol()
        rol._id = data["id"]
        rol._nombre = data["nombre"] #IMPORTANTE: Al escribir entre los corchetes [] se escribe todo en minusculas
        rol._detalle = data["detalle"]
        rol._estado = data["estado"]
        rol._idCuenta = data["idcuenta"]
        #Consulta a la bdd para obtener los permisos del rol
        pc = PermisoControl()
        if pc._list().isEmpty:
            permisos = Linked_List()
        else:
            permisos = pc._list() #Obtenermos todos los permisos de la bdd
            permisos = permisos.lineal_binary_search_models(str(rol._id),"_idRol") #IMPORTANTE: Buscamos los permisos del rol
            #IMPORTANTE: al buscar debemos colocar un guion bajo "_" seguido del nombre del atributo como se ve "_idRol"
        rol._permisos = permisos
        return rol
    
    def __str__(self):
        return f"Id: {self.__id}, Nombre: {self.__nombre}, Detalle: {self.__detalle}, Estado: {self.__estado}, IdCuenta: {self.__idCuenta}"

    