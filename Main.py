from typing import List
import Library
from Book import Book
from User import User

book1 = Book("Title1", "Author1", True, 2, "Science-Fiction", 1962)
book2 = Book("Title2", "Author2", False, 3, "Maybe", 2000)
book3 = Book("1984", "George Orwell", True, 5, "Dystopian", 1949)

books = [book2]
library = Library.Library(books)

library.add_book(book2)
library.add_book(book1)
library.add_book(book1)
library.add_book(book1)

library.remove_book(book1)

library.lend_book(book2)

user = User("shakedm100", "aesnhftk1")
library.add_user(user)