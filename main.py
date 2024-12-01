from infraestructure.mysqlconnection import MySQLConnection
from infraestructure.user_repository import UserRepository
from credentials_db import user, password, database, host
from models.user import User

conn = MySQLConnection(host, user, password, database)
user_repository = UserRepository(conn)

while True:
    print("MENU MANTENEDOR")
    print("1. Mostrar todos los usuarios")
    print("2. Agregar un usuario")
    print("3. Editar un usuario")
    print("4. Eliminar un usuario")
    print("5. Salir")
    option = input("Ingrese su opcion: ")
    if(option == "1"):
        print("id \t\t nombre \t\t email")
        users = user_repository.get_all_user()
        for user in users:
            print(f"{user.get_id()} \t\t {user.get_name()} \t\t {user.get_email()}")
    if(option == "2"):
        name = input("Ingrese el nombre del usuario: ")
        email = input("Ingrese el email del usuario: ")
        user = User()
        user.set_name(name)
        user.set_email(email)
        user_repository.create_user(user)
        print("Usuario registrado exitosamente.")
    if(option == "3"):
        id = input("Ingrese el id del usuario: ")
        name = input("Ingrese el nombre del usuario: ")
        email = input("Ingrese el email del usuario: ")
        user = User()
        user.set_id(id)
        user.set_name(name)
        user.set_email(email)
        user_repository.update_user(user)
        print("El usuario fue modificado exitosamente.")
    if (option == "4"):
        id = input("Ingrese el id del usuario: ")
        user_repository.delete_user(id)
        print("El usuario fue eliminado exitosamente.")
    if(option == "5"):
        break
