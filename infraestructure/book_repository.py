from infraestructure.connection import Connection
from models.book import Book
from typing import List
import requests
import json

class BookRepository:
    def __init__(self, conn: Connection) -> None:
        self.__conn = conn
        
     def obtener_book_desde_api(self, isbn):
        url = f"https://poo.nsideas.cl/api/libros/{isbn}"

        try:
            # hacer solicitud get a la API
            response = requests.get(url)
            response.raise_for_status()  # Lanza una excepción si la solicitud tiene un error

            # imprimir la respuesta completa para inspeccionar #TODO dar formato a la respuesta
            print(f"Respuesta de la API para ISBN {isbn}: {response.text}")

            # asignar formato JSON a la respuesta obtenida anteriormente
            data = response.json()
            # Convertir el JSON a un objeto Book
            # book_json = json.dumps(data)  # Convertir a string JSON #json.dups No lo utilizamos ya que lo enviaremos directo a la base de datos y no hacia una API o archivo
            book = Book.from_json(data)  # Deserializar a un objeto Book
            self.guardar_book_en_database(book)
        except requests.exceptions.RequestException as e:
            print(f"Error al consumir la API: {e}")
            return None
        except ValueError as e:
            print(f"Error al procesar la respuesta de la API: {e}")
            return None
            
    def guardar_book_en_database(self, book):
        try:
            # Verificar si el libro ya existe en la base de datos
            verificar_libro = "SELECT COUNT(*) FROM libros WHERE isbn = %s"
            self.__conn.execute(verificar_libro, (book.get_isbn(),))  # acceso al tributo con get
            result = self.__conn.fetchone()
            if result[0] == 0:
                self.create_book(book)
                self.__conn.commit()
                print(f"Libro con ISBN {book.get_isbn()} almacenado correctamente.")
            else:
                print(f"El libro con ISBN {book.get_isbn()} ya está registrado en la base de datos.")

        except Exception as e:
            print(f"Error al guardar el libro en la base de datos: {e}")
        except Exception as e:
            print(f"Error al guardar el libro en la base de datos: {e}")
            
    def get_book_by_id(self, book_id: int) -> Book:
        sql = "SELECT id, author, category, description, isbn, num_pag, title FROM Book WHERE id = %s"
        self.__conn.execute(sql, (book_id))
        result = self.__conn.fetchone()
        book = Book()
        book.set_id(result[0])
        book.set_author(result[1])
        book.set_category(result[2])
        book.set_description(result[3])
        book.set_isbn(result[4])
        book.set_num_pag(result[5])
        book.set_title(result[6])
        print("\n")
        print(f" ID: {book.get_id()} \n Autor: {book.get_author()} \n Categoría: {book.get_category()} \n Descripción: {book.get_description()} \n ISBN: {book.get_isbn()} \n Numero de paginas: {book.get_num_pag()} \n Título: {book.get_title()}")
        # TODO: Realizar validacion para que retorne none cuando no exista el book
        return book

    # TODO: insert
    def create_book(self, book: Book) -> Book:
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
        return book

    # TODO: update
    def update_book(self, book: Book) -> Book:
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
        return book

    # TODO: delete
    def delete_book(self, id: int) -> None:
        sql = "DELETE FROM Book WHERE id = %s"
        self.__conn.execute(sql, (id))
        self.__conn.commit()

    # TODO: Select all
    def get_all_book(self) -> List[Book]:
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
    
    #metodo para mostrar información parcial de todos los libros
    def books_info(self):
        books = self.get_all_book()
        print("Estos son los libros con los que cuenta nuestra biblioteca: ")
        print("\n")
        for book in books:
            print(f" ID: {book.get_id()} \n Título: {book.get_title()} \n Categoría: {book.get_category()}")
            print("\n")

    #metodo para mostrar la información completa de todos los libros
    def all_books_info(self):
        books = self.get_all_book()
        print("Estos son los libros con los que cuenta nuestra biblioteca: ")
        print("\n")
        for book in books:
            print(f" ID: {book.get_id()} \n Autor: {book.get_author()} \n Categoría: {book.get_category()} \n Descripción: {book.get_description()} \n ISBN: {book.get_isbn()} \n Numero de paginas: {book.get_num_pag()} \n Título: {book.get_title()}")
            print("\n")

    #valida que el id ingresado por el usuario sea valido
    def valid_id(self, id: int) -> bool:
        sql = "SELECT id FROM Book WHERE id = %s"
        self.__conn.execute(sql, (id,))
        result = self.__conn.fetchone()
        return result is not None #esto devuelve true si encuentra un id valido en la base de datos
