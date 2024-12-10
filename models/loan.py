class Loan:
    def __init__(self) -> None:
        self.__loan_id: int = -1
        self.__user: object = None 
        self.__book: object = None
    
    def get_loan_id(self) -> int:
        return self.__loan_id
    
    def set_loan_id(self, loan_id: int):
        self.__loan_id = loan_id

    def get_user(self) -> object:
        return self.__user
    
    def set_user(self, user: object):
        self.__user = user

    def get_book(self) -> object:
        return self.__book
    
    def set_book(self, book: object):
        self.__book = book
