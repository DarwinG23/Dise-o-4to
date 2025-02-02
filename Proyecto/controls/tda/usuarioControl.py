from controls.dao.daoAdapter import DaoAdapter
from models.usuario import Usuario
from controls.tda.administradorControl import AdministradorControl
from controls.tda.estudianteControl import EstudianteControl
from controls.tda.docenteControl import DocenteControl

class UsuarioControl(DaoAdapter):
    def __init__(self):
        super().__init__(Usuario)
        self.__usuario = None

    @property
    def _usuario(self):
        if self.__usuario is None:
            self.__usuario = Usuario()
        return self.__usuario

    @_usuario.setter
    def _usuario(self, value):
        self.__usuario = value
        
    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        return self._save(self._usuario)
    
    def merge(self, pos):
        self._merge(self._usuario, pos)
        
        
    def crearUsuario(self, nombre, apellido, ci, fechaNacimiento, telefono, direccion):
        self._usuario._nombre = nombre
        self._usuario._apellido = apellido
        self._usuario._ci = ci
        self._usuario._fechaNacimiento = fechaNacimiento #IMPORTANTE EL FORMATO ES DD/MM/YYYY
        self._usuario._direccion = direccion
        self._usuario._telefono = telefono
        self.save

    def modificarUsuario(self, nombre, apellido, ci, fechaNacimiento, telefono, direccion):
        self._usuario._nombre = nombre
        self._usuario._apellido = apellido
        self._usuario._ci = ci
        self._usuario._fechaNacimiento = fechaNacimiento
        self._usuario._direccion = direccion
        self._usuario._telefono = telefono
        self.save
    
        
    