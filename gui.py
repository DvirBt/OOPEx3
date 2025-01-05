from tkinter import *
from Library import *

#library = Library(None)

# to be implemented
def add_book():
    pass

def remove_book():
    pass

def search_book(book_name, author_name):
    pass

def view_books(type):
    pass

def borrow_book(book):
    pass

def return_book(book):
    pass

def register():
    pass

def login(username, password):
    user = User(username, password)
    success, dont_care = Library.login_user(user)
    if (success):
        home_page(User)
    else:
        login_failed = Label(login_window,
                             text="Login failed!",
                             font=('Ink Free', 18, 'bold'),
                             bg="#cae8cd")
        login_failed.grid(row=6, columnspan=3, padx=250, pady=25, sticky="nsew")


def logout():
    pass

def popular_books():
    pass

def books_by_category(category):
    pass

login_window = Tk()
login_window.geometry("720x720")
login_window.title("Login/Register")
login_window.config(background="#cae8cd")
#login_window.grid_rowconfigure(0, weight=1)
login_window.grid_columnconfigure(0, weight=0)
login_window.grid_columnconfigure(1, weight=0)  # Entry's column expands proportionally


login_label = Label(login_window,
                    text="Login / Register page",
                    font=('Ink Free', 30, 'bold'),
                    bg="#cae8cd",
                    pady=40)
login_label.grid(row=0, columnspan=3, padx=170, pady=10, sticky="nsew")

username_label = Label(login_window,
                    text="Username: ",
                    font=('Ink Free', 18, 'bold'),
                    bg="#cae8cd")
username_label.grid(row=1, column=0, columnspan=1, pady=25, sticky="nsew")

username_entry = Entry(login_window, width=20)
username_entry.grid(row=1, column=1, pady=25, sticky="nsew")

password_label = Label(login_window,
                    text="Password: ",
                    font=('Ink Free', 18, 'bold'),
                    bg="#cae8cd")
password_label.grid(row=2, column=0, pady=25, sticky="nsew")

password_entry = Entry(login_window, show="*", width=20)
password_entry.grid(row=2, column=1, pady=25, sticky="nsew")

# Buttons
login = Button(login_window, text="Login")
login.config(command=login,
                  font=('Ink Free', 15, 'bold'),
                  bg="#cae8cd")
login.grid(row=4, columnspan=3, padx=250, pady=25, sticky="nsew")

register = Button(login_window, text="Register")
register.config(command=register,
                  font=('Ink Free', 15, 'bold'),
                  bg="#cae8cd")
register.grid(row=5, columnspan=3, padx=250, pady=25, sticky="nsew")

login_window.mainloop()

def home_page(user):
    window = Tk()
    window.geometry("720x720")
    window.title("Library")
    #icon = PhotoImage(file="library.jpeg")
    #window.iconphoto(False, icon)
    window.config(background="#cae8cd")

    welcome = Label(window,
                    text=f"Welcome back {user.get_username()}",
                    font=('Ink Free', 18, 'bold'),
                    bg="#cae8cd")
    welcome.pack()

    add_button = Button(window, text="Add Book")
    add_button.config(command=add_book,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    add_button.pack()

    remove_book = Button(window, text="Remove Book")
    remove_book.config(command=remove_book,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    remove_book.pack()

    search_book = Button(window, text="Search Book")
    search_book.config(command=search_book,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    search_book.pack()

    view_books = Button(window, text="View Books")
    view_books.config(command=view_books,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    view_books.pack()

    borrow_book = Button(window, text="Lend Book")
    borrow_book.config(command=borrow_book,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    borrow_book.pack()

    return_book = Button(window, text="Return Book")
    return_book.config(command=return_book,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    return_book.pack()

    logout = Button(window, text="Logout")
    logout.config(command=logout,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    logout.pack()

    popular_books = Button(window, text="Popular Books")
    popular_books.config(command=popular_books,
                      font=('Ink Free', 15, 'bold'),
                      bg="#cae8cd")
    popular_books.pack()

    window.mainloop()