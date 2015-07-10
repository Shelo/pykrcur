from src.editor import KREditor
import sys
from src.level import Level
import os
from src.reader import Reader

name, width, height = sys.argv[1:4]

width = int(width)
height = int(height)

level_file = os.path.join(os.getcwd(), os.path.join(os.path.join('levels', '%dx%d' % (width, height)), name + ".krk"))

if os.path.exists(level_file):
    confirm = raw_input("That level exists, are you sure? [y/n]: ")
else:
    confirm = 'y'

if confirm.lower() == 'y':
    level = Level(name, width, width / 2 + 1, height / 2 + 1, height)
    editor = KREditor(level, os.path.join(os.getcwd(), 'levels'))
    editor.start()
