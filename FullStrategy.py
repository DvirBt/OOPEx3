from SearchStrategy import SearchStrategy
import FileManagement


class FullStrategy(SearchStrategy):

    def search_name(self, name):
        return FileManagement.select_book_by_name(name)

    def search_author(self, name):
        return FileManagement.select_book_by_author(name)

    def search_genre(self, name):
        return FileManagement.select_book_by_genre(name)
