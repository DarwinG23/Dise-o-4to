import sys
sys.path.append('../')
from controls.atencionControl import AtencionControl
from controls.servidorControl import ServidorControl
from controls.tda.queque.queque import QueQue
from controls.tda.linked.linkedList import Linked_List
import random
import time




atencion = AtencionControl()
servidor = ServidorControl()
cola = QueQue(5)

atencion._atencion._dia = "05/17/2024"
atencion._atencion._tiempo = "2:30"
atencion._atencion._calificacion = "Bueno"
atencion._atencion._motivo = "Consulta"
#atencion.save
cola.queque(atencion._atencion)
atencion._atencion = None

atencion._atencion._dia = "05/17/2024"
atencion._atencion._tiempo = "1:15"
atencion._atencion._calificacion = "Normal"
atencion._atencion._motivo = "Tratamiento"
#atencion.save
cola.queque(atencion._atencion)
atencion._atencion = None

servidor._servidor._nombre = "Maria"
servidor._servidor._apellido = "Torres"
servidor._servidor._cedula = "110551144"
servidor._servidor._atenciones = cola
servidor.save
servidor._servidor = None


# lista = servidor._list()

# lista.print

# listaNueva = lista.lineal_binary_search_models("Sanchez", "_apellido")


# print("Lista Nueva")
# listaNueva.print

#lista de 10 numeros

# lista = Linked_List()
# for i in range(25000):
#     lista.addNode(random.randint(1, 1000))

# lista.addNode(2323)
#lista.print

# listaQ = lista
# listaM = lista
# listaS = lista

# inicioQ = time.time()
# listaQ.sort(1,3)
# finalQ = time.time()

# inicioM = time.time()
# listaM.sort(1,4)
# finalM = time.time()

# inicioS = time.time()
# listaS.sort(1,5)
# finalS = time.time()

#busquedas
#inicioLineal = time.time()
#data = lista.lineal_binary_search_number(1000)
# finLineal = time.time()

# inicioBinaria = time.time()
# data = lista.binary_search_number(2323)
# finBinaria = time.time()




# listaQ.print
# listaM.print
# listaS.print

# print("QuickSort: ", finalQ - inicioQ)
# print("MergeSort: ", finalM - inicioM)
# print("ShellSort: ", finalS - inicioS)
# print("Lineal-binaria: ", finLineal - inicioLineal)
# print("Binaria: ", finBinaria - inicioBinaria)

# lista = servidor._list()

# lista.print

# lista.sort_models("_nombre",2,5)

# lista.print



