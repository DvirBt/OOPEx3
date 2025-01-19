import os
from functools import wraps
from Book import Book
import FileManagement
from User import User
import logging
from BookFactory import BookFactory
from SearchContext import SearchContext
import FullStrategy
import PartialStrategy


class Observer:
    """Abstract observer class."""

    def update(self, subject):
        pass


class NotificationService(Observer):
    """Concrete Observer for sending notifications."""

    def update(self, subject):
        if isinstance(subject, Library):
            print(f"Notification: {subject.notification_message}")


class Subject:
    """The Subject class maintains a list of observers and notifies them of changes."""

    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self):
        for observer in self._observers:
            observer.update(self)


LOG_FILE = rf"{os.getcwd()}\log.txt"

logging.basicConfig(
    filename=LOG_FILE,  # File where logs will be saved
    level=logging.INFO,
    format='%(message)s'
)


def log_to_file(func):
    """
    This decorator acts as a log wrapper for library class.
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


class Library(Subject):
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
            self.notification_message = ""
            self._initialized = True  # Mark the instance as initialized
            self.search_context = FullStrategy.FullStrategy()  # Default searching strategy

    @log_to_file
    def borrow_book(self, book_to_lend: Book, librarian: User, client_full_name, client_email, client_phone):
        """
        This function is given a book to borrow and return True if the book was successfully borrowed
        :param book_to_lend: the book to borrow
        :param librarian: the librarians the lends the book
        :param count: how many copies to lend
        :return: True if succeeded
        """
        if book_to_lend is not None:
            try:
                check = FileManagement.lend_book(book_to_lend, librarian, client_full_name, client_email,
                                                 client_phone)
                if check == 1:
                    self.log_text = "book borrowed successfully"
                    self.log_level = logging.INFO
                elif check == 2:
                    self.log_text = "book added to queue successfully"
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
                check, clients_to_update = FileManagement.return_book(book_to_return)
                if check:
                    self.log_text = "book returned successfully"
                    self.log_level = logging.INFO
                else:
                    self.log_text = "book returned fail"
                    self.log_level = logging.INFO
                if clients_to_update is not None and len(clients_to_update) > 0:
                    for client in clients_to_update:
                        # I DON'T KNOW WHAT TO DO AAAAAAAAAAAAAAAAAAAAAAAAA
                        self.notification_message = f"Hey, {client[2]}! The book '{book_to_return.get_title()}' is ready for you to pickup."
                        self.notify()
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
    def add_book(self, book: Book):
        """
        This function is given a new book to add and return True if the book was successfully added
        if the book already exists it will return False
        :param book: the book to add
        :return: True if succeeded
        """
        if book is not None and book.get_title() != "" and book.get_genre() != "" and book.get_author() != "" and book.get_copies() >= 0:
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
        This function is given a user1 to register and returns True if the user1 successfully registered
        if the username already exists it will return False
        Note: username and password cannot be "" (at least one char)
        :param user: the user1 to register
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
        This function is given a user1 to remove and returns True if the user1 was successfully removed
        if the username doesn't exist it will return False
        :param user: the user1 to register
        :return: True if succeeded
        """
        if user is not None:
            try:
                if FileManagement.is_user_exists(user):
                    FileManagement.remove_username(user)
                    self.log_text = f"Successfully removed user1: {user.get_username()}"
                    self.log_level = logging.INFO
                    return True
                else:
                    self.log_text = f"The user1 {user.get_username()} doesn't exists"
                    self.log_level = logging.INFO
                    return False
            except Exception as e:
                self.log_text = f"Failed to remove the user1 {user.get_username()} because {e}"
                self.log_level = logging.ERROR
                return False
        else:
            self.log_text = "User can't be None"
            self.log_level = logging.ERROR
            return False

    @log_to_file
    def login_user(self, user: User):
        """
        This function is given a user1 to login and returns True if the user1 successfully login to the system
        if the username doesn't exist it will return False
        :param user: the user1 to login
        :return: True if succeeded
        """
        if user is not None:
            try:
                check = FileManagement.user_login(user)
                if check:
                    self.log_text = "logged in successfully"
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
    def search_book_by_name(self, name):
        """
        Given a name of a book returns a Book object with all it's properties
        :param name: the books name
        :return: book
        """
        try:
            self.search_context = SearchContext(FullStrategy.FullStrategy())

            result = self.search_context.search_name(name)

            if not result:
                self.search_context.set_searching_strategy(PartialStrategy.PartialStrategy())
                result = self.search_context.search_name(name)

            if result:
                self.log_text = f"Search book {name} by name completed successfully"
                self.log_level = logging.INFO
            else:
                self.log_text = f"Search book {name} by name completed fail"
                self.log_level = logging.INFO
                return None

            return result

        except Exception as e:
            self.log_text = f"Search book {name} by name completed fail"
            self.log_level = logging.ERROR

    @log_to_file
    def search_book_by_author(self, name):
        """
        Given an author's name the function returns a list with all the books
        written by the given author
        :param name: the author's name
        :return: a list of books
        """
        try:
            self.search_context = SearchContext(FullStrategy.FullStrategy())

            result = self.search_context.search_author(name)

            if not result or len(result) == 0:
                self.search_context.set_searching_strategy(PartialStrategy.PartialStrategy())
                result = self.search_context.search_author(name)

            if result and len(result) > 0:
                self.log_text = f"Search book {result[0].get_title()} by author completed successfully"
                self.log_level = logging.INFO
            else:
                self.log_text = f"Search book by author completed fail"
                self.log_level = logging.INFO
                return None

            return result

        except Exception as e:
            self.log_text = f"Search book by author completed fail"
            self.log_level = logging.ERROR

    @log_to_file
    def search_book_by_genre(self, name):
        """
        Given a genre name the function returns a list with all the books
        written by in the same genre
        :param name: the genre name
        :return: a list of books
        """
        try:
            self.search_context = SearchContext(FullStrategy.FullStrategy())

            result = self.search_context.search_genre(name)

            if not result or len(result) == 0:
                self.search_context.set_searching_strategy(PartialStrategy.PartialStrategy())
                result = self.search_context.search_genre(name)

            if result and len(result) > 0:
                self.log_text = "Displayed book by category successfully"
                self.log_level = logging.INFO
            else:
                self.log_text = "Displayed book by category fail"
                self.log_level = logging.INFO
                return None

            return result

        except Exception as e:
            self.log_text = "Displayed book by category fail"
            self.log_level = logging.ERROR

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
            books = FileManagement.select_book_by_is_loaned(False)
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

    def get_borrowed_books_by_user(self):
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
        This function's primary goal is to print to log if the user1 successfully logged out
        :param check: True if the user1 successfully logged out
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
            popular_books = FileManagement.get_popular_books()
            if len(popular_books) > 0:
                full_popular_books = []
                for book in popular_books:
                    full_popular_books.append(FileManagement.select_book_by_name(book)[0])
                return full_popular_books
            return None
        except Exception as e:
            return None

    def get_borrowed_copies_by_book_and_user(self, book: Book, librarian: User):
        try:
            return FileManagement.get_borrowed_copies_by_book_and_user(book, librarian)
        except Exception as e:
            return 0
