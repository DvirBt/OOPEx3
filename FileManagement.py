import os
import csv
from Book import Book
from functools import wraps
from User import User
import hashlib
from BookFactory import BookFactory
from CSVIterator import CSVIterator


def check(func):
    r"""
    This decorator's purpose is to check if all the required .csv files are present at the correct location
    before trying to access them. Currently, it checks if available_books.csv and books.csv and users.csv
    are present under $current_file_location$\Files\
    :param func: a function that the decorator is going the wrap
    :return: the return value of the function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        check_csv_exists()
        result = func(*args, **kwargs)
        return result

    return wrapper


"""
This are variables that are required for managing and accessing the .csv files
"""
current_path = os.getcwd()
available_books_path = rf"{current_path}\Files\available_books.csv"
book_path = rf"{current_path}\Files\books.csv"
users_database = rf"{current_path}\Files\users.csv"
book_factory = BookFactory()  # Creates a factory to creates books for later


def check_csv_exists():
    """
    This function checks if all the required .csv files are present
    and calls the creation of each .csv if needed
    :return:
    """
    if not os.path.exists(available_books_path):
        create_available_books_file()
    if not os.path.exists(book_path):
        create_book_csv_file()
    if not os.path.exists(users_database):
        create_users_csv()


def create_available_books_file():
    """
    This function creates the available_books.csv by accessing books.csv
    and assuming that all the copies at the time of initial creating exist
    :return:
    """
    header = ["title", "available"]
    data = []
    with CSVIterator(book_path, "r") as book_iterator:
        next(book_iterator)
        for row in book_iterator:
            title = row[0]
            copies = row[3]
            data.append([title, copies])

    with CSVIterator(available_books_path, "a") as available_file:
        available_file.write_row(header)
        available_file.write_rows(data)


@check
def add_book(book: Book):
    """
    This function adds a given book to books.csv and available_books.csv
    :param book: new book to add
    :return:
    """
    if book is not None:
        with CSVIterator(book_path, mode="a") as iterator:
            iterator.write_row([book.get_title(), book.get_author(), book.get_is_loaned(), book.get_copies(), book.get_genre(), book.get_year()])

        with CSVIterator(available_books_path, mode="a") as iterator:
            iterator.write_row([book.get_title(), book.get_copies()])


@check
def remove_book(book: Book):
    """
    This function removes a given book from both books.csv and available_books.csv
    :param book: a book to remove
    :return:
    """
    if book is not None:
        with CSVIterator(book_path, mode="r") as iterator:
            header = next(iterator)
            rows = [row for row in iterator if row[0] != book.get_title()]

        with CSVIterator(book_path, mode="w") as iterator:
            iterator.write_row(header)
            iterator.write_rows(rows)

        with CSVIterator(available_books_path, mode="r") as iterator:
            header = next(iterator)
            rows = [row for row in iterator if row[0] != book.get_title()]

        with CSVIterator(available_books_path, mode="w") as iterator:
            iterator.write_row(header)
            for row in rows:
                iterator.write_row([row[0], row[1]])


@check
def available_copies(book: Book):
    """
    This function counts how many copies are currently available of a given book
    :param book: a book
    :return: how many copies available
    """
    with CSVIterator(available_books_path, "r") as iterator:
        next(iterator)
        for row in iterator:
            if row[0] == book.get_title():
                return int(row[1])
    return 0


@check
def decrease_from_availability(book: Book):
    """
    This function reduces the availability of a given book if possible
    and if the current copies amount drops to zero it calls to change
    the is_loaned status of the book
    :param book: a book
    :return: True if succeeded, False otherwise
    """
    rows = []
    check_found = False
    with CSVIterator(available_books_path, "r") as iterator:
        for row in iterator:
            if row[0] == book.get_title():
                x = int(row[1])
                check_found = True
                if x == 0:
                    return False
                x -= 1
                if x == 0:
                    change_loaned_status(row[0])
                row[1] = str(x)
            rows.append(row)

    if check_found:
        with CSVIterator(available_books_path, "w") as iterator:
            iterator.write_rows(rows)

    return check_found


@check
def change_loaned_status(name):
    """
    This function changes the loaned status from True to False or the other way around
    (In the .csv files from Yes to No or the other way around)
    :param name: a name of a book
    :return:
    """
    rows = []
    with CSVIterator(book_path, "r") as iterator:
        for row in iterator:
            if row[0] == name:
                if row[2].lower() == "yes":
                    row[2] = "No"
                else:
                    row[2] = "Yes"
            rows.append(row)

    with CSVIterator(book_path, "w") as iterator:
        iterator.write_rows(rows)


@check
def lend_book(book: Book):
    """
    This function takes care of the logic behind borrowing a book
    :param book: the book to borrow
    :return: True if succeeded, False otherwise
    """
    try:
        return decrease_from_availability(book)
    except Exception as e:
        return False


@check
def return_book(book: Book):
    """
        This function takes care of the logic behind returning a book
        :param book: the book to return
        :return: True if succeeded, False otherwise
        """
    try:
        return increase_available_book(book)
    except Exception as e:
        return False


@check
def increase_available_book(book: Book):
    """
        This function increases the availability of a given book if possible
        and if the current copies amount increases to one it calls to change
        the is_loaned status of the book
        :param book: a book
        :return: True if succeeded, False otherwise
        """
    rows = []
    check_found = False
    with CSVIterator(available_books_path, "r") as iterator:
        for row in iterator:
            if row[0] == book.get_title():
                x = int(row[1])
                if x == 0:
                    change_loaned_status(row[0])
                x += 1
                row[1] = str(x)
                check_found = True
            rows.append(row)

    if check_found:
        with CSVIterator(available_books_path, "w") as iterator:
            iterator.write_rows(rows)

    return check_found


@check
def get_book_name_list():
    """
    This function creates a list of all the books name that exist
    :return: a list of names
    """
    names = []
    with CSVIterator(book_path, "r") as iterator:
        for row in iterator:
            names.append(row[0])

    return names


@check
def update_book(book: Book):
    """
    This function updates the information of a given book
    Note: the title of a books cannot be changed on purpose
    because the book's name is the key for finding it
    :param book: a book to update
    :return:
    """
    rows = []
    with CSVIterator(book_path, "r") as iterator:
        for row in iterator:
            if row[0] == book.get_title():
                row[1] = book.get_author()
                row[2] = book.get_is_loaned()
                row[3] = book.get_copies()
                row[4] = book.get_genre()
                row[5] = book.get_year()
            rows.append(row)

    with CSVIterator(book_path, "w") as iterator:
        iterator.write_rows(rows)


def create_users_csv():
    """
    Creates a user.csv file if non existent
    :return:
    """
    header = ["Username", "Password"]
    with CSVIterator(users_database, "w") as iterator:
        iterator.write_row(header)


def create_book_csv_file():
    """
    Creates a books.csv file if non existent
    :return:
    """
    header = ["title", "author", "is_loaned", "copies", "genre", "year"]
    with CSVIterator(book_path, "w") as iterator:
        iterator.write_row(header)


@check
def add_user(user: User):
    """
    Checks if a given user already exists, if not it registers the new user to users.csv
    :param user: new user
    :return: True if succeeded, False otherwise
    """
    if is_user_exists(user):
        return False

    password = encrypt_password(user.get_password())
    with CSVIterator(users_database, "a") as iterator:
        iterator.write_row([user.get_username(), password])

    return True


@check
def is_user_exists(user: User):
    """
    Check if a given user already exists in users.csv
    :param user: a user
    :return: True if exists
    """
    with CSVIterator(users_database, "r") as iterator:
        for row in iterator:
            if row[0] == user.get_username():
                return True
    return False


def encrypt_password(password):
    """
    This function encrypts a password in a one way fashion using hashlib sha256 encryption
    :param password: a password to encrypt
    :return: encrypted password
    """
    password_bytes = password.encode('utf-8')
    hash_obj = hashlib.sha256(password_bytes)
    hashed_password = hash_obj.hexdigest()
    return hashed_password


@check
def remove_username(user: User):
    """
    This function removes from users.csv a given user by its username
    :param user: user to remove
    :return:
    """
    rows = []
    with CSVIterator(users_database, "r") as iterator:
        for row in iterator:
            if row[0] != user.get_username():
                rows.append(row)

    with CSVIterator(users_database, "w") as iterator:
        iterator.write_rows(rows)


@check
def user_login(user: User):
    """
    This function checks if the given user can log in to the system
    :param user: the user to log in
    :return: True if the user is allowed to log in
    """
    password = encrypt_password(user.get_password())
    with CSVIterator(users_database, "r") as iterator:
        for check_user in iterator:
            if check_user[0] == user.get_username() and check_user[1] == password:
                return True
    return False


@check
def select_book_by_name(name):
    """
    Given a name of a book returns a Book object with all it's properties
    :param name: the books name
    :return: book
    """
    book = None
    with CSVIterator(book_path, "r") as iterator:
        for row in iterator:
            if row[0] == name:
                book = book_factory.get_book("book", row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))

    return book


@check
def select_book_by_author(name):
    """
    Given an author's name the function returns a list with all the books
    written by the given author
    :param name: the author's name
    :return: a list of books
    """
    books = []
    with CSVIterator(book_path, "r") as iterator:
        for row in iterator:
            if row[1] == name:
                book = book_factory.get_book("book", row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))
                books.append(book)

    return books


@check
def select_book_by_genre(genre):
    """
    Given a genre name the function returns a list with all the books
    written by in the same genre
    :param genre: the genre name
    :return: a list of books
    """
    books = []
    with CSVIterator(book_path, "r") as iterator:
        for row in iterator:
            if row[4] == genre:
                book = book_factory.get_book("book", row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))
                books.append(book)

    return books


@check
def select_book_by_year(year):
    """
    Given a year the function returns a list with all the books
    written at the given year
    :param year: the year
    :return: a list of books
    """
    books = []
    with CSVIterator(book_path, "r") as iterator:
        for row in iterator:
            if row[5] == year:
                book = book_factory.get_book("book", row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))
                books.append(book)

    return books


@check
def select_book_by_is_loaned(is_loaned):
    """
    Given an is_loaned value the function returns a list with all the books
    that are currently available or aren't available at all
    :param is_loaned: True or False
    :return: a list of books
    """
    books = []

    if is_loaned:
        is_loaned_string = "yes"
    else:
        is_loaned_string = "no"

    with CSVIterator(book_path, "r") as iterator:
        for row in iterator:
            if row[2].lower() == is_loaned_string:
                book = book_factory.get_book("book", row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))
                books.append(book)

    return books


@check
def select_book_by_copies(copies):
    """
    Given amount of copies the function returns a list with all the books
    of all the books with the same amount of copies
    :param copies: how many copies
    :return: a list of books
    """
    books = []
    with CSVIterator(book_path, "r") as iterator:
        for row in iterator:
            if row[3] == copies:
                book = book_factory.get_book("book", row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))
                books.append(book)

    return books


@check
def get_user_by_username(name):
    """
    Given a username the function returns a new username with the hashed password
    :param name: the username
    :return: a user object
    """
    user = None
    with CSVIterator(users_database, "r") as iterator:
        for row in iterator:
            if row[0] == name:
                user = User(row[0], row[1])

    return user


@check
def init_popular_books():
    """
    This function find the 10 most popular books. (The books that were borrowed the most)
    if there are less than 10 different books that were burrowed it chooses the first ones
    TODO: Think about should I change it so I can have less then 10 most popular books
    :return: a list of the most popular books
    """
    maximum_copies_list = []
    current_copies_list = []
    most_popular_list = []

    with CSVIterator(book_path, "r") as iterator:
        next(iterator)
        for row in iterator:
            maximum_copies_list.append([row[0], int(row[3])])

    with CSVIterator(available_books_path, "r") as iterator:
        next(iterator)
        for row in iterator:
            current_copies_list.append([row[0], int(row[1])])

    i = 0
    for item in maximum_copies_list:
        if len(most_popular_list) < 10:
            most_popular_list.append(item)

        if i > 9:
            gap = maximum_copies_list[i][1] - current_copies_list[i][1]
            if gap > 0:
                minimum_index, minimum_value = find_min_index(maximum_copies_list, current_copies_list,
                                                              most_popular_list)
                if gap > minimum_value:
                    most_popular_list[minimum_index][0] = item[0]
                    most_popular_list[minimum_index][1] = item[1]

        i += 1

    return most_popular_list


def find_min_index(original_list, available_list, most_popular_list):
    """
    This is a helper function for most popular books.
    Given 3 lists it checks which index can it switch in most_popular_list
    by checking the difference between the maximum values and the currently available values
    and returns the index with the smallest difference
    :param original_list: the original list from books.csv
    :param available_list: the available list from available_books.csv
    :param most_popular_list: the current most popular list that is being created
    :return: the index with the smallest difference
    """
    current_min = original_list[0][1] - available_list[0][1]
    min_book_index = 0
    i = 0

    for book in original_list:
        if book in most_popular_list:
            check_min = book[1] - available_list[i][1]
            if check_min < current_min:
                min_book_index = i
            i += 1

    return min_book_index, current_min


@check
def select_books_by_name_partly(name_partly):
    """
    Given a name that is part of a book's name returns all the books that start with the same string
    :param name_partly: the books part_name
    :return: books list
    """
    books = []
    with CSVIterator(book_path, "r") as iterator:
        next(iterator)
        for row in iterator:
            if name_partly.lower() in row[0].lower():
                book = book_factory.get_book("book", row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))
                books.append(book)

    return books


@check
def select_book_by_author_partly(name_partly):
    """
        Given an author's name that is part of an author's name returns all
        the books that start with the same string
        :param name_partly: the authors part_name
        :return: books list
        """
    books = []
    with CSVIterator(book_path, "r") as iterator:
        for row in iterator:
            if name_partly.lower() in row[1].lower():
                book = book_factory.get_book("book", row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))
                books.append(book)

    return books


@check
def select_book_by_genre_partly(genre_partly):
    """
    I highly doubt this will be needed
    Given a part of a genre name returns all the books that start with the same genre name
    :param genre_partly: part of the genres names
    :return: a list of books
    """
    books = []
    with CSVIterator(book_path, "r") as iterator:
        for row in iterator:
            if genre_partly.lower() in row[4].lower():
                book = book_factory.get_book("book", row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))
                books.append(book)

    return books


@check
def get_all_books():
    """
    This function returns a list of all the books that exists in the library
    :return: a list of books
    """
    books = []
    with CSVIterator(book_path, "r") as iterator:
        next(iterator)
        for row in iterator:
            book = book_factory.get_book("book", row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))
            books.append(book)

    return books


@check
def get_borrowed_books():
    """
    This function returns all the books that are currently borrowed from the library
    :return: a list of books
    """
    books = []
    with CSVIterator(book_path, "r") as all_books:
        with CSVIterator(available_books_path, "r") as available_books:
            reader_all = csv.reader(all_books)
            reader_available = csv.reader(available_books)
            next(reader_all)
            next(reader_available)

            for row_all, row_available in zip(reader_all, reader_available):
                if int(row_all[3]) != int(row_available[1]):
                    book = book_factory.get_book("book", row_all[0], row_all[1], row_all[2], int(row_all[3]),
                                                 row_all[4], int(row_all[5]))
                    books.append(book)

    return books
