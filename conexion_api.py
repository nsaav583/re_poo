import requests

print("-----Lista de libros-----")
response_book = requests.get("https://poo.nsideas.cl/api/libros")

for book in response_book.json():
    print(f"Título: {book["titulo"]}, ISBN: {book["isbn"]}")

isbn = input("Ingrese el isbn del libro: ")

# Request al endpoint de la API
response = requests.get(f"https://poo.nsideas.cl/api/libros/{isbn}")

# Validar que la respuesta a la peticion es in OK
if response.status_code == 200:
    print("Peticion OK!!!")
    # Obtener el contenido json de la respuesta
    data = response.json()
    print("Nombre del Libro: " + data["titulo"])
    print("Autor: " + data["autor"])
    print("Categorias: " + data["categorias"[1]])
    print("Descripción: " + data["descripcion"])
    print("ISBN: " + data["isbn"])
    print("Número de paginas: " + str(data["numero_paginas"]))
else:
    print("Error")

