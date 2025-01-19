from SearchStrategy import SearchStrategy
import FileManagement


class PartialStrategy(SearchStrategy):

    def search_name(self, name):
        return FileManagement.select_books_by_name_partly(name)

    def search_author(self, name):
        return FileManagement.select_book_by_author_partly(name)

    def search_genre(self, name):
        return FileManagement.select_book_by_genre_partly(name)
