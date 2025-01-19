import logging
import os
from pathlib import Path

LOG_FILE = Path.cwd() / "log.txt"

logging.basicConfig(
    filename=LOG_FILE,  # File where logs will be saved
    level=logging.INFO,
    format='%(message)s'
)


class Observer:
    """Abstract observer class"""

    def update(self, subject1, subject2):
        pass


class BookObserver(Observer):

    def __init__(self, book_name, client_name, client_email, client_phone):
        self.book_name = book_name
        self.client_name = client_name
        self.client_email = client_email
        self.client_phone = client_phone

    def update(self, book_name, client_name):
        if self.book_name == book_name and self.client_name == client_name:
            logging.info(f"Sending an email to {self.client_email} and a text message to {self.client_phone}")
            return True
