from infraestructure.connection import Connection
from models.book import Book
from typing import List
import requests
from infraestructure.logs_utils import Logger

class BookRepository:
    def __init__(self, conn: Connection) -> None:
        self.__conn = conn
        # Instancia el Logger una vez en el constructor
        self.logger = Logger(self.__conn)  # ahora puedes usar `self.logger` en todos los métodos
        
    def get_book_by_isbn(self, isbn: str) -> Book:
        # funcion que intenta obtener un libro de la base de datos por ISBN.
        try:
            sql = "SELECT * FROM book WHERE isbn = %s"
            self.__conn.execute(sql, (isbn,))
            result = self.__conn.fetchone()
            if result:
                book = Book()
                book.set_id(result[0])
                book.set_author(result[1])
                book.set_category(result[2])
                book.set_description(result[3])
                book.set_isbn(result[4])
                book.set_num_pag(result[5])
                book.set_title(result[6])
                #print("\n")
                #print(f" ID: {book.get_id()} \n Autor: {book.get_author()} \n Categoría: {book.get_category()} \n Descripción: {book.get_description()} \n ISBN: {book.get_isbn()} \n Numero de paginas: {book.get_num_pag()} \n Título: {book.get_title()}")
                return book
            else:
                self.logger.register_log(f"No se encontró un libro con el ISBN {isbn}.")
                return None
        except Exception as e:
            self.logger.register_log(f"Error al intentar obtener libro con isbn {isbn}: {e}")
            print(f"Error fetching book by ISBN: {e}")
            return None
            
    def get_book_from_api(self, isbn: str) -> Book:
        url = f"https://poo.nsideas.cl/api/libros/{isbn}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                # Obtenemos los datos de la respuesta en formato JSON
                data = response.json()
                # Verificamos si la respuesta contiene los campos clave
                if "titulo" in data and "autor" in data:
                    # Crear un objeto Book usando la respuesta de la API
                    book = Book.from_json(data)
                    return book
                else:
                    self.logger.register_log("No se encontró información completa del libro para ese ISBN.")
            except Exception as e:
                self.logger.register_log(f"Error al procesar la respuesta de la API: {e}")
        else:
            print(f"Error al realizar la solicitud a la API: {response.status_code}")
        return None  

    def create_book(self, book: Book) -> Book: # funcion modificada para lanzar excepciones
            try:
                sql = "INSERT INTO book (author, category, description, isbn, num_pag, title) VALUES (%s, %s, %s, %s, %s, %s)"
                self.__conn.execute(sql, (
                    book.get_author(), 
                    book.get_category(),
                    book.get_description(),
                    book.get_isbn(),
                    book.get_num_pag(),
                    book.get_title()
                ))
                # TODO: Obtener el id del booke insertado en base de datos y asignar al objeto
                self.__conn.commit()
            except Exception as e:
                self.logger.register_log(f"Error al agregar un libro a la base de datos: {e}")

    def update_book(self, book: Book) -> Book:
        try:
            sql = "UPDATE book SET author = %s, category = %s, description = %s, isbn = %s, num_pag = %s, title = %s WHERE id = %s"
            self.__conn.execute(sql, (
                book.get_author(),
                book.get_category(),
                book.get_description(),
                book.get_isbn(),
                book.get_num_pag(),
                book.get_title(),
                book.get_id()
            ))
            self.__conn.commit()
        except Exception as e:
            self.logger.register_log(f"Error al editar un libro a la base de datos: {e}")
            
    #elimina un libro de la base de datos por id
    def delete_book(self, id: int) -> None:
        try:
            sql = "DELETE FROM Book WHERE id = %s"
            self.__conn.execute(sql, (id))
            self.__conn.commit()
        except Exception as e:
            self.logger.register_log(f"Error al eliminar un libro a la base de datos: {e}")

    #selecciona todos los libros de la base de datos
    def get_all_book(self) -> List[Book]:
        try:
            sql = "SELECT id, author, category, description, isbn, num_pag, title FROM Book"
            self.__conn.execute(sql)
            results = self.__conn.fetchall()
            books = []
            for item in results:
                book = Book()
                book.set_id(item[0])
                book.set_author(item[1])
                book.set_category(item[2])
                book.set_description(item[3])
                book.set_isbn(item[4])
                book.set_num_pag(item[5])
                book.set_title(item[6])
                books.append(book)
            return books
        except Exception as e:
            self.logger.register_log(f"Error al consultar libros a la base de datos: {e}")
            
    #metodo para mostrar información parcial de todos los libros
    
    def books_info(self):
        try:
            books = self.get_all_book()
            print("Estos son los libros con los que cuenta nuestra biblioteca: ")
            print("\n")
            for book in books:
                print(f" ID: {book.get_id()} \n Título: {book.get_title()} \n Categoría: {book.get_category()}")
                print("\n")
        except Exception as e:
            self.logger.register_log(f"Error al agregar un libro a la base de datos: {e}")
            
    #metodo para mostrar la información completa de todos los libros
    def all_books_info(self):
        try:
            books = self.get_all_book()
            print("Estos son los libros con los que cuenta nuestra biblioteca: ")
            print("\n")
            for book in books:
                print(f" ID: {book.get_id()} \n Autor: {book.get_author()} \n Categoría: {book.get_category()} \n Descripción: {book.get_description()} \n ISBN: {book.get_isbn()} \n Numero de paginas: {book.get_num_pag()} \n Título: {book.get_title()}")
                print("\n")
        except Exception as e:
            self.logger.register_log(f"Error al agregar un libro a la base de datos: {e}")

    #valida que el isbn ingresado por el usuario sea valido
    def valid_isbn(self, isbn: str) -> bool:
        sql = "SELECT isbn FROM Book WHERE isbn = %s"
        self.__conn.execute(sql, (isbn,))
        result = self.__conn.fetchone()
        return result is not None #esto devuelve true si encuentra un isbn valido en la base de datos
        
    # funcion usada en el main.py para ingresar datos de un libro con input (refactorización)
    def get_book_input(self):
        print("Ingrese a continuación los siguientes datos del libro que desea crear")
        author = input("autor: ")
        category = input("categoria: ")
        description = input("descripción: ")
        while True:
            isbn = input("codigo ISBN (formato correcto 12-45 o 1245): ")
            if isbn:  # verifica que no esté vacio
                break
            else:
                print("El ISBN no puede estar vacío. Por favor, ingrese un código válido.")

        while True:
            try:
                num_pag = int(input("Número de páginas: "))
                break
            except ValueError:
                self.logger.register_log("Por favor, ingrese un número válido para el número de páginas.")
        title = input("titulo: ")
        book = Book()
        book.set_author(author)
        book.set_category(category)
        book.set_description(description)
        book.set_isbn(isbn)
        book.set_num_pag(num_pag)
        book.set_title(title)
        return book

    def get_book_input_for_editing(self):
        # Solicita el ID del libro a editar
        while True:
            try: #con try validamos que sea un entero y con valid_isbn validamos que el isbn se encuentre en la base de datos
                book_isbn = input("Ingrese el ISBN del libro que desea editar: ")
                if self.valid_isbn(book_isbn) is False:
                    print(f"No se encontró un libro con el ISBN {book_isbn}. Intente con otro ISBN.")
                    continue
                break
            except ValueError:
                self.logger.register_log("El ISBN debe ser un texto. Intente nuevamente.")

        book = self.get_book_input() #llama al metodo que pide todos los datos menos id
        book.set_isbn(book_isbn) #a ese objeto instanciado le agrega el id que previamente validamos
        return book
