import pygame
import numpy as np
import random

from game import Game
game = Game(32,32,20)
_,_,_,_ = game.step(0)
print(game.grid.board)