import numpy as np
import pygame



class Pattern:
    def __init__(self, p, q, cell_size, id = 0, render = None):
        self.p = p  # Số dòng
        self.q = q  # Số cột
        self.cell_size = cell_size  # Kích thước ô vuông
        self.size = max(p, q) * cell_size  # Kích thước tổng thể của pattern
        self.pattern = np.random.randint(2, size=(p, q))  # Ma trận 2D chứa giá trị 0 hoặc 1
        if id == 1:
            #1 o tat ca
            for i in range(p):
                for j in range(q):
                    self.pattern[i][j] =1
        elif id == 2:
            #1 o hang chan, 0 o hang le
            for i in range(p):
                for j in range(q):
                    if i % 2 == 0:
                        self.pattern[i][j] = 1
                    else:
                        self.pattern[i][j] = 0
        else:
            #1 o cot chan, 0 o cot le
            for i in range(p):
                for j in range(q):
                    if j % 2 == 0:
                        self.pattern[i][j] = 1
                    else:
                        self.pattern[i][j] = 0
        self.top = (0, 0)
        self.bottom = (0, 0)
        # Tạo surface để vẽ pattern với độ trong suốt
        if render:
            self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            self.update_surface()

    def update_surface(self):
        """Cập nhật surface của pattern với các màu tương ứng."""
        for y in range(self.p):
            for x in range(self.q):
                color = (255, 255, 255, 150) if self.pattern[y, x] == 0 else (255, 0, 0, 150)  # Đỏ cho 1, trắng cho 0
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.surface, color, rect)

    def draw(self, screen, x, y):
        """Vẽ pattern lên màn hình."""
        screen.blit(self.surface, (x, y))
        self.top = (x, y)
        self.bottom = (x + self.size, y + self.size)

    def draw_transparent(self, screen, x, y):
        """Vẽ pattern với độ trong suốt."""
        transparent_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        transparent_surface.blit(self.surface, (0, 0))
        screen.blit(transparent_surface, (x, y))
        self.top = (x, y)
        self.bottom = (x + self.size, y + self.size)


# import numpy as np
# import pygame



# class Pattern:
#     def __init__(self, p, q, cell_size, id = 0):
        
#         self.p = p  # Số dòng
#         self.q = q  # Số cột
#         self.cell_size = cell_size  # Kích thước ô vuông
#         self.size = max(p, q) * cell_size  # Kích thước tổng thể của pattern
#         self.pattern = np.random.randint(2, size=(p, q))  # Ma trận 2D chứa giá trị 0 hoặc 1
#         if id == 1:
#             #1 o tat ca
#             for i in range(p):
#                 for j in range(q):
#                     self.pattern[i][j] =1
#         elif id == 2:
#             #1 o hang chan, 0 o hang le
#             for i in range(p):
#                 for j in range(q):
#                     if i % 2 == 0:
#                         self.pattern[i][j] = 1
#                     else:
#                         self.pattern[i][j] = 0
#         else:
#             #1 o cot chan, 0 o cot le
#             for i in range(p):
#                 for j in range(q):
#                     if j % 2 == 0:
#                         self.pattern[i][j] = 1
#                     else:
#                         self.pattern[i][j] = 0
#         self.top = (0, 0)
#         self.bottom = (0, 0)
#         # Tạo surface để vẽ pattern với độ trong suốt
#         self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
#         self.update_surface()

#     def update_surface(self):
#         """Cập nhật surface của pattern với các màu tương ứng."""
#         for y in range(self.p):
#             for x in range(self.q):
#                 color = (255, 255, 255, 150) if self.pattern[y, x] == 0 else (255, 0, 0, 150)  # Đỏ cho 1, trắng cho 0
#                 rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
#                 pygame.draw.rect(self.surface, color, rect)
    
#     def generate_pattern_matrix(self, size):
#         if self.pattern_id == 1:
#             return [[1 for _ in range(size)] for _ in range(size)]
#         elif self.pattern_id == 2:  # Hàng chẵn 1, hàng lẻ 0
#             return [[(i % 2) for _ in range(size)] for i in range(size)]
#         elif self.pattern_id == 3:  # Cột chẵn 1, cột lẻ 0
#             return [[(j % 2) for j in range(size)] for _ in range(size)]
#         else:
#             return [[0 for _ in range(size)] for _ in range(size)]

#     def draw(self, screen, x, y):
#         """Vẽ pattern lên màn hình."""
#         screen.blit(self.surface, (x, y))
#         self.top = (x, y)
#         self.bottom = (x + self.size, y + self.size)

#     def draw_transparent(self, screen, x, y):
#         """Vẽ pattern với độ trong suốt."""
#         transparent_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
#         transparent_surface.blit(self.surface, (0, 0))
#         screen.blit(transparent_surface, (x, y))
#         self.top = (x, y)
#         self.bottom = (x + self.size, y + self.size)

