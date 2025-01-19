import unittest
import FileManagement
from User import User
from Library import Library
from BookFactory import BookFactory


class Test(unittest.TestCase):

    def setUp(self):
        self.book_factory = BookFactory()
        self.book = self.book_factory.get_book("book", "Title1", "Author1", "No", 3, "Science-Fiction", 1962)
        self.user = User("dvirbto", "123")
        self.library = Library()

    def test_add_book(self):
        self.library.remove_book(self.book)
        check = self.library.add_book(self.book)
        added_book = self.library.search_book_by_name(self.book.get_title())

        self.assertEqual(added_book[0], self.book)

    def test_remove_book(self):
        self.library.add_book(self.book)
        self.library.remove_book(self.book)

        removed_book = self.library.search_book_by_name(self.book.get_title())

        self.assertEqual(removed_book, None)

    def test_borrow_book(self):
        self.library.remove_book(self.book)
        check = self.library.borrow_book(self.book, self.user, "Shaked Michael", "shaked1mi@gmail.com", "0542857333")

        self.assertEqual(check, 0)
        self.assertEqual(self.library.get_book_copies(self.book), 0)

        self.library.add_book(self.book)

        self.assertEqual(self.library.get_book_copies(self.book), 3)

        check = self.library.borrow_book(self.book, self.user, "Shaked Michael", "shaked1mi@gmail.com", "0542857333")

        self.assertEqual(self.library.get_book_copies(self.book), 2)
        self.assertEqual(check, 1)

        self.library.borrow_book(self.book, self.user, "Shaked Michael", "shaked1mi@gmail.com", "0542857333")
        self.library.borrow_book(self.book, self.user, "Shaked Michael", "shaked1mi@gmail.com", "0542857333")

        self.assertEqual(self.library.get_book_copies(self.book), 0)

        check = self.library.borrow_book(self.book, self.user, "Shaked Michael", "shaked1mi@gmail.com", "0542857333")

        self.assertEqual(check, 2)
        self.assertEqual(self.library.get_book_copies(self.book), 0)

        self.library.remove_book(self.book)
        self.library.add_book(self.book)

        check = self.library.borrow_book(self.book, self.user, "Shaked Michael", "shaked1mi@gmail.com", "0542857333")
        self.assertEqual(check, 1)
        self.assertEqual(self.book.get_is_loaned(), True)

        check = self.library.borrow_book(self.book, self.user, "Shaked Michael", "shaked1mi@gmail.com", "0542857333")
        self.assertEqual(check, 1)

    def test_return_book(self):
        self.library.remove_book(self.book)
        check = self.library.return_book(self.book)

        self.assertEqual(check, False)

        self.library.add_book(self.book)
        check = self.library.return_book(self.book)

        self.assertEqual(check, False)

        self.library.borrow_book(self.book, self.user, "Shaked Michael", "shaked1mi@gmail.com", "0542857333")
        self.library.return_book(self.book)
        self.assertEqual(self.library.get_book_copies(self.book), 3)

        self.library.return_book(self.book)
        self.assertEqual(self.library.get_book_copies(self.book), 3)

    def test_update_book(self):
        self.library.add_book(self.book)

        self.book.set_author("Zurbavel")
        self.book.set_copies(3)
        self.book.set_is_loaned(False)
        self.book.set_genre("New-Genre")
        self.book.set_year(2000)

        self.library.update_book(self.book)

        self.assertEqual(self.library.search_book_by_name(self.book.get_title())[0], self.book)

        # Reset it
        self.book = self.book_factory.get_book("book", "Title1", "Author1", "Yes", 2, "Science-Fiction", 1962)
        self.library.update_book(self.book)

        self.assertEqual(self.library.search_book_by_name(self.book.get_title())[0], self.book)

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
        self.library.remove_book(self.book)  # Reset
        self.library.add_book(self.book)  # Reset
        self.library.register_user(self.user)

        self.library.borrow_book(self.book, self.user, "Shaked Michael", "shaked1mi@gmail.com", "0542857333")
        books = FileManagement.get_borrowed_books()

        if len(books) >= 2:
            check = True
        else:
            check = False

        self.assertEqual(check, True)

    def test_popular_books(self):
        self.library.remove_book(self.book)  # Reset
        self.library.add_book(self.book)  # Reset

        self.library.borrow_book(self.book, self.user, "Shaked Michael", "shaked1mi@gmail.com", "0542857333")
        popular_books = self.library.get_popular_list()

        if self.book in popular_books:
            check = True
        else:
            check = False

        self.assertEqual(check, True)

    def test_get_borrowed_copies_by_book_and_user(self):
        self.library.remove_book(self.book)
        self.library.add_book(self.book)

        self.library.borrow_book(self.book, self.user, "Shaked Michael", "shaked1mi@gmail.com", "0542857333")

        count = self.library.get_borrowed_copies_by_book_and_user(self.book, self.user)

        self.assertEqual(count, 1)

    def test_search_book_by_genre(self):
        genre = self.library.search_book_by_genre("Fiction")
        check = False
        if len(genre) > 0:
            check = True

        self.assertEqual(check, True)

        genre = self.library.search_book_by_genre("Fic")
        check = False
        if len(genre) > 0:
            check = True

        self.assertEqual(check, True)
