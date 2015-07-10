import curses
from src.writer import Writer
import utils
from puzzle import KRPuzzle


class KREditor(KRPuzzle):
    def __init__(self, level, root):
        KRPuzzle.__init__(self, level)

        self.allow_help = False
        self.writer = Writer(self.level, root)

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

        elif char == ord('s'):
            self.save()

        x = utils.clamp(x, 0, self.level.width - 1)
        y = utils.clamp(y, 0, self.level.height - 1)

        self.cursor_pos = (y, x)

        # Update rows side.
        types, groups = self.get_marks_row(y)

        self.level.clear_row(y)

        marks = 0
        for i, group in enumerate(groups[-1::-1]):
            if types[-(i + 1)] == self.MARK:
                marks += 1
                self.level.add_to_left(self.level.left_margin - marks, y, group)

        # Update cols side.
        types, groups = self.get_marks_col(x)

        self.level.clear_col(x)

        marks = 0
        for i, group in enumerate(groups[-1::-1]):
            if types[-(i + 1)] == self.MARK:
                marks += 1
                self.level.add_to_top(x, self.level.top_margin - marks, group)

    def save(self):
        self.writer.write()
