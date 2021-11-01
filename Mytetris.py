from tetris import game_config
from tetris.game_config import Position
import random
import copy
import time


class Mytetris(object):
    def __init__(self) -> None:
        self.window_size = Position(game_config.game_sizes["width"], game_config.game_sizes["height"])
        self.direction = game_config.D_None
        self.body = []
        self.body_rotate = []
        self.termstart_flag = True
        self.rotate_flag = False
        self.rotate_times = 0
        self.init_x = int(round(self.window_size.x / 2))
        #self.block_dic = {'0': 'block', '1': 'bar', '2': 'L_bar', '3': 'J_bar', '4': 'Z_bar'}
        self.termstart_block_num = 0
        self.fixed_body = []


    def termstart(self) :          #新的一个回合
        self.rotate_flag = False
        if self.termstart_flag == True:
            self.body = []
            self.termstart_block()
            self.body_rotate = []
            self.rotate_times = 0

    def reset(self) :     #复位
        self.body = []
        self.body_rotate = []
        self.rotate_times = 0
        self.termstart_flag = True
        self.rotate_flag = False
        self.termstart_block()
        self.fixed_body = []
        '''
        self.fixed_body = [Position(1,9),Position(2,9),Position(3,9),\
       Position(4,9),Position(5,9),Position(6,9),Position(7,9),Position(8,9),Position(9,9),\
                           Position(10,9),Position(11,9),Position(12,9),Position(13,9)]
        '''
        #for i in range(1,self.window_size.x-1):
            #self.fixed_body.append(Position(i,self.window_size.y-2))

    def termstart_block(self) -> int:   #每回合之前随机一个方块 更新body&代号
        self.termstart_block_num = random.randint(0, 4)
        if self.termstart_block_num == 0:
            self.block()
        elif self.termstart_block_num == 1:
            self.bar()
        elif self.termstart_block_num == 2:
            self.L_bar()
        elif self.termstart_block_num == 3:
            self.T_bar()
        else:
            self.Z_bar()

        self.termstart_flag = False

    def vanish_check(self) -> int:   #检查某一行被完全填满 返回行号
        for j in range(self.window_size.y-1, 0, -1):
            for i in range(1, self.window_size.x):
                if Position(i,j) not in self.fixed_body:
                    break
            else:
                return j
        return 0

    def vanish_block(self) -> bool:  #消除全满的一行
        row = self.vanish_check()
        copy_body = copy.deepcopy(self.fixed_body)
        if row > 0:
            for i in range(self.window_size.x-1, 0, -1):
                self.fixed_body.remove(Position(i, row))
                for j in range(row):
                    if Position(i, j) in copy_body:
                        self.fixed_body.remove(Position(i, j))
                        self.fixed_body.append(Position(i, j+1))
            return True
        else:
            return False

    def fixed_body_pos(self) :  #碰到底部或别的fixed_body后加入fixed_body
        last_fixed_body = copy.deepcopy(self.fixed_body)
        last_body = copy.copy(self.body)
        fixed_body_reapt = []
        for i in range(1, self.window_size.x):
            for pos in last_body:
                if pos == Position(i, self.window_size.y-2):
                    fixed_body_reapt.extend(last_body)
                    self.body = []
                    self.termstart_flag = True
                    break
        for f in last_fixed_body:
            for pos in last_body:
                if pos == Position(f.x, f.y - 1):
                    fixed_body_reapt.extend(last_body)
                    self.body = []
                    self.termstart_flag = True
                    break
        for i in fixed_body_reapt:
            if not i in last_fixed_body:
                last_fixed_body.append(i)   #直接append没有返回值
        self.fixed_body = last_fixed_body
        #[self.fixed_body.append(i) for i in fixed_body_reapt if i not in fixed_body_reapt]

    def get_dis_inc_factor(self) -> Position:  #得到左右移的坐标变换情况
        dis_increment_factor = Position(0, 0)
        highest_y = self.window_size.y-1
        for f in self.fixed_body:
            if len(self.fixed_body) != 0:
                if highest_y > f.y:
                    highest_y = f.y
        # 修改每个方向上的速度
        if self.direction == game_config.D_Left:
            dis_increment_factor.x = -1
        elif self.direction == game_config.D_Right:
            dis_increment_factor.x = 1
        elif self.direction == game_config.D_Down:
            for i in range(4):
                if self.body[i].y >= highest_y - 2:
                    break
            else:
                dis_increment_factor.y = 1
        else:
            dis_increment_factor.x = 0
            dis_increment_factor.y = 0
        return dis_increment_factor

    def rotate_check(self) :    #转了多少次
        last_rotate_times = copy.deepcopy(self.rotate_times)
        self.rotate_times = last_rotate_times + 1

    def get_rotate_factor(self) -> list :    #得到旋转的坐标变换情况 每个方块不一样
        dis_rotate_factor = []
        if self.direction == game_config.D_Rotate:
            self.rotate_check()
            self.rotate_flag = True
            if self.termstart_block_num == 0:
                self.block()
            elif self.termstart_block_num == 1:
                self.bar()
            elif self.termstart_block_num == 2:
                self.L_bar()
            elif self.termstart_block_num == 3:
                self.T_bar()
            else:
                self.Z_bar()
            dis_rotate_factor = self.body_rotate
        else:
            dis_rotate_factor = [Position(0,0),Position(0,0),Position(0,0),Position(0,0)]
        self.rotate_flag = False
        return dis_rotate_factor

    def update_tetris_pos(self) -> None:   #更新位置 一直下落
        dis_increment_factor = self.get_dis_inc_factor()
        dis_rotate_factor = self.get_rotate_factor()
        for index, item in enumerate(self.body):
            item.x += dis_increment_factor.x
            item.x += dis_rotate_factor[index].x
            item.y += dis_increment_factor.y
            item.y += dis_rotate_factor[index].y
        dis_increment_factor = Position(0,0)
        self.direction = game_config.D_None
        self.body_rotate = [Position(0,0),Position(0,0),Position(0,0),Position(0,0)]

    def auto_tetris_pos(self):
        auto_increment_factor = Position(0, 1)
        for index, item in enumerate(self.body):
            item.y += auto_increment_factor.y

    def check_alive(self) -> bool: #上面进墙里死亡 死亡是False
        for col in range(1,self.window_size.x-1):
            if Position(col,0) in self.fixed_body:
                return False
        return True

    def block(self):   #田和它的旋转姿态
        if self.termstart_flag == True:
            self.body.clear()
            self.body.append(Position(self.init_x - 1, 0))
            self.body.append(Position(self.init_x, 0))
            self.body.append(Position(self.init_x - 1, 1))
            self.body.append(Position(self.init_x, 1))
        elif self.rotate_flag == True:    #转几次都一样
            self.body_rotate = [Position(0, 0), Position(0, 0), Position(0, 0), Position(0, 0)]
        else:
            self.body_rotate = [Position(0,0),Position(0,0),Position(0,0),Position(0,0)]

    def bar(self):   #0000
        if self.termstart_flag == True:
            self.body.clear()
            self.body.append(Position(self.init_x - 2, 0))
            self.body.append(Position(self.init_x - 1, 0))
            self.body.append(Position(self.init_x, 0))
            self.body.append(Position(self.init_x + 1, 0))
        elif self.rotate_flag == True and self.rotate_times % 2 == 1:
            self.body_rotate.clear()
            self.body_rotate.append(Position(1, 0))
            self.body_rotate.append(Position(0, 1))
            self.body_rotate.append(Position(-1, 2))
            self.body_rotate.append(Position(-2, 3))
        elif self.rotate_flag == True and self.rotate_times % 2 == 0:
            self.body_rotate.clear()
            self.body_rotate.append(Position(-1, 0))
            self.body_rotate.append(Position(0, -1))
            self.body_rotate.append(Position(1, -2))
            self.body_rotate.append(Position(2, -3))
        else:
            self.body_rotate = [Position(0,0),Position(0,0),Position(0,0),Position(0,0)]

    def L_bar(self) :   #|___
        if self.termstart_flag == True:
            self.body.clear()
            self.body.append(Position(self.init_x - 1, 0))
            self.body.append(Position(self.init_x - 1, 1))
            self.body.append(Position(self.init_x, 1))
            self.body.append(Position(self.init_x + 1, 1))
        elif self.rotate_flag == True and self.rotate_times % 4 == 1:
            self.body_rotate.clear()
            self.body_rotate.append(Position(1, 0))
            self.body_rotate.append(Position(0, -1))
            self.body_rotate.append(Position(-1, 0))
            self.body_rotate.append(Position(-2, 1))
        elif self.rotate_flag == True and self.rotate_times % 4 == 2:
            self.body_rotate.clear()
            self.body_rotate.append(Position(-1, 0))
            self.body_rotate.append(Position(1, 0))
            self.body_rotate.append(Position(2, -1))
            self.body_rotate.append(Position(2, -1))
        elif self.rotate_flag == True and self.rotate_times % 4 == 3:
            self.body_rotate.clear()
            self.body_rotate.append(Position(2, 0))
            self.body_rotate.append(Position(1, 1))
            self.body_rotate.append(Position(0, 2))
            self.body_rotate.append(Position(-1, 1))
        elif self.rotate_flag == True and self.rotate_times % 4 == 0:
            self.body_rotate.clear()
            self.body_rotate.append(Position(-1, 1))
            self.body_rotate.append(Position(-1, 1))
            self.body_rotate.append(Position(0, 0))
            self.body_rotate.append(Position(2, 0))
        else:
            self.body_rotate = [Position(0,0),Position(0,0),Position(0,0),Position(0,0)]

    def T_bar(self) :   #T
        if self.termstart_flag == True:
            self.body.clear()
            self.body.append(Position(self.init_x - 1, 0))
            self.body.append(Position(self.init_x, 0))
            self.body.append(Position(self.init_x + 1, 0))
            self.body.append(Position(self.init_x, 1))
        elif self.rotate_flag == True and self.rotate_times % 4 == 1:
            self.body_rotate.clear()
            self.body_rotate.append(Position(1, 0))
            self.body_rotate.append(Position(0, 1))
            self.body_rotate.append(Position(-1, 2))
            self.body_rotate.append(Position(-1, 0))
        elif self.rotate_flag == True and self.rotate_times % 4 == 2:
            self.body_rotate.clear()
            self.body_rotate.append(Position(1, 1))
            self.body_rotate.append(Position(0, 0))
            self.body_rotate.append(Position(-1, -1))
            self.body_rotate.append(Position(1, -1))
        elif self.rotate_flag == True and self.rotate_times % 4 == 3:
            self.body_rotate.clear()
            self.body_rotate.append(Position(-1, 1))
            self.body_rotate.append(Position(0, 0))
            self.body_rotate.append(Position(1, -1))
            self.body_rotate.append(Position(1, 1))
        elif self.rotate_flag == True and self.rotate_times % 4 == 0:
            self.body_rotate.clear()
            self.body_rotate.append(Position(-1, -1))
            self.body_rotate.append(Position(0, 0))
            self.body_rotate.append(Position(1, 1))
            self.body_rotate.append(Position(-1, 1))
        else:
            self.body_rotate = [Position(0,0),Position(0,0),Position(0,0),Position(0,0)]

    def Z_bar(self) :  # Z
        if self.termstart_flag == True:
            self.body.clear()
            self.body.append(Position(self.init_x - 1, 0))
            self.body.append(Position(self.init_x, 0))
            self.body.append(Position(self.init_x, 1))
            self.body.append(Position(self.init_x + 1, 1))
        elif self.rotate_flag == True and self.rotate_times % 4 == 1:
            self.body_rotate.clear()
            self.body_rotate.append(Position(1, 0))
            self.body_rotate.append(Position(0, 1))
            self.body_rotate.append(Position(-1, 0))
            self.body_rotate.append(Position(-2, 1))
        elif self.rotate_flag == True and self.rotate_times % 4 == 2:
            self.body_rotate.clear()
            self.body_rotate.append(Position(1, 2))
            self.body_rotate.append(Position(0, 1))
            self.body_rotate.append(Position(1, 0))
            self.body_rotate.append(Position(0, -1))
        elif self.rotate_flag == True and self.rotate_times % 4 == 3:
            self.body_rotate.clear()
            self.body_rotate.append(Position(-2, 1))
            self.body_rotate.append(Position(-1, 0))
            self.body_rotate.append(Position(0, 1))
            self.body_rotate.append(Position(1, 0))
        elif self.rotate_flag == True and self.rotate_times % 4 == 0:
            self.body_rotate.clear()
            self.body_rotate.append(Position(-1, -1))
            self.body_rotate.append(Position(0, 0))
            self.body_rotate.append(Position(-1, 1))
            self.body_rotate.append(Position(0, 2))
        else:
            self.body_rotate = [Position(0,0),Position(0,0),Position(0,0),Position(0,0)]
