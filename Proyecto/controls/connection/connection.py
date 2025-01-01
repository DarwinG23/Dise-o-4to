import cx_Oracle

class Connection:
    def __init__(self):
        self.__db = None
    
    @property
    def _db(self):
        return self.__db

    @_db.setter
    def _db(self, value):
        self.__db = value
    
    def connect(self, user, password, db, host="localhost", port="1521"):
        try:
            dsn = cx_Oracle.makedsn(host, port, service_name=db)
            self.__db = cx_Oracle.connect(user, password, dsn)
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print(f"Error al conectarse a la base de datos: {error.message}")
        return self
    
    def close(self):
        if self.__db:
            self.__db.close()
            print("Conexión cerrada correctamente")
    
