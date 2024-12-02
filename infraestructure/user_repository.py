from infraestructure.connection import Connection
from models.user import User
from typing import List

class UserRepository:
    def __init__(self, conn: Connection) -> None:
        self.__conn = conn

    def get_user_by_id(self, user_id: int) -> User:
        sql = "SELECT id, name, email FROM User WHERE id = %s"
        self.__conn.execute(sql, (user_id))
        result = self.__conn.fetchone()
        user = User()
        user.set_id(result[0])
        user.set_name(result[1])
        user.set_email(result[2])
        # TODO: Realizar validacion para que retorne none cuando no exista el usuario
        return user

   # Funcion para insertar un usuario y contraseña en la tabla User, encriptar contraseña y almacenar en la base de datos (probar)
    def create_user(self, user: User) -> User:
        # consulta sql para insertar usuario y contraseña
        sql = "INSERT INTO User (usuario, password) VALUES (%s, %s)"
        self.__conn.execute(sql, (
            user.get_usuario(), 
            user._hash_password_()
        ))
 # Obtener el id del cliente insertado en base de datos y asignar al objeto
        user_id = self.__conn.lastrowid
        user.set_id(user_id)
        self.__conn.commit()
        return user

    # TODO: update
    def update_user(self, user: User) -> User:
        sql = "UPDATE User SET name = %s, email = %s WHERE id = %s"
        self.__conn.execute(sql, (
            user.get_name(),
            user.get_email(),
            user.get_id()
        ))
        self.__conn.commit()
        return user

    # TODO: delete
    def delete_user(self, id: int) -> None:
        sql = "DELETE FROM User WHERE id = %s"
        self.__conn.execute(sql, (id))
        self.__conn.commit()

    # TODO: Select all
    def get_all_user(self) -> List[User]:
        sql = "SELECT id, name, email FROM User"
        self.__conn.execute(sql)
        results = self.__conn.fetchall()
        users = []
        for item in results:
            user = User()
            user.set_id(item[0])
            user.set_name(item[1])
            user.set_email(item[2])
            users.append(user)
        return users
