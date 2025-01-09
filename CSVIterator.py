import csv

"""
CSVIterator is an iterator class (that implements iterator pattern design)
to better navigate, open, close, read, write and append all the different .csv files
"""


class CSVIterator:

    def __init__(self, file_path, mode="r"):
        self.file_path = file_path
        self.mode = mode
        self.file = None
        self.reader = None
        self.writer = None

    def __iter__(self):
        if self.reader:
            return iter(self.reader)
        raise ValueError("File is not in read mode.")

    def __next__(self):
        if self.reader is None:
            raise StopIteration
        try:
            return next(self.reader)
        except StopIteration:
            self.file.close()
            raise

    def __enter__(self):
        self.file = open(self.file_path, self.mode, newline="")
        if "r" in self.mode:
            self.reader = csv.reader(self.file)
        elif "w" in self.mode or "a" in self.mode:
            self.writer = csv.writer(self.file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

    def write_row(self, row):
        if self.writer:
            self.writer.writerow(row)
        else:
            raise ValueError("File is not in write/append mode")

    def write_rows(self, rows):
        if self.writer:
            self.writer.writerows(rows)
        else:
            raise ValueError("File is not in write/append mode")

    def reset_to_start(self):
        if "r" in self.mode:
            self.file.seek(0)
        else:
            raise ValueError("Reset is only supported in read mode.")
