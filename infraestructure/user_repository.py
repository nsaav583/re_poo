from infraestructure.connection import Connection
from infraestructure.logs_utils import Logger
from models.user import User
import pymysql
import bcrypt 

class UserRepository:
    def __init__(self, conn: Connection) -> None:
        self.__conn = conn
        self.logger = Logger(conn)
    def create_user(self, user: User) -> User:
        try:
    # verificar si el usuario ya existe en la base de datos
            sql_check = "SELECT COUNT(*) FROM User WHERE name = %s"
            self.__conn.execute(sql_check, (user.get_name(),))
            self.__conn.fetchone()
            sql_insert = "INSERT INTO User (name, password) VALUES (%s, %s)"
            self.__conn.execute(sql_insert, (
            user.get_name(),
            user.get_password()
            ))
            self.__conn.commit() # confirmar insercion
            return user
        except pymysql.err.IntegrityError as e:
            self.logger.register_log(f"Error al crear un usuario {user.get_name}: ")
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
                self.logger.register_log(e)
        # Captura errores específicos de la base de datos (ej., problemas de conexión o ejecución de consulta)
                return f"Error de base de datos: {e}"
        except bcrypt.exceptions.BcryptError as e:
                self.logger.register_log(e)
        # Captura cualquier error relacionado con bcrypt
                return f"Error de bcrypt: {e}"
        except Exception as e:
                self.logger.register_log(e)
        # Captura cualquier otro error inesperado
                return f"Ocurrió un error inesperado: {e}"
        
    def get_user_input(self):
        # Validar nombre de usuario
        name = input("Ingrese el nombre del usuario: ").strip()
        while not name:
            print("El nombre no puede estar vacío. ¡Por favor ingresa un nombre!")
            name = input("Ingrese el nombre del usuario: ").strip()
        # Validar contraseña
        password = input("Ingrese la contraseña del usuario: ").strip()
        while not password or len(password) < 6:
            print("La contraseña debe tener al menos 6 caracteres. ¡Intenta de nuevo!")
            password = input("Ingrese la contraseña del usuario: ").strip()
        return name, password
