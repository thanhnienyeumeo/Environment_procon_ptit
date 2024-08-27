import pygame
import numpy as np
import random

# Khởi tạo pygame
from grid import Grid
from pattern import Pattern
pygame.init()


def main():
    m,n = 32,32
    cell_size = 20
    grid = Grid(m, n, cell_size)  # Tạo một lưới 7x7 với kích thước ô là 50
    running = True
    dragging = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                # print(event.pos)
                grid.update_hovered_cell(event.pos)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                  #print(f"Click tại vị trí: {pos}")
                    if grid.is_selecting_direction:
                        
                        grid.handle_direction_selection(pos)
                    else:
                        # print(1)
                        grid.check_pattern_click(pos)
                        dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and dragging:
                    pos = pygame.mouse.get_pos()
                    grid.stop_dragging(pos)
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    pos = pygame.mouse.get_pos()
                    grid.update_dragging(pos)

        grid.screen.fill((200, 200, 200))  # Màu nền của cửa sổ
        grid.draw()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()