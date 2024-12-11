from infraestructure.connection import Connection

class Logger:
    def __init__(self, conn : Connection) -> None:
        self.__conn = conn

    def register_log(self, message):
        try:
            sql = "INSERT INTO log (message) VALUES (%s)"
            self.__conn.execute(sql, (message,))
            self.__conn.commit()
        except Exception as e:
            print(f"[ERROR] No se pudo registrar el log: {e}")
