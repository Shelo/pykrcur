from os import listdir
from os.path import isfile, join
from src.puzzle import KRPuzzle
from src.reader import Reader
from random import choice

DIRECTORY = "levels/"
categories = [f for f in listdir(DIRECTORY) if not isfile(join(DIRECTORY, f))]

print "Categories:"
print "  0. Exit"
for i, _file in enumerate(categories):
    print "  " + str(i + 1) + ".", _file

print

category = -1
while category < 0 or category > len(categories):
    category = int(raw_input("Enter the category number: "))

if category != 0:
    category -= 1
    category_dir = join(DIRECTORY, categories[category])
    cat_files = [f for f in listdir(category_dir) if isfile(join(category_dir, f))]

    random_puzzle = choice(cat_files)

    reader = Reader(join(category_dir, random_puzzle))
    puzzle = KRPuzzle(reader.get_level())
    puzzle.start()
    # puzzle.output()
