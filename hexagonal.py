import pygame
import sys
import math

# Импортируем твои цвета из хелпера
from src.helper import Colors

# ----------------------------------------------------------------------
# Класс доски (с добавленными методами для работы с мышью)
# ----------------------------------------------------------------------
class Board:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.SIDE = 30
        self.BACKGROUND = (30, 30, 30)
        
        # --- ИЗМЕНЕННЫЕ ЦВЕТА ---
        # Доска из трех цветов
        self.COLORS = [Colors.DARK, Colors.MIDDLE, Colors.LIGHT]
        self.LINE_COLOR = Colors.BLACK
        
        # Цвета фигур (добавлен оранжевый по твоему запросу)
        self.PLAYER_COLORS = {
            'white': Colors.WHITE, 
            'black': Colors.BLACK,
            'orange': Colors.ORANGE
        }
        # ------------------------
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Гексагональные шахматы")
        self.clock = pygame.time.Clock()
        
        self.SQRT3 = math.sqrt(3)
        self.ANGLES = [i * math.pi / 3 for i in range(6)]
        
        # Генерация гексов
        self.hexes = []
        for x in range(-5, 6):
            for y in range(-5, 6):
                z = -x - y
                if abs(z) <= 5:
                    self.hexes.append((x, y, z))
        
        # Смещение центра
        self.offset_x = self.WIDTH // 2
        self.offset_y = self.HEIGHT // 2

        # Список фигур (будет заполнен позже)
        self.pieces = []

    def cube_to_pixel(self, x, y, z):
        q = x
        r = z
        px = self.SIDE * 1.5 * q + self.offset_x
        py = self.SIDE * self.SQRT3 * (r + q / 2.0) + self.offset_y
        return int(px), int(py)

    def pixel_to_cube(self, px, py):
        """Преобразует экранные координаты в дробные кубические координаты."""
        x = (px - self.offset_x) / (self.SIDE * 1.5)
        z = (py - self.offset_y) / (self.SIDE * self.SQRT3) - x / 2.0
        y = -x - z
        return x, y, z

    def cube_round(self, x, y, z):
        """Округление дробных кубических координат до ближайшего целого гекса."""
        rx = round(x)
        ry = round(y)
        rz = round(z)

        x_diff = abs(rx - x)
        y_diff = abs(ry - y)
        z_diff = abs(rz - z)

        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry - rz
        elif y_diff > z_diff:
            ry = -rx - rz
        else:
            rz = -rx - ry
        return int(rx), int(ry), int(rz)

    def get_hex_at(self, px, py):
        """Возвращает координаты (x,y,z) гекса под точкой (px,py) или None."""
        fx, fy, fz = self.pixel_to_cube(px, py)
        x, y, z = self.cube_round(fx, fy, fz)
        if (x, y, z) in self.hexes:
            return (x, y, z)
        return None

    def get_piece_at(self, x, y, z):
        """Возвращает фигуру на указанных координатах или None."""
        for p in self.pieces:
            if p.x == x and p.y == y and p.z == z:
                return p
        return None

    def draw_hex(self, surface, x, y, z, color):
        cx, cy = self.cube_to_pixel(x, y, z)
        vertices = []
        for angle in self.ANGLES:
            vx = cx + self.SIDE * math.cos(angle)
            vy = cy + self.SIDE * math.sin(angle)
            vertices.append((vx, vy))
        pygame.draw.polygon(surface, color, vertices)
        pygame.draw.polygon(surface, self.LINE_COLOR, vertices, 2)

    def draw_piece(self, surface, piece):
        cx, cy = self.cube_to_pixel(piece.x, piece.y, piece.z)
        color = self.PLAYER_COLORS.get(piece.color, Colors.WHITE)
        radius = int(self.SIDE * 0.4)
        pygame.draw.circle(surface, color, (cx, cy), radius)
        pygame.draw.circle(surface, self.LINE_COLOR, (cx, cy), radius, 2)
        font = pygame.font.Font(None, int(radius * 1.5))
        
        # Текст на фигуре адаптируется под ее цвет
        text_color = Colors.WHITE if piece.color in ['black', 'orange'] else self.LINE_COLOR
        text = font.render(piece.symbol, True, text_color)
        text_rect = text.get_rect(center=(cx, cy))
        surface.blit(text, text_rect)

    def draw_highlight(self, surface, x, y, z, color=(255, 255, 0, 80)):
        """Рисует полупрозрачный круг для подсветки возможного хода."""
        cx, cy = self.cube_to_pixel(x, y, z)
        s = pygame.Surface((self.SIDE*2, self.SIDE*2), pygame.SRCALPHA)
        pygame.draw.circle(s, color[:3] + (80,), (self.SIDE, self.SIDE), int(self.SIDE*0.3))
        surface.blit(s, (cx - self.SIDE, cy - self.SIDE))


# ----------------------------------------------------------------------
# Базовый класс фигуры
# ----------------------------------------------------------------------
class Piece:
    def __init__(self, color, x, y, z, symbol):
        self.color = color      # 'white', 'black' или 'orange'
        self.x = x
        self.y = y
        self.z = z
        self.symbol = symbol    # буква для отображения ('P','N','B','R','Q','K')

    def get_moves(self, board):
        """Возвращает список допустимых ходов (переопределяется в наследниках)."""
        return []

    def __repr__(self):
        return f"{self.color[0]}{self.symbol}"


# ----------------------------------------------------------------------
# Конкретные классы фигур с реализацией логики ходов
# ----------------------------------------------------------------------
class Pawn(Piece):
    def __init__(self, color, x, y, z):
        super().__init__(color, x, y, z, 'P')
        self.has_moved = False   # для первого хода на две клетки

    def get_moves(self, board):
        moves = []
        if self.color == 'white':
            forward = (0, 1, -1)
            captures = [(-1, 2, -1), (1, 1, -2)]  # диагональные взятия
        else:  # black или orange
            forward = (0, -1, 1)
            captures = [(1, -2, 1), (-1, -1, 2)]

        # Ход на одну клетку вперёд
        nx, ny, nz = self.x + forward[0], self.y + forward[1], self.z + forward[2]
        if (nx, ny, nz) in board.hexes and board.get_piece_at(nx, ny, nz) is None:
            moves.append((nx, ny, nz))
            # Ход на две клетки, если пешка ещё не двигалась
            if not self.has_moved:
                nx2, ny2, nz2 = self.x + 2*forward[0], self.y + 2*forward[1], self.z + 2*forward[2]
                if (nx2, ny2, nz2) in board.hexes and board.get_piece_at(nx2, ny2, nz2) is None:
                    moves.append((nx2, ny2, nz2))

        # Взятия по диагонали
        for dx, dy, dz in captures:
            nx, ny, nz = self.x + dx, self.y + dy, self.z + dz
            if (nx, ny, nz) in board.hexes:
                p = board.get_piece_at(nx, ny, nz)
                if p and p.color != self.color:
                    moves.append((nx, ny, nz))
        return moves


class Knight(Piece):
    def __init__(self, color, x, y, z):
        super().__init__(color, x, y, z, 'N')

    def get_moves(self, board):
        moves = []
        # Все 12 ходов коня (комбинации 1,2,-3)
        knight_dirs = [
            (1,2,-3), (1,-3,2), (2,1,-3), (2,-3,1), (-3,1,2), (-3,2,1),
            (-1,-2,3), (-1,3,-2), (-2,-1,3), (-2,3,-1), (3,-1,-2), (3,-2,-1)
        ]
        for dx, dy, dz in knight_dirs:
            nx, ny, nz = self.x + dx, self.y + dy, self.z + dz
            if (nx, ny, nz) in board.hexes:
                p = board.get_piece_at(nx, ny, nz)
                if p is None or p.color != self.color:
                    moves.append((nx, ny, nz))
        return moves


class Bishop(Piece):
    def __init__(self, color, x, y, z):
        super().__init__(color, x, y, z, 'B')

    def get_moves(self, board):
        moves = []
        # Диагональные направления (сохраняют цвет клетки)
        diag_dirs = [
            (2,-1,-1), (-2,1,1),
            (-1,2,-1), (1,-2,1),
            (-1,-1,2), (1,1,-2)
        ]
        for dx, dy, dz in diag_dirs:
            step = 1
            while True:
                nx, ny, nz = self.x + step*dx, self.y + step*dy, self.z + step*dz
                if (nx, ny, nz) not in board.hexes:
                    break
                p = board.get_piece_at(nx, ny, nz)
                if p is None:
                    moves.append((nx, ny, nz))
                    step += 1
                elif p.color != self.color:
                    moves.append((nx, ny, nz))
                    break
                else:
                    break
        return moves


class Rook(Piece):
    def __init__(self, color, x, y, z):
        super().__init__(color, x, y, z, 'R')

    def get_moves(self, board):
        moves = []
        # Ортогональные направления (прямые)
        orth_dirs = [
            (1,-1,0), (-1,1,0),
            (1,0,-1), (-1,0,1),
            (0,1,-1), (0,-1,1)
        ]
        for dx, dy, dz in orth_dirs:
            step = 1
            while True:
                nx, ny, nz = self.x + step*dx, self.y + step*dy, self.z + step*dz
                if (nx, ny, nz) not in board.hexes:
                    break
                p = board.get_piece_at(nx, ny, nz)
                if p is None:
                    moves.append((nx, ny, nz))
                    step += 1
                elif p.color != self.color:
                    moves.append((nx, ny, nz))
                    break
                else:
                    break
        return moves


class Queen(Piece):
    def __init__(self, color, x, y, z):
        super().__init__(color, x, y, z, 'Q')

    def get_moves(self, board):
        moves = []
        # Все 12 направлений (ортогональные + диагональные)
        all_dirs = [
            (1,-1,0), (-1,1,0),
            (1,0,-1), (-1,0,1),
            (0,1,-1), (0,-1,1),
            (2,-1,-1), (-2,1,1),
            (-1,2,-1), (1,-2,1),
            (-1,-1,2), (1,1,-2)
        ]
        for dx, dy, dz in all_dirs:
            step = 1
            while True:
                nx, ny, nz = self.x + step*dx, self.y + step*dy, self.z + step*dz
                if (nx, ny, nz) not in board.hexes:
                    break
                p = board.get_piece_at(nx, ny, nz)
                if p is None:
                    moves.append((nx, ny, nz))
                    step += 1
                elif p.color != self.color:
                    moves.append((nx, ny, nz))
                    break
                else:
                    break
        return moves


class King(Piece):
    def __init__(self, color, x, y, z):
        super().__init__(color, x, y, z, 'K')

    def get_moves(self, board):
        moves = []
        # Все 6 соседних клеток (ортогональные направления)
        orth_dirs = [
            (1,-1,0), (-1,1,0),
            (1,0,-1), (-1,0,1),
            (0,1,-1), (0,-1,1)
        ]
        for dx, dy, dz in orth_dirs:
            nx, ny, nz = self.x + dx, self.y + dy, self.z + dz
            if (nx, ny, nz) in board.hexes:
                p = board.get_piece_at(nx, ny, nz)
                if p is None or p.color != self.color:
                    moves.append((nx, ny, nz))
        return moves


# ----------------------------------------------------------------------
# Начальная расстановка (без изменений)
# ----------------------------------------------------------------------
def create_initial_pieces():
    white_data = [
        (0, -5, 5, 'B'), (0, -4, 4, 'B'), (0, -3, 3, 'B'),
        (1, -5, 4, 'K'), (2, -5, 3, 'N'), (3, -5, 2, 'R'), (4, -5, 1, 'P'),
        (-1, -4, 5, 'Q'), (-2, -3, 5, 'N'), (-3, -2, 5, 'R'), (-4, -1, 5, 'P'),
        (3, -4, 1, 'P'), (-3, -1, 4, 'P'),
        (2, -3, 1, 'P'), (-2, -1, 3, 'P'),
        (1, -2, 1, 'P'), (-1, -1, 2, 'P'),
        (0, -1, 1, 'P')
    ]

    pieces = []
    # Белые фигуры
    for x, y, z, sym in white_data:
        if sym == 'P':
            pieces.append(Pawn('white', x, y, z))
        elif sym == 'N':
            pieces.append(Knight('white', x, y, z))
        elif sym == 'B':
            pieces.append(Bishop('white', x, y, z))
        elif sym == 'R':
            pieces.append(Rook('white', x, y, z))
        elif sym == 'Q':
            pieces.append(Queen('white', x, y, z))
        elif sym == 'K':
            pieces.append(King('white', x, y, z))

    # Чёрные фигуры (симметричное отражение)
    for x, y, z, sym in white_data:
        if sym == 'P':
            pieces.append(Pawn('black', -x, -y, -z))
        elif sym == 'N':
            pieces.append(Knight('black', -x, -y, -z))
        elif sym == 'B':
            pieces.append(Bishop('black', -x, -y, -z))
        elif sym == 'R':
            pieces.append(Rook('black', -x, -y, -z))
        elif sym == 'Q':
            pieces.append(Queen('black', -x, -y, -z))
        elif sym == 'K':
            pieces.append(King('black', -x, -y, -z))

    return pieces


# ----------------------------------------------------------------------
# Главная функция с игровым циклом
# ----------------------------------------------------------------------
def main():
    board = Board()
    pieces = create_initial_pieces()
    board.pieces = pieces   # необходимо для работы get_piece_at

    # Переменные состояния игры
    selected_piece = None
    possible_moves = []
    turn = 'white'

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                hex_coord = board.get_hex_at(mx, my)
                if hex_coord is None:
                    # Клик вне доски — сбрасываем выделение
                    selected_piece = None
                    possible_moves = []
                    continue

                hx, hy, hz = hex_coord
                piece_here = board.get_piece_at(hx, hy, hz)

                if selected_piece and (hx, hy, hz) in possible_moves:
                    # --- Выполняем ход ---
                    # Удаляем взятую фигуру, если есть
                    if piece_here:
                        board.pieces.remove(piece_here)
                    # Обновляем координаты выбранной фигуры
                    selected_piece.x, selected_piece.y, selected_piece.z = hx, hy, hz
                    # Если это пешка, отмечаем, что она двигалась
                    if isinstance(selected_piece, Pawn):
                        selected_piece.has_moved = True
                    # Сбрасываем выделение
                    selected_piece = None
                    possible_moves = []
                    # Меняем игрока
                    turn = 'black' if turn == 'white' else 'white'
                else:
                    # Если кликнули на свою фигуру согласно очереди — выбираем её
                    if piece_here and piece_here.color == turn:
                        selected_piece = piece_here
                        possible_moves = piece_here.get_moves(board)
                    else:
                        # Иначе сбрасываем выделение
                        selected_piece = None
                        possible_moves = []

        # Отрисовка
        board.screen.fill(board.BACKGROUND)

        # Рисуем гексы
        for x, y, z in board.hexes:
            color_index = (x + 2 * y) % 3
            board.draw_hex(board.screen, x, y, z, board.COLORS[color_index])

        # Подсвечиваем возможные ходы
        for (mx, my, mz) in possible_moves:
            board.draw_highlight(board.screen, mx, my, mz, (0, 0, 0))

        # Рисуем фигуры
        for piece in pieces:
            board.draw_piece(board.screen, piece)

        # Обновляем заголовок окна с текущим игроком
        pygame.display.set_caption(f"Гексагональные шахматы - Ход: {'Белые' if turn == 'white' else 'Чёрные'}")

        pygame.display.flip()
        board.clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()