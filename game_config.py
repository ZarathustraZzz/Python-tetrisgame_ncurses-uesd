from dataclasses import dataclass
import curses

D_Left  = 0
D_Right = 1
D_Down = 2
D_Rotate = 3
D_None = 5


@dataclass
class Position:  #每个方块都是四个小格子
    x: int
    y: int
    '''
    x1: int   #1
    y1: int
    x2: int   #2
    y2: int
    x3: int   #3
    y3: int
    '''

tetris_config = {
    "lives": 3,
    "speed": 1,
}


keys = {
    'LEFT': 0x44,
    'RIGHT': 0x43,
    'DOWN': 0x42,
    'Q': 0x71,
    'R': 0x72,
    'P': 0x70,
    'BACKSPACE': 0x20,   #空格键码 好像不能直接.KEY_BACKSPACE
}

game_sizes = {
    'height': 14,
    'width': 14,
}

game_themes = {
    "colors": {
        "default": (curses.COLOR_WHITE, curses.COLOR_BLACK),
        "bar": (curses.COLOR_BLUE, curses.COLOR_BLACK),      #0000
        "block": (curses.COLOR_YELLOW, curses.COLOR_BLACK),  #田
        "L_bar": (curses.COLOR_GREEN, curses.COLOR_BLACK),   #|___
        "J_bar": (curses.COLOR_GREEN, curses.COLOR_BLACK),   #___|先不要
        "T_bar": (curses.COLOR_CYAN, curses.COLOR_BLACK),    #T
        "Z_bar": (curses.COLOR_MAGENTA, curses.COLOR_BLACK), #Z
        "NZ_bar": (curses.COLOR_MAGENTA, curses.COLOR_BLACK),#反Z 先不要
        "lives": (curses.COLOR_RED, curses.COLOR_BLACK),
    },
    "tiles": {
        "tetris": '#',
        "lives": '♥ ',
    }

}
