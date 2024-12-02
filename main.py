from infraestructure.mysqlconnection import MySQLConnection
from infraestructure.user_repository import UserRepository
from credentials_db import user, password, database, host
from models.user import User

conn = MySQLConnection(host, user, password, database)
user_repository = UserRepository(conn)

# DESplegar mmenu para gestionar usuarios
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
        print(user.get_password()) 
    elif(option == "2"):
        name = input("Ingrese el nombre del usuario: ")
        password = input("Ingrese la contraseña del usuario: ")
        user.set_name(name)
        user.set_password(password)
        print("Sesión iniciada exitosamente.")
    elif(option == "3"):
        break
    else:
        print("debe ingresar una opción valida, entre 1 a 3")
