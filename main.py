from infraestructure.mysqlconnection import MySQLConnection
from infraestructure.user_repository import UserRepository
from infraestructure.book_repository import BookRepository
from infraestructure.loan_repository import LoanRepository
from infraestructure.logs_utils import Logger
from credentials_db import user, password, database, host
from models.user import User

conn = MySQLConnection(host, user, password, database)
user_repository = UserRepository(conn)
book_repository = BookRepository(conn)
loan_repository = LoanRepository(conn)
logs_utils = Logger(conn)

#menu para la gestión o CRUD de libros
def menu_libros():
    
    while True:
        try:
            print("\n")
            print("1. Crear un libro")
            print("2. Ver información de todos los libros")
            print("3. Ver información de un libro")
            print("4. Editar un libro")                
            print("5. Eliminar un libro")
            print("6. Pedir prestado un libro")
            print("7. Devolver un libro")
            print("8. Volver al menu principal")
            option = input("Ingrese una opción: ")
            if option == "1":
                book = book_repository.get_book_input() # opcion refactorizada
                book_repository.create_book(book)
                print("Libro creado con exito")
            elif option == "2":
                book_repository.all_books_info()
            elif option == "3":
                print("----LISTA DE LIBROS----")
                book_repository.get_all_books_from_api()
                isbn = input("Por favor ingresa el ISBN del libro: ")
                book = book_repository.get_book_by_isbn(isbn)
                if book:
        # Si se encuentra el libro en la base de datos se mustran los datos del libro
                    print("Libro encontrado en la base de datos:")
                    print(f"Título: {book.get_title()}")
                    print(f"Autor: {book.get_author()}")
                    print(f"Categoría: {book.get_category()}")
                    print(f"Descripción: {book.get_description()}")
                    print(f"Número de páginas: {book.get_num_pag()}")
                else:
        # si no se encuentra el libro en la base de datos, consultamos la API
                    print("Libro no encontrado en la base de datos. Consultando API...")
                    book_from_api = book_repository.get_book_from_api(isbn)
                    if book_from_api:
            # Mostrar la información obtenida de la API
                        print("Información del libro desde la API:")
                        print(f"Título: {book_from_api.get_title()}")
                        print(f"Autor: {book_from_api.get_author()}")
                        print(f"Categoría: {book_from_api.get_category()}")
                        print(f"Descripción: {book_from_api.get_description()}")
                        print(f"Número de páginas: {book_from_api.get_num_pag()}")
            # Guardar el libro en la base de datos para futuras consultas
                        book_repository.create_book(book_from_api)
                        print("Libro guardado en la base de datos.")
                    else:
                        print("No se pudo encontrar el libro ni en la base de datos ni en la API.")
            elif option == "4":
                book_repository.all_books_info()
                #ver si se puede optimizar y reutilizar el codigo para hacer preguntas, como se hizo en el semestre anterior
                # se utiliza la funcion que pide los datos del libro
                book = book_repository.get_book_input_for_editing()
                book_repository.update_book(book)
                print("\n")
                print("Libro editado correctamente")
            elif option == "5":
                book_repository.all_books_info()
                id = int(input("Ingrese el ID del libro que desea eliminar: "))
                if book_repository.valid_isbn(id) is None:
                    print("Debe ingresar un ID valido")
                else:
                    book_repository.delete_book(id)
                    print("Libro eliminado correctamente")
            elif option == "6":
                book_repository.all_books_info()
                try:
                    book_isbn = input("Ingrese el ISBN del libro que desea tomar prestado: ")
                    if book_repository.valid_isbn(book_isbn) is None:
                        print("Debe ingresar un ISBN valido")
                    else:
                        name = input("Ingrese el nombre del usuario: ")
                        password = input("Ingrese la contraseña del usuario: ")
                        user_and_pwd = user_repository.login_user(name, password) #desde el login se sacan los datos del usuario
                        if isinstance(user_and_pwd, str):  # si el resultado es un mensaje de error (tipo string)
                            print(user_and_pwd)  # mostrar el error ocurrido (puede ser de la base de datos o bcrypt)
                        elif user_and_pwd is None:  # si es None, las credenciales no son válidas
                            print("El Usuario o contraseña no son válidos.")
                        else:
                            book = book_repository.get_book_by_isbn(book_isbn) #desde este metodo se toman los datos del libro usando el id
                            loan_repository.loan_book(book, user) #este metodo toma un libro y un usuario para guardar la información   
                except Exception as e:
                    print(f"ha ocurrido un error: {e}") 
                    logs_utils.register_log(f"ocurrio el siguiente tipo de error: {e}")
            elif option == "7":
                loan_repository.show_loans()
                loan_id = input("ingrese el id del prestamo que realizo: ")
                book_isbn = input("ingrese el isbn del libro que desea devolver: ") 
                book = book_repository.get_book_by_isbn(book_isbn)
                loan_repository.return_book(loan_id, book) 
                #falta correjir la validación para que no agregue un libro si es que no esta disponible
            elif option == "8":
                print("\n")
                print("Volviendo al menu principal")
                print("\n")
                return
        except ValueError as e:
                print(e) #primero muestra el error en consola y la linea siguiente almacena el error en la base de datos
                logs_utils.register_log(f"ocurrio el siguiente tipo de error: {e}")
# Desplegar menu para gestionar usuarios
while True:
    print("LIBRASTOCK")
    print("1. Registrar un usuario")
    print("2. Iniciar sesión")
    print("3. Salir")
    option = input("Ingrese su opcion: ")
    if(option == "1"):
        try:
            name, password = user_repository.get_user_input()
            if not name or not password:
                print("Error: Nombre o contraseña no pueden estar vacíos.")
            else:
                user = User()
                user.set_name(name)
                user.set_password(password)
                user_repository.create_user(user) 
                print("Usuario registrado exitosamente.")
        except ValueError as e:
            print(f"Error: {e}")
    elif(option == "2"):
        name = input("Ingrese el nombre del usuario: ")
        password = input("Ingrese la contraseña del usuario: ")
        # llamamos a login_user y manejamos el retorno
        result = user_repository.login_user(name, password)
        if isinstance(result, str):  # si el resultado es un mensaje de error (tipo string)
            print(result)  # mostrar el error ocurrido (puede ser de la base de datos o bcrypt)
        elif result is None:  # si es None, las credenciales no son válidas
            print("El Usuario o contraseña no son válidos.")
        else:  # si no es un mensaje de error ni none, entonces es un objeto User válido
            print(f"Bienvenido a la tienda {result.get_name()}")
            menu_libros()
    elif(option == "3"):
        print("El programa se ha cerrado correctamente")
        break
    else:
        print("debe ingresar una opción valida, entre 1 a 3")
