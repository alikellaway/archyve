from csv import reader
from pathlib import Path
from file_funcs import path_handler

class NameMap:
    def __init__(self, path: Path | str) -> None:
        self.map = {}
        with CSVFile(path) as f:
            for row in f.rows:
                self.map[row[0]] = row[1]





class CSVFile:
    """
    Class abstracts CSVFile loading to make iterating through rows easier.
    """

    def __init__(self, path: str | Path):
        """
        Constructs a new CSVFile object given the path of the csv file to load.
        :param path: The path of the csv file to load.
        """
        self.path = path_handler(path)
        self.reader = None
        self.header = None
        self.rows = None

    def __enter__(self):
        self.csv = open(self.path, 'rt')
        self.rows = reader(self.csv)
        self.header = self.rows.__next__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.csv.close()
        self.reader = None
        self.header = None
        self.rows = None