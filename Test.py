import unittest

import FileManagement
from User import User
from Library import Library
from BookFactory import BookFactory


class Test(unittest.TestCase):

    def setUp(self):
        self.book_factory = BookFactory()
        self.book = self.book_factory.get_book("book", "Title1", "Author1", "Yes", 2, "Science-Fiction", 1962)
        self.user = User("dvirbto", "123")
        self.library = Library()

    def test_add_book(self):
        self.library.remove_book(self.book)
        check = self.library.add_book(self.book)
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
        self.book.set_is_loaned(False)
        self.book.set_genre("New-Genre")
        self.book.set_year(2000)

        self.library.update_book(self.book)

        self.assertEqual(self.library.get_book_by_title(self.book.get_title()), self.book)

        # Reset it
        self.book = self.book_factory.get_book("book", "Title1", "Author1", "Yes", 2, "Science-Fiction", 1962)
        self.library.update_book(self.book)

        self.assertEqual(self.library.get_book_by_title(self.book.get_title()), self.book)

    def test_add_and_remove_user(self):
        self.library.remove_user(self.user)
        user = FileManagement.get_user_by_username(self.user)
        self.assertEqual(user, None)

        check_registered = self.library.register_user(self.user)
        self.assertEqual(check_registered, True)

        check_user = FileManagement.get_user_by_username(self.user.get_username())
        self.user.set_password(FileManagement.encrypt_password(self.user.get_password()))

        self.assertEqual(check_user, self.user)

        self.library.remove_user(self.user)
        user = FileManagement.get_user_by_username(self.user)
        self.assertEqual(user, None)

    def test_get_all_books(self):
        books = FileManagement.get_all_books()
        if len(books) > 0:
            check = True
        else:
            check = False

        self.assertEqual(check, True)

    def test_get_all_borrowed(self):
        self.library.add_book(self.book)
        self.library.borrow_book(self.book)
        books = FileManagement.get_borrowed_books()

        if len(books) > 0:
            check = True
        else:
            check = False

        self.assertEqual(check, True)
