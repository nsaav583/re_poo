class Libro:
    def __init__(self) -> None:
        self.__id: int = -1
        self.__titulo: str = ""
        self.__autor: str = ""
        self.__isbn: str = ""
        # self.__disponibilidad: # definir tipo para dispinibilidad
    
    def get_id(self):
        return self.__id
    
    def set_id(self, id: int):
        self.__id = id

    def get_titulo(self) -> str:
        return self.__titulo
    
    def set_titulo(self, titulo: str):
        self.__titulo = titulo

    def get_autor(self) -> str:
        return self.__autor
    
    def set_autor(self, autor: str):
        self.__autor = autor

    def get_isbn(self) -> str:
        return self.__autor
    
    def set_isbn(self, isbn: str):
        self.__isbn = isbn
