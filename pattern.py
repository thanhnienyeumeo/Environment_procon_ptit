import numpy as np
import pygame

class Pattern:
    def __init__(self, p, q, cell_size):
        self.p = p  # Số dòng
        self.q = q  # Số cột
        self.cell_size = cell_size  # Kích thước ô vuông
        self.size = max(p, q) * cell_size  # Kích thước tổng thể của pattern
        self.pattern = np.random.randint(2, size=(p, q))  # Ma trận 2D chứa giá trị 0 hoặc 1
        self.top = (0, 0)
        self.bottom = (0, 0)
        # Tạo surface để vẽ pattern với độ trong suốt
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

