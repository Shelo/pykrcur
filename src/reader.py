from src.level import *
from os.path import basename

class Reader(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.left = []
        self.top = []

        # information about the level.
        self.left_margin = 0
        self.top_margin = 0
        self.height = 0
        self.width = 0

        self.read()
        self.info()

    def read(self):
        reading_top = True

        with open(self.file_path) as data:
            for line in data:
                if line and line[0] != "=":
                    numbers = self.get_numbers(self.no_newline(line))

                    if reading_top:
                        self.top.append(numbers)
                    else:
                        self.left.append(numbers)

                else:
                    reading_top = False

    @staticmethod
    def get_numbers(line):
        raw_numbers = line.split('\t')

        numbers = [-1] * len(raw_numbers)

        for i, raw_number in enumerate(raw_numbers):
            if raw_number != '':
                numbers[i] = int(raw_number)

        return numbers

    def info(self):
        self.top_margin = len(self.top)
        self.width = 0
        for row in self.top:
            if len(row) > self.width:
                self.width = len(row)

        self.height = len(self.left)
        self.left_margin = 0
        for row in self.left:
            if len(row) > self.left_margin:
                self.left_margin = len(row)

    def get_level(self):
        level_id = basename(self.file_path).replace('.krk', '')
        level = Level(level_id, self.width, self.top_margin, self.left_margin, self.height)

        for y, row in enumerate(self.top):
            for x, number in enumerate(row):
                level.add_to_top(x, y, number)

        for y, row in enumerate(self.left):
            for x, number in enumerate(row):
                level.add_to_left(x, y, number)

        return level

    @staticmethod
    def no_newline(line):
        return line[:-1] if line[-1] == '\n' else line
