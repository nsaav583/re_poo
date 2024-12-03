from infraestructure.connection import Connection
from models.user import User
from typing import List

class UserRepository:
    def __init__(self, conn: Connection) -> None:
        self.__conn = conn

    def get_user_by_id(self, user_id: int) -> User:
        sql = "SELECT id, name FROM User WHERE id = %s"
        self.__conn.execute(sql, (user_id))
        result = self.__conn.fetchone()
        user = User()
        user.set_id(result[0])
        user.set_name(result[1])
        # TODO: Realizar validacion para que retorne none cuando no exista el usuario
        return user

# Funcion para insertar un usuario y contraseña en la tabla User, encriptar contraseña y almacenar en la base de datos (probar)
    def create_user(self, user: User) -> User:
        sql = "INSERT INTO User (name, password) VALUES (%s, %s)"
        self.__conn.execute(sql, (
            user.get_name(),
            user.get_password()
        ))
        # Obtener el id del cliente insertado en base de datos y asignar al objeto
        self.__conn.commit()
        return user

# FUNCION PARA logear usuario, verificar contraseña y/o name, en caso de que el usuario exista en la base de datos imprimir "bienvenido !!!" y en caso de que no imprime "Usuario no encontrado o contraseña incorrecta".
    def login_usuario(self, name: str, password: str) -> User:
        sql = "SELECT id, name, password FROM User WHERE name = %s"
        self.__conn.execute(sql, (name,))
        result = self.__conn.fetchone()
        if result is None:
            return None
        contraseña_guardada = result[2]
        if bcrypt.checkpw(password.encode('utf-8'), contraseña_guardada.encode('utf-8')):
            return User()
        else:
            return None
