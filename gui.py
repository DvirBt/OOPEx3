from tkinter import *
from tkinter.ttk import Treeview
from Book import Book
from User import User
from Library import Library

"""""
Global variables
================
"""""

library = Library()
main_window = Tk()
icon = PhotoImage(file="LibraryLogo.png")
main_window.iconphoto(False, icon)
global user, categories, alert_window, value_tree, categories

"""""
Helper functions
=================
"""""

def valid_input(parameter):
    """
    Checks if the input represents an Integer.

    Parameters
    ----------
    parameter : String
        A String.

    Returns
    -------
    boolean
        True if the String contains only numbers. Otherwise - False.
    """

    try:
        # Try converting the input to an integer
        int(parameter)
        return True
    except ValueError:
        return False

    #return parameter.isdigit()

validate_command = main_window.register(valid_input)  # Register the function

def main():
    """
    Configurate the main window Tkinter and navigates to Login Register Page
    """
    main_window.geometry("640x640")
    main_window.config(background="#cae8cd")
    login_page()
    main_window.mainloop()

def clear():
    """
    Remove all the widgets of the current window
    """
    for widget in main_window.winfo_children():
        widget.destroy()

def init_page():
    """
    Remove all the widgets of the current window and creating a button which returns to Home Page.
    """
    clear()
    back_button = Button(main_window, text="Home page")
    back_button.config(command=home_page,
                       font=('Times New Roman', 15, 'bold'),
                       bg="#cae8cd")
    back_button.grid(row=10, column=2, pady=10)

def search_book(book_name, author_name):
    """
    Searches a book by title or it's author.
    The search checks first for books by the full title of the book or author.
    Then, checks for books and authors which contains parts of the given parameters.

    Parameters
    ----------
    book_name : String
        The title of the book.

    author_name : String
        The name of the author.

    Returns
    -------
    list
         Of books which contains the full or partial name of it's title or author.
    """
    if book_name == "":
        book_name = None
    if author_name == "":
        author_name = None

    books_by_title = library.search_book_by_name(book_name)
    books_by_author = library.search_book_by_author(author_name)

    books_list = []

    if books_by_title:
        for book in books_by_title:
            books_list.append(book)

    if books_by_author:
        for book in books_by_author:
            if book not in books_list:
                books_list.append(book)

    if books_list:
        init_page()
        topic_label = Label(main_window,
                            text="Books",
                            font=('Times New Roman', 22, 'bold'),
                            bg="#cae8cd")
        topic_label.grid(row=0, column=1, columnspan=3, padx=100, pady=25, sticky="nsew")
        create_tree_for_view_page("Results", books_list)

    else:
        notification("No books found!", search_page)

def notification(message, next_page):
    """
    Opens a pop-up Tkinter window as a notification.

    Parameters
    ----------
    message : String
        The notification.

    next_page : String
        The next page to go to.
    """
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
    alert_button = Button(alert_window, text="ok", command= lambda : alert_window.destroy())
    alert_button.pack(pady=10)
    #alert_window.mainloop()
    if next_page:
        next_page()

def register(username, password):
    """
    Registers a new User by a given username and password.

    Parameters
    ----------
    username : String
        The username of the new User.

    password : String
        The password of the new User.
    -------
    A notification with the relevant message if the new User created successfully or failed.
    """
    global user
    user = User(username, password)
    success = library.register_user(user)
    if success:
        notification("User registered successfully!", login_page)
    else:
        notification("User register failed!", None)

def login(username, password):
    """
    Logs in to an existing User by entering username and password.

    Parameters
    ----------
    username : String
        The username.

    password : String
        The password.
    -------
    A notification with the relevant message if the user managed to log in successfully or failed.
    If the user is valid - navigates to Home Page.
    """
    global user
    user = User(username,password)
    success = library.login_user(user)
    if success:
        notification("Login succeeded!", home_page)
    else:
        notification("Login failed!", None)

def logout():
    """
    Logs out of the user and returns to the Login Register Page.
    """
    if user:
        library.logout(True)
    else:
        library.logout(False)
    main()

def add_to_categories(category):
    """
    Adds a new category to the list of categories if a new book with a new category is created.

    Parameters
    ----------
    category : String
        The category.
    """
    global categories
    if category not in categories:
        categories.append(category)

def add_book(title, author, copies, genre, year):
    """
    Adds a new book to the Library.

    Parameters
    ----------
    title : String
        The title of the book

    author : String
        The author of the book.

    copies : String
        The amount of copies of the book.

    genre : String
        The category of the book.

    year : String
        The year the book established.
    -------
    A notification with the relevant message if the book is created successfully or failed.
    """

    if title == "" or author == "" or copies == "" or genre == "" or year == "":
        notification("Fill all the entries!", None)
        return

    if not valid_input(year):
        notification("Year must be a number!", None)
        return

    # determine is_loaned? property
    if copies == "0":
        book = Book(title, author, True, 0, genre, int(year))
    else:
        book = Book(title, author, False, int(copies), genre, int(year))

    success = library.add_book(book)
    if success:
        add_to_categories(book.get_genre())
        notification("Book added successfully!", add_book_page)
    else:
        notification("Book added failed!", None)

def try_return_book(book):
    """
    Attempts to return a given book.

    Parameters
    ----------
    book : Book
        A book to be returned to the Library.

    Returns
    -------
    Book
        The selected book of the TreeView.
    """
    if book:
        success = library.return_book(book)
    else:
        success = False

    if success:
        if len(library.get_borrowed_books()) > 0:
            notification("Book returned successfully!", return_book_page)
        else:
            notification("Book returned successfully!\nNo more books to return!", home_page)
    else:
        notification("Book returned failed!", return_book_page)


def try_lend_book(book, client, email, phone):
    """
    Attempts to lend a book from the Library.

    Parameters
    ----------
    book : Book
        The Book that will be lent.

    client : String
        The name of the client.

    email : String
        The email of the client.

    phone : String
        The phone number of the client.
    ----------
    A pop-up notification will appear with the relevant message if the Book has been lent successfully or failed.
    """
    global user
    if book:
        success = library.borrow_book(book, user, client, email, phone)
    else:
        success = False

    if success == 0:
        notification("Book lend failed!", None)
    elif success == 1:
        notification("Book lend successfully!", borrow_book_page)
    else:  # success == 2 -> entered the queue
        notification("This book is unavailable at the moment!\nYou entered to the waiting list!", borrow_book_page)


def remove_book(book):
    """
    Removes a book from the Library.

    Parameters
    ----------
    book : Book
        The Book that will be removed.
    ----------
    A pop-up notification will appear with the relevant message if the Book has been removed successfully or failed.
    """
    if book:
        success = library.remove_book(book)
    else:
        success = False

    if success:
        notification("Book removed successfully!", remove_book_page)
    else:
        notification("Book removed failed!", None)

"""""
TreeView methods
=================
"""""

def get_selected_book_from_tree(event=None):
    """
    Gets the selected book from the TreeView.

    Parameters
    ----------
    event : event
        An even which is None.

    Returns
    -------
    Book
        The selected book of the TreeView.
    """
    global value_tree
    selected_book = value_tree.selection()
    if selected_book:
        item_values = value_tree.item(selected_book, "values")
        title = item_values[0]
        book = library.search_book_by_name(title) # returns a list
        if book:
            return book[0]
        else:
            notification("Invalid book!", None)
    else:
        #notification("Invalid book!", None)
        return None

def tree_select_value(books_list):
    """
    Creates a TreeView that a Book can be selected from.

    Parameters
    ----------
    books_list : list
        The list of the Books that will be displayed.
    """
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

    if books_list:
        for item in books_list:
            value_tree.insert("", "end",
                    values=(
                    item.get_title(), item.get_author(), item.get_is_loaned(), item.get_copies(), item.get_genre(),
                    item.get_year()))


def create_tree_for_view_page(topic, book_list):
    """
    Creates a new page with a given topic and a TreeView out of the list of the books.

    Parameters
    ----------
    topic : String
        The topic of this page.

    book_list : list
        The list of the books.
    """
    init_page()
    books_label = Label(main_window,
                           text=f"{topic}",
                           font=('Times New Roman', 22, 'bold'),
                           bg="#cae8cd")
    books_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    if topic != "Popular books":
        back_button = Button(main_window, text="Back")
        back_button.config(command=lambda: view_books_page(),
                         font=('Times New Roman', 15, 'bold'),
                         bg="#cae8cd")
        back_button.grid(row=0, column=0, columnspan=3, padx=50, pady=25, sticky="w")
        if topic == "Results":
            back_button.config(command=lambda : search_page())

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

    if book_list:
        for item in book_list:
            tree.insert("", "end",
                    values=(item.get_title(), item.get_author(), item.get_is_loaned(), item.get_copies(), item.get_genre(), item.get_year()))

"""""
Pages
======
"""""

def login_page():
    """
    Login Register page
    --------------------
    Available functions:
        - Login with a username and a password
        - Register a new user
    """
    global user
    user = None
    clear()
    main_window.title("Login/Register")
    main_window.grid_rowconfigure(1, weight=0)
    main_window.grid_columnconfigure(1, weight=0)

    login_label = Label(main_window,
                        text="Login / Register page",
                        font=('Times New Roman', 30, 'bold'),
                        bg="#cae8cd",
                        pady=40)
    login_label.grid(row=0, columnspan=3, padx=150, pady=10, sticky="nsew")

    username_label = Label(main_window,
                        text="Username: ",
                        font=('Times New Roman', 18, 'bold'),
                        bg="#cae8cd")
    username_label.grid(row=1, column=0, columnspan=1, pady=25, sticky="nsew")

    username_entry = Entry(main_window, width=20)
    username_entry.grid(row=1, column=1, pady=25, sticky="nsew")

    password_label = Label(main_window,
                        text="Password: ",
                        font=('Times New Roman', 18, 'bold'),
                        bg="#cae8cd")
    password_label.grid(row=2, column=0, pady=25, sticky="nsew")

    password_entry = Entry(main_window, show="*", width=20)
    password_entry.grid(row=2, column=1, pady=25, sticky="nsew")

    # Buttons
    login_button = Button(main_window, text="Login")
    login_button.config(command=lambda: login(username_entry.get(), password_entry.get()),
                      font=('Times New Roman', 15, 'bold'),
                      bg="#cae8cd")
    login_button.grid(row=4, columnspan=3, padx=250, pady=25, sticky="nsew")

    register_button = Button(main_window, text="Register") # (username_entry.get(), password_entry.get())
    register_button.config(command= lambda : register(username_entry.get(), password_entry.get()),
                      font=('Times New Roman', 15, 'bold'),
                      bg="#cae8cd")
    register_button.grid(row=5, columnspan=3, padx=250, pady=25, sticky="nsew")

def home_page():
    """
    Home Page
    ----------
    Available functions:
        - Add a new book
        - Remove an existing book
        - Search a book
        - View books
        - Lend a book
        - Return a book
        - Popular books
        - Logout
    """
    global user
    clear()
    main_window.title("Library")
    main_window.grid_rowconfigure(1, weight=0)
    main_window.grid_columnconfigure(1, weight=0)

    welcome = Label(main_window,
                    text=f"Welcome back {user.get_username()}",
                    font=('Times New Roman', 22, 'bold'),
                    bg="#cae8cd")
    welcome.grid(row=0, column=1, pady=25, sticky="nsew")

    add_button = Button(main_window, text="Add Book")
    add_button.config(command=add_book_page,
                      font=('Times New Roman', 15, 'bold'),
                      bg="#cae8cd")
    add_button.grid(row=1, column=1, pady=10, sticky="nsew")

    remove_book_button = Button(main_window, text="Remove Book")
    remove_book_button.config(command=remove_book_page,
                      font=('Times New Roman', 15, 'bold'),
                      bg="#cae8cd")
    remove_book_button.grid(row=2, column=1, pady=10, sticky="nsew")

    search_book_button = Button(main_window, text="Search Book")
    search_book_button.config(command=search_page,
                      font=('Times New Roman', 15, 'bold'),
                      bg="#cae8cd")
    search_book_button.grid(row=3, column=1, pady=10, sticky="nsew")

    view_books_button = Button(main_window, text="View Books")
    view_books_button.config(command=view_books_page,
                      font=('Times New Roman', 15, 'bold'),
                      bg="#cae8cd")
    view_books_button.grid(row=4, column=1, pady=10, sticky="nsew")

    borrow_book_button = Button(main_window, text="Lend Book")
    borrow_book_button.config(command=borrow_book_page,
                      font=('Times New Roman', 15, 'bold'),
                      bg="#cae8cd")
    borrow_book_button.grid(row=5, column=1, pady=10, sticky="nsew")

    return_book_button = Button(main_window, text="Return Book")
    return_book_button.config(command=return_book_page,
                      font=('Times New Roman', 15, 'bold'),
                      bg="#cae8cd")
    return_book_button.grid(row=6, column=1, pady=10, sticky="nsew")

    popular_books__button = Button(main_window, text="Popular Books")
    popular_books__button.config(command=popular_page,
                              font=('Times New Roman', 15, 'bold'),
                              bg="#cae8cd")
    popular_books__button.grid(row=7, column=1, pady=10, sticky="nsew")

    logout_button = Button(main_window, text="Logout")
    logout_button.config(command=logout,
                      font=('Times New Roman', 15, 'bold'),
                      bg="#cae8cd")
    logout_button.grid(row=10, column=0, padx=15, pady=25, sticky="nsew")

def add_book_page():
    """
    Add a new book Page
    -------------------
    By entering valid parameters - a new book will be created and a notification will appear if the book created successfully or failed.

    Available functions:
        - Add a new book
        - Return to Home Page
    """
    init_page()
    # create all necessary widgets
    add_book_label = Label(main_window,
                    text="Add a new book",
                    font=('Times New Roman', 22, 'bold'),
                    bg="#cae8cd")
    add_book_label.grid(row=0, column=1, columnspan=3, padx=220, pady=25, sticky="nsew")

    title_label = Label(main_window,
                           text="Title:",
                           font=('Times New Roman', 15, 'bold'),
                           bg="#cae8cd")
    title_label.grid(row=1, column=1, pady=10, sticky="nsew")

    title_entry = Entry(main_window)
    title_entry.grid(row=1, column=2, pady=10, sticky="nsew")

    author_label = Label(main_window,
                        text="Author:",
                        font=('Times New Roman', 15, 'bold'),
                        bg="#cae8cd")
    author_label.grid(row=2, column=1, pady=10, sticky="nsew")

    author_entry = Entry(main_window)
    author_entry.grid(row=2, column=2, pady=10, sticky="nsew")

    copies_label = Label(main_window,
                           text="Copies:",
                           font=('Times New Roman', 15, 'bold'),
                           bg="#cae8cd")
    copies_label.grid(row=3, column=1, pady=10, sticky="nsew")
    copies_entry = Entry(main_window, validate="key", validatecommand=(validate_command, "%P"))
    copies_entry.grid(row=3, column=2, pady=10, sticky="nsew")

    genre_label = Label(main_window,
                         text="Genre:",
                         font=('Times New Roman', 15, 'bold'),
                         bg="#cae8cd")
    genre_label.grid(row=4, column=1, pady=10, sticky="nsew")

    genre_entry = Entry(main_window)
    genre_entry.grid(row=4, column=2, pady=10, sticky="nsew")

    year_label = Label(main_window,
                        text="Year:",
                        font=('Times New Roman', 15, 'bold'),
                        bg="#cae8cd")
    year_label.grid(row=5, column=1, pady=10, sticky="nsew")

    year_entry = Entry(main_window)
    year_entry.grid(row=5, column=2, pady=10, sticky="nsew")

    add_button = Button(main_window, text="Add book")
    add_button.config(command=lambda : add_book(title_entry.get(), author_entry.get(), copies_entry.get(), genre_entry.get(), year_entry.get()),
                      font=('Times New Roman', 22, 'bold'),
                      bg="#cae8cd")
    add_button.grid(row=8, column=2, pady=10, sticky="nsew")

def search_page():
    """
    Search page
    -----------
    A book can be searched by a given full or partial title and autor name.
    If such books exist - a new page with all these books will be displayed.
    Otherwise - a failed notification will appear.

    Available functions:
        - Search a book by title and author name
        - Return to Home Page
    """
    init_page()
    search_label = Label(main_window,
                             text="Search books",
                             font=('Times New Roman', 22, 'bold'),
                             bg="#cae8cd")
    search_label.grid(row=0, column=1, columnspan=3, padx=220, pady=25, sticky="nsew")

    title_label = Label(main_window,
                         text="Title:",
                         font=('Times New Roman', 15, 'bold'),
                         bg="#cae8cd")
    title_label.grid(row=1, column=1, pady=10, sticky="nsew")

    title_entry = Entry(main_window)
    title_entry.grid(row=1, column=2, pady=10, sticky="nsew")

    author_label = Label(main_window,
                        text="Author:",
                        font=('Times New Roman', 15, 'bold'),
                        bg="#cae8cd")
    author_label.grid(row=2, column=1, pady=10, sticky="nsew")

    author_entry = Entry(main_window)
    author_entry.grid(row=2, column=2, pady=10, sticky="nsew")

    search_button = Button(main_window, text="Search")
    search_button.config(command=lambda: search_book(title_entry.get(), author_entry.get()),
                      font=('Times New Roman', 22, 'bold'),
                      bg="#cae8cd")
    search_button.grid(row=3, column=2, pady=25, sticky="nsew")

def view_books_page():
    """
    View books page
    ----------------
    Books can be viewed by the choice of the current User.

    Available functions:
        - All books
        - Available books
        - Lent books
        - By specific category
        - Return to Home Page
    """
    init_page()
    # create all necessary widgets
    view_books_label = Label(main_window,
                             text="View books",
                             font=('Times New Roman', 22, 'bold'),
                             bg="#cae8cd")
    view_books_label.grid(row=0, column=1, columnspan=3, padx=220, pady=25, sticky="nsew")

    all_button = Button(main_window, text="All books")
    all_button.config(command=lambda: create_tree_for_view_page("All books", library.get_all_books()),
                      font=('Times New Roman', 15, 'bold'),
                      bg="#cae8cd")
    all_button.grid(row=1, column=2, pady=10, sticky="nsew")

    available_button = Button(main_window, text="Available books")
    available_button.config(command=lambda: create_tree_for_view_page("Available books", library.get_available_books()),
                            font=('Times New Roman', 15, 'bold'),
                            bg="#cae8cd")
    available_button.grid(row=2, column=2, pady=10, sticky="nsew")
    global user
    borrowed_button = Button(main_window, text="Lent books")
    borrowed_button.config(command=lambda: create_tree_for_view_page("Lent books", library.get_borrowed_books()),
                           font=('Times New Roman', 15, 'bold'),
                           bg="#cae8cd")
    borrowed_button.grid(row=3, column=2, pady=10, sticky="nsew")

    category_button = Button(main_window, text="By category")
    category_button.config(command=category_page,
                           font=('Times New Roman', 15, 'bold'),
                           bg="#cae8cd")
    category_button.grid(row=4, column=2, pady=10, sticky="nsew")

def category_page():
    """
    Category page
    -------------
    By selecting a category - a TreeView with all the related books will be displayed.

    Available functions:
        - Select a category
        - Submit the selected category and display the relevant books
        - Return to Home Page
    """
    init_page()
    # create all necessary widgets
    view_books_label = Label(main_window,
                           text="By category",
                           font=('Times New Roman', 22, 'bold'),
                           bg="#cae8cd")
    view_books_label.grid(row=0, column=1, columnspan=3, padx=220, pady=25, sticky="nsew")

    category_label = Label(main_window,
                         text="Category:",
                         font=('Times New Roman', 15, 'bold'),
                         bg="#cae8cd")
    category_label.grid(row=1, column=1, pady=10, sticky="nsew")
    global categories
    selected_category = StringVar(value="")  # Default value is an empty string

    # StringVar to hold the selected category
    selected_category = StringVar()
    selected_category.set("Select a Category")  # Default value

    # Create the OptionMenu
    dropdown = OptionMenu(main_window, selected_category, *categories)
    dropdown.config(font=('Times New Roman', 15, 'bold'), width=20)  # Styling the dropdown
    dropdown.grid(row=1, column=2, pady=10, sticky="nsew")

    """"
    # Function to display the selected category
    def show_selection():
        print(f"Selected Category: {selected_category.get()}")
    """

    category_button = Button(main_window, text="Submit")
    category_button.config(command=lambda : create_tree_for_view_page(f"Books of {selected_category.get()}", library.search_book_by_genre(selected_category.get())),
                         font=('Times New Roman', 15, 'bold'),
                         bg="#cae8cd")
    category_button.grid(row=2, column=2, pady=20, sticky="nsew")

def popular_page():
    """
    Popular page
    -------------
    This page shows the most 10 popular books that has been lent if one's exists.

    Available functions:
        - Return to Home Page
    """
    books_list = library.get_popular_list()
    if books_list:
        init_page()
        create_tree_for_view_page("Popular books", books_list)
    else:
        notification("No popular books!", None)



def return_book_page():
    """
    Return a book page
    ------------------
    This page shows all the lent books and by selecting a book from a TreeView the book can be returned to the Library.

    Available functions:
        - Return a selected book from the TreeView
        - Return to Home Page
    """
    init_page()
    return_label = Label(main_window,
                         text="Return a book",
                         font=('Times New Roman', 22, 'bold'),
                         bg="#cae8cd")
    return_label.grid(row=0, column=1, columnspan=3, padx=220, pady=25, sticky="nsew")
    global user
    borrowed_books_list = library.get_borrowed_books()
    if borrowed_books_list:
        tree_select_value(borrowed_books_list)
        lend_button = Button(main_window, text="Return selected book")
        lend_button.config(
            command=lambda: try_return_book(get_selected_book_from_tree()),
            font=('Times New Roman', 15, 'bold'),
            bg="#cae8cd")
        lend_button.grid(row=3, column=1, columnspan=2, padx=100, pady=10, sticky="nsew")

    else:
        notification("No borrowed books!", home_page)


def remove_book_page():
    """
    Remove a book page
    ------------------
    This page shows all the books in the Library.

    Available functions:
        - Remove a selected book from the TreeView
        - Return to Home Page
    """
    init_page()
    remove_label = Label(main_window,
                         text="Remove a book",
                         font=('Times New Roman', 22, 'bold'),
                         bg="#cae8cd")
    remove_label.grid(row=0, column=1, columnspan=3, padx=220, pady=25, sticky="nsew")
    books_list = library.get_all_books()
    if books_list:
        global value_tree
        tree_select_value(books_list)
        remove_button = Button(main_window, text="Remove selected book")
        remove_button.config(command=lambda: remove_book(get_selected_book_from_tree()),
                             font=('Times New Roman', 15, 'bold'),
                             bg="#cae8cd")
        remove_button.grid(row=4, column=1, columnspan=3, padx=100, pady=25, sticky="nsew")

    else:
        notification("No books to remove!", home_page)



def borrow_book_page():
    """
    Lent a book page
    -----------------
    This page is used to lend a Book from a given TreeView.

    Available functions:
        - Lend the selected book
        - Return to Home Page
    -----------------
    A pop-up with the relevant message will appear if the book has been lent successfully, failed or if the client is in the waiting list.
    """
    init_page()
    main_window.grid_rowconfigure(1, weight=0)
    main_window.grid_columnconfigure(1, weight=0)
    borrow_label = Label(main_window,
                         text="Lend a book",
                         font=('Times New Roman', 22, 'bold'),
                         bg="#cae8cd")
    borrow_label.grid(row=0, column=1, columnspan=3, padx=100, pady=15, sticky="nsew")
    books_list = library.get_all_books()
    if books_list:
        global value_tree
        tree_select_value(books_list)

        client_label = Label(main_window,
                             text="Name:",
                             font=('Times New Roman', 15, 'bold'),
                             bg="#cae8cd")
        client_label.grid(row=3, column=2, padx=100, pady=5, sticky="w")
        client_entry = Entry(main_window)
        client_entry.grid(row=3, column=2, padx=50, pady=5)

        email_label = Label(main_window,
                             text="Email:",
                             font=('Times New Roman', 15, 'bold'),
                             bg="#cae8cd")
        email_label.grid(row=4, column=2, padx=100, pady=5, sticky="w")
        email_entry = Entry(main_window)
        email_entry.grid(row=4, column=2, padx=50, pady=5)

        phone_label = Label(main_window,
                             text="Phone:",
                             font=('Times New Roman', 15, 'bold'),
                             bg="#cae8cd")
        phone_label.grid(row=5, column=2, padx=100, pady=10, sticky="w")

        phone_entry = Entry(main_window, textvariable=StringVar(value="05"), validate="key",
                            validatecommand=(validate_command, "%P"))
        phone_entry.grid(row=5, column=2, padx=50, pady=5)

        lend_button = Button(main_window, text="Lend selected book")
        lend_button.config(command=lambda: try_lend_book(get_selected_book_from_tree(), client_entry.get(), email_entry.get(), phone_entry.get()),
                             font=('Times New Roman', 15, 'bold'),
                             bg="#cae8cd")
        lend_button.grid(row=6, column=1, columnspan=2, padx=100, pady=10, sticky="nsew")

    else:
        notification("No books to lend!", home_page)

if __name__ == "__main__":
    books = library.get_all_books()
    categories = []
    for book in books:
        if book.get_genre() not in categories:
            categories.append(book.get_genre())
    main()
