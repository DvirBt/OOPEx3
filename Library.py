from typing import List
import os
from functools import wraps
from Book import Book
import FileManagement
from User import User
import logging

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
                logging.error(f"Encountered a problem at log decorator: {e}")
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


    @log_to_file
    def borrow_book(self, book_to_lend: Book):
        if book_to_lend is not None:
            try:
                self.log_text = FileManagement.lend_book(book_to_lend)
                self.log_level = logging.INFO
                return True
            except Exception as e:
                self.log_text = f"Failed to borrow the book {book_to_lend.get_title()} because {e}"
                self.log_level = logging.DEBUG
                return False
        else:
            self.log_text = "Book can't be None"
            self.log_level = logging.ERROR
            return False

    @log_to_file
    def return_book(self, book_to_return: Book):
        if book_to_return is not None:
            try:
                self.log_text = FileManagement.return_book(book_to_return)
                self.log_level = logging.INFO
                return True
            except Exception as e:
                self.log_text = f"Failed to return the book {book_to_return.get_title()} because {e}"
                self.log_level = logging.ERROR
                return False
        else:
            self.log_text = "Book can't be None"
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
                    self.log_text = f"Successfully added the book {book.get_title()}"
                    self.log_level = logging.INFO
                    return True
            except Exception as e:
                self.log_text = f"Failed to add the book {book.get_title()} because: {e}"
                self.log_level = logging.ERROR
                return False
        else:
            self.log_text = "Book can't be None"
            self.log_level = logging.ERROR
            return False

    @log_to_file
    def remove_book(self, book):
        if book is not None:
            try:
                FileManagement.remove_book(book)
                self.log_text = f"Successfully removed the book {book.get_title()}"
                self.log_level = logging.INFO
                return True
            except Exception as e:
                self.log_text = f"Failed to remove the book {book.get_title()} because {e}"
                self.log_level = logging.ERROR
                return False
        else:
            self.log_text ="Book can't be None"
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
        if user is not None:
            try:
                if not FileManagement.is_user_exists(user):
                    FileManagement.add_user(user)
                    self.log_text = f"Successfully registered user: {user.get_username()}"
                    self.log_level = logging.INFO
                    return True
                else:
                    self.log_text = f"The user {user.get_username()} already exists"
                    self.log_level = logging.INFO
                    return False
            except Exception as e:
                self.log_text = f"Failed to register user {user.get_username()} because {e}"
                self.log_level = logging.ERROR
                return False
        else:
            self.log_text = "User can't be None"
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
                FileManagement.user_login(user)
                self.log_text = f"User {user.get_username()} successfully logged in"
                self.log_level = logging.INFO
                return True
            except Exception as e:
                self.log_text = f"Failed to log in user {user.get_username()} because {e}"
                self.log_level = logging.ERROR
                return False
        else:
            self.log_text = "User can't be None"
            self.log_level = logging.ERROR
            return False

    def get_book_by_name(self, name):
        try:
            book = FileManagement.select_book_by_name(name)
            if book is not None:
                self.log_text = f"Successfully found the book {name}"
                self.log_level = logging.INFO
            else:
                self.log_text = f"Failed to search the book by the name {name}"
            return book
        except Exception as e:
            self.log_text = f"Encountered an error when tried to search the book {name} by name"
            self.log_level = logging.ERROR

    def get_book_by_author(self, name):
        try:
            books = FileManagement.select_book_by_author(name)
            if len(books) > 0:
                self.log_text = f"Successfully found the books by the author {name}"
                self.log_level = logging.INFO
            else:
                self.log_text = f"Failed to find any books by the author {name}"
                self.log_level = logging.INFO
            return books
        except Exception as e:
            self.log_text = f"Encountered an error when tried to search by the author {name}"
            self.log_level = logging.ERROR

    def get_book_by_genre(self, name):
        try:
            books = FileManagement.select_book_by_genre(name)
            if len(books) > 0:
                self.log_text = f"Successfully found the books by the genre {name}"
                self.log_level = logging.INFO
            else:
                self.log_text = f"Failed to find any books by the genre {name}"
                self.log_level = logging.INFO
            return books
        except Exception as e:
            self.log_text = f"Encountered an error when tried to search by the genre {name}"
            self.log_level = logging.ERROR

    def get_book_by_year(self, year):
        try:
            books = FileManagement.select_book_by_year(year)
            if len(books) > 0:
                self.log_text = f"Successfully found the books by the year {year}"
                self.log_level = logging.INFO
            else:
                self.log_text = f"Failed to find any books by the year {year}"
                self.log_level = logging.INFO
            return books
        except Exception as e:
            self.log_text = f"Encountered an error when tried to search by the year {year}"
            self.log_level = logging.ERROR