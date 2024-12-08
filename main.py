from infraestructure.mysqlconnection import MySQLConnection
from infraestructure.user_repository import UserRepository
from infraestructure.book_repository import BookRepository
from credentials_db import user, password, database, host
from models.user import User
from models.book import Book

conn = MySQLConnection(host, user, password, database)
user_repository = UserRepository(conn)
book_repository = BookRepository(conn)

#menu para la gestión o CRUD de libros
def menu_libros():
    print("Bienvenido a la tienda")
    
    while True:
        try:
            print("\n")
            print("1. Crear un libro")
            print("2. Ver información de todos los libros")
            print("3. Ver información de un libro")
            print("4. Editar un libro")                
            print("5. Eliminar un libro")
            print("6. Volver al menu principal")
            option = input("Ingrese una opción: ")

            if option == "1":
                #ver si se puede refactorizar esta opción
                print("Ingrese a continuación los siguientes datos del libro que desea crear")
                author = input("autor: ")
                category = input("categoria: ")
                description = input("descripción: ")
                isbn = input("codigo ISBN: ")
                num_pag = input("numero de paginas: ")
                title = input("titulo: ")
                book = Book()
                book.set_author(author)
                book.set_category(category)
                book.set_description(description)
                book.set_isbn(isbn)   #si se usa un isbn como 12-45, solo mostrara 12, hay que implementar bien esto
                book.set_num_pag(num_pag)
                book.set_title(title)
                book_repository.create_book(book)
                print("Libro creado con exito")
            elif option == "2":
                book_repository.all_books_info()
            elif option == "3":
                book_repository.books_info()
                id = int(input("Eliga el ID del libro sobre el cual quiera ver toda la información: "))
                if book_repository.valid_id(id) is False: #si el id no se encuentra en la BD, devuelve False y se ejecuta el if
                    print("Debe ingresar un ID valido")
                else:
                    book_repository.get_book_by_id(id)
            elif option == "4":
                book_repository.all_books_info()
                id = int(input("Eliga el ID del libro que desea editar: "))
                if book_repository.valid_id(id) is False:
                    print("Debe ingresar un ID valido")
                else:
                #ver si se puede optimizar y reutilizar el codigo para hacer preguntas, como se hizo en el semestre anterior
                #ver si se puede refactorizar esta opción
                    print("Ingrese a continuación los siguientes datos del libro que desea editar")
                    author = input("autor: ")
                    category = input("categoria: ")
                    description = input("descripción: ")
                    isbn = input("codigo ISBN: ")
                    num_pag = input("numero de paginas: ")
                    title = input("titulo: ")
                    book = Book()
                    book.set_id(id)
                    book.set_author(author)
                    book.set_category(category)
                    book.set_description(description)
                    book.set_isbn(isbn)  
                    book.set_num_pag(num_pag)
                    book.set_title(title)
                    book_repository.update_book(book)
                    print("\n")
                    print("Libro editado correctamente")
            elif option == "5":
                book_repository.all_books_info()
                id = int(input("Ingrese el ID del libro que desea eliminar: "))
                if book_repository.valid_id(id) is None:
                    print("Debe ingresar un ID valido")
                else:
                    book_repository.delete_book(id)
                    print("Libro eliminado correctamente")
            elif option == "6":
                print("\n")
                print("Volviendo al menu principal")
                print("\n")
                return
        except ValueError as e:
                print(e)

# Desplegar menu para gestionar usuarios
while True:
    print("LIBRASTOCK")
    print("1. Registrar un usuario")
    print("2. Iniciar sesión")
    print("3. Salir")
    option = input("Ingrese su opcion: ")
    if(option == "1"):
        name = input("Ingrese el nombre del usuario: ")
        password = input("Ingrese el la contraseña del usuario: ")
        user = User()
        user.set_name(name)
        user.set_password(password)
        user_repository.create_user(user)
        print("Usuario registrado exitosamente.")
    elif(option == "2"):
        name = input("Ingrese el nombre del usuario: ")
        password = input("Ingrese la contraseña del usuario: ")
        user = user_repository.login_user(name, password)
        if user is None:
            print("Usuario no encontrado o contraseña incorrecta.")
        else:
            # Si login_user devuelve un usuario válido se llama la menu de gestión de libros (CRUD)
            print("Bienvenido !!!!.")
            menu_libros()
    elif(option == "3"):
        print("el programa se ha cerrado correctamente")
        break
    else:
        print("debe ingresar una opción valida, entre 1 a 3")


# ESTO ES PARA VER DETALLE DE UN LIBRO Y ALMACENARLO EN LA BASE DE DATOS (debo implementarlo en menu)
# isbn = input("Ingrese ISBN del libro")  # ISBN de ejemplo
# book_repository.obtener_book_desde_api(isbn)
