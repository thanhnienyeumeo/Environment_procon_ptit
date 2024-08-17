import pygame
import numpy as np
import random

# Khởi tạo pygame
pygame.init()

class Grid:
    def __init__(self, m, n, cell_size):
        self.m = m  # Số dòng
        self.n = n  # Số cột
        self.cell_size = cell_size  # Kích thước ô vuông
        self.width = n * cell_size  # Chiều rộng cửa sổ
        self.height = m * cell_size  # Chiều cao cửa sổ
        self.board = np.zeros((m, n), dtype=int)  # Bảng 2D chứa các giá trị từ 0 đến 3
        self.colors = {
            0: (255, 255, 255),  # Trắng
            1: (255, 0, 0),      # Đỏ
            2: (0, 255, 0),      # Xanh lá
            3: (0, 0, 255)       # Xanh dương
        }
        self.font = pygame.font.SysFont(None, 18)  # Font chữ để hiển thị số
        self.screen = pygame.display.set_mode((self.width + 400, self.height))  # Tạo cửa sổ, +400 cho phần giao diện pattern

        self.fill_board()  # Gán giá trị cho bảng
        self.patterns_3x3 = [Pattern(3, 3, cell_size) for _ in range(3)]  # Tạo 3 pattern 3x3 ngẫu nhiên
        self.patterns_2x2 = [Pattern(2, 2, cell_size) for _ in range(2)]  # Tạo 2 pattern 2x2 ngẫu nhiên
        self.selected_pattern = None  # Pattern được chọn
        self.original_pattern_pos = None  # Vị trí gốc của pattern
        self.current_pattern_pos = None  # Vị trí hiện tại của pattern

    def fill_board(self):
        """Gán ngẫu nhiên giá trị từ 0 đến 3 cho các ô trong bảng, đảm bảo mỗi giá trị chiếm ít nhất 10% số phần tử."""
        num_cells = self.m * self.n
        min_count = num_cells // 10
        values = [0, 1, 2, 3]
        remaining_cells = list(range(num_cells))

        for value in values:
            for _ in range(min_count):
                idx = random.choice(remaining_cells)
                y, x = divmod(idx, self.n)
                self.board[y][x] = value
                remaining_cells.remove(idx)

        for idx in remaining_cells:
            y, x = divmod(idx, self.n)
            self.board[y][x] = random.choice(values)

    def draw(self):
        """Vẽ bảng lên màn hình."""
        for y in range(self.m):
            for x in range(self.n):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.colors[self.board[y][x]], rect)

                # Hiển thị số trên ô vuông
                text = self.font.render(str(self.board[y][x]), True, (0, 0, 0))  # Màu chữ là đen
                text_rect = text.get_rect(center=(x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2))
                self.screen.blit(text, text_rect)

        # Vẽ 3 pattern 3x3
        for i, pattern in enumerate(self.patterns_3x3):
            pattern_x = self.width + 10
            pattern_y = i * (pattern.size + 10) + 10
            pattern.draw(self.screen, pattern_x, pattern_y)

        # Vẽ 2 pattern 2x2
        for i, pattern in enumerate(self.patterns_2x2):
            pattern_x = self.width + 10 + 3 * (self.patterns_3x3[0].size + 10)
            pattern_y = i * (pattern.size + 10) + 10
            pattern.draw(self.screen, pattern_x, pattern_y)

        # Vẽ pattern đang được kéo, nếu có
        if self.selected_pattern:
            x, y = self.current_pattern_pos
            self.selected_pattern.draw_transparent(self.screen, x, y)

    def check_pattern_click(self, pos):
        """Kiểm tra xem người dùng có click vào pattern nào không."""
        for i, pattern in enumerate(self.patterns_3x3):
            pattern_x = self.width + 10
            pattern_y = i * (pattern.size + 10) + 10
            if pattern_x <= pos[0] <= pattern_x + pattern.size and pattern_y <= pos[1] <= pattern_y + pattern.size:
                rel_x = (pos[0] - pattern_x) // pattern.cell_size
                rel_y = (pos[1] - pattern_y) // pattern.cell_size
                if 0 <= rel_x < pattern.q and 0 <= rel_y < pattern.p:
                    self.selected_pattern = pattern
                    self.original_pattern_pos = (pattern_x, pattern_y)
                    self.current_pattern_pos = (pos[0] - pattern.cell_size * rel_x, pos[1] - pattern.cell_size * rel_y)
                    return

        for i, pattern in enumerate(self.patterns_2x2):
            pattern_x = self.width + 10 + 3 * (self.patterns_3x3[0].size + 10)
            pattern_y = i * (pattern.size + 10) + 10
            if pattern_x <= pos[0] <= pattern_x + pattern.size and pattern_y <= pos[1] <= pattern_y + pattern.size:
                rel_x = (pos[0] - pattern_x) // pattern.cell_size
                rel_y = (pos[1] - pattern_y) // pattern.cell_size
                if 0 <= rel_x < pattern.q and 0 <= rel_y < pattern.p:
                    self.selected_pattern = pattern
                    self.original_pattern_pos = (pattern_x, pattern_y)
                    self.current_pattern_pos = (pos[0] - pattern.cell_size * rel_x, pos[1] - pattern.cell_size * rel_y)
                    return

    # def process_grid(self, pos):
    #     """Xử lý grid khi pattern được thả vào."""
    #     if self.selected_pattern:
    #         print("Vị trí click lưu lại:", pos)
    #         grid_x = pos[0] // self.cell_size
    #         grid_y = pos[1] // self.cell_size
    #         print(f"Ô trong grid được click: ({grid_x}, {grid_y})")
    #         self.selected_pattern = None
    #         self.original_pattern_pos = None
    #         self.current_pattern_pos = None
    def process_grid(self, pos):
        """Xử lý grid khi pattern được thả vào."""
        if self.selected_pattern:
            grid_x = pos[0] // self.cell_size
            grid_y = pos[1] // self.cell_size
            print("grid_x: ", grid_x)
            print("grid_y: ", grid_y)
            if grid_x > self.m or grid_y > self.n:
                print("ERROR: Out of grid")
                return
            print(self.board[grid_y][grid_x])
            pattern_p = self.selected_pattern.p
            pattern_q = self.selected_pattern.q
            lifted_elements = []

            # Bước 1: Đặt pattern P lên bảng B và "nhấc" các phần tử trong B tương ứng với phần tử 1 trong P
            for i in range(pattern_p):
                for j in range(pattern_q):
                    if self.selected_pattern.pattern[i][j] == 1:
                        if 0 <= grid_y + i < self.m and 0 <= grid_x + j < self.n:
                            lifted_elements.append(self.board[grid_y + i][grid_x + j])
                            self.board[grid_y + i][grid_x + j] = -1  # Sử dụng giá trị đặc biệt để chỉ định ô trống

            # Bước 2: Dịch các phần tử còn lại theo hướng đã chọn
            for i in range(self.m):
                for j in range(self.n - 1, -1, -1):  # Dịch sang trái
                    if self.board[i][j] == -1:  # Nếu ô này bị nhấc lên
                        for k in range(j, self.n - 1):  # Dịch các phần tử bên phải sang trái
                            self.board[i][k] = self.board[i][k + 1]
                        self.board[i][self.n - 1] = -1  # Đánh dấu ô cuối cùng là trống

            # Bước 3: Đặt lại các phần tử đã "nhấc" vào các ô trống
            for i in range(self.m):
                for j in range(self.n):
                    if self.board[i][j] == -1 and lifted_elements:
                        self.board[i][j] = lifted_elements.pop(0)

            self.selected_pattern = None
            self.original_pattern_pos = None
            self.current_pattern_pos = None



    def update_dragging(self, pos):
        """Cập nhật vị trí của pattern đang kéo."""
        if self.selected_pattern:
            offset_x = pos[0] - self.original_pattern_pos[0]
            offset_y = pos[1] - self.original_pattern_pos[1]
            self.current_pattern_pos = (self.original_pattern_pos[0] + offset_x, self.original_pattern_pos[1] + offset_y)

    def stop_dragging(self, pos):
        """Dừng kéo và xử lý grid."""
        if self.selected_pattern:
            self.process_grid(pos)
            self.selected_pattern = None
            self.original_pattern_pos = None
            self.current_pattern_pos = None

class Pattern:
    def __init__(self, p, q, cell_size):
        self.p = p  # Số dòng
        self.q = q  # Số cột
        self.cell_size = cell_size  # Kích thước ô vuông
        self.size = max(p, q) * cell_size  # Kích thước tổng thể của pattern
        self.pattern = np.random.randint(2, size=(p, q))  # Ma trận 2D chứa giá trị 0 hoặc 1

        # Tạo surface để vẽ pattern với độ trong suốt
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.draw(self.surface, 0, 0)  # Vẽ pattern lên surface

    def draw(self, screen, x, y):
        """Vẽ pattern lên màn hình."""
        for i in range(self.p):
            for j in range(self.q):
                rect = pygame.Rect(x + j * self.cell_size, y + i * self.cell_size, self.cell_size, self.cell_size)
                color = (0, 0, 0) if self.pattern[i][j] == 1 else (255, 255, 255)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (150, 150, 150), rect, 1)  # Đường viền

    def draw_transparent(self, screen, x, y):
        """Vẽ pattern lên màn hình với độ trong suốt."""
        alpha_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        for i in range(self.p):
            for j in range(self.q):
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                color = (0, 0, 0) if self.pattern[i][j] == 1 else (255, 255, 255)
                pygame.draw.rect(alpha_surface, color, rect)
                pygame.draw.rect(alpha_surface, (150, 150, 150), rect, 1)  # Đường viền
        alpha_surface.set_alpha(128)  # Thiết lập độ trong suốt (0-255, 0 là trong suốt hoàn toàn, 255 là không trong suốt)
        screen.blit(alpha_surface, (x, y))

def main():
    # Khởi tạo lưới (Grid)
    m, n = 32, 32  # Kích thước bảng
    cell_size = 20  # Kích thước ô vuông
    grid = Grid(m, n, cell_size)

    # Vòng lặp chính
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # pos[0], pos[1] = pos[1], pos[0]
                if grid.selected_pattern:
                    grid.stop_dragging(pos)
                else:
                    grid.check_pattern_click(pos)
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                grid.update_dragging(pos)

        grid.screen.fill((0, 0, 0))  # Xóa màn hình với màu đen
        grid.draw()  # Vẽ bảng và các pattern
        pygame.display.flip()  # Cập nhật màn hình

    pygame.quit()

if __name__ == "__main__":
    main()
