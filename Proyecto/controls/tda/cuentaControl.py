from controls.dao.daoAdapter import DaoAdapter
from models.cuenta import Cuenta
from controls.tda.cursoControl import CursoControl
from controls.tda.docenteControl import DocenteControl
from controls.tda.estudianteControl import EstudianteControl
from controls.tda.linked.linkedList import Linked_List
from controls.tda.usuarioControl import UsuarioControl

class CuentaControl(DaoAdapter):
    def __init__(self):
        super().__init__(Cuenta)
        self.__cuenta = None

    @property
    def _cuenta(self):
        if self.__cuenta is None:
            self.__cuenta = Cuenta()
        return self.__cuenta

    @_cuenta.setter
    def _cuenta(self, value):
        self.__cuenta = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._cuenta)
    
    def merge(self, pos):
        self._merge(self._cuenta, pos)
        
        
    def crearCuenta(self, correo, contrasena, id):
        #SEGUNDO CREAMOS LA CUENTA
        self._cuenta._correo = correo
        self._cuenta._contrasena = contrasena
        self._cuenta._estado = 1
        self._cuenta._idUsuario = id
        self.save
        
    def iniciarSesion(self, correo, contrasena):
        cuenta = self._list().binary_search_models(correo, "_correo")
        rol = False
        if cuenta == -1:
            logueado = -1
        elif cuenta._contrasena == contrasena:
            logueado = 1
            roles = cuenta._roles
            admin = roles.binary_search_models("Administrador", "_nombre")
            docente = roles.binary_search_models("Docente", "_nombre")
            estudiante = roles.binary_search_models("Estudiante", "_nombre")
            
            if admin != -1:
                rol = "Administrador"
            elif docente != -1:
                rol = "Docente"
            elif estudiante != -1:
                rol = "Estudiante"
            uc = UsuarioControl()
            usuario = uc._list().binary_search_models(cuenta._idUsuario, "_id")
            
            cursos = Linked_List()
            cc = CursoControl()
            if rol == "Docente" or rol == "Estudiante":
                if rol == "Docente":
                    dc = DocenteControl()
                    docente = dc._list().binary_search_models(cuenta._idUsuario, "_idUsuario")
                    cursos = cc._list().lineal_binary_search_models(docente._id, "_idDocente")
                else:
                    ec = EstudianteControl()
                    estudiantes = ec._list().lineal_binary_search_models(str(cuenta._idUsuario), "_idUsuario")
                    estudiantes = estudiantes.toArray
                    for est in estudiantes:
                        curso = cc._list().binary_search_models(est._idCurso, "_id")
                        cursos.addNode(curso)
                    
                    
            tiene = "Falso"                    
            if cursos._length > 1:
                tiene = "Verdadero"
                
            
            return logueado, rol, cursos, tiene, rol, usuario._nombre, usuario._apellido
        else:
            logueado = 0
            
        return logueado, rol, None, None, None, None, None
        
        
    
    

    