import numpy as np
import pygame
from grid import Grid, apply_shift
from pattern import Pattern


def solve(question):
    return {"n": 1, "ops": [{"x": 1, "y": 1, "s": 1, "p": 1}]}

import time
class Game():
    N_DISCRETE_ACTIONS = 10674304

    
    def __init__(self, m, n,  start_board = None, end_board = None, patterns = None, render = None, cell_size = 10):
        super().__init__()
        self.m = m
        self.n = n
        self.cell_size = cell_size
        self.grid = Grid(m, n, cell_size, render = render, board = start_board, patterns = patterns)
        self.start_time = time.time()
        self.dict = []
        self.init_action()
        # self.action_space = gym.spaces.Discrete(self.init_action())
        # self.observation_space = gym.spaces.Box(low=0, high=3, shape=(self.m, self.n), dtype=np.uint8)
        #final grid having the same size, same count of 1,2,3 as grid but shuffle
        self.final_grid = Grid(m, n, cell_size, self.grid.cnt, board = end_board)
        self.running = True
        self.dragging = False
        
    
    def init_action(self):

        for b in range(0, len(self.grid.patterns)):
            sz_hori = self.grid.patterns[b].p
            sz_vert = self.grid.patterns[b].q
            
            for a in range(4):  
                for x in range(-sz_hori + 1,self.m):
                    for y in range(-sz_vert + 1,self.n):
                                self.dict.append([x, y, a, b])
        print(len(self.dict))
        return len(self.dict)

    

    def is_end(self):
        return self.grid == self.final_grid
    
    def convert(self, x, y, s, p):
        return self.dict.index([x,y,s,p])
        

    def step(self, action):
        
        x,y, direction, p = self.dict[action]
        if self.grid.patterns[p].p > self.m or self.grid.patterns[p].q > self.n:
            return (self.grid.board, 0, False, False, {})
        self.grid.selected_pattern = self.grid.patterns[p]
        self.grid.cur_x = x
        self.grid.cur_y = y
        self.grid.apply_shift(direction)
        #my destiny is alonej
        reward = 0
        done = False
        if self.is_end():
            done = True
            if self.grid == self.final_grid:
                reward = 1
            else:
                reward = 0
        else:
            reward = 1 / (self.cntDifferece() + 1)
        truncated = False
        return (self.grid.board, reward, done, truncated, {})
    
    def fake_step(self, action):
        
        x,y, direction, p = self.dict[action]
        if self.grid.patterns[p].p > self.m or self.grid.patterns[p].q > self.n:
            return (self.grid.board, 9999999, False, False, {})
        self.grid.selected_pattern = self.grid.patterns[p]
        self.grid.cur_x = x
        self.grid.cur_y = y
        new_board = self.grid.apply_shift(direction, inplace = False)
        
        #my destiny is alonej
        reward = 0
        done = False
        if np.all(new_board == self.final_grid.board):
            done = True
            reward = 0
        else:
            reward = self.cntDifferece(new_board)
            # print(reward)
        truncated = False
        return (new_board, reward, done, truncated, {})
    
    def cntDifferece(self, board = None):
            if board is None:
                board = self.grid.board
            cnt = 0
            for i in range(self.m):
                for j in range(self.n):
                    if self.final_grid.board[i][j] != board[i][j]:
                        cnt += 1
            return cnt

    def render(self):   
        pass

    def reset(self):
        self.grid = Grid(self.m, self.n, self.cell_size)
        self.final_grid = Grid(self.m, self.n, self.cell_size, self.grid.cnt)
        self.start_time = time.time()
        return self.grid.board, {}


    #def convert(self, action):
    #     #32x32, pattern 3x3 -> 34 x 34
    #     #from action --> (x,y,s,p)
    #     #max size of pattern is 256x256
    #     #because we can place pattern outside of the grid if at least one cell of pattern is inside the grid
    #     # so if size of grid is mxn, 
    #     # action = (255 + m + 255) (255 + n + 255) * s * p
    #     # max_m = 256 => 255 + 256 = 511
    #     p = action % 25
    #     action //= 25
    #     s = action % 4
    #     action //= 4
    #     x = action % 511
    #     x -= 255
    #     action //= 511
    #     y = action % 511
    #     y -= 255
    #     action //= 511
    #     print(x,y,s,p)
    #     return (x, y, s, p)
    #     # h h h n n n n n h s


    # def convert_back(self, x, y, s, p):
    #     action = 0
    #     action = action * 511 + y + 255
    #     action = action * 511 + x + 255
    #     action = action * 4 + s
    #     action = action * 25 + p
    #     return action
    
    