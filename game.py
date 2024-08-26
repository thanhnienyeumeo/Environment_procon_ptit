import numpy as np
import pygame
from grid import Grid
from pattern import Pattern
import gym
class Game(gym.Env):
    def __init__(self, m, n, cell_size):
        self.m = m
        self.n = n
        self.cell_size = cell_size
        self.grid = Grid(m, n, cell_size)
        #final grid having the same size, same count of 1,2,3 as grid but shuffle
        self.final_grid = Grid(m, n, cell_size, self.grid.cnt)
        self.running = True
        self.dragging = False
        
    
    def convert(self, action):
        id = action // 4
        direction = action % 4
        return id, direction

    def is_end(self):
        return self.grid == self.final_grid


    def step(self, action):
        id, direction = self.convert(action)
        self.grid.selected_pattern = self.grid.patterns[id]
        self.grid.apply_shift(direction)

        reward = 0
        done = False
        if self.is_end():
            done = True
            reward = 1
        return self.grid, reward, done, None

    def render(self):
        pass

    def reset(self):
        self.grid = Grid(self.m, self.n, self.cell_size)
        self.final_grid = Grid(self.m, self.n, self.cell_size, self.grid.cnt)
        return self.grid
