from controls.tda.queque.quequeOperation import QuequeOperation

#Encuapsulamos para que no se vean esos metodos que no pertenecen a stack, PATRON DE DEISEÑO FACADE
class QueQue():
    def __init__(self, top):
        self.__queque = QuequeOperation(top)

    def queque(self, data):
        self.__queque.queque(data)

    @property
    def dequeque(self):
        return self.__queque.dequeque
    
    @property
    def print(self):
        self.__queque.print
    
    @property
    def verifyTop(self):
        return self.__queque.verifyTop

    @property
    def isEmpty(self):
        self.__queque.isEmpty
    
    @property
    def serializable(self):
        return self.__queque.serializable
    
    @property
    def print(self):
        self.__queque.print

    @property
    def _top(self):
        return self.__queque._top
    
    @_top.setter
    def _top(self, value):
        self.__queque._top = value

    
    def deserializar(self, data):
        new_queque = QueQue(self.__queque.deserializar(data)._length)
        for i in range(self.__queque.deserializar(data)._length):
            new_queque.queque(self.__queque.deserializar(data).getData(i))
        return new_queque

    