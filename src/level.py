import utils

class Level(object):
    def __init__(self, id, width, top_margin, left_margin, height):
        self.left_margin = left_margin
        self.top_margin = top_margin
        self.height = height
        self.width = width
        self.id = id

        self.left = utils.new_matrix(left_margin, height, -1)
        self.top = utils.new_matrix(width, top_margin, -1)

    def clear_row(self, y):
        for i in range(self.left_margin):
            self.left[i][y] = -1

    def clear_col(self, x):
        for i in range(self.top_margin):
            self.top[x][i] = -1

    def add_to_top(self, x, y, value):
        self.top[x][y] = value

    def add_to_left(self, x, y, value):
        self.left[x][y] = value

    def get_top_at(self, x, y):
        return self.top[x][y]

    def get_left_at(self, x, y):
        return self.left[x][y]

    def size(self):
        """
        Returns the complete size of the level, taking into account all tiles.

        :return: a tuple of (width, height)
        """
        return self.width + self.left_margin, self.top_margin + self.height

    def get_row(self, index):
        row = []

        for x in range(self.left_margin):
            value = self.left[x][index]

            if value != -1:
                row.append(value)

        return row

    def get_col(self, index):
        col = []

        for y in range(self.top_margin):
            value = self.top[index][y]

            if value != -1:
                col.append(value)

        return col
