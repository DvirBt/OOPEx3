from tkinter import *
from tkinter.ttk import Treeview
from PIL import Image, ImageTk
from Book import Book
from FileManagement import lend_book
from User import User
from Library import Library

library = Library()
main_window = Tk()
icon = PhotoImage(file="LibraryLogo.png")
main_window.iconphoto(False, icon)
global user, categories, alert_window, value_tree, categories
#categories = ["Fiction", "Dystopian", "Classic", "Adventure", "Romance", "Psychological Drama", "Philosophy",
             # "Epic Poetry", "Gothic Romance", "Realism", "Modernism", "Satire", "Science Fiction", "Tragedy", "Fantasy"]

def valid_input(input):
    return input.isdigit()

validate_command = main_window.register(valid_input)  # Register the function

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
    register_button.config(command= lambda : register(username_entry.get(), password_entry.get()),
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    register_button.grid(row=5, columnspan=3, padx=250, pady=25, sticky="nsew")
    """"
    image = Image.open("books_png.png")
    photo = ImageTk.PhotoImage(image)
    image_label = Label(main_window, image=photo)
    image_label.grid(row=1, column=2)
    """

def clear():
    # remove all the widgets of the current window
    for widget in main_window.winfo_children():
        widget.destroy()

def init_page():
    # remove all the widgets and create a back button
    clear()
    back_button = Button(main_window, text="Home page")
    back_button.config(command=home_page,
                       font=('Ink Free', 15, 'bold'),
                       bg="#cae8cd")
    back_button.grid(row=10, column=2, pady=10)

def search_book(book_name, author_name):
    book_by_title = library.search_book_by_name(book_name)
    books_by_author = library.search_book_by_author(author_name)
    books_list = []
    if book_by_title:
        books_list.append(book_by_title)
    if books_by_author:
        books_list += books_by_author

    if books_list:
        init_page()
        topic_label = Label(main_window,
                            text="Books",
                            font=('Ink Free', 22, 'bold'),
                            bg="#cae8cd")
        topic_label.grid(row=0, column=1, columnspan=3, padx=100, pady=25, sticky="nsew")
        tree_select_value(books_list)

    else:
        notification("No books found!")

def close_alert_window():
    global alert_window
    alert_window.destroy()
    home_page()

def notification(message):
    global alert_window
    alert_window = Tk()

    # place the alert popup in the middle
    main_window_x = main_window.winfo_x()
    main_window_y = main_window.winfo_y()
    main_window_width = main_window.winfo_width()
    main_window_height = main_window.winfo_height()
    alert_width = 250
    alert_height = 100
    pos_x = main_window_x + (main_window_width // 2) - (alert_width // 2)
    pos_y = main_window_y + (main_window_height // 2) - (alert_height // 2)
    alert_window.geometry(f"{alert_width}x{alert_height}+{pos_x}+{pos_y}")
    alert_window.title("Notification")
    main_window.grid_rowconfigure(1, weight=0)
    main_window.grid_columnconfigure(1, weight=0)
    alert_label = Label(alert_window, text=message)
    alert_label.pack(pady=10) # there is no need for grid -> pack
    alert_button = Button(alert_window, text="ok", command=close_alert_window)
    alert_button.pack(pady=20)
    alert_window.mainloop()

def register_notify(message):
    global alert_window
    alert_window = Tk()

    # place the alert popup in the middle
    main_window_x = main_window.winfo_x()
    main_window_y = main_window.winfo_y()
    main_window_width = main_window.winfo_width()
    main_window_height = main_window.winfo_height()
    alert_width = 250
    alert_height = 100
    pos_x = main_window_x + (main_window_width // 2) - (alert_width // 2)
    pos_y = main_window_y + (main_window_height // 2) - (alert_height // 2)
    alert_window.geometry(f"{alert_width}x{alert_height}+{pos_x}+{pos_y}")
    alert_window.title("Login/Register notifications")
    main_window.grid_rowconfigure(1, weight=0)
    main_window.grid_columnconfigure(1, weight=0)
    alert_label = Label(alert_window, text=message)
    alert_label.pack(pady=10)  # there is no need for grid -> pack
    alert_button = Button(alert_window, text="ok", command=lambda : alert_window.destroy())
    alert_button.pack(pady=20)
    alert_window.mainloop()

def register(username, password):
    global user
    user = User(username, password)
    success = library.register_user(user)
    if success:
        register_notify("User registered successfully!")
    else:
        #notification("User could not be registered!")
        register_notify("User register failed!")

def login(username, password):
    global user
    user = User(username,password)
    user = User("shakedm100", "aesnhftk1")
    success = library.login_user(user)
    if success:
        notification("Login succeeded!")
    else:
        register_notify("Login failed!")

def logout():
    main()

def add_to_categories(category):
    global categories
    if category not in categories:
        categories.append(category)

def add_book(title, author, copies, genre, year):
    book = Book(title, author, False, copies, genre, year)
    success = library.add_book(book)
    if success:
        add_to_categories(book.get_genre())
        notification("Book added successfully!")
    else:
        notification("Book added failed!")


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
    remove_book_button.config(command=remove_book_page,
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
    borrow_book_button.config(command=borrow_book_page,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    borrow_book_button.grid(row=5, column=1, pady=10, sticky="nsew")

    return_book_button = Button(main_window, text="Return Book")
    return_book_button.config(command=return_book_page,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    return_book_button.grid(row=6, column=1, pady=10, sticky="nsew")

    popular_books__button = Button(main_window, text="Popular Books")
    popular_books__button.config(command=popular_page,
                              font=('Ink Free', 15, 'bold'),
                              bg="#cae8cd")
    popular_books__button.grid(row=7, column=1, pady=10, sticky="nsew")

    logout_button = Button(main_window, text="Logout")
    logout_button.config(command=logout,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    logout_button.grid(row=10, column=0, padx=15, pady=25, sticky="nsew")

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

    copies_label = Label(main_window,
                           text="Copies:",
                           font=('Ink Free', 15, 'bold'),
                           bg="#cae8cd")
    copies_label.grid(row=3, column=1, pady=10, sticky="nsew")
    copies_entry = Entry(main_window, textvariable=StringVar(value=0), validate="key", validatecommand=(valid_input, "%P"))
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

    year_entry = Entry(main_window, textvariable=StringVar(value=0), validate="key", validatecommand=(valid_input, "%P"))
    year_entry.grid(row=5, column=2, pady=10, sticky="nsew")

    add_button = Button(main_window, text="Add book")
    add_button.config(command=lambda : add_book(title_entry.get(), author_entry.get(), int(copies_entry.get()), genre_entry.get(), int(year_entry.get())),
                      font=('Ink Free', 22, 'bold'),
                      bg="#cae8cd")
    add_button.grid(row=8, column=2, pady=10, sticky="nsew")

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

    all_button = Button(main_window, text="All books")
    all_button.config(command=lambda: create_tree("All books", library.get_all_books()),
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    all_button.grid(row=1, column=2, pady=10, sticky="nsew")

    available_button = Button(main_window, text="Available books")
    available_button.config(command=lambda: create_tree("Available books", library.get_available_books()),
                            font=('Ink Free', 15, 'bold'),
                            bg="#cae8cd")
    available_button.grid(row=2, column=2, pady=10, sticky="nsew")
    global user
    borrowed_button = Button(main_window, text="Lent books")
    borrowed_button.config(command=lambda: create_tree("All books", library.get_borrowed_books_by_user()),
                           font=('Ink Free', 15, 'bold'),
                           bg="#cae8cd")
    borrowed_button.grid(row=3, column=2, pady=10, sticky="nsew")

    category_button = Button(main_window, text="By category")
    category_button.config(command=category_page,
                           font=('Ink Free', 15, 'bold'),
                           bg="#cae8cd")
    category_button.grid(row=4, column=2, pady=10, sticky="nsew")

def category_page():
    init_page()
    # create all necessary widgets
    view_books_label = Label(main_window,
                           text="By category",
                           font=('Ink Free', 22, 'bold'),
                           bg="#cae8cd")
    view_books_label.grid(row=0, column=1, columnspan=3, padx=220, pady=25, sticky="nsew")

    category_label = Label(main_window,
                         text="Category:",
                         font=('Ink Free', 15, 'bold'),
                         bg="#cae8cd")
    category_label.grid(row=1, column=1, pady=10, sticky="nsew")
    global categories
    selected_category = StringVar(value="")  # Default value is an empty string

    # StringVar to hold the selected category
    selected_category = StringVar()
    selected_category.set("Select a Category")  # Default value

    # Create the OptionMenu
    dropdown = OptionMenu(main_window, selected_category, *categories)
    dropdown.config(font=('Ink Free', 15, 'bold'), width=20)  # Styling the dropdown
    dropdown.grid(row=1, column=2, pady=10, sticky="nsew")

    """"
    # Function to display the selected category
    def show_selection():
        print(f"Selected Category: {selected_category.get()}")
    """

    category_button = Button(main_window, text="Submit")
    category_button.config(command=lambda : create_tree(f"Books of {selected_category.get()}", library.get_book_by_genre(selected_category.get())),
                         font=('Ink Free', 15, 'bold'),
                         bg="#cae8cd")
    category_button.grid(row=2, column=2, pady=20, sticky="nsew")

# TODO: implement for borrowed different columns!
def create_tree_for_borrowed(books_list):
    init_page()
    books_label = Label(main_window,
                        text="Lent books",
                        font=('Ink Free', 22, 'bold'),
                        bg="#cae8cd")
    books_label.grid(row=0, column=1, columnspan=3, padx=100, pady=25, sticky="nsew")

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
    tree.column("Author", width=130)
    tree.column("Is loaned?", width=70)
    tree.column("Copies", width=50)
    tree.column("Genre", width=80)
    tree.column("Year", width=50)
    v_scrollbar = Scrollbar(main_window, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=v_scrollbar.set)
    v_scrollbar.grid(row=2, column=3, sticky="ns")
    tree.grid(row=2, column=2, padx=40, pady=20, sticky="nsew")

    for item in books_list:
        tree.insert("", "end",
                    values=(
                    item.get_title(), item.get_author(), item.get_is_loaned(), item.get_copies(), item.get_genre(),
                    item.get_year()))


def create_tree(topic, book_list):
    init_page()
    books_label = Label(main_window,
                           text=f"{topic}",
                           font=('Ink Free', 22, 'bold'),
                           bg="#cae8cd")
    books_label.grid(row=0, column=1, columnspan=3, padx=100, pady=25, sticky="nsew")

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
    tree.column("Author", width=130)
    tree.column("Is loaned?", width=70)
    tree.column("Copies", width=50)
    tree.column("Genre", width=80)
    tree.column("Year", width=50)
    v_scrollbar = Scrollbar(main_window, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=v_scrollbar.set)
    v_scrollbar.grid(row=2, column=3, sticky="ns")
    tree.grid(row=2, column=2, padx=40, pady=20, sticky="nsew")

    for item in book_list:
        tree.insert("", "end",
                    values=(item.get_title(), item.get_author(), item.get_is_loaned(), item.get_copies(), item.get_genre(), item.get_year()))

    #tree.pack(fill="both", expand=True)

def popular_page():
    books_list = library.get_popular_list()
    if books_list:
        init_page()
        create_tree("Popular books", books_list)
    else:
        notification("No popular books!")

def get_selected_book_from_tree(event=None):
    global value_tree
    selected_book = value_tree.selection()
    if selected_book:
        item_values = value_tree.item(selected_book, "values")
        title = item_values[0]
        author = item_values[1]
        is_loaned = item_values[2]
        copies = item_values[3]
        genre = item_values[4]
        year = item_values[5]
        return Book(title, author, is_loaned, copies, genre, year)
    else:
        notification("Invalid book!")
        return None

def return_book_page():
    init_page()
    return_label = Label(main_window,
                         text="Return a book",
                         font=('Ink Free', 22, 'bold'),
                         bg="#cae8cd")
    return_label.grid(row=0, column=1, columnspan=3, padx=220, pady=25, sticky="nsew")
    global user
    borrowed_books_list = library.get_borrowed_books_by_user()
    if borrowed_books_list:
        tree_select_value(borrowed_books_list)

    else:
        notification("No borrowed books by this user!")

def tree_select_value(books_list):
    global value_tree
    columns = ("Title", "Author", "Is loaned?", "Copies", "Genre", "Year")
    value_tree = Treeview(main_window, columns=columns, show="headings", height=10)
    # set headings
    value_tree.heading("Title", text="Title")
    value_tree.heading("Author", text="Author")
    value_tree.heading("Is loaned?", text="Is loaned?")
    value_tree.heading("Copies", text="Copies")
    value_tree.heading("Genre", text="Genre")
    value_tree.heading("Year", text="Year")
    # set columns
    value_tree.column("Title", width=150)
    value_tree.column("Author", width=130)
    value_tree.column("Is loaned?", width=70)
    value_tree.column("Copies", width=50)
    value_tree.column("Genre", width=80)
    value_tree.column("Year", width=50)
    v_scrollbar = Scrollbar(main_window, orient=VERTICAL, command=value_tree.yview)
    value_tree.configure(yscrollcommand=v_scrollbar.set)
    v_scrollbar.grid(row=2, column=3, sticky="ns")
    value_tree.bind("<<TreeviewSelect>>", get_selected_book_from_tree) # value_tree.selection()
    value_tree.grid(row=2, column=2, padx=20, pady=20, sticky="nsew")

    for item in books_list:
        value_tree.insert("", "end",
                    values=(
                    item.get_title(), item.get_author(), item.get_is_loaned(), item.get_copies(), item.get_genre(),
                    item.get_year()))


def remove_book(book):
    success = library.remove_book(book)
    if success:
        notification("Book removed successfully!")
        home_page()
    else:
        notification("Book removed failed!")

def remove_book_page():
    init_page()
    remove_label = Label(main_window,
                         text="Remove a book",
                         font=('Ink Free', 22, 'bold'),
                         bg="#cae8cd")
    remove_label.grid(row=0, column=1, columnspan=3, padx=220, pady=25, sticky="nsew")
    books_list = library.get_all_books()
    if books_list:
        global value_tree
        tree_select_value(books_list)
        remove_button = Button(main_window, text="Remove selected book")
        remove_button.config(command=lambda: remove_book(get_selected_book_from_tree()),
                             font=('Ink Free', 15, 'bold'),
                             bg="#cae8cd")
        remove_button.grid(row=4, column=1, columnspan=3, padx=100, pady=25, sticky="nsew")

    else:
        notification("No books to remove!")

def try_lend_book(book, copies, client, email, phone):
    global user
    success = library.borrow_book(book, user, copies, client, email, phone) # ALWAYS TRUE!!!
    if success:
        notification("Book lend successfully!")
    else:
        notification("Book lend failed!")

def borrow_book_page():
    init_page()
    main_window.grid_rowconfigure(1, weight=0)
    main_window.grid_columnconfigure(1, weight=0)
    borrow_label = Label(main_window,
                         text="Lend a book",
                         font=('Ink Free', 22, 'bold'),
                         bg="#cae8cd")
    borrow_label.grid(row=0, column=1, columnspan=3, padx=100, pady=15, sticky="nsew")
    books_list = library.get_all_books()
    if books_list:
        global value_tree
        tree_select_value(books_list)
        copies_label = Label(main_window,
                             text="Amount:",
                             font=('Ink Free', 15, 'bold'),
                             bg="#cae8cd")
        copies_label.grid(row=3, column=2, padx=100, pady=5, sticky="w")
        copies_entry = Entry(main_window, textvariable=StringVar(value=1), validate="key", validatecommand=(valid_input, "%P"))
        copies_entry.grid(row=3, column=2, padx=50, pady=5)

        client_label = Label(main_window,
                             text="Name:",
                             font=('Ink Free', 15, 'bold'),
                             bg="#cae8cd")
        client_label.grid(row=4, column=2, padx=100, pady=5, sticky="w")
        client_entry = Entry(main_window)
        client_entry.grid(row=4, column=2, padx=50, pady=5)

        email_label = Label(main_window,
                             text="Email:",
                             font=('Ink Free', 15, 'bold'),
                             bg="#cae8cd")
        email_label.grid(row=5, column=2, padx=100, pady=5, sticky="w")
        email_entry = Entry(main_window)
        email_entry.grid(row=5, column=2, padx=50, pady=5)

        phone_label = Label(main_window,
                             text="Phone:",
                             font=('Ink Free', 15, 'bold'),
                             bg="#cae8cd")
        phone_label.grid(row=6, column=2, padx=100, pady=10, sticky="w")
        phone_entry = Entry(main_window, textvariable=StringVar(value=0), validate="key",
                             validatecommand=(valid_input, "%P"))
        phone_entry.grid(row=6, column=2, padx=50, pady=5)

        lend_button = Button(main_window, text="Lend selected book")
        lend_button.config(command=lambda: try_lend_book(get_selected_book_from_tree(), int(copies_entry.get()), client_entry.get(), email_entry.get(), int(phone_entry.get())),
                             font=('Ink Free', 15, 'bold'),
                             bg="#cae8cd")
        lend_button.grid(row=7, column=1, columnspan=2, padx=100, pady=10, sticky="nsew")

    else:
        notification("No books to remove!")

if __name__ == "__main__":
    books = library.get_all_books()
    categories = []
    for book in books:
        if book.get_genre() not in categories:
            categories.append(book.get_genre())
    main()
