
###


# ###
import pygame
import random
import numpy as np
from pattern import Pattern
class Grid:
    def __init__(self, m, n, cell_size = 20, cnt=None, render = None, board = None, patterns = None):
        self.cnt = [0, 0, 0, 0]
        self.m = m  # Số dòng
        self.n = n  # Số cột
        self.cell_size = cell_size  # Kích thước ô vuông
        self.grid_margin = 50  # Khoảng trống thêm bên trái grid
        self.top_margin = 50
        self.width = n * cell_size + self.grid_margin  # Chiều rộng cửa sổ
        self.height = m * cell_size + 2 *self.top_margin # Chiều cao cửa sổ
        self.board = np.zeros((m, n), dtype=int)  # Bảng 2D chứa các giá trị từ 0 đến 3
        self.colors = {
            0: (255, 255, 255),  # Trắng
            1: (255, 0, 0),      # Đỏ
            2: (0, 255, 0),      # Xanh lá
            3: (0, 0, 255)       # Xanh dương
        }
        if board is not None:
            self.board = board
        elif cnt is None:
            self.fill_board_random()  # Gán giá trị cho bảng
        else:
            self.fill_board(cnt)
        self.hovered_cell = None

        # Tạo các pattern
        self.patterns = [Pattern(1,1,cell_size,1, render)]
        for sz in range(1,9):
            size = 2**sz
            for _ in range(3):
                self.patterns.append(Pattern(size,size,cell_size,_, render))
        if patterns is not None:
            for pattern in patterns:
                self.patterns.append(pattern)
        #sort the patterns by pattern.m
        self.patterns = sorted(self.patterns, key = lambda x: x.size)
        
        self.patterns_3x3 = [Pattern(3, 3, cell_size,_, render) for _ in range(3)]  # Tạo 3 pattern 3x3 ngẫu nhiên
        self.patterns_2x2 = [Pattern(2, 2, cell_size,_, render) for _ in range(3)]  # Tạo 2 pattern 2x2 ngẫu nhiên
        self.selected_pattern = None  # Pattern được chọn
        self.original_pattern_pos = None  # Vị trí gốc của pattern
        self.current_pattern_pos = None  # Vị trí hiện tại của pattern
        self.is_selecting_direction = False  # Trạng thái chọn hướng
        self.direction_buttons = []  # Các nút chọn hướng
        self.cur_x = -1 # Vị trí x của ô được chọn
        self.cur_y = -1 # Vị trí y của ô được chọn
        if render is not None:
            self.font = pygame.font.SysFont(None, 18)  # Font chữ để hiển thị số
            self.screen = pygame.display.set_mode((self.width + 300, self.height))  # Tạo cửa sổ, +300 cho phần giao diện pattern

    
    def fill_board_random(self):
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
                self.cnt[value] += 1

        for idx in remaining_cells:
            y, x = divmod(idx, self.n)
            cur = random.choice(values)
            self.board[y][x] = cur
            self.cnt[cur] += 1
    

    def fill_board(self, cnt):
        """Gán số lượng cụ thể của các giá trị 0, 1, 2, 3 vào các ô trong bảng, đảm bảo số lượng mỗi giá trị như yêu cầu."""
        num_cells = self.m * self.n
        total_cnt = sum(cnt)
        
        if total_cnt != num_cells:
            raise ValueError("Tổng số lượng các giá trị không khớp với kích thước của bảng.")
        
        values = [0, 1, 2, 3]
        counts = dict(zip(values, cnt))
        remaining_cells = list(range(num_cells))
        
        # Gán các giá trị vào các ô trong bảng theo số lượng yêu cầu
        for value in values:
            for _ in range(counts[value]):
                idx = random.choice(remaining_cells)
                y, x = divmod(idx, self.n)
                self.board[y][x] = value
                remaining_cells.remove(idx)

        


    def create_direction_buttons(self):
        """Tạo các nút chọn hướng ở góc dưới cùng bên phải của cửa sổ."""
        button_size = self.cell_size
        self.direction_buttons = [
            {"rect": pygame.Rect(self.width + 250 - button_size - 10, self.height - button_size - 50 - button_size, button_size, button_size), "direction": "up"},
            {"rect": pygame.Rect(self.width + 250 - button_size - 10 + button_size, self.height - button_size - 50, button_size, button_size), "direction": "right"},
            {"rect": pygame.Rect(self.width + 250 - button_size - 10, self.height - button_size - 50 + button_size, button_size, button_size), "direction": "down"},
            {"rect": pygame.Rect(self.width + 250 - button_size - 10 - button_size, self.height - button_size - 50, button_size, button_size), "direction": "left"},
        ]

    def draw_direction_buttons(self):
        """Vẽ các nút chọn hướng lên màn hình."""
        for button in self.direction_buttons:
            pygame.draw.rect(self.screen, (255, 255, 0), button["rect"])
            text = self.font.render(button["direction"][0].upper(), True, (0, 0, 0))
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)

    def handle_direction_selection(self, pos):
        """Xử lý việc chọn hướng."""
        for button in self.direction_buttons:
            if button["rect"].collidepoint(pos):
                self.apply_shift(button["direction"])
                break
        self.is_selecting_direction = False

    def draw(self):
        """Vẽ bảng lên màn hình."""
        # Vẽ grid
        for y in range(self.m):
            for x in range(self.n):
                if self.hovered_cell and (x, y) == self.hovered_cell:
                    color = (200, 200, 200)  # Màu xám
                else:
                    color = self.colors[self.board[y][x]]
                rect = pygame.Rect(self.grid_margin + x * self.cell_size,self.top_margin + y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)

                # Hiển thị số trên ô vuông
                text = self.font.render(str(self.board[y][x]), True, (0, 0, 0))  # Màu chữ là đen
                text_rect = text.get_rect(center=(self.grid_margin + x * self.cell_size + self.cell_size // 2, self.top_margin +  y * self.cell_size + self.cell_size // 2))
                self.screen.blit(text, text_rect)

        # Vẽ 3 pattern ngẫu nhiên
        for i, pattern in enumerate(self.patterns_3x3):
            pattern_x = self.width + self.grid_margin + 2
            pattern_y = i * (pattern.size + 10) + 10
            pattern.draw(self.screen, pattern_x, pattern_y)

        # Vẽ 2 pattern ngẫu nhiên
        for i, pattern in enumerate(self.patterns_2x2):
            pattern_x = self.width + self.grid_margin + 2 + 3 * (self.patterns_3x3[0].size + 10)
            pattern_y = i * (pattern.size + 10) + 10
            pattern.draw(self.screen, pattern_x, pattern_y)

        # Vẽ pattern đang được kéo, nếu có
        if self.selected_pattern:
            x, y = self.current_pattern_pos
            self.selected_pattern.draw_transparent(self.screen, x, y)

        # Vẽ các nút chọn hướng nếu đang trong quá trình chọn hướng
        if self.is_selecting_direction:
            self.create_direction_buttons()
            self.draw_direction_buttons()

    def update_hovered_cell(self, pos):
        """Cập nhật vị trí ô đang được hover."""
        grid_x = (pos[0] - self.grid_margin) // self.cell_size
        grid_y = (pos[1] - self.top_margin) // self.cell_size

        # Kiểm tra xem vị trí có hợp lệ không
        if 0 <= grid_x < self.n and 0 <= grid_y < self.m:
            self.hovered_cell = (grid_x, grid_y)
        else:
            self.hovered_cell = None

    def check_pattern_click(self, pos):
        """Kiểm tra xem người dùng có click vào pattern nào không."""
        for i, pattern in enumerate(self.patterns_3x3):
            pattern_x = self.width + self.grid_margin + 2
            pattern_y = i * (pattern.size + 10) + 10
            if pattern_x <= pos[0] <= pattern_x + pattern.size and pattern_y <= pos[1] <= pattern_y + pattern.size:
                rel_x = (pos[0] - pattern_x) // pattern.cell_size
                rel_y = (pos[1] - pattern_y) // pattern.cell_size
                if 0 <= rel_x < pattern.q and 0 <= rel_y < pattern.p:
                    self.selected_pattern = pattern
                    self.original_pattern_pos = (pattern_x, pattern_y)
                    self.current_pattern_pos = (pos[0] - pattern.cell_size * rel_x, pos[1] - pattern.cell_size * rel_y)
                    pattern.top = (pattern_x, pattern_y)
                    pattern.bottom = (pattern_x + pattern.size, pattern_y + pattern.size)
                    return

        for i, pattern in enumerate(self.patterns_2x2):
            pattern_x = self.width + self.grid_margin + 2 + 3 * (self.patterns_3x3[0].size + 10)
            pattern_y = i * (pattern.size + 10) + 10
            if pattern_x <= pos[0] <= pattern_x + pattern.size and pattern_y <= pos[1] <= pattern_y + pattern.size:
                rel_x = (pos[0] - pattern_x) // pattern.cell_size
                rel_y = (pos[1] - pattern_y) // pattern.cell_size
                if 0 <= rel_x < pattern.q and 0 <= rel_y < pattern.p:
                    self.selected_pattern = pattern
                    self.original_pattern_pos = (pattern_x, pattern_y)
                    self.current_pattern_pos = (pos[0] - pattern.cell_size * rel_x, pos[1] - pattern.cell_size * rel_y)
                    pattern.top = (pattern_x, pattern_y)
                    pattern.bottom = (pattern_x + pattern.size, pattern_y + pattern.size)
                    return

        print(None)


    def process_grid(self, pos):
        """Xử lý grid khi pattern được thả vào và cho phép chọn hướng."""
        if self.selected_pattern:
            # print("Vị trí click lưu lại:", pos)
            grid_x = (pos[0] - self.grid_margin) // self.cell_size 
            grid_y = (pos[1] - self.top_margin) // self.cell_size
            print("grid_x: ", grid_x)
            print("grid_y: ", grid_y)
            # if grid_x > self.m or grid_y > self.n:
            #     print("ERROR: Out of grid")
            #     return
            self.cur_x = grid_x
            self.cur_y = grid_y
            self.is_selecting_direction = True
            self.create_direction_buttons()

    def apply_shift(self, direction, inplace  = True):
        """Áp dụng phép dịch pattern vào grid."""
        grid_x, grid_y = self.cur_x, self.cur_y
        pattern_p = self.selected_pattern.p
        pattern_q = self.selected_pattern.q
        lifted_elements = []
        cur_board = self.board.copy()
        # Bước 1: Đặt pattern P lên bảng B và "nhấc" các phần tử trong B tương ứng với phần tử 1 trong P
        for i in range(pattern_p):  
            for j in range(pattern_q):
                if self.selected_pattern.pattern[i][j] == 1:
                    if 0 <= grid_y + i < self.m and 0 <= grid_x + j < self.n:
                        lifted_elements.append(cur_board[grid_y + i][grid_x + j])
                        cur_board[grid_y + i][grid_x + j] = -1  # Sử dụng giá trị đặc biệt để chỉ định ô trống

        # Bước 2: Dịch các phần tử còn lại theo hướng đã chọn
        if direction == 'right' or direction == 2:
            for i in range(self.m):
                for j in range(self.n - 1, -1, -1):
                    if cur_board[i][j] == -1:
                        for k in range(j, self.n - 1):
                            cur_board[i][k] = cur_board[i][k + 1]
                        cur_board[i][self.n - 1] = -1

        elif direction == 'left' or direction == 3:
            for i in range(self.m):
                for j in range(self.n):
                    if cur_board[i][j] == -1:
                        for k in range(j, 0, -1):
                            cur_board[i][k] = cur_board[i][k - 1]
                        cur_board[i][0] = -1

        elif direction == 'down' or direction == 0:
            for j in range(self.n):
                for i in range(self.m - 1, -1, -1):
                    if cur_board[i][j] == -1:
                        for k in range(i, self.m - 1):
                            cur_board[k][j] = cur_board[k + 1][j]
                        cur_board[self.m - 1][j] = -1

        elif direction == 'up' or direction == 1:
            for j in range(self.n):
                for i in range(self.m):
                    if cur_board[i][j] == -1:
                        for k in range(i, 0, -1):
                            cur_board[k][j] = cur_board[k - 1][j]
                        cur_board[0][j] = -1

        # Bước 3: Đặt lại các phần tử đã "nhấc" vào các ô trống
        for i in range(self.m):
            for j in range(self.n):
                if cur_board[i][j] == -1 and lifted_elements:
                    cur_board[i][j] = lifted_elements.pop(0)
        #reset
        self.selected_pattern = None
        self.original_pattern_pos = None
        self.current_pattern_pos = None
        if inplace:
            self.board = cur_board
        return cur_board


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
            

