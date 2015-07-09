import curses
import sys
import utils

from src.reader import Reader


class KRPuzzle(object):
    NULL = 0
    MARK = 1
    DISC = 2

    def __init__(self, level):
        self.level = level

        # position of the cursor (y, x)
        self.cursor_pos = (0, 0)
        self.master = None
        self.daemon = True
        self.win = None
        self.out = ""

        # matrix for the marks on the puzzle.
        self.marks = utils.new_matrix(level.width, level.height, self.NULL)

    def start(self):
        """
        Starts the game environment on the terminal using curses.
        """
        # setup curses stuff.
        self.master = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.cbreak()
        curses.noecho()

        # window dimensions.
        max_height, max_width = self.master.getmaxyx()
        width, height = self.level.size()
        width = width * 3 + 1
        y = (max_height - self.level.height) / 2 - self.level.top_margin
        x = (max_width - self.level.width * 3) / 2 - self.level.left_margin * 3

        # create window for the actual game.
        self.win = curses.newwin(height, width, y, x)
        self.win.keypad(True)

        # setup theme.
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_YELLOW)

        # this block will always restore the terminal.
        try:
            self.__mainloop()
        except Exception as e:
            print e.message
        finally:
            self.end()

    def __mainloop(self):
        while self.daemon:
            self.render()
            self.refresh()
            self.place_cursor()
            char = self.__input()
            self.update(char)

    def __input(self):
        char = self.win.getch()

        if char == ord('q'):
            self.daemon = False

        return char

    def update(self, char):
        """
        Updates the puzzle given the character.

        :param char:    the character to emulate.
        """
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

        x = self.clamp(x, 0, self.level.width - 1)
        y = self.clamp(y, 0, self.level.height - 1)

        self.cursor_pos = (y, x)

    def mark(self, x, y):
        self.marks[x][y] = self.MARK if self.marks[x][y] in (self.NULL, self.DISC) else self.NULL

    def discard(self, x, y):
        self.marks[x][y] = self.DISC if self.marks[x][y] in (self.NULL, self.MARK) else self.NULL

    def place_cursor(self):
        y, x = self.cursor_pos
        self.win.move(y + self.level.top_margin, (x + self.level.left_margin) * 3 + 1)

    def render(self):
        self.__draw_top()
        self.__draw_left()
        self.__draw_marks()

    def __draw_top(self):
        for x in range(self.level.width):
            complete_indices = self.get_completed_indices(self.level.get_col(x), *self.get_marks_col(x))

            # iterate over every column, always tracking the actual index of the value (real_y).
            real_y = 0
            for y, value in enumerate(self.level.top[x]):
                if value == -1:
                    continue

                # this is the default attribute for a value.
                attributes = curses.A_NORMAL

                # add style if completed.
                if real_y in complete_indices:
                    attributes |= curses.color_pair(4)

                str_value = str(value).center(3, ' ')
                if x == self.cursor_pos[1]:
                    # draw with other style if the cursor is in this column.
                    self.__addchs(y, (self.level.left_margin + x) * 3, str_value, attributes | curses.A_BOLD)

                else:
                    self.__addchs(y, (self.level.left_margin + x) * 3, str_value, attributes)

                real_y += 1

    def __draw_left(self):
        for y in range(self.level.height):
            complete_indices = self.get_completed_indices(self.level.get_row(y), *self.get_marks_row(y))

            # iterate over every column, always tracking the actual index of the value (real_x).
            real_x = 0
            for x in range(self.level.left_margin):
                value = self.level.left[x][y]

                if value == -1:
                    continue

                str_value = str(value).center(3, ' ')

                attributes = curses.A_NORMAL

                # add underline if completed.
                if real_x in complete_indices:
                    attributes |= curses.color_pair(4)

                if y == self.cursor_pos[0]:
                    self.__addchs(self.level.top_margin + y, x * 3, str_value, attributes | curses.A_BOLD)
                else:
                    self.__addchs(self.level.top_margin + y, x * 3, str_value, attributes)

                real_x += 1

    def __draw_marks(self):
        for x in range(self.level.width):
            for y in range(self.level.height):
                value = self.marks[x][y]

                pos_y, pos_x = self.level.top_margin + y, (self.level.left_margin + x) * 3

                chars = ' ' * 3

                if value == self.MARK:
                    self.__addchs(pos_y, pos_x, chars, curses.color_pair(1))

                elif value == self.DISC:
                    self.__addchs(pos_y, pos_x, chars, curses.color_pair(2))

                else:
                    if (x + y) % 2 == 0:
                        self.__addchs(pos_y, pos_x, chars, None)
                    else:
                        self.__addchs(pos_y, pos_x, chars, curses.color_pair(3))

    def __addchs(self, y, x, chs, style):
        """
        Adds multiple characters at a position using the given color, or None.

        :param y:       y position.
        :param x:       x position.
        :param chs:     characters.
        :param style:   style for the chars.
        """
        for i in range(len(chs)):
            if style is not None:
                self.win.addch(y, x + i, ord(chs[i]), style)
            else:
                self.win.addch(y, x + i, ord(chs[i]))

    def refresh(self):
        self.master.refresh()
        self.win.refresh()

    def get_marks_row(self, index):
        """
        Returns the types and groups of the given row of marks.

        For instance:
        0, 1, 1, 2, 2, 1, 2, 0

        Will give the groups:
        1, 2, 2, 1, 1, 1

        with types:
        0, 1, 2, 1, 2, 0

        This is for easy comparison.

        :param index:   the index of the row.
        :return:        types, groups
        """
        row = [self.marks[x][index] for x in range(self.level.width)]

        actual_group = -1
        types, groups = [], []

        for value in row:
            if value != actual_group:
                actual_group = value
                types.append(value)
                groups.append(1)

            else:
                groups[-1] += 1

        return types, groups

    def get_marks_col(self, index):
        """
        Returns the types and groups of the given column of marks.

        For instance:
        0, 1, 1, 2, 2, 1, 2, 0

        Will give the groups:
        1, 2, 2, 1, 1, 1

        with types:
        0, 1, 2, 1, 2, 0

        This is for easy comparison.

        :param index:   the index of the column.
        :return:        types, groups
        """
        col = self.marks[index]

        actual_group = -1
        types, groups = [], []

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

    @staticmethod
    def end():
        curses.endwin()

    def output(self):
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

            if group_type == self.NULL:
                # if the type is self.NULL quit trying.
                break

            elif group_type == self.MARK:
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

            if group_type == self.NULL:
                # if the type is self.NULL quit trying.
                break

            elif group_type == self.MARK:
                mark_group_i -= 1

                if mark_group_i >= 0 and row[mark_group_i] == group:
                    indices.add(mark_group_i)

        return indices

    @staticmethod
    def clamp(value, minimum, maximum):
        return max(minimum, min(value, maximum))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        reader = Reader("levels/lambda.krk")
    else:
        reader = Reader(sys.argv[1])

    _level = reader.get_level()

    puzzle = KRPuzzle(_level)
    puzzle.start()
