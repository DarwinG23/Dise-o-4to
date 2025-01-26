class Binary:
    
    #busqueda binaria numeros
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
    
    
    #busqueda binaria modelos
    def binary_search_models(self, data, atribute):
        self.sort_models(atribute)
        arr = self.toArray
        left = 0
        right = len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if getattr(arr[mid], atribute).lower() == data.lower():
                return arr[mid] 
            elif getattr(arr[mid], atribute).lower() < data.lower():
                left = mid + 1
            else:
                right = mid - 1
        return -1 
    
    