from typing import List

import Book
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
            self.add_book(book)

    @log_to_file
    def lend_book(self, book_to_lend):
        return FileManagement.lend_book(book_to_lend)

    @log_to_file
    def return_book(self, book_to_return):
        return FileManagement.return_book(book_to_return)

    def is_book_exists(self, book: Book):
        books = FileManagement.get_book_name_list()
        if book.get_title() in books:
            return True
        return False

    @log_to_file
    def add_book(self, book):
        try:
            if book is not None and not self.is_book_exists(book):
                FileManagement.add_book(book)
                return f"Successfully added the book {book.get_title()}"
        except Exception as e:
            return f"Failed to add the book {book.get_title()} because: {e}"

    @log_to_file
    def remove_book(self, book):
        try:
            if book is not None:
                FileManagement.remove_book(book)
                return f"Successfully removed the book {book.get_title()}"
        except Exception as e:
            return f"Failed to remove the book {book.get_title()} because: {e}"

    @log_to_file
    def update_book(self, book_to_update: Book):
        if book_to_update is not None:
            FileManagement.update_book(book_to_update)
            return f"Successfully update the book: {book_to_update.get_title()}"
        else:
            return "Error: book cannot be None"

    @log_to_file
    def add_user(self, user: User):
        if not FileManagement.is_user_exists(user):
            FileManagement.add_user(user)
            return f"Successfully added user: {user.get_username()}"
        else:
            return f"The user {user.get_username()} already exists"

    @log_to_file
    def remove_user(self, user: User):
        if FileManagement.is_user_exists(user):
            FileManagement.remove_username(user)
            return f"Successfully removed user: {user.get_username()}"
        else:
            return f"The user {user.get_username()} doesn't exists"
