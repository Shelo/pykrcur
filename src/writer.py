import os

class Writer(object):

    def __init__(self, level, root):
        self.level = level
        self.root = root

    def write(self):
        top = self.gen_top()
        left = self.gen_left()
        directory = '%dx%d' % (self.level.width, self.level.height)
        path = os.path.join(self.root, directory)
        if not os.path.exists(path):
            os.mkdir(path)
        file_name = self.level.id + '.krk'
        print os.path.join(path, file_name)
        with open(os.path.join(path, file_name), 'w') as f:
            f.write(top)
            f.write('\n===================\n')
            f.write(left)

    def gen_top(self):
        top = []
        for y in range(self.level.top_margin):
            has_one_value = False
            row = []
            for x in range(self.level.width):
                value = self.level.get_top_at(x, y)
                if y == self.level.top_margin - 1 and sum(self.level.get_col(x)) == 0:
                    row.append('0')
                else:
                    row.append(str(value) if value != -1 else '')
                if value != -1:
                    has_one_value = True

            if has_one_value:
                top.append('\t'.join(row))

        return '\n'.join(top)

    def gen_left(self):
        rows = []
        for y in range(self.level.height):
            row = []
            for x in range(self.level.left_margin):
                value = self.level.get_left_at(x, y)
                row.append(str(value) if value != -1 else '')

            rows.append(row)

        has_one_value = False
        while not has_one_value:
            for row in rows:
                if row[0] != '':
                    has_one_value = True

            if not has_one_value:
                for row in rows:
                    del row[0]

        left = []
        for row in rows:
            if row.count('') == len(row):
                row[-1] = '0'
            left.append('\t'.join(row))

        return '\n'.join(left)