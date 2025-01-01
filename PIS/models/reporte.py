from controls.circular_errors.reporteAsignacion import ReporteAsignacion

class Reporte:
    def __init__(self):
        self.__id = 0
        self.__cedulaEstudiante = ""
        self.__nota = 0
        self.__asistencia = 0
        self.__codigoUnidad = 0
        self.__codigoMateria = 0
        self.__numMatricula = 0
        self.__idAsignacion = 0

    @property
    def _idAsignacion(self):
        return self.__idAsignacion

    @_idAsignacion.setter
    def _idAsignacion(self, value):
        self.__idAsignacion = value


    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value

    @property
    def _cedulaEstudiante(self):
        return self.__cedulaEstudiante

    @_cedulaEstudiante.setter
    def _cedulaEstudiante(self, value):
        self.__cedulaEstudiante = value

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
    def _codigoUnidad(self):
        return self.__codigoUnidad

    @_codigoUnidad.setter
    def _codigoUnidad(self, value):
        self.__codigoUnidad = value

    @property
    def _codigoMateria(self):
        return self.__codigoMateria

    @_codigoMateria.setter
    def _codigoMateria(self, value):
        self.__codigoMateria = value

    @property
    def _numMatricula(self):
        return self.__numMatricula

    @_numMatricula.setter
    def _numMatricula(self, value):
        self.__numMatricula = value
    
    @property
    def serializable(self):
        return {
            "id": self.__id,
            "cedulaEstudiante": self.__cedulaEstudiante,
            "nota": self.__nota,
            "asistencia": self.__asistencia,
            "codigoUnidad": self.__codigoUnidad,
            "codigoMateria": self.__codigoMateria,
            "numMatricula": self.__numMatricula,
            "idAsignacion": self.__idAsignacion
        }
    
    @classmethod
    def deserializar(self, data):
        reporte = Reporte()
        reporte._id = data["id"]
        reporte._cedulaEstudiante = data["cedulaestudiante"]
        reporte._nota = data["nota"]
        reporte._asistencia = data["asistencia"]
        reporte._codigoUnidad = str(data["codigounidad"])
        reporte._codigoMateria = data["codigomateria"]
        reporte._numMatricula = data["nummatricula"]
        reporte._idAsignacion = data["idasignacion"]
        return reporte
    
    def __str__(self):
        return "Reporte: " + " " +str(self._codigoMateria) + "CedulaEstu:" + str(self._cedulaEstudiante) + "CodigoU: " + str(self._codigoUnidad)


    

