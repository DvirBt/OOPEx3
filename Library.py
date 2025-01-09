import os
from functools import wraps
from Book import Book
import FileManagement
from User import User
import logging
from BookFactory import BookFactory

LOG_FILE = rf"{os.getcwd()}\log.txt"

logging.basicConfig(
    filename=LOG_FILE,  # File where logs will be saved
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def log_to_file(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w") as f:
                f.write("")
        with open(LOG_FILE, "a") as f:
            try:
                result = func(self, *args, **kwargs)
                if self.log_text != "":
                    logging.log(self.log_level, self.log_text)
                return result
            except Exception as e:
                """logging.error(f"Encountered a problem at log decorator: {e}")"""
                raise

    return wrapper


class Library:
    """ Singleton?
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Library, cls).__new__(cls)
        return cls.instance
    """

    def __init__(self):
        self.log_text = ""
        self.log_level = logging.ERROR
        self.book_factory = BookFactory()


    @log_to_file
    def borrow_book(self, book_to_lend: Book):
        if book_to_lend is not None:
            try:
                check = FileManagement.lend_book(book_to_lend)
                if check:
                    self.log_text = "book borrowed successfully"
                    self.log_level = logging.INFO
                else:
                    self.log_text = "book borrowed fail"
                    self.log_level = logging.INFO
                return check
            except Exception as e:
                self.log_text = "book borrowed fail"
                self.log_level = logging.ERROR
                return False
        else:
            self.log_text = "book borrowed fail"
            self.log_level = logging.ERROR
            return False

    @log_to_file
    def return_book(self, book_to_return: Book):
        if book_to_return is not None:
            try:
                check = FileManagement.return_book(book_to_return)
                if check:
                    self.log_text = "book returned successfully"
                    self.log_level = logging.INFO
                else:
                    self.log_text = "book returned fail"
                    self.log_level = logging.INFO
                return check
            except Exception as e:
                self.log_text = "book returned fail"
                self.log_level = logging.ERROR
                return False
        else:
            self.log_text = "book returned fail"
            self.log_level = logging.ERROR
            return False

    @log_to_file
    def is_book_exists(self, book: Book):
        try:
            books = FileManagement.get_book_name_list()
            if book.get_title() in books:
                return True
            return False
        except Exception as e:
            self.log_text = f"Failed to find the book because {e}"
            self.log_level = logging.DEBUG

    @log_to_file
    def add_book(self, book):
        if book is not None:
            try:
                if book is not None and not self.is_book_exists(book):
                    FileManagement.add_book(book)
                    self.log_text = "book added successfully"
                    self.log_level = logging.INFO
                    return True
            except Exception as e:
                self.log_text = "book added failed"
                self.log_level = logging.ERROR
                return False
        else:
            self.log_text = "book added failed"
            self.log_level = logging.ERROR
            return False

    @log_to_file
    def remove_book(self, book):
        if book is not None:
            try:
                FileManagement.remove_book(book)
                self.log_text = "book removed successfully"
                self.log_level = logging.INFO
                return True
            except Exception as e:
                self.log_text = "book removed failed"
                self.log_level = logging.ERROR
                return False
        else:
            self.log_text = "book removed failed"
            self.log_level = logging.ERROR
            return False

    @log_to_file
    def update_book(self, book_to_update: Book):
        if book_to_update is not None:
            try:
                FileManagement.update_book(book_to_update)
                self.log_text = f"Successfully update the book: {book_to_update.get_title()}"
                self.log_level = logging.INFO
                return True
            except Exception as e:
                self.log_text = f"Failed to update the book {book_to_update.get_title()} because: {e}"
                self.log_level = logging.ERROR
                return False
        else:
            self.log_text = "Book can't be None"
            self.log_level = logging.ERROR
            return False

    @log_to_file
    def register_user(self, user: User):
        """
        TODO Add basic requirements checks for user name and password
        :param user:
        :return:
        """
        if user is not None:
            try:
                if not FileManagement.is_user_exists(user):
                    check = FileManagement.add_user(user)
                    if check:
                        self.log_text = "registered successfully"
                        self.log_level = logging.INFO
                    else:
                        self.log_text = "registered fail"
                        self.log_level = logging.INFO
                    return check
                else:
                    self.log_text = "registered fail"
                    self.log_level = logging.INFO
                    return False
            except Exception as e:
                self.log_text = "registered fail"
                self.log_level = logging.ERROR
                return False
        else:
            self.log_text = "registered fail"
            self.log_level = logging.ERROR
            return False

    @log_to_file
    def remove_user(self, user: User):
        if user is not None:
            try:
                if FileManagement.is_user_exists(user):
                    FileManagement.remove_username(user)
                    self.log_text = f"Successfully removed user: {user.get_username()}"
                    self.log_level = logging.INFO
                    return True
                else:
                    self.log_text = f"The user {user.get_username()} doesn't exists"
                    self.log_level = logging.INFO
                    return False
            except Exception as e:
                self.log_text = f"Failed to remove the user {user.get_username()} because {e}"
                self.log_level = logging.ERROR
                return False
        else:
            self.log_text = "User can't be None"
            self.log_level = logging.ERROR
            return False

    @log_to_file
    def login_user(self, user: User):
        if user is not None:
            try:
                check = FileManagement.user_login(user)
                if check:
                    self.log_text = "logged in succesfully"
                    self.log_level = logging.INFO
                    return True
                else:
                    self.log_text = "logged in fail"
                    self.log_level = logging.INFO
                    return False
            except Exception as e:
                self.log_text = "logged in fail"
                self.log_level = logging.ERROR
                return False
        else:
            self.log_text = "User can't be None"
            self.log_level = logging.ERROR
            return False

    @log_to_file
    def get_book_by_title(self, name):
        try:
            book = FileManagement.select_book_by_name(name)
            if book is not None:
                self.log_text = f"Search book {name} by name completed successfully"
                self.log_level = logging.INFO
            else:
                self.log_text = f"Search book {name} by name completed fail"
            return book
        except Exception as e:
            self.log_text = f"Search book {name} by name completed"
            self.log_level = logging.ERROR

    @log_to_file
    def get_book_by_author(self, name):
        try:
            books = FileManagement.select_book_by_author(name)
            if len(books) > 0:
                self.log_text = f"Search book {books[0].get_title()} by author completed successfully"
                self.log_level = logging.INFO
            else:
                self.log_text = f"Search book by author completed fail"
                self.log_level = logging.INFO
            return books
        except Exception as e:
            self.log_text = f"Search book by author completed fail"
            self.log_level = logging.ERROR

    @log_to_file
    def get_book_by_genre(self, name):
        try:
            books = FileManagement.select_book_by_genre(name)
            if len(books) > 0:
                self.log_text = "Displayed book by category successfully"
                self.log_level = logging.INFO
            else:
                self.log_text = "Displayed book by category fail"
                self.log_level = logging.INFO
            return books
        except Exception as e:
            self.log_text = "Displayed book by category fail"
            self.log_level = logging.ERROR

    @log_to_file
    def get_book_by_year(self, year):
        try:
            books = FileManagement.select_book_by_year(year)
            """if len(books) > 0:
                self.log_text = f"Successfully found the books by the year {year}"
                self.log_level = logging.INFO
            else:
                self.log_text = f"Failed to find any books by the year {year}"
                self.log_level = logging.INFO"""
            return books
        except Exception as e:
            """self.log_text = f"Encountered an error when tried to search by the year {year}"
            self.log_level = logging.ERROR"""


    @log_to_file
    def get_book_copies(self, book: Book):
        try:
            return FileManagement.available_copies(book)
        except Exception as e:
            """self.log_text = f"Encountered an error when trying to find the book {book.get_title()} available copies"
            self.log_level = logging.ERROR"""
            return False


    @log_to_file
    def get_all_books(self):
        try:
            books = FileManagement.get_all_books()
            if len(books) > 0:
                self.log_text = "Displayed all books successfully"
                self.log_level = logging.INFO
            else:
                self.log_text = "Displayed all books fail"
                self.log_level = logging.INFO
            return books
        except Exception as e:
            self.log_text = "Displayed all books fail"
            self.log_level = logging.ERROR
            return None

    @log_to_file
    def get_available_books(self):
        try:
            books = FileManagement.select_book_by_is_loaned(True)
            if len(books) > 0:
                self.log_text = "Displayed available books successfully"
                self.log_level = logging.INFO
            else:
                self.log_text = "Displayed available books fail"
                self.log_level = logging.INFO
            return books
        except Exception as e:
            self.log_text = "Displayed available books fail"
            self.log_level = logging.ERROR


    def get_borrowed_book(self):
        try:
            books = FileManagement.get_borrowed_books()
            if len(books) > 0:
                self.log_text = "Displayed borrowed books successfully"
                self.log_level = logging.INFO
            else:
                self.log_text = "Displayed borrowed books fail"
                self.log_level = logging.INFO
            return books
        except Exception as e:
            self.log_text = "Displayed borrowed books fail"
            self.log_level = logging.ERROR


    def logout(self, check):
        if check:
            self.log_text = "log out successful"
            self.log_level = logging.INFO
        else:
            self.log_text = "log out fail"
            self.log_level = logging.INFO

