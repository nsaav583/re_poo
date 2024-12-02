import bcrypt

class User:
    def __init__(self) -> None:
        self.__id = -1
        self.__name: str = ""
        self.__password: str = ""
        

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str):
        self.__name = name

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
