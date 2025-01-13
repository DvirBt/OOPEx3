
class Book:

    def __init__(self, title, author, is_loaned, copies, genre, year):
        self._title = title
        self._author = author

        if is_loaned == "yes" or is_loaned == "Yes" or is_loaned == "True":
            self._is_loaned = True
        elif is_loaned == "no" or is_loaned == "No" or is_loaned == "False":
            self._is_loaned = False
        else:
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

    def __eq__(self, other):
        if isinstance(other, Book):
            return (self._title == other._title and self._author == other._author and self._is_loaned == other._is_loaned and self._copies == other._copies and self._genre == other._genre and self._year == other._year)

    def get_is_loaned_string(self):
        if self._is_loaned:
            return "Yes"

        return "No"
