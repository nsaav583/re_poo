from infraestructure.connection import Connection
from models.user import User
import pymysql
import bcrypt 

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
        try:
        # verificar si el usuario ya existe en la base de datos
            sql_check = "SELECT COUNT(*) FROM User WHERE name = %s"
            self.__conn.execute(sql_check, (user.get_name(),))
            result = self.__conn.fetchone()
            sql_insert = "INSERT INTO User (name, password) VALUES (%s, %s)"
            self.__conn.execute(sql_insert, (
            user.get_name(),
            user.get_password()
            ))
            self.__conn.commit() # confirmar insercion
            return user
        except pymysql.err.IntegrityError as e:
        # si ocurre un error de duplicado, lanzar una excepcion ValueError personalizada
            raise ValueError(f"El nombre de usuario '{user.get_name()}' ya se encuentra registrado.") from e
    
# FUNCION PARA logear usuario, verificar contraseña y/o name, en caso de que el usuario exista en la base de datos imprimir "bienvenido !!!" y en caso de que no imprime "Usuario no encontrado o contraseña incorrecta".
    def login_user(self, name: str, password: str) -> User:
        try:
            sql = "SELECT id, name, password FROM User WHERE name = %s"
            self.__conn.execute(sql, (name,))
            result = self.__conn.fetchone()
        # Si no se encuentra al usuario
            if result is None:
                return None
        # Obtener la contraseña guardada
            contraseña_guardada = result[2]
        # Verificar la contraseña
            if bcrypt.checkpw(password.encode('utf-8'), contraseña_guardada.encode('utf-8')):
                user = User()
                user.set_id(result[0])
                user.set_name(result[1])
                return user
            else:
            # Si la contraseña no es correcta, retorna none
                return None
        except pymysql.MySQLError as e:
        # Captura errores específicos de la base de datos (p.ej., problemas de conexión o ejecución de consulta)
                return f"Error de base de datos: {e}"
        except bcrypt.exceptions.BcryptError as e:
        # Captura cualquier error relacionado con bcrypt
            return f"Error de bcrypt: {e}"
        except Exception as e:
        # Captura cualquier otro error inesperado
            return f"Ocurrió un error inesperado: {e}"
