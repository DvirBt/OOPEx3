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
    """
    This decorator acts as a log warpper for library class.
    every function that needs to log something to log.txt assigns to self.log_txt and self.log_level
    the values and when wrapper is called it will log to log.txt the given text
    :param func: the function that needs to write to log.txt
    :return: the value of the given function
    """

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
    """
    This class is primarily to handle the calls between the GUI and FileManagement
    and handling of the return values to the GUI and the exceptions
    that can occur
    Because there can only be one library with one log.txt file this class is implemented as a Singleton
    """

    _instance = None  # Class-level variable to store the single instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Library, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Only initialize if it's the first instance
        if not hasattr(self, "_initialized"):
            self.log_text = ""
            self.log_level = logging.ERROR
            self.book_factory = BookFactory()
            self._initialized = True  # Mark the instance as initialized

    @log_to_file
    def borrow_book(self, book_to_lend: Book, librarian: User, count):
        """
        This function is given a book to borrow and return True if the book was successfully borrowed
        :param book_to_lend: the book to borrow
        :return: True if succeeded
        """
        if book_to_lend is not None:
            try:
                check = FileManagement.lend_book(book_to_lend, librarian, count)
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
        """
        This function is given a book to return and return True if the book was successfully returned
        :param book_to_return: the book to return
        :return: True if succeeded
        """
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
        """
        This function is given a book to check if exist and return True if the book does exist
        :param book: the book to check
        :return: True if exists
        """
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
        """
        This function is given a new book to add and return True if the book was successfully added
        if the book already exists it will return False
        :param book: the book to add
        :return: True if succeeded
        """
        if book is not None:
            try:
                if not self.is_book_exists(book):
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
        """
        This function is given a book to remove and returns True if the book was successfully removed
        if the book doesn't exist it will return False
        :param book: the book to add
        :return: True if succeeded
        """
        if book is not None and self.is_book_exists(book):
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
        """
        This function is given a book to update and returns True if the book was successfully updated
        if the book doesn't exist it will return False
        :param book_to_update: the book to add
        :return: True if succeeded
        """
        if book_to_update is not None and self.is_book_exists(book_to_update):
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
        This function is given a user to register and returns True if the user successfully registered
        if the username already exists it will return False
        Note: username and password cannot be "" (at least one char)
        :param user: the user to register
        :return: True if succeeded
        """
        if user is not None and len(user.get_username()) > 0 and len(user.get_password()) > 0:
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
        """
        This function is given a user to remove and returns True if the user was successfully removed
        if the username doesn't exist it will return False
        :param user: the user to register
        :return: True if succeeded
        """
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
        """
        This function is given a user to login and returns True if the user successfully login to the system
        if the username doesn't exist it will return False
        :param user: the user to login
        :return: True if succeeded
        """
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
        """
        Given a name of a book returns a Book object with all it's properties
        :param name: the books name
        :return: book
        """
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
        """
        Given an author's name the function returns a list with all the books
        written by the given author
        :param name: the author's name
        :return: a list of books
        """
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
        """
        Given a genre name the function returns a list with all the books
        written by in the same genre
        :param name: the genre name
        :return: a list of books
        """
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
        """
        Given a year the function returns a list with all the books
        written at the given year
        :param year: the year
        :return: a list of books
        """
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
        """
        This returns how many copies are currently available of a given book
        :param book: a book
        :return: how many copies available
        """
        try:
            return FileManagement.available_copies(book)
        except Exception as e:
            """self.log_text = f"Encountered an error when trying to find the book {book.get_title()} available copies"
            self.log_level = logging.ERROR"""
            return False

    @log_to_file
    def get_all_books(self):
        """
        This function returns a list of all the books that exists in the library
        :return: a list of books
        """
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
        """
        This function returns a list of all the books that there is at least one copy available
        :return: a list of books
        """
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
        """
        This function returns all the books that are currently borrowed from the library
        :return: a list of books
        """
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

    @log_to_file
    def logout(self, check):
        """
        This function's primary goal is to print to log if the user successfully logged out
        :param check: True if the user successfully logged out
        :return:
        """
        if check:
            self.log_text = "log out successful"
            self.log_level = logging.INFO
        else:
            self.log_text = "log out fail"
            self.log_level = logging.INFO

    def get_popular_list(self):
        try:
            popular_books = FileManagement.init_popular_books()
            if len(popular_books) > 0:
                return popular_books
            return None
        except Exception as e:
            return None
