import Library
from Book import Book
from User import User

book1 = Book("Title1", "Author1", "Yes", 2, "Science-Fiction", 1962)
book2 = Book("Title2", "Author2", "No", 3, "Maybe", 2000)
book3 = Book("1984", "George Orwell", "Yes", 5, "Dystopian", 1949)

books = [book2]
library = Library.Library(books)

library.add_book(book2)
library.add_book(book1)
library.add_book(book1)
library.add_book(book1)

library.remove_book(book1)

library.borrow_book(book2)

user = User("shakedm100", "aesnhftk1")
library.register_user(user)
library.remove_user(user)

book2.set_author("Shaked Michael")
book2.set_year(2005)
book2.set_is_loaned("No")

library.update_book(book2)

#library.return_book(book2)