from controls.tda.linked.linkedList import Linked_List
from models.cursa import Cursa
from models.persona import Persona
from models.rol import Rol

from controls.login.personaDaoControl import PersonaDaoControl
from controls.login.rolDaoControl import RolDaoControl
from controls.administrativo.cursaControl import CursaControl

class Estudiante(Persona):
    def __init__(self):
        super().__init__()
        self.__nota = ""
        self.__asistencia = ""
        self.__colegioProcedencia = ""
        self.__cursas = Linked_List()
        self.__idPersona = 0

    @property
    def _idPersona(self):
        return self.__idPersona

    @_idPersona.setter
    def _idPersona(self, value):
        self.__idPersona = value


    @property
    def _cursas(self):
        return self.__cursas

    @_cursas.setter
    def _cursas(self, value):
        self.__cursas = value

    @property
    def _nota(self):
        return self.__nota

    @_nota.setter
    def _nota(self, value):
        self.__nota = value

    @property
    def _asistencia(self):
        return self.__asistencia

    @_asistencia.setter
    def _asistencia(self, value):
        self.__asistencia = value

    @property
    def _colegioProcedencia(self):
        return self.__colegioProcedencia

    @_colegioProcedencia.setter
    def _colegioProcedencia(self, value):
        self.__colegioProcedencia = value
    
    @property
    def serializable(self):
        data = super().serializable
        
        data.update({
            "promedio": self.__nota,
            "asistencia": self.__asistencia,
            "colegioProcedencia": self.__colegioProcedencia,
            "idPersona": self.__idPersona,
            #"cursas": self.__cursas.serializable
        })
        return data
    
    def deserializar(data):
        estudiante = Estudiante()
        personas = PersonaDaoControl()._list()
        persona = personas.binary_search_models(str(data["idpersona"]), "_id")
        estudiante._id = data["id"]
        if persona != -1:
            estudiante._dni = persona._dni
            estudiante._nombre = persona._nombre
            estudiante._apellido = persona._apellido
            estudiante._fechaNacimiento = persona._fechaNacimiento
            estudiante._numTelefono = persona._numTelefono
            #HACER CONSULTA
            rc = RolDaoControl()
            if rc._list().isEmpty:
                roles = Linked_List()
            else:
                roles = rc._list()
                roles = roles.lineal_binary_search_models(str(persona._id),"_idPersona")
            estudiante._roles = roles
        estudiante._idPersona = data["idpersona"]
        estudiante._nota = data["promedio"]
        estudiante._asistencia = data["asistencia"]
        estudiante._colegioProcedencia = data["colegioprocedencia"]
        cc = CursaControl()
        if cc._list().isEmpty:
            cursas = Linked_List()
        else:
            cursas = cc._list()
            cursas = cursas.lineal_binary_search_models(str(estudiante._id),"_idEstudiante")
        estudiante._cursas = cursas
        return estudiante
    
    
    def __str__(self):
        return str(super()._id) + " " + super()._nombre 



