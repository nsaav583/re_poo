import json

class Book:
    def __init__(self) -> None:
        self.__id: int = -1
        self.__author: str = ""
        self.__category: str = ""
        self.__description: str = ""
        self.__isbn: str = ""
        self.__num_pag: int = ""
        self.__title: str = ""
        # self.__disponibilidad: # falta definir tipo para dispinibilidad
    
    def get_id(self) -> int:
        return self.__id
    
    def set_id(self, id: int):
        self.__id = id

    def get_author(self) -> str:
        return self.__author
    
    def set_author(self, author: str):
        self.__author = author

    def get_category(self) -> str:
        return self.__category
    
    def set_category(self, category: str):
        self.__category = category

    def get_description(self) -> str:
        return self.__description
    
    def set_description(self, description: str):
        self.__description = description

    def get_isbn(self) -> str:
        return self.__isbn
    
    def set_isbn(self, isbn: str):
        self.__isbn = isbn

    def get_num_pag(self) -> int:
        return self.__num_pag
    
    def set_num_pag(self, num_pag: int):
        self.__num_pag = num_pag

    def get_title(self) -> str:
        return self.__title
    
    def set_title(self, title: str):
        self.__title = title

    def to_json(self):
        return {
            "autor": self.__author, # Asigna el autor del libro
            "categorias": self.__category.split(", "), # Convierte las categorías (cadena) en una lista de categorías
            "descripcion": self.__description, # Asigna la descripción del libro
            "isbn": self.__isbn, # Asigna el ISBN del libro
            "numero_paginas": self.__num_pag, # Asigna el número de páginas del libro
            "titulo": self.__title # Asigna el título del libro
        }
        
    # Método estático para deserializar el JSON a un objeto Libro
    @staticmethod
    def from_json(data: str) -> 'Book':
        book = Book()
        book.set_author(data.get("autor", ""))
        book.set_category(", ".join(data.get("categorias", [])))  # Une las categorías con ", " en una sola cadena
        book.set_description(data.get("descripcion", ""))
        book.set_isbn(data.get("isbn", ""))
        book.set_num_pag(data.get("numero_paginas", 0)) # Asigna el número de páginas, por defecto 0
        book.set_title(data.get("titulo", ""))
        return book
