import curses
from reader import Reader
import sys


NULL = 0
MARK = 1
DISC = 2


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


class Puzzle(object):
    def __init__(self, level):
        self.level = level

        self.master = None
        self.win = None
        self.daemon = True
        self.out = ""
        self.cursor_pos = (0, 0)

        self.marks = [[NULL for i in range(level.left_height)] for j in range(level.top_width)]

    def start(self):
        self.master = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.cbreak()
        curses.noecho()

        max_height, max_width = self.master.getmaxyx()
        width, height = self.level.size()
        width = width * 3 + 1
        self.win = curses.newwin(height, width,
                                 (max_height - self.level.left_height) / 2 - self.level.top_height,
                                 (max_width - self.level.top_width * 3) / 2 - self.level.left_width * 3)
        self.win.keypad(True)

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)

        self.mainloop()

    def mainloop(self):
        while self.daemon:
            self.render()
            self.refresh()
            self.place_cursor()
            char = self.input()
            self.update(char)

        self.end()

    def input(self):
        char = self.win.getch()

        if char == ord('q'):
            self.daemon = False

        return char

    def update(self, char):
        y, x = self.cursor_pos
        if char == curses.KEY_RIGHT:
            x += 1

        elif char == curses.KEY_LEFT:
            x -= 1

        elif char == curses.KEY_UP:
            y -= 1

        elif char == curses.KEY_DOWN:
            y += 1

        elif char in (ord(' '), ord('z')):
            self.mark(x, y)

        elif char == ord('x'):
            self.discard(x, y)

        x = clamp(x, 0, self.level.top_width - 1)
        y = clamp(y, 0, self.level.left_height - 1)

        self.cursor_pos = (y, x)

    def mark(self, x, y):
        self.marks[x][y] = MARK if self.marks[x][y] in (NULL, DISC) else NULL

    def discard(self, x, y):
        self.marks[x][y] = DISC if self.marks[x][y] in (NULL, MARK) else NULL

    def place_cursor(self):
        y, x = self.cursor_pos
        self.win.move(y + self.level.top_height, (x + self.level.left_width) * 3 + 1)

    def render(self):
        self.draw_top()
        self.draw_left()
        self.draw_marks()

    def draw_top(self):
        for x in range(self.level.top_width):

            col = self.level.get_top_col(x)
            types, groups = self.get_top_marks_col(x)

            complete_indices = self.get_completed_indices(col, types, groups)

            raw_y = 0
            for y in range(_level.top_height):
                value = self.level.top[x][y]

                if value == -1:
                    continue

                attributes = curses.A_NORMAL

                # add underline if completed.
                if raw_y in complete_indices:
                    attributes |= curses.color_pair(4)

                str_value = str(value).center(3, ' ')
                if x == self.cursor_pos[1]:
                    self.addchs(y, (self.level.left_width + x) * 3, str_value, attributes | curses.A_BOLD)
                else:
                    self.addchs(y, (self.level.left_width + x) * 3, str_value, attributes)

                raw_y += 1

    def draw_left(self):
        for y in range(self.level.left_height):

            row = self.level.get_left_row(y)
            types, groups = self.get_left_marks_row(y)

            complete_indices = self.get_completed_indices(row, types, groups)

            raw_x = 0
            for x in range(self.level.left_width):
                value = self.level.left[x][y]

                if value == -1:
                    continue

                str_value = str(value).center(3, ' ')

                attributes = curses.A_NORMAL

                # add underline if completed.
                if raw_x in complete_indices:
                    attributes |= curses.color_pair(4)

                if y == self.cursor_pos[0]:
                    self.addchs(self.level.top_height + y, x * 3, str_value, attributes | curses.A_BOLD)
                else:
                    self.addchs(self.level.top_height + y, x * 3, str_value, attributes)

                raw_x += 1

    def draw_marks(self):
        for x in range(self.level.top_width):
            for y in range(self.level.left_height):
                value = self.marks[x][y]

                pos_y, pos_x = self.level.top_height + y, (self.level.left_width + x) * 3

                if value == MARK:
                    self.addchs(pos_y, pos_x, ' ' * 3, curses.color_pair(1))

                elif value == DISC:
                    self.addchs(pos_y, pos_x, ' ' * 3, curses.color_pair(2))

                else:
                    if (x + y) % 2 == 0:
                        self.addchs(pos_y, pos_x, ' ' * 3, None)
                    else:
                        self.addchs(pos_y, pos_x, ' ' * 3, curses.color_pair(3))

    def addchs(self, y, x, chs, color):
        for i in range(len(chs)):
            if color is not None:
                self.win.addch(y, x + i, ord(chs[i]), color)
            else:
                self.win.addch(y, x + i, ord(chs[i]))

    def refresh(self):
        self.master.refresh()
        self.win.refresh()

    def get_left_marks_row(self, index):
        row = []

        for x in range(self.level.top_width):
            row.append(self.marks[x][index])

        types = []
        groups = []

        actual_group = row[0]

        # prepare the first iteration.
        groups.append(0)
        types.append(actual_group)

        for value in row:
            if value != actual_group:
                actual_group = value
                types.append(value)
                groups.append(1)
            else:
                groups[-1] += 1

        return types, groups

    def get_top_marks_col(self, index):
        col = []

        for y in range(self.level.left_height):
            col.append(self.marks[index][y])

        types = []
        groups = []

        actual_group = col[0]

        # prepare the first iteration.
        groups.append(0)
        types.append(actual_group)

        for value in col:
            if value != actual_group:
                actual_group = value
                types.append(value)
                groups.append(1)
            else:
                groups[-1] += 1

        return types, groups

    def log(self, message):
        self.out += "%s\n" % message

    def end(self):
        curses.endwin()

        print "----------- OUTPUT ------------"
        print self.out[:-1]
        print "--------- END OUTPUT ----------"

    def get_completed_indices(self, row, types, groups):
        indices = set()
        used_groups = set()

        # first, try from the left to the right.
        mark_group_i = -1
        for i, group in enumerate(groups):
            group_type = types[i]

            if group_type == NULL:
                # if the type is NULL quit trying.
                break
            elif group_type == MARK:
                mark_group_i += 1

                if mark_group_i < len(row) and row[mark_group_i] == group:
                    indices.add(mark_group_i)
                    used_groups.add(i)

        # now, try from the right to the left.
        mark_group_i = len(row)
        for i, group in list(enumerate(groups))[-1::-1]:
            if i in used_groups:
                continue

            group_type = types[i]

            if group_type == NULL:
                # if the type is NULL quit trying.
                break

            elif group_type == MARK:
                mark_group_i -= 1

                if mark_group_i >= 0 and row[mark_group_i] == group:
                    indices.add(mark_group_i)

        return indices

if __name__ == '__main__':
    if len(sys.argv) == 1:
        reader = Reader("levels/lambda.krk")
    else:
        reader = Reader(sys.argv[1])

    _level = reader.get_level()

    puzzle = Puzzle(_level)
    puzzle.start()