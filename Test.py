import unittest

import FileManagement
from Book import Book
from User import User
from Library import Library

class Test(unittest.TestCase):

    def setUp(self):
        self.book = Book("Title1", "Author1", "Yes", 2, "Science-Fiction", 1962)
        self.user = User("shakedm100", "123")
        self.library = Library()

    def test_add_book(self):
        self.library.add_book(self.book)
        added_book = self.library.get_book_by_title(self.book.get_title())

        self.assertEqual(added_book, self.book)


    def test_remove_book(self):
        self.library.add_book(self.book)
        self.library.remove_book(self.book)

        removed_book = self.library.get_book_by_title(self.book.get_title())

        self.assertEqual(removed_book, None)


    def test_borrow_book(self):
        self.library.remove_book(self.book)
        check = self.library.borrow_book(self.book)

        self.assertEqual(check, False)
        self.assertEqual(self.library.get_book_copies(self.book), 0)

        self.library.add_book(self.book)

        self.assertEqual(self.library.get_book_copies(self.book), 2)

        check = self.library.borrow_book(self.book)

        self.assertEqual(self.library.get_book_copies(self.book), 1)
        self.assertEqual(check, True)

        self.library.borrow_book(self.book)

        self.assertEqual(self.library.get_book_copies(self.book), 0)

        check = self.library.borrow_book(self.book)

        self.assertEqual(check, False)
        self.assertEqual(self.library.get_book_copies(self.book), 0)


    def test_return_book(self):
        self.library.remove_book(self.book)
        check = self.library.return_book(self.book)

        self.assertEqual(check, False)

        self.library.add_book(self.book)
        check = self.library.return_book(self.book)

        self.assertEqual(check, True)
        self.assertEqual(self.library.get_book_copies(self.book), 3)


    def test_update_book(self):
        self.library.add_book(self.book)

        self.book.set_author("Zurbavel")
        self.book.set_copies(3)
        self.book.set_is_loaned("No")
        self.book.set_genre("New-Genre")
        self.book.set_year(2000)

        self.library.update_book(self.book)

        self.assertEqual(self.library.get_book_by_title(self.book.get_title()), self.book)

        #Reset it
        self.book = Book("Title1", "Author1", "Yes", 2, "Science-Fiction", 1962)
        self.library.update_book(self.book)

        self.assertEqual(self.library.get_book_by_title(self.book.get_title()), self.book)


    def





