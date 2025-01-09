from Book import Book


class BookFactory:

    @staticmethod
    def get_book(book_type: str, title, author, isloaned, copies, genre, year):
        if book_type.lower() == "book":
            return Book(title, author, isloaned, copies, genre, year)

