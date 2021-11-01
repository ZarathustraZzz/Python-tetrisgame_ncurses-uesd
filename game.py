import curses
from random import randrange
from tetris import game_config
from tetris.game_config import Position
from tetris import graphic
from tetris import Mytetris
import time


class Game:
    def __init__(self) -> None:
        self.start_time = time.time()
        self.lives = game_config.tetris_config["lives"]
        self.scores = 0
        self.highest_score = 0
        self.game_flag = True
        self.graphic = graphic.Graphic()
        self.tetris = Mytetris.Mytetris()

    def start(self) -> None:
        self.reset()

        while self.game_flag:
            self.graphic.draw_game(self.tetris, self.lives, self.scores, self.highest_score)
            self.tetris.update_tetris_pos()

            if not self.update_control():
                continue
            if time.time() - self.start_time < 1/game_config.tetris_config["speed"]:
                continue
            #速度0.5s/格
            self.start_time = time.time()
            self.update_tetris()

    def reset(self) -> None:
        self.lives = game_config.tetris_config["lives"]
        self.scores = 0
        self.highest_score = 0
        self.game_flag = True
        self.tetris.reset()

    def update_tetris(self) -> None:
        self.tetris.termstart()
        self.tetris.auto_tetris_pos()
        self.tetris.fixed_body_pos()
        self.graphic.draw_game(self.tetris, self.lives, self.scores, self.highest_score)
        vanish_flag = self.tetris.vanish_check()
        if vanish_flag > 0:
            time.sleep(1)
        for i in range(4):  #最多一次消除四行
            vanish_block = self.tetris.vanish_block()
            if vanish_block == True:
                self.scores += 1
                if self.scores >= 30:
                    self.win()
                self.graphic.draw_game(self.tetris, self.lives, self.scores, self.highest_score)
                time.sleep(1)
        if not self.tetris.check_alive():
            self.game_over()

    def update_control(self) -> bool:
        key = self.graphic.game_area.getch()

        if key == curses.KEY_LEFT:
            self.tetris.direction = game_config.D_Left
        elif key == curses.KEY_RIGHT:
            self.tetris.direction = game_config.D_Right
        elif key == curses.KEY_DOWN:
            self.tetris.direction = game_config.D_Down
        elif key == game_config.keys['BACKSPACE']:
            self.tetris.direction = game_config.D_Rotate
        elif key == game_config.keys['Q']:
            self.game_flag = False
            return False
        elif key == game_config.keys['R']:
            self.reset()
            return False
        elif key == game_config.keys['P']:
            self.game_pause()
            return False

        return True

    def win(self):
        self.game_flag = False
        self.graphic.draw_game(self.tetris, self.lives, self.scores, self.highest_score)
        text1 = "You Win!"
        text2 = "Your score is %d" % max(self.scores, self.highest_score)
        self.graphic.draw_message_window([text1, text2])
        self.reset()

    def game_over(self):
        if self.lives > 1:
            self.lives -= 1
            self.highest_score = max(self.highest_score, self.scores)
            self.scores = 0
            self.tetris.reset()
            curses.flash()
            return

        self.game_flag = False
        self.lives -= 1
        self.graphic.draw_game(self.tetris, self.lives, self.scores, self.highest_score)
        text1 = "GG!"
        text2 = "Your score is %d" % max(self.scores, self.highest_score)
        self.graphic.draw_message_window([text1, text2])
        self.reset()

    def game_pause(self):
        pause_text = 'You have paused the game...'
        self.game_flag = False
        self.graphic.draw_message_window([pause_text])
        self.game_flag = True


    def quit(self):
        curses.echo()
        curses.endwin()
