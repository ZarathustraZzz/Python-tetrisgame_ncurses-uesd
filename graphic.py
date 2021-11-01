from tetris import game_config
from tetris.game_config import Position
from tetris.Mytetris import Mytetris
import curses
import time
import copy


class Graphic:
    def __init__(self) -> None:
        self.target_fps = 50
        self.true_fps = 50
        self.window = curses.initscr()
        curses.noecho()

        # 让游戏窗口居中
        self.window_height = game_config.game_sizes['height']
        self.window_width = game_config.game_sizes['width']

        x = (self.window.getmaxyx()[1] - self.window_width) / 2
        y = (self.window.getmaxyx()[0] - self.window_height) / 2
        if x < 0 or y < 2:
            raise ValueError('Not enough space to display the game.')
        self.game_area_pos = Position(int(x), int(y))      #游戏窗口起始左上坐标 开个游戏小窗
        self.game_area = self.window.subwin(self.window_height, self.window_width,
                                            self.game_area_pos.y, self.game_area_pos.x)
        self.game_area.nodelay(True)
        self.game_area.keypad(True)
        self.last_time = time.time()
        self.delay_time = 0.02
        self.fps_update_interval = 4
        self.frame_count = 0

        curses.curs_set(0) #光标不可见
        curses.start_color()

        curses.init_pair(1, *game_config.game_themes["colors"]["default"])
        curses.init_pair(2, *game_config.game_themes["colors"]["lives"])
        curses.init_pair(3, *game_config.game_themes["colors"]["bar"])
        curses.init_pair(4, *game_config.game_themes["colors"]["block"])
        curses.init_pair(5, *game_config.game_themes["colors"]["L_bar"])
        curses.init_pair(6, *game_config.game_themes["colors"]["T_bar"])
        curses.init_pair(7, *game_config.game_themes["colors"]["Z_bar"])

        self.C_default = curses.color_pair(1)
        self.C_lives = curses.color_pair(2)
        self.C_bar = curses.color_pair(3)
        self.C_block = curses.color_pair(4)
        self.C_L_bar = curses.color_pair(5)
        self.C_T_bar = curses.color_pair(6)
        self.C_Z_bar = curses.color_pair(7)

    def draw_body(self,Mytetris:Mytetris) -> None:
        if Mytetris.termstart_block_num == 0:
            for item in Mytetris.body:
                self.game_area.addch(item.y, item.x,
                            game_config.game_themes["tiles"]["tetris"],
                            self.C_block)
        elif Mytetris.termstart_block_num == 1:
            for item in Mytetris.body:
                self.game_area.addch(item.y, item.x,
                            game_config.game_themes["tiles"]["tetris"],
                            self.C_bar)
        elif Mytetris.termstart_block_num == 2:
            for item in Mytetris.body:
                self.game_area.addch(item.y, item.x,
                            game_config.game_themes["tiles"]["tetris"],
                            self.C_L_bar)
        elif Mytetris.termstart_block_num == 3:
            for item in Mytetris.body:
                self.game_area.addch(item.y, item.x,
                            game_config.game_themes["tiles"]["tetris"],
                            self.C_T_bar)
        else:
            for item in Mytetris.body:
                self.game_area.addch(item.y, item.x,
                            game_config.game_themes["tiles"]["tetris"],
                            self.C_Z_bar)

    def draw_fixed_body(self,Mytetris:Mytetris) -> None:
        for item in Mytetris.fixed_body:
            self.game_area.addch(item.y,
                                 item.x,
                                 game_config.game_themes["tiles"]["tetris"],
                                 self.C_default)

    def draw_border(self) -> None:
        self.game_area.border(0,0,0,'X',0,0,' ','X')

    def draw_help(self):
        helps = ["Help:",
                 "Press ←  or  → to change direction",
                 "Press 'R' to reset",
                 "Press 'Q' to quit",
                 "Press 'P' to pause"]
        pos = Position(0, 0)
        for help_text in helps:
            self.window.addstr(pos.y, pos.x, help_text)
            pos.y += 1

    def draw_game(self, Mytetris: Mytetris, lives, scores, highest_score) -> None:
        self.window.erase()
        self.draw_help()
        self.update_fps()
        self.draw_fps()
        self.draw_lives_and_scores(lives, scores, highest_score)
        self.draw_border()
        self.draw_body(Mytetris)
        self.draw_fixed_body(Mytetris)
        self.window.refresh()
        self.game_area.refresh()
        time.sleep(self.delay_time)

    def draw_fps(self) -> None:
        text = "fps: %.1f" % self.true_fps
        pos = copy.deepcopy(self.game_area_pos)
        pos.y -= 2
        self.draw_text(self.window,
                       pos, text, self.C_default)

    def draw_lives_and_scores(self, lives, scores, highest_score):
        text = "lives: "
        pos = copy.deepcopy(self.game_area_pos)
        pos.y -= 1
        self.draw_text(self.window,
                       pos, text,
                       self.C_default)

        pos.x += len(text)
        text = lives * game_config.game_themes["tiles"]["lives"]
        self.draw_text(self.window,
                       pos, text,
                       self.C_lives)

        pos.x += len(text)
        text = "scores: {} highest_socre: {}".format(scores, highest_score)
        self.draw_text(self.window,
                       pos, text,
                       self.C_default)

    def draw_text(self, win, pos, text, attr=None) -> None:
        win.addstr(pos.y, pos.x, text, attr)

    def draw_message_window(self, texts: list) -> None:  # 接收一个 str 列表
        text1 = "Press any key to continue."
        nrows = 6 + len(texts)  # 留出行与行之间的空隙
        ncols = max(*[len(len_tex) for len_tex in texts], len(text1)) + 20

        x = (self.window.getmaxyx()[1] - ncols) / 2
        y = (self.window.getmaxyx()[0] - nrows) / 2
        pos = Position(int(x), int(y))
        message_win = curses.newwin(nrows, ncols, pos.y, pos.x)
        message_win.nodelay(False)
        # 绘制文字提示
        # 底部文字居中
        pos.y = nrows - 2
        pos.x = self.get_middle(ncols, len(text1))
        message_win.addstr(pos.y, pos.x, text1, self.C_default)

        pos.y = 2
        for text in texts:
            pos.x = self.get_middle(ncols, len(text))
            message_win.addstr(pos.y, pos.x, text, self.C_default)
            pos.y += 1

        message_win.border()
        message_win.refresh()
        message_win.getch()

        message_win.nodelay(True)
        message_win.clear()
        del message_win

    def get_middle(self, win_len, text_len) -> int:
        return int((win_len - text_len) / 2)

    def esp_fps(self) -> bool:  # 返回是否更新了fps
        # 每两帧计算一次
        if self.frame_count < self.fps_update_interval:
            self.frame_count += 1
            return False
        time_span = time.time() - self.last_time
        self.last_time = time.time()
        self.true_fps = 1.0 / (time_span / self.frame_count)
        self.frame_count = 0
        return True

    def update_fps(self) -> None:
        if self.esp_fps():
            err = self.true_fps - self.target_fps
            self.delay_time += 0.00001 * err

    def quite(self):
        pass
