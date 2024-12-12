from infraestructure.connection import Connection
from models.book import Book
from models.user import User
from models.loan import Loan

class LoanRepository:
    def __init__(self, conn: Connection) -> None:
        self.__conn = conn
    #metodo para prestar un libro, recibiendo un usuario y un libro, extrayendo de ambos información
    def loan_book(self, book: Book, user: User) -> Loan:
        if self.is_available(book.get_id()): 
            try:
            # Iniciar la transacción de préstamo
                sql = "INSERT INTO loan (user_name, user_id, book_title, book_isbn) VALUES (%s, %s, %s, %s)"
                self.__conn.execute(sql, (
                    user.get_name(),
                    user.get_id(),
                    book.get_title(),
                    book.get_isbn()
                    ))
                self.__conn.commit()
                # Actualizar disponibilidad del libro en la base de datos
                sql_update = "UPDATE book SET is_available = 0 WHERE id = %s"
                self.__conn.execute(sql_update, (book.get_id(),))
                self.__conn.commit()
                print(f"Préstamo realizado con éxito, ahora el usuario: {user.get_name()} tiene el libro: {book.get_title()}")
            # Crear una instancia de Loan y usa los setters
                loan = Loan()
                loan.set_user(user)  # Asignamos el objeto User
                loan.set_book(book)  # Asignamos el objeto Book
            # Si deseas establecer también el ID del préstamo, puedes hacerlo después de obtenerlo de la base de datos:
            # Suponiendo que el ID del préstamo se autoincremente en la tabla 'loan' y se puede recuperar
                return loan
            except Exception as e:
                print(f"Error al procesar el préstamo: {e}")
                return None
        else:          
            print("El libro no se encuentra disponible")
            return None

    #metodo para ver si un libro esta disponible en la BD, en proceso (este tambien se modificó)

    def is_available(self, book_id: int) -> bool:
        sql = "SELECT is_available FROM book WHERE id = %s"
        self.__conn.execute(sql, (book_id,))
        result = self.__conn.fetchone()
        if result and result[0] == 1:  # verificamos que 'is_available' sea 1 (disponible)
            return True
        else:
            return False
    
    def return_book(self, loan_id: int, book: Book):
        try:
            #primero se revisa si hay algun prestamo que coincida con los datos ingresados
            sql_check = "SELECT * from loan WHERE loan_id = %s AND book_isbn = %s"
            self.__conn.execute(sql_check, (loan_id, book.get_isbn()))
            result = self.__conn.fetchone()

            if not result: #valida que result contenga datos, osea que haya un prestamo valido
                print("El préstamo no existe o los datos no coinciden.")
                return

            #una vez hecho la validación procede a eliminar el prestamo y a actualizar la disponibilidad a disponible
            sql = "DELETE FROM loan WHERE loan_id = %s AND book_isbn = %s" 
            self.__conn.execute(sql, (loan_id, book.get_isbn()))
            result = self.__conn.commit()

            sql_update = "UPDATE book SET is_available = 1 WHERE id = %s" 
            self.__conn.execute(sql_update, (book.get_id()))
            self.__conn.commit()
            print(f"El libro '{book.get_title()}' ha sido devuelto.")
        except Exception as e:
            print(f"Error al registrar la devolución: {e}")

    def show_loans(self):
        #Muestra todos los préstamos activos
        sql = "SELECT loan_id, user_name, user_id, book_title, book_isbn FROM loan"
        self.__conn.execute(sql)
        results = self.__conn.fetchall()
        if not results:
            print("No hay préstamos activos.")
        else:
            for loan in results:
                print(f"ID de Préstamo: {loan[0]}, Usuario: {loan[1]}, ID de Usuario: {loan[2]}, Titulo del libro: {loan[3]}, ISBN del libro: {loan[4]}")
