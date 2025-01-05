from controls.tda.linked.linkedList import Linked_List
from controls.tda.recomendacionControl import RecomendacionControl
from controls.tda.cursoControl import CursoControl
from controls.tda.asignacionControl import AsignacionControl

class Docente:
    def __init__(self):
        self.__id = 0 
        self.__titulo = ""
        self.__idUsuario = 0
        self.__recomendaciones = Linked_List()
        self.__cursos = Linked_List()
        self.__asignaciones = Linked_List()

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
    def _idUsuario(self):
        return self.__idUsuario

    @_idUsuario.setter
    def _idUsuario(self, value):
        self.__idUsuario = value

    @property
    def _recomendaciones(self):
        return self.__recomendaciones

    @_recomendaciones.setter
    def _recomendaciones(self, value):
        self.__recomendaciones = value

    @property
    def _cursos(self):
        return self.__cursos

    @_cursos.setter
    def _cursos(self, value):
        self.__cursos = value

    @property
    def _asignaciones(self):
        return self.__asignaciones

    @_asignaciones.setter
    def _asignaciones(self, value):
        self.__asignaciones = value
        
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "titulo": self.__titulo,
            "idUsuario": self.__idUsuario
        }
    @classmethod
    def deserializar(cls, data):
        docente = Docente()
        docente._id = data["id"]
        docente._titulo = data["titulo"]
        docente._idUsuario = data["idUsuario"]
        return docente
   
    
    @classmethod
    def deserializar(self, data):
        docente = Docente()
        docente._id = data["id"]
        docente._titulo = data["titulo"]
        docente._idUsuario = data["idusuario"]
        rc = RecomendacionControl()
        cc = CursoControl()
        if cc._list().isEmpty:
            cursos = Linked_List()
        else:
            cursos = cc._list()
            cursos = cursos.lineal_binary_search_models(str(docente._id),"_idDocente")
        docente._cursos = cursos
        if rc._list().isEmpty:
            recomendaciones = Linked_List()
        else:
            recomendaciones = rc._list()
            recomendaciones = recomendaciones.lineal_binary_search_models(str(docente._id),"_idDocente")
        return docente
        