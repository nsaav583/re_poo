import json

class Book:
    def __init__(self) -> None:
        self.__id: int = -1
        self.__author: str = ""
        self.__category: str = ""
        self.__description: str = ""
        self.__isbn: int = ""
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

    def get_isbn(self) -> int:
        return self.__isbn
    
    def set_isbn(self, isbn: int):
        self.__isbn = isbn

    def get_num_pag(self) -> int:
        return self.__num_pag
    
    def set_num_pag(self, num_pag: int):
        self.__num_pag = num_pag

    def get_title(self) -> str:
        return self.__title
    
    def set_title(self, title: str):
        self.__title = title

    #def to_json(self): (sacar del github del profe) #falta implementar
        #return 
        #pass
        
    #def from_json(data): -> 'Libro':
        #data_dict = json.loads(data)
        #return Libro(**data_dict)
