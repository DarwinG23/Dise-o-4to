import sys
sys.path.append('../')
from controls.tda.linked.linkedList import Linked_List
from controls.usuarios.docenteDaoControl import DocenteControl
from controls.usuarios.estudianteDaoControl import EstudianteControl
from controls.login.cuentaDaoControl import CuentaDaoControl
from controls.academico.mallaCurricularControl import MallaCurricularControl
from controls.academico.cicloControl import CicloControl
from controls.login.personaDaoControl import PersonaDaoControl
from controls.login.rolDaoControl import RolDaoControl
from controls.seguimiento.asignacionControl import AsignacionDaoControl
from controls.academico.materiaControl import MateriaControl
from controls.seguimiento.unidadControl import UnidadControl
from controls.administrativo.cursaControl import CursaControl
from controls.administrativo.periodoAcademicoControl import PeriodoAcademicoControl
from controls.seguimiento.reporteControl import ReporteControl
from models.persona import Persona
from controls.connection.connection import Connection

dc = DocenteControl()
ec = EstudianteControl()
cc = CuentaDaoControl()
mc = MallaCurricularControl()
cic = CicloControl()
pc = PersonaDaoControl()  # Instanciar correctamente
rc = RolDaoControl()
mac = MateriaControl()
ac = AsignacionDaoControl()
uc = UnidadControl()
pac = PeriodoAcademicoControl()
cuc = CursaControl()
rec = ReporteControl()
con = Connection()

try:
   
   pass
   # rec._reporte._cedulaEstudiante = "1108853832"
   # rec._reporte._nota = 5.3
   # rec._reporte._asistencia = 70
   # rec._reporte._codigoUnidad = "3001"
   # rec._reporte._codigoMateria = "2464"
   # rec._reporte._numMatricula = 3
   # rec._reporte._idAsignacion = 1
   # rec.save
   
   
   # uc._unidad._nombre = "SQL"
   # uc._unidad._codigo = "5521"
   # uc._unidad._estado = 1
   # uc._unidad._asignacion = 1
   # uc._unidad._fecha_inicio = "03/06/2022"
   # uc._unidad._fecha_limite = "03/08/2022"
   # uc._unidad._numero = 3
   # uc.save
   
   # ec._estudiante._colegioProcedencia = "Bernardo Valdiviezo"
   # ec._estudiante._asistencia = 95
   # ec._estudiante._idPersona = 3
   # ec._estudiante._nota = 9.2
   # ec.save

   # cuc._cursa._idEstudiante = 2
   # cuc._cursa._asignacion = 1
   # cuc._cursa._periodoAcademico = 2
   # cuc._cursa._paralelo = "B"
   # cuc.save
   
   # pac._periodo_academico._fecha_inicio = "01/10/2021"
   # pac._periodo_academico._fecha_fin = "10/11/2022"
   # pac.save

   # mc._mallaCurricular._nombre = "Ingenieria en Sistemas"
   # mc._mallaCurricular._descripcion = "Malla Curricular de Ingenieria en Sistemas"
   # mc._mallaCurricular._vigencia = 1
   # mc.save

   cic._ciclo._descripcion = "Ciclo 1"
   cic._ciclo._vigencia = 1
   cic._ciclo._malla_curricular = 1
   cic.save
   
   # dc._docente._titulo = "Ingeniero en Sistemas"
   # dc._docente._cubiculo = "A-1"
   # dc._docente._tipoContrato = "Contrato"
   # dc._docente._idPersona = 1
   # dc.save
   
   # mac._materia._nombre = "Base de Datos"
   # mac._materia._codigo = "2464"
   # mac._materia._horas = 275
   # mac.save
   
   # ac._asignacion._numero_unidades = 3
   # ac._asignacion._cedula_docente = "1106006123"
   # ac._asignacion._id_materia = 1
   # ac.save
   
   # pc._persona._apellido = "Sanchez"
   # pc._persona._nombre = "Alexander"
   # pc._persona._dni = "1104753890"
   # pc._persona._fechaNacimiento = "08/10/2003"
   # pc._persona._numTelefono = "0959681192"
   # pc.save

   # cc._cuenta._correo = "alexander.a.sanchez@unl.edu.ec"
   # cc._cuenta._contrasenia = "alex123"
   # cc._cuenta._idPersona = 1
   # cc._cuenta._estado = 1
   # cc.save

   # rc._rol._nombre = "Estudiante"
   # rc._rol._descripcion = "Rol de Estudiante"
   # rc._rol._estado = 1
   # rc._rol._idPersona = 1
   # rc.save
   
   
   
   
   
   
   
   # lista = pc._list()
   # print("^^^^^^^^^^^^^^^^^^^^^^^^^")
   # lista.print
   # persona = lista.binary_search_models("2", "_id")
   # print("ROLES DE LA PERSONA")
   # persona._roles.print
   # print(lista._length)
   
   #ARREGLAR DESERIALIZAR CUENTA
   # listaCuenta = cc._list()
   # listaCuenta.print
   
   #EDITANDO PERSONA
   # pc._persona._apellido = "Torres"
   # pc._persona._nombre = "Alejandro"
   # pc._persona._dni = "1104526352"
   # pc._persona._fechaNacimiento = "10/04/1994"
   # pc._persona._numTelefono = "0987654321"
   # pc._persona._idCuenta = 2
   # pc._merge(pc._persona, 1)
   #lista.sort_models("_nombre", 1)
   #lista.print   
   # connection = Connection()
   # connection.connect("USUARIO_DBA", "1104753890", "XE")


except Exception as error:
   print(error)