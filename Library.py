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
        for book in self.books:
            if book.get_title() == book_to_return.get_title():
                book.decrease_copy()
                print(f"Returned book: {book.get_title()}")
                return
        print("Book was not found")

    def is_book_exists(self, book:Book):
        books = FileManagement.get_book_name_list()
        if book.get_title() in books:
            return True
        return False

    @log_to_file
    def add_book(self, book):
        try:
            if book is not None and not self.is_book_exists(book):
                self.books.append(book)
                FileManagement.add_book(book)
                return f"Successfully added the book {book.get_title()}"
        except Exception as e:
            return f"Failed to add the book {book.get_title()} because: {e}"



    @log_to_file
    def remove_book(self, book):
        try:
            if book is not None:
                self.books.append(book)
                FileManagement.remove_book(book)
                return f"Successfully removed the book {book.get_title()}"
        except Exception as e:
            return f"Failed to remove the book {book.get_title()} because: {e}"

    @log_to_file
    def update_book(self, book_to_update):
        for book in self.books:
            if book.get_title() == book_to_update.get_title():
                book.set_author(book_to_update.get_author())
                book.set_year(book_to_update.get_year())
                book.set_genre(book_to_update.get_genre())
                book.set_copies(book_to_update.get_copies())
                book.set_is_loaned(book_to_update.get_is_loaned())
                print(f"Successfully updated the book {book.get_title()}")
                return

        print("Book to update wasn't found")


    @log_to_file
    def add_user(self, user:User):
        if not FileManagement.is_user_exists(user):
            FileManagement.add_user(user)
            return f"Successfully added user: {user.get_username()}"
        else:
            return f"The user {user.get_username()} already exists"

