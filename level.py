class Level(object):
    def __init__(self, top_width, top_height, left_width, left_height):
        self.top_width = top_width
        self.top_height = top_height
        self.left_width = left_width
        self.left_height = left_height

        self.top = [[-1 for i in range(top_height)] for j in range(top_width)]
        self.left = [[-1 for i in range(left_height)] for j in range(left_width)]

    def add_to_top(self, x, y, value):
        self.top[x][y] = value

    def add_to_left(self, x, y, value):
        self.left[x][y] = value

    def size(self):
        """
        Returns the complete size of the level, taking into account all tiles.

        :return: a tuple of (width, height)
        """
        return self.top_width + self.left_width, self.top_height + self.left_height

    def get_left_row(self, index):
        row = []

        for x in range(self.left_width):
            value = self.left[x][index]

            if value != -1:
                row.append(value)

        return row

    def get_top_col(self, index):
        col = []

        for y in range(self.top_height):
            value = self.top[index][y]

            if value != -1:
                col.append(value)

        return col
