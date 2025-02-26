from controls.tda.linked.node import Node
from controls.exception.linkedEmpty import LinkedEmpty
from controls.exception.arrayPositionException import ArrayPositionException
#from controls.tdaArray import TDAArray
from numbers import Number
from controls.tda.linked.insercion import Insercion
from controls.tda.linked.quicksort import QuickSort
from controls.tda.linked.mergesort import MergeSort
from controls.tda.linked.shellsort import ShellSort
from controls.tda.linked.burbuja import Burbuja

class Linked_List(object):
    def __init__(self):
        self.__head = None
        self.__last = None
        self.__length = 0
    
    

    @property
    def _atype(self):
        return self.__atype

    @_atype.setter
    def _atype(self, value):
        self.__atype = value


    @property
    def _length(self):
        return self.__length

    @_length.setter
    def _length(self, value):
        self.__length = value
 
        
    @property    
    def isEmpty(self):
        return self.__head == None or self._length == 0
    
    def _getFirst_(self, poss):
        if not self.isEmpty:
            return self.__head
        else:
            return "List is Empty"
    
    def _getLast_(self):
        if not self.isEmpty:
            return self.__last
        else:
            return "List is Empty"
        
    def getData(self, poss):
        if self.isEmpty:
           raise LinkedEmpty("List is Empty")
        elif poss < 0 or poss >= self.__length:
            raise ArrayPositionException("Index out of range")
        elif poss == 0:
            return self.__head._data
        elif poss == (self.__length - 1):
            return self.__last._data
        else:
            node = self.__head
            cont = 0
            while cont < poss:
                cont += 1
                node = node._next
            return node._data
        

    def getNode(self, poss):
        if self.isEmpty:
           raise LinkedEmpty("List is Empty")
        elif poss < 0 or poss >= self.__length:
            raise ArrayPositionException("Index out of range")
        elif poss == 0:
            return self.__head
        elif poss == (self.__length - 1):
            return self.__last
        else:
            node = self.__head
            cont = 0
            while cont < poss:
                cont += 1
                node = node._next
            return node
            
        
    
    def addFirst(self, data):
        if self.isEmpty:
            node = Node(data)
            self.__head = node
            self.__last = node
            self.__length += 1
        else:
            headOld = self.__head #guarada toda la lista hara ahora
            node = Node(data, headOld)  
            self.__head = node
            self.__length += 1

    def addLast(self, data):
        if self.isEmpty:
            self.addFirst(data)
        else:
            node = Node(data)
            self.__last._next = node 
            self.__last = node
            self.__length += 1

    
    def addNode(self, data, poss = 0):
       
        if poss == 0:
            self.addFirst(data)
        elif poss == self.__length:
            self.addLast(data)
        else:
            node_preview = self.getNode(poss - 1)
            node_actuality = node_preview._next
            node = Node(data, node_actuality)
            node_preview._next = node
            self.__length += 1


    def edit (self, data, poss = 0):
        if poss == 0:

            self.__head._data = data
        elif poss == (self.__length - 1):
            self.__last._data = data
        else:
            node = self.getNode(poss)
            node._data = data


    @property
    def toArray (self):
        array = []
        node = self.__head
        while node != None:
            array.append(node._data)
            node = node._next
        return array
    
    def toList(self, array):
        for i in array:
            self.addLast(i)


    def dicToListLast(self, array_dict, clase):
        for i in range(0, len(array_dict)):
            data = clase.deserializar(array_dict[i])               
            self.addLast(data)
            


    def dicToListFirst(self, array_dict, clase):
        for i in range(0, len(array_dict)):
            a = clase.deserializar(array_dict[i])           
            self.addFirst(a)

            
    
    def delete(self, poss = 0 ):
        if self.isEmpty:
            raise LinkedEmpty("List is Empty")
        elif poss < 0 or poss >= self.__length:
            raise ArrayPositionException("Index out of range")
        elif poss == 0:
            node = self.__head._next
            del self.__head
            self.__head = node
            self.__length -= 1
        elif poss == (self.__length - 1):
            node = self.getNode(self.__length - 2)
            node._next = None
            del self.__last
            self.__last = node
            self.__length -= 1
        else:
            node_previous = self.getNode(poss-1)
            node_next = node_previous._next._next
            node_previous._next = node_next
            self.__length -= 1
        
        

    #serializable
    @property
    def serializable(self):
        array = self.toArray 
        array_dict = []
        for i in range(0, len(array)): 
            array_dict.append(array[i].serializable) 
        return array_dict
    

    @classmethod
    def deserializar(self, array_dict, clase):
        linked = Linked_List()
        linked.dicToListLast(array_dict, clase)
        return linked
    
    @property
    def clear(self):
        self.__head = None
        self.__last = None
        self.__length = 0

    def __str__(self) -> str: #metodo toString    #cometar ctrl+k+c   / ctrl+k+u
        out = ""
        if self.isEmpty:
            out = "List is Empty"
        else:
            node = self.__head
            while node != None:
                out += str(node._data) + " -> "
                node = node._next
        return out
    
    @property
    def print(self):
        node = self.__head
        data = ""
        while node != None :
            data += str(node._data) + "   "
            node = node._next
        print("Lista de datos")
        print(data)
        
    
              
    def sort(self, type = 1, method = 3):
        if self.isEmpty:
            raise LinkedEmpty("List is Empty")
        else:  
            array = self.toArray
            self.clear
            #datos primitivos
            if isinstance(array[0], Number) or isinstance(array[0], str):
                if type == 1:
                    if method == 1:
                        order = Burbuja()
                        array = order.sort_burbuja_number_ascent(array)
                    elif method == 2:
                        order = Insercion()
                        array = order.sort_primitive_ascent(array)
                    elif method == 3:
                        order = QuickSort()
                        array = order.quicksort_numbers_ascent(array, 0, len(array) - 1)
                    elif method == 4:
                        order = MergeSort()
                        array = order.mergeSort_number_ascent(array)
                    elif method == 5:
                        order = ShellSort()
                        array = order.shell_number_ascent(array)

                else:
                    if method == 1:
                        order = Burbuja()
                        array = order.sort_burbuja_number_descent(array)
                    elif method == 2:
                        order = Insercion()
                        array = order.sort_primitive_descent(array)
                    elif method == 3:
                        order = QuickSort()
                        array = order.quicksort_numbers_descent(array, 0, len(array) - 1)
                    elif method == 4:
                        order = MergeSort()
                        array = order.mergeSort_number_descent(array)
                    elif method == 5:
                        order = ShellSort()
                        array = order.shell_number_descent(array)
          
            self.toList(array)

            
    def  sort_models(self, atribute ,type = 1, method = 3):
        if self.isEmpty:
            raise LinkedEmpty("List is Empty")
        else:  
            array = self.toArray
            self.clear
            if isinstance(array[0], object): 
                if type == 1:
                    if method == 1:
                        order = Burbuja()
                        array = order.sort_burbuja_atribute_ascent(array, atribute)                  
                    elif method == 2:
                        order = Insercion()
                        array = order.sort_models_ascent(array, atribute)
                    elif method == 3:
                        order = QuickSort()
                        array = order.quicksort_models_ascent(array, 0, len(array) - 1, atribute)
                    elif method == 4:
                        order = MergeSort()
                        array = order.mergeSort_models_ascent(array, atribute)
                    elif method == 5:
                        order = ShellSort()
                        array = order.shell_models_ascent(array, atribute)
                else:
                    if method == 1:
                        order = Burbuja()
                        array = order.sort_burbuja_atribute_descent(array, atribute)
                    elif method == 2:
                        order = Insercion()
                        array = order.sort_models_descent(array, atribute)
                    elif method == 3:
                        order = QuickSort()
                        array = order.quicksort_models_descent(array, 0, len(array) - 1, atribute)
                    elif method == 4:
                        order = MergeSort()
                        array = order.mergeSort_models_descent(array, atribute)
                    elif method == 5:
                        order = ShellSort()
                        array = order.shell_models_descent(array, atribute)
            self.toList(array)
       
      
    def search_equals(self, data):
        list = Linked_List()
        if self.isEmpty:
            raise LinkedEmpty("List is Empty")
        else:  
            array = self.toArray
            for i in range(0, len(array)):
                if array[i].lower().__contains__(data.lower()):  # < > <= >= !=  == startswith() endswith()
                    list.addNode(array[i], list._length)
        return list
    
    def search_equals_models(self, data, atribute):
        list = Linked_List()
        if self.isEmpty:
            raise LinkedEmpty("List is Empty")
        else:  
            array = self.toArray
            for i in range(0, len(array)):
                if str(getattr(array[i], atribute)).lower().__contains__(data.lower()):
                    list.addNode(array[i], list._length)
        return list
    
    
    def binary_search_number(self, data):
        self.sort()
        arr = self.toArray
        left = 0
        right = len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == data:
                return arr[mid] 
            elif arr[mid] < data:
                left = mid + 1
            else:
                right = mid - 1
        return -1
    
    def lineal_binary_search_number(self, data):
        self.sort()
        arr = self.toArray
        left = 0
        right = len(arr) - 1
        list = Linked_List()
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == data:
                for i in range(left, len(arr)):
                    if arr[i] == data:
                        list.addNode(arr[i], list._length)
                break
            elif arr[mid] < data:
                left = mid + 1
            else:
                right = mid - 1
        return -1
    
    
    #busqueda binaria
    def binary_search_models(self, data, atribute):
        self.sort_models(atribute)
        arr = self.toArray
        left = 0
        right = len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if str(getattr(arr[mid], atribute)).lower() == str(data).lower():
                return arr[mid] 
            elif str(getattr(arr[mid], atribute)).lower() < str(data).lower():
                left = mid + 1
            else:
                right = mid - 1
        return -1   
    
    #busqueda binaria
    def binary_search_models_id(self, data, atribute):
        self.sort_models(atribute)
        arr = self.toArray
        left = 0
        right = len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            attribute_value = getattr(arr[mid], atribute)
            if attribute_value is None:
                attribute_value = 0
                
            if int(attribute_value) == int(data):
                return arr[mid] 
            elif int(attribute_value) < int(data):
                left = mid + 1
            else:
                right = mid - 1
        return -1   
    
    
    #busqueda lineal-binaria
    def lineal_binary_search_models(self, data, atribute):       
        self.sort_models(atribute)
        arr = self.toArray
        left = 0
        right = len(arr) - 1
        list = Linked_List()
        
        
        while left <= right:
            mid = (left + right) // 2
            if str(getattr(arr[mid], atribute)).lower() == str(data).lower():  
                for i in range(left, len(arr)):
                    if str(getattr(arr[i], atribute)).lower() == str(data).lower():  
                        list.addNode(arr[i], list._length)         
                break                  
            elif str(getattr(arr[mid], atribute)).lower() < data.lower():
                left = mid + 1
            else:
                right = mid - 1
        return list
    
     #busqueda lineal-binaria por id
    def lineal_binary_search_models_id(self, data, atribute):       
        self.sort_models(atribute)
        arr = self.toArray
        left = 0
        right = len(arr) - 1
        list = Linked_List()
        
        
        while left <= right:
            mid = (left + right) // 2
            if int(getattr(arr[mid], atribute)) == int(data):  
                for i in range(left, len(arr)):
                    if int(getattr(arr[i], atribute)) == int(data):  
                        list.addNode(arr[i], list._length)         
                break                  
            elif int(getattr(arr[mid], atribute)) < int(data):
                left = mid + 1
            else:
                right = mid - 1
        return list
    
    #menores
    def search_lower(self, data):
        list = Linked_List()
        if self.isEmpty:
            raise LinkedEmpty("List is Empty")
        else:  
            array = self.toArray
            for i in range(0, len(array)):
                if array[i].lower() < data.lower():  # < > <= >= !=  == startswith() endswith()
                    list.addNode(array[i], list._length)
        return list 
     
 
        
    def search_lower_models(self, data, atribute):
        list = Linked_List()
        if self.isEmpty:
            raise LinkedEmpty("List is Empty")
        else:  
            array = self.toArray
            for i in range(0, len(array)):
                original = self.convertir(str(getattr(array[i], atribute)))
                data = self.convertir(str(data))
                
                if getattr(array[i], atribute) < data:
                    list.addNode(array[i], list._length)
        return list
    

    def convertir(self, valor):
        try:
            return float(valor)
        except ValueError:
            return valor