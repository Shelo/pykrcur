from os import listdir
from os.path import isfile, join
from src.main import KRPuzzle
from src.reader import Reader

DIRECTORY = "levels/"
files = [f for f in listdir(DIRECTORY) if isfile(join(DIRECTORY, f)) and f.split('.')[-1] == 'krk']

for i, _file in enumerate(files):
    print str(i) + ".", '.'.join(_file.split('.')[:-1]).capitalize()

puzzle = -1
while puzzle < 0 or puzzle >= len(files):
    puzzle = int(raw_input("Enter the puzzle number: "))

reader = Reader(join(DIRECTORY, files[puzzle]))
puzzle = KRPuzzle(reader.get_level())
puzzle.start()
puzzle.output()