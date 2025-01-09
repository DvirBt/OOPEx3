import os
import csv
from Book import Book
from functools import wraps
from User import User
import hashlib
from BookFactory import BookFactory

class CSVIterator:

    def __init__(self, file_path):
        self.file_path = file_path
        self.file = None
        self.reader = None

    def __iter__(self):
        self.file = open(self.file_path, "r", newline="")
        self.reader = csv.reader(self.file)
        next(self.reader)
        return self

    def __next__(self):
        if self.reader is None:
            raise StopIteration
        try:
            return next(self.reader)
        except StopIteration:
            self.file.close()
            raise


def check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        check_csv_exists()
        result = func(*args, **kwargs)
        return result

    return wrapper


current_path = os.getcwd()
available_books_path = rf"{current_path}\Files\available_books.csv"
book_path = rf"{current_path}\Files\books.csv"
users_database = rf"{current_path}\Files\users.csv"
book_factory = BookFactory()

def check_csv_exists():
    if not os.path.exists(available_books_path):
        create_available_books_file()
    if not os.path.exists(book_path):
        create_csv_file(book_path)
    if not os.path.exists(users_database):
        create_users_csv()


def create_csv_file(path):
    with open(path, "w") as file:
        file.write("")
    create_csv_header(path)


def create_csv_header(path):
    if path == available_books_path:
        with open(path, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["title", "available"])
    if path == book_path:
        with open(path, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["title", "author", "is_loaned", "copies", "genre", "year"])


def create_available_books_file():
    """
    TODO: Find out why the catcher in the rye's name in available_books.csv is being cut
    :return:
    """
    header = ["title", "available"]
    data = []
    with open(available_books_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)

        with open(book_path, "r") as book_file:
            reader = csv.reader(book_file)
            next(reader)
            for row in reader:
                title = row[0]
                copies = row[3]
                data.append([title, copies])

        with open(available_books_path, "a", newline="") as available_file:
            writer = csv.writer(available_file)
            for item in data:
                writer.writerow([item[0], item[1]])


@check
def add_book(book: Book):
    if book is not None:
        with open(book_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([book.get_title(), book.get_author(), book.get_is_loaned()
                                , book.get_copies(), book.get_genre(), book.get_year()])

        with open(available_books_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([book.get_title(), book.get_copies()])


@check
def remove_book(book: Book):
    if book is not None:
        with open(book_path, mode="r", newline="") as file:
            reader = csv.reader(file)
            header = next(reader)
            rows = [row for row in reader if row[0] != book.get_title()]

        with open(book_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for row in rows:
                writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5]])

        with open(available_books_path, mode="r", newline="") as file:
            reader = csv.reader(file)
            header = next(reader)
            rows = [row for row in reader if row[0] != book.get_title()]

        with open(available_books_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for row in rows:
                writer.writerow([row[0], row[1]])


@check
def available_copies(book: Book):
    count = 0
    with open(available_books_path, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[0] == book.get_title():
                count += int(row[1])
    return count


@check
def decrease_from_availability(book: Book):
    rows = []
    check_found = False
    with open(available_books_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
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
        with open(available_books_path, "w", newline="") as file:
            writer = csv.writer(file)
            for row in rows:
                writer.writerow([row[0], row[1]])

    return check_found

@check
def change_loaned_status(name):
    rows = []
    with open(book_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == name:
                if row[2].lower() == "yes":
                    row[2] = "No"
                else:
                    row[2] = "Yes"
            rows.append(row)

    with open(book_path, "w", newline="") as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5]])

@check
def lend_book(book: Book):
    check_completed = decrease_from_availability(book)
    if check_completed:
        return True
    else:
        return False


@check
def return_book(book: Book):
    try:
        check_completed = increase_available_book(book)
        if check_completed:
            return True
        else:
            return False
    except Exception as e:
        return False


@check
def increase_available_book(book: Book):
    rows = []
    check_found = False
    with open(available_books_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == book.get_title():
                x = int(row[1])
                if x == 0:
                    change_loaned_status(row[0])
                x += 1
                row[1] = str(x)
                check_found = True
            rows.append(row)

    if check_found:
        with open(available_books_path, "w", newline="") as file:
            writer = csv.writer(file)
            for row in rows:
                writer.writerow([row[0], row[1]])

    return check_found


@check
def get_book_name_list():
    names = []
    with open(book_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            names.append(row[0])

    return names


@check
def update_book(book: Book):
    rows = []
    with open(book_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == book.get_title():
                row[1] = book.get_author()
                row[2] = book.get_is_loaned()
                row[3] = book.get_copies()
                row[4] = book.get_genre()
                row[5] = book.get_year()
            rows.append(row)

    with open(book_path, "w", newline="") as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5]])


def create_users_csv():
    header = ["Username", "Password"]
    with open(users_database, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)


@check
def add_user(user: User):
    if is_user_exists(user):
        return False

    password = encrypt_password(user.get_password())
    with open(users_database, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([user.get_username(), password])

    return True


@check
def is_user_exists(user: User):
    with open(users_database, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == user.get_username():
                return True
    return False


def encrypt_password(password):
    password_bytes = password.encode('utf-8')
    hash_obj = hashlib.sha256(password_bytes)
    hashed_password = hash_obj.hexdigest()
    return hashed_password


@check
def remove_username(user: User):
    rows = []
    with open(users_database, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != user.get_username():
                rows.append(row)
    with open(users_database, "w", newline="") as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow([row[0], row[1]])


@check
def user_login(user: User):
    password = encrypt_password(user.get_password())
    with open(users_database, "r", newline="") as file:
        reader = csv.reader(file)
        for check_user in reader:
            if check_user[0] == user.get_username() and check_user[1] == password:
                return True
    return False

@check
def select_book_by_name(name):
    book = None
    with open(book_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == name:
                book = book_factory.get_book("book", row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))

    return book

@check
def select_book_by_author(name):
    books = []
    with open(book_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == name:
                book = book_factory.get_book("book", row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))
                books.append(book)

    return books

@check
def select_book_by_genre(genre):
    books = []
    with open(book_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[4] == genre:
                book = book_factory.get_book("book", row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))
                books.append(book)

    return books

@check
def select_book_by_year(year):
    books = []
    with open(book_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[5] == year:
                book = book_factory.get_book("book",row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))
                books.append(book)

    return books

@check
def select_book_by_is_loaned(is_loaned):
    books = []
    is_loaned_string = ""

    if is_loaned:
        is_loaned_string = "yes"
    else:
        is_loaned_string = "no"

    with open(book_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[2].lower() == is_loaned_string:
                book = book_factory.get_book("book",row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))
                books.append(book)

    return books

@check
def select_book_by_copies(copies):
    books = []
    with open(book_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[3] == copies:
                book = book_factory.get_book("book",row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))
                books.append(book)

    return books

@check
def get_user_by_username(name):
    user = None
    with open(users_database, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == name:
                user = User(row[0], row[1])

    return user

@check
def init_popular_books():
    maximum_copies_list = []
    current_copies_list = []
    most_popular_list = []

    with open(book_path, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            maximum_copies_list.append([row[0],int(row[3])])

    with open(available_books_path, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            current_copies_list.append([row[0], int(row[1])])

    i = 0
    for item in maximum_copies_list:
        if len(most_popular_list) < 10:
            most_popular_list.append(item)

        if i > 9:
            gap = maximum_copies_list[i][1] - current_copies_list[i][1]
            if gap > 0:
                minimum_index, minimum_value = find_min_index(maximum_copies_list,current_copies_list, most_popular_list)
                if gap > minimum_value:
                    most_popular_list[minimum_index][0] = item[0]
                    most_popular_list[minimum_index][1] = item[1]

        i += 1

    return most_popular_list

def find_min_index(original_list,available_list, most_popular_list):
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
    books = []
    with open(book_path, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if name_partly.lower() in row[0].lower():
                book = book_factory.get_book("book", row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))
                books.append(book)

    return books

@check
def select_book_by_author_partly(name_partly):
    books = []
    with open(book_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if name_partly.lower() in row[1].lower():
                book = book_factory.get_book("book", row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))
                books.append(book)

    return books

@check
def select_book_by_genre_partly(genre_partly):
    books = []
    with open(book_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if genre_partly.lower() in row[4].lower():
                book = book_factory.get_book("book", row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))
                books.append(book)

    return books

@check
def get_all_books():
    books = []
    with open(book_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            book = book_factory.get_book("book", row[0], row[1], row[2], int(row[3]), row[4], int(row[5]))
            books.append(book)

    return books

@check
def get_borrowed_books():
    books = []
    with open(book_path, "r", newline="") as all_books:
        with open(available_books_path, "r", newline="") as available_books:
            reader_all = csv.reader(all_books)
            reader_available = csv.reader(available_books)
            next(reader_all)
            next(reader_available)

            for row_all, row_available in zip(reader_all, reader_available):
                if int(row_all[3]) != int(row_available[1]):
                    book = book_factory.get_book("book", row_all[0], row_all[1], row_all[2], int(row_all[3]), row_all[4], int(row_all[5]))
                    books.append(book)

    return books