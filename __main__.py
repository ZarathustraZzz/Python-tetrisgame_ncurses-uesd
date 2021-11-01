import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath("G:\mypymodule\\tetris\\requirements.txt")))
sys.path.append(BASE_DIR)
from tetris import game

g = game.Game()
g.start()
g.quit()

