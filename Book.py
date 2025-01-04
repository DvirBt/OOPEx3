
class Book:

    def __init__(self, title, author, is_loaned, copies, genre, year):
        self._title = title
        self._author = author
        self._is_loaned = is_loaned
        self._copies = copies
        self._genre = genre
        self._year = year

    def get_title(self):
        return self._title

    def get_author(self):
        return self._author

    def get_is_loaned(self):
        return self._is_loaned

    def get_copies(self):
        return self._copies

    def get_genre(self):
        return self._genre

    def get_year(self):
        return self._year

    def set_author(self, author):
        self._author = author

    def set_is_loaned(self, is_loaned):
        self._is_loaned = is_loaned

    def set_copies(self, copies):
        self._copies = copies

    def set_genre(self, genre):
        self._genre = genre

    def set_year(self, year):
        self._year = year

    def increase_copy(self):
        self._copies += 1

    def decrease_copy(self):
        self._copies -= 1
        


