import numpy as np
import pygame
from grid import Grid
from pattern import Pattern
import gym

def solve(question):
    return {"n": 1, "ops": [{"x": 1, "y": 1, "s": 1, "p": 1}]}

import time
class Game(gym.Env):
    N_DISCRETE_ACTIONS = 10674304

    
    def __init__(self, m, n, cell_size):
        super.__init__()
        self.m = m
        self.n = n
        self.cell_size = cell_size
        self.grid = Grid(m, n, cell_size)
        self.start_time = time.time()
        self.dict = []
        self.action_space = gym.spaces.Discrete(self.init_action())
        self.observation_space = gym.spaces.Box(low=0, high=3, shape=(self.m, self.n), dtype=np.uint8)
        #final grid having the same size, same count of 1,2,3 as grid but shuffle
        self.final_grid = Grid(m, n, cell_size, self.grid.cnt)
        self.running = True
        self.dragging = False
        
    
    def init_action(self):
        for b in range(25):
            sz = int((b-1)/3+1)
            sz = 2 ** (sz)
            for a in range(4):  
                for x in range(-sz + 1,self.n):
                    for y in range(-sz + 1,self.m):
                                self.dict.append([x, y, a, b])
        print(len(self.dict))
        return len(self.dict)

    

    def is_end(self):
        return self.grid == self.final_grid or time.time() - self.start_time > 60*4


    def step(self, action):
        
        x,y, direction, p = self.dict[action]
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
    
    def cntDifferece(self):
            cnt = 0
            for i in range(self.m):
                for j in range(self.n):
                    if self.grid.board[i][j] != self.final_grid.board[i][j]:
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
    
    