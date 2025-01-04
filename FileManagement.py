import os
import csv
from Book import Book
from functools import wraps
from User import User
import hashlib


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


@check
def create_available_books_file():
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
            for data in rows:
                writer.writerow([data[0], data[1], data[2], data[3], data[4], data[5]])

        with open(available_books_path, mode="r", newline="") as file:
            reader = csv.reader(file)
            header = next(reader)
            rows = [row for row in reader if row[0] != book.get_title()]

        with open(available_books_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for data in rows:
                writer.writerow([data[0], data[1]])


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
    with open(available_books_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == book.get_title():
                x = int(row[1])
                x -= 1
                row[1] = str(x)
            rows.append(row)

    with open(available_books_path, "w", newline="") as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow([row[0], row[1]])


@check
def lend_book(book: Book):
    if available_copies(book) > 0:
        decrease_from_availability(book)
        return f"Successfully lent the book {book.get_title()}"
    else:
        return f"Failed to lend the book {book.get_title()}"


@check
def get_book_name_list():
    names = []
    with open(book_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            names.append(row[0])

    return names


def create_users_csv():
    header = ["Username", "Password"]
    with open(users_database, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)


def add_user(user: User):
    password = encrypt_password(user.get_password())
    with open(users_database, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([user.get_username(), password])


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
