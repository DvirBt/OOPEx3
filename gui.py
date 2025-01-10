from tkinter import *
from tkinter.ttk import Treeview

from Book import Book
from OOPEx3.Main import library
from User import User
from Library import Library

library = Library()
main_window = Tk()
#main_frame = Frame(main_window)
#icon = PhotoImage(file="library.jpeg")
#window.iconphoto(False, icon)
global user, book, my_categories


def main():
    main_window.geometry("640x640")
    main_window.config(background="#cae8cd")
    login_page()
    main_window.mainloop()

def login_page():
    global user
    user = None
    clear()
    main_window.title("Login/Register")
    main_window.grid_rowconfigure(1, weight=0)
    main_window.grid_columnconfigure(1, weight=0)

    login_label = Label(main_window,
                        text="Login / Register page",
                        font=('Ink Free', 30, 'bold'),
                        bg="#cae8cd",
                        pady=40)
    login_label.grid(row=0, columnspan=3, padx=170, pady=10, sticky="nsew")

    username_label = Label(main_window,
                        text="Username: ",
                        font=('Ink Free', 18, 'bold'),
                        bg="#cae8cd")
    username_label.grid(row=1, column=0, columnspan=1, pady=25, sticky="nsew")

    username_entry = Entry(main_window, width=20)
    username_entry.grid(row=1, column=1, pady=25, sticky="nsew")

    password_label = Label(main_window,
                        text="Password: ",
                        font=('Ink Free', 18, 'bold'),
                        bg="#cae8cd")
    password_label.grid(row=2, column=0, pady=25, sticky="nsew")

    password_entry = Entry(main_window, show="*", width=20)
    password_entry.grid(row=2, column=1, pady=25, sticky="nsew")

    # Buttons
    login_button = Button(main_window, text="Login")
    login_button.config(command=lambda: login(username_entry.get(), password_entry.get()),
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    login_button.grid(row=4, columnspan=3, padx=250, pady=25, sticky="nsew")

    register_button = Button(main_window, text="Register") # (username_entry.get(), password_entry.get())
    register_button.config(command=register,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    register_button.grid(row=5, columnspan=3, padx=250, pady=25, sticky="nsew")

def clear():
    # remove all the widgets of the current window
    for widget in main_window.winfo_children():
        widget.destroy()

def init_page():
    # remove all the widgets and create a back button
    clear()
    #back()
    back_button = Button(main_window, text="Home page")
    back_button.config(command=home_page,
                       font=('Ink Free', 15, 'bold'),
                       bg="#cae8cd")
    back_button.grid(row=10, column=2, pady=10, sticky="nsew")

def add_book():
    global book
    library.add_book(book)

def search_book(book_name, author_name):
    books_by_name = library.get_book_by_name(book_name)
    books_by_author = library.get_book_by_author(author_name)
    books_list = [books_by_name] + [books_by_author]
    create_list(books_list)

def borrow_book():
    pass

def notification(message):
    alert = Label(main_window,
                  text=message,
                  font=('Ink Free', 18, 'bold'),
                  bg="#cae8cd")
    alert.grid(row=6, columnspan=4, padx=220, pady=25, sticky="nsew")

def register(username, password):
    global user
    user = User(username, password)
    success = library.register_user(user)
    if success:
        notification("User created successfully!")
    else:
        notification("User could not be registered!")


def login(username, password):
    global user
    user = User(username,password)
    success = library.login_user(user)
    if success:
        home_page()
    else:
        notification("Login failed!")

def logout():
    main()

def books_by_category(category):
    pass

def home_page():
    global user
    clear()
    main_window.title("Library")
    main_window.grid_rowconfigure(1, weight=0)
    main_window.grid_columnconfigure(1, weight=0)

    welcome = Label(main_window,
                    text=f"Welcome back {user.get_username()}",
                    font=('Ink Free', 22, 'bold'),
                    bg="#cae8cd")
    welcome.grid(row=0, column=1, pady=25, sticky="nsew")

    add_button = Button(main_window, text="Add Book")
    add_button.config(command=add_book_page,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    add_button.grid(row=1, column=1, pady=10, sticky="nsew")

    remove_book_button = Button(main_window, text="Remove Book")
    remove_book_button.config(command=remove_book,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    remove_book_button.grid(row=2, column=1, pady=10, sticky="nsew")

    search_book_button = Button(main_window, text="Search Book")
    search_book_button.config(command=search_page,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    search_book_button.grid(row=3, column=1, pady=10, sticky="nsew")

    view_books_button = Button(main_window, text="View Books")
    view_books_button.config(command=view_books_page,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    view_books_button.grid(row=4, column=1, pady=10, sticky="nsew")

    borrow_book_button = Button(main_window, text="Lend Book")
    borrow_book_button.config(command=borrow_book,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    borrow_book_button.grid(row=5, column=1, pady=10, sticky="nsew")

    return_book_button = Button(main_window, text="Return Book")
    return_book_button.config(command=return_book,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    return_book_button.grid(row=6, column=1, pady=10, sticky="nsew")

    logout_button = Button(main_window, text="Logout")
    logout_button.config(command=logout,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    logout_button.grid(row=10, column=0, pady=25, sticky="nsew")

def add_book_page():
    init_page()
    # create all necessary widgets
    add_book_label = Label(main_window,
                    text="Add a new book",
                    font=('Ink Free', 22, 'bold'),
                    bg="#cae8cd")
    add_book_label.grid(row=0, column=1, columnspan=3, padx=220, pady=25, sticky="nsew")

    title_label = Label(main_window,
                           text="Title:",
                           font=('Ink Free', 15, 'bold'),
                           bg="#cae8cd")
    title_label.grid(row=1, column=1, pady=10, sticky="nsew")

    title_entry = Entry(main_window)
    title_entry.grid(row=1, column=2, pady=10, sticky="nsew")

    author_label = Label(main_window,
                        text="Author:",
                        font=('Ink Free', 15, 'bold'),
                        bg="#cae8cd")
    author_label.grid(row=2, column=1, pady=10, sticky="nsew")

    author_entry = Entry(main_window)
    author_entry.grid(row=2, column=2, pady=10, sticky="nsew")

    """""
    isloaned_label = Label(main_window,
                         text="Is loaned?",
                         font=('Ink Free', 15, 'bold'),
                         bg="#cae8cd")
    isloaned_label.grid(row=3, column=1, pady=10, sticky="nsew")

    isloaned_checkbox = Checkbutton(main_window)
    isloaned_checkbox.grid(row=3, column=2, pady=10, sticky="nsew")
    """

    copies_label = Label(main_window,
                           text="Copies:",
                           font=('Ink Free', 15, 'bold'),
                           bg="#cae8cd")
    copies_label.grid(row=3, column=1, pady=10, sticky="nsew")

    copies_entry = Entry(main_window)
    copies_entry.grid(row=3, column=2, pady=10, sticky="nsew")

    genre_label = Label(main_window,
                         text="Genre:",
                         font=('Ink Free', 15, 'bold'),
                         bg="#cae8cd")
    genre_label.grid(row=4, column=1, pady=10, sticky="nsew")

    genre_entry = Entry(main_window)
    genre_entry.grid(row=4, column=2, pady=10, sticky="nsew")

    year_label = Label(main_window,
                        text="Year:",
                        font=('Ink Free', 15, 'bold'),
                        bg="#cae8cd")
    year_label.grid(row=5, column=1, pady=10, sticky="nsew")

    year_entry = Entry(main_window)
    year_entry.grid(row=5, column=2, pady=10, sticky="nsew")

    global book
    book = Book(title_entry.get(), author_entry.get(), False, copies_entry.getint, genre_entry.get(), year_entry.getint)
    add_button = Button(main_window, text="Add book")
    add_button.config(command=add_book,
                      font=('Ink Free', 22, 'bold'),
                      bg="#cae8cd")
    add_button.grid(row=8, column=2, pady=25, sticky="nsew")

def search_page():
    init_page()
    search_label = Label(main_window,
                             text="Search books",
                             font=('Ink Free', 22, 'bold'),
                             bg="#cae8cd")
    search_label.grid(row=0, column=1, columnspan=3, padx=220, pady=25, sticky="nsew")

    title_label = Label(main_window,
                         text="Title:",
                         font=('Ink Free', 15, 'bold'),
                         bg="#cae8cd")
    title_label.grid(row=1, column=1, pady=10, sticky="nsew")

    title_entry = Entry(main_window)
    title_entry.grid(row=1, column=2, pady=10, sticky="nsew")

    author_label = Label(main_window,
                        text="Author:",
                        font=('Ink Free', 15, 'bold'),
                        bg="#cae8cd")
    author_label.grid(row=2, column=1, pady=10, sticky="nsew")

    author_entry = Entry(main_window)
    author_entry.grid(row=2, column=2, pady=10, sticky="nsew")

    search_button = Button(main_window, text="Search")
    search_button.config(command=lambda: search_book(title_entry.get(), author_entry.get()),
                      font=('Ink Free', 22, 'bold'),
                      bg="#cae8cd")
    search_button.grid(row=3, column=2, pady=25, sticky="nsew")

def view_books_page():
    init_page()
    # create all necessary widgets
    view_books_label = Label(main_window,
                           text="View books",
                           font=('Ink Free', 22, 'bold'),
                           bg="#cae8cd")
    view_books_label.grid(row=0, column=1, columnspan=3, padx=220, pady=25, sticky="nsew")
    #view_books_label.pack()

    category_button = Button(main_window, text="By category")
    category_button.config(command=category_page,
                         font=('Ink Free', 15, 'bold'),
                         bg="#cae8cd")
    category_button.grid(row=1, column=2, pady=20, sticky="nsew")

    popular_button = Button(main_window, text="Popular books")
    popular_button.config(command=popular_page,
                           font=('Ink Free', 15, 'bold'),
                           bg="#cae8cd")
    popular_button.grid(row=2, column=2, pady=20, sticky="nsew")


def create_list(book_list):
    init_page()

    books_label = Label(main_window,
                           text="Books",
                           font=('Ink Free', 22, 'bold'),
                           bg="#cae8cd")
    books_label.grid(row=0, column=1, columnspan=3, padx=220, pady=25, sticky="nsew")

    columns = ("Title", "Author", "Is loaned?", "Copies", "Genre", "Year")
    tree = Treeview(main_window, columns=columns, show="headings", height=10)
    # set headings
    tree.heading("Title", text="Title")
    tree.heading("Author", text="Author")
    tree.heading("Is loaned?", text="Is loaned?")
    tree.heading("Copies", text="Copies")
    tree.heading("Genre", text="Genre")
    tree.heading("Year", text="Year")
    # set columns
    tree.column("Title", width=150)
    tree.column("Author", width=100)
    tree.column("Is loaned?", width=75)
    tree.column("Copies", width=75)
    tree.column("Genre", width=75)
    tree.column("Year", width=75)
    tree.grid(row=2, column=2, padx=20, pady=20, sticky="nsew")

    for item in book_list:
        tree.insert("", "end",
                    values=(item.get_title(), item.get_author(), item.get_is_loaned(), item.get_copies(), item.get_genre(), item.get_year()))
                        #item["_title"], item["_author"], item["_is_loaned"], item["_copies"], item["_genre"], item["_year"]))

    #tree.pack(fill="both", expand=True)

def category_page(category):
    init_page()
    category_label = Label(main_window,
                             text=f"Books of {category}",
                             font=('Ink Free', 22, 'bold'),
                             bg="#cae8cd")
    category_label.grid(row=0, column=1, columnspan=3, padx=220, pady=25, sticky="nsew")

    categories = ["Fiction", "Dystopian", "Classic", "Adventure", "Romance", "Psychological Drama", "Philosophy", "Epic Poetry",
                  "Gothic Romance", "Realism", "Modernism", "Satire", "Science Fiction", "Tragedy", "Fantasy"]

    variables = [IntVar() for _ in categories]
    # Creating Checkbuttons
    for i, option in enumerate(categories):
        Checkbutton(main_window, text=option, variable=variables[i]).grid(anchor="w")

    # Submit Button
    submit_button = Button(main_window, text="Submit", command=lambda : create_categories_list(categories, variables))
    submit_button.grid(pady=10)

    global my_categories
    books = None
    for category in my_categories:
        books += library.get_book_by_genre(category)

    create_list(books)

def create_categories_list(categories, variables):
    global my_categories
    my_categories = [categories[i] for i in range(len(categories)) if variables[i].get() == 1]

def popular_page():
    init_page()
    popular_label = Label(main_window,
                         text="Popular books",
                         font=('Ink Free', 22, 'bold'),
                         bg="#cae8cd")
    popular_label.grid(row=0, column=1, columnspan=3, padx=220, pady=25, sticky="nsew")
    create_list(library)

def remove_page():
    init_page()
    remove_label = Label(main_window,
                           text="Remove a book",
                           font=('Ink Free', 22, 'bold'),
                           bg="#cae8cd")
    remove_label.grid(row=0, column=1, columnspan=3, padx=220, pady=25, sticky="nsew")


def return_book():
    init_page()
    return_label = Label(main_window,
                           text="Return a book",
                           font=('Ink Free', 22, 'bold'),
                           bg="#cae8cd")
    return_label.grid(row=0, column=1, columnspan=3, padx=220, pady=25, sticky="nsew")

    title_label = Label(main_window,
                        text="Title:",
                        font=('Ink Free', 15, 'bold'),
                        bg="#cae8cd")
    title_label.grid(row=1, column=1, pady=10, sticky="nsew")

    title_entry = Entry(main_window)
    title_entry.grid(row=1, column=2, pady=10, sticky="nsew")

    author_label = Label(main_window,
                         text="Author:",
                         font=('Ink Free', 15, 'bold'),
                         bg="#cae8cd")
    author_label.grid(row=2, column=1, pady=10, sticky="nsew")

    author_entry = Entry(main_window)
    author_entry.grid(row=2, column=2, pady=10, sticky="nsew")

    copies_label = Label(main_window,
                         text="Copies:",
                         font=('Ink Free', 15, 'bold'),
                         bg="#cae8cd")
    copies_label.grid(row=3, column=1, pady=10, sticky="nsew")

    copies_entry = Entry(main_window)
    copies_entry.grid(row=3, column=2, pady=10, sticky="nsew")

    genre_label = Label(main_window,
                        text="Genre:",
                        font=('Ink Free', 15, 'bold'),
                        bg="#cae8cd")
    genre_label.grid(row=4, column=1, pady=10, sticky="nsew")

    genre_entry = Entry(main_window)
    genre_entry.grid(row=4, column=2, pady=10, sticky="nsew")

    year_label = Label(main_window,
                       text="Year:",
                       font=('Ink Free', 15, 'bold'),
                       bg="#cae8cd")
    year_label.grid(row=5, column=1, pady=10, sticky="nsew")

    year_entry = Entry(main_window)
    year_entry.grid(row=5, column=2, pady=10, sticky="nsew")

    global book
    book = Book(title_entry.get(), author_entry.get(), False, copies_entry.getint,
                genre_entry.get(), year_entry.getint)
    return_button = Button(main_window, text="Return book")
    return_button.config(command=lambda : library.return_book(book),
                      font=('Ink Free', 22, 'bold'),
                      bg="#cae8cd")
    return_button.grid(row=8, column=2, pady=25, sticky="nsew")

def remove_book(remove):
    pass

if __name__ == "__main__":
    main()
