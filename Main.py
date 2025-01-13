import FileManagement
import Library
from Book import Book
from User import User

book1 = Book("Title1", "Author1", "No", 2, "Science-Fiction", 1962)
book2 = Book("Title2", "Author2", "No", 3, "Maybe", 2000)
book3 = Book("1984", "George Orwell", "No", 5, "Dystopian", 1949)
user1 = User("shakedm100", "123")
user2 = User("dvirbto", "123")

books = [book2]
library = Library.Library()

library.remove_book(book2)
library.remove_book(book3)
library.add_book(book3)
library.add_book(book2)

library.add_book(book1)
library.add_book(book1)
library.add_book(book1)

library.borrow_book(book2, user1, 3, "Shaked Michael", "shaked1mi@gmail.com", "0542857333")
library.borrow_book(book3, user1, 9, "Shaked Michael", "shaked1mi@gmail.com", "0542857333")
# library.remove_book(book1)

library.borrow_book(book2, user1, 1, "Shaked Michael", "shaked1mi@gmail.com", "0542857333")

library.register_user(user1)

# library.remove_user(user1)


book2.set_author("Shaked Michael")
book2.set_year(2005)
book2.set_is_loaned("No")

library.update_book(book2)

library.add_book(None)
library.remove_book(book1)

library.return_book(book3, user1, 3)

most_popular_books = FileManagement.get_popular_books()

books_partly = FileManagement.select_books_by_name_partly("title")

print(f"books partly: {books_partly}")
