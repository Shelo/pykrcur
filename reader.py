from level import *

class Reader(object):
    def __init__(self, file_path):
        self.filePath = file_path
        self.top = []
        self.left = []

        # information about the level.
        self.top_width = 0
        self.top_height = 0
        self.left_width = 0
        self.left_height = 0

        self.read()
        self.info()

    def read(self):
        reading_top = True

        with open(self.filePath) as data:
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
        self.top_height = len(self.top)
        self.top_width = 0
        for row in self.top:
            if len(row) > self.top_width:
                self.top_width = len(row)

        self.left_height = len(self.left)
        self.left_width = 0
        for row in self.left:
            if len(row) > self.left_width:
                self.left_width = len(row)

    def get_level(self):
        level = Level(self.top_width, self.top_height, self.left_width, self.left_height)

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
