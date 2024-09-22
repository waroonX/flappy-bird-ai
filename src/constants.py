import pathlib
from os import path

# Folder constants
CURR_DIR = pathlib.Path(__file__).parent.resolve()
WORK_DIR = CURR_DIR.parent.resolve()

SRC_DIR = path.join(WORK_DIR, 'src')
IMG_DIR = path.join(SRC_DIR, 'imgs')

# Pygame window constants

WIN_WIDTH = 500
WIN_HEIGHT = 800