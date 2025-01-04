from typing import List

from Book import Book
from LogDecorator import log_to_file
import FileManagement
from User import User


class Library:
    """ Singleton?
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Library, cls).__new__(cls)
        return cls.instance
    """

    def __init__(self, books):
        self.books: List[Book] = books
        for book in books:
            if book is not None:
                self.add_book(book)

    @log_to_file
    def lend_book(self, book_to_lend: Book):
        if book_to_lend is not None:
            try:
                return FileManagement.lend_book(book_to_lend)
            except Exception as e:
                return f"Couldn't borrow the book {book_to_lend.get_title()} because {e}"
        else:
            return "Error: book can't be None"

    @log_to_file
    def return_book(self, book_to_return: Book):
        if book_to_return is not None:
            try:
                return FileManagement.return_book(book_to_return)
            except Exception as e:
                return f"Couldn't return the book {book_to_return.get_title()} because {e}"
        else:
            return "Error: book can't be None"

    def is_book_exists(self, book: Book):
        try:
            books = FileManagement.get_book_name_list()
            if book.get_title() in books:
                return True
            return False
        except Exception as e:
            print(f"Couldn't find the book because {e}")

    @log_to_file
    def add_book(self, book):
        if book is not None:
            try:
                if book is not None and not self.is_book_exists(book):
                    FileManagement.add_book(book)
                    return f"Successfully added the book {book.get_title()}"
            except Exception as e:
                return f"Failed to add the book {book.get_title()} because: {e}"
        else:
            return "Error: book can't be None"

    @log_to_file
    def remove_book(self, book):
        if book is not None:
            try:
                FileManagement.remove_book(book)
                return f"Successfully removed the book {book.get_title()}"
            except Exception as e:
                return f"Error: failed to remove the book {book.get_title()} because {e}"
        else:
            return "Error: book can't be None"

    @log_to_file
    def update_book(self, book_to_update: Book):
        if book_to_update is not None:
            try:
                FileManagement.update_book(book_to_update)
                return f"Successfully update the book: {book_to_update.get_title()}"
            except Exception as e:
                return f"Error: failed to update the book {book_to_update.get_title()} because: {e}"
        else:
            return "Error: book can't be None"

    @log_to_file
    def add_user(self, user: User):
        if user is not None:
            try:
                if not FileManagement.is_user_exists(user):
                    FileManagement.add_user(user)
                    return f"Successfully added user: {user.get_username()}"
                else:
                    return f"The user {user.get_username()} already exists"
            except Exception as e:
                return f"Error: failed to add user {user.get_username()} because {e}"
        else:
            return "Error: user can't be None"

    @log_to_file
    def remove_user(self, user: User):
        if user is not None:
            try:
                if FileManagement.is_user_exists(user):
                    FileManagement.remove_username(user)
                    return f"Successfully removed user: {user.get_username()}"
                else:
                    return f"The user {user.get_username()} doesn't exists"
            except Exception as e:
                return f"Error: failed to remove the user {user.get_username()} because {e}"
        else:
            return "Error: user can't be None"
