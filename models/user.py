import bcrypt

class User:
    def __init__(self) -> None:
        self.__usuario: str = ""
        self.__password: str = ""
        self.__id = -1

    def get_usuario(self) -> str:
        return self.__usuario

    def set_usuario(self, usuario: str):
        self.__usuario = usuario

    def get_password(self) -> str:
        return self.__password

    def set_password(self, password: str):
        # encripta la contraseña antes de asignarla
        self.__password = self._hash_password(password)

    def _hash_password(self, password: str) -> str:
        # Genera el hash de la contraseña usando bcrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        # devuelve contraseña encriptada
        return hashed_password.decode('utf-8')

    def get_id(self) -> int:
        return self.__id

    def set_id(self, user_id: int):
        self.__id = user_id

    def check_password(self, password: str) -> bool:
        
        # Verifica si la contraseña proporcionada coincide con la encriptada
        
        return bcrypt.checkpw(password.encode('utf-8'), self.__password.encode('utf-8'))
