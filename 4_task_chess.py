import pygame
import sys
import math

# Константы цветов для доски
BOARD_DARK = (123, 108, 85)    # #7b6c55
BOARD_MIDDLE = (162, 131, 85)  # #a28355
BOARD_LIGHT = (216, 185, 132)   # #d8b984

# ----------------------------------------------------------------------
# Классы фигур
# ----------------------------------------------------------------------
class Piece:
    def __init__(self, color, x, y, z, symbol):
        self.color = color      
        self.x = x
        self.y = y
        self.z = z
        self.symbol = symbol    
        self.has_moved = False  # Флаг для первого хода пешки (и рокировки в будущем)

    def get_moves(self, board, occupied):
        return []

class Pawn(Piece):
    def __init__(self, color, x, y, z):
        super().__init__(color, x, y, z, 'P')

    def get_moves(self, board, occupied):
        moves = []
        forward_map = {
            'white': (1, 0, -1),
            'black': (0, -1, 1),
            'orange': (-1, 1, 0)
        }
        capture_map = {
            'white': [(1, -1, 0), (0, 1, -1)],
            'black': [(-1, 0, 1), (1, -1, 0)],
            'orange': [(0, 1, -1), (-1, 0, 1)]
        }
        
        fdx, fdy, fdz = forward_map[self.color]
        
        # 1. Ход на одну клетку вперёд
        nx, ny, nz = self.x + fdx, self.y + fdy, self.z + fdz
        if board.is_on_board(nx, ny, nz) and (nx, ny, nz) not in occupied:
            moves.append((nx, ny, nz))
            
            # 2. Ход на две клетки вперёд (только если первый ход и первая клетка была пуста)
            if not self.has_moved:
                nx2, ny2, nz2 = self.x + 2*fdx, self.y + 2*fdy, self.z + 2*fdz
                if board.is_on_board(nx2, ny2, nz2) and (nx2, ny2, nz2) not in occupied:
                    moves.append((nx2, ny2, nz2))

        # 3. Взятие фигуры противника
        for cdx, cdy, cdz in capture_map[self.color]:
            nx, ny, nz = self.x + cdx, self.y + cdy, self.z + cdz
            if board.is_on_board(nx, ny, nz):
                if (nx, ny, nz) in occupied and occupied[(nx, ny, nz)].color != self.color:
                    moves.append((nx, ny, nz))
        return moves

class Knight(Piece):
    def __init__(self, color, x, y, z):
        super().__init__(color, x, y, z, 'N')
    def get_moves(self, board, occupied):
        moves = []
        knight_dirs = [(3, -2, -1), (2, -3, 1), (3, -1, -2), (2, 1, -3), (1, 2, -3), (-1, 3, -2), 
                       (-2, 3, -1), (-3, 2, 1), (-3, 1, 2), (-2, -1, 3), (-1, -2, 3), (1, -3, 2)]
        for dx, dy, dz in knight_dirs:
            nx, ny, nz = self.x + dx, self.y + dy, self.z + dz
            if board.is_on_board(nx, ny, nz):
                if (nx, ny, nz) not in occupied or occupied[(nx, ny, nz)].color != self.color:
                    moves.append((nx, ny, nz))
        return moves

class Bishop(Piece):
    def __init__(self, color, x, y, z):
        super().__init__(color, x, y, z, 'B')
    def get_moves(self, board, occupied):
        moves = []
        directions = [(2, -1, -1), (1, 1, -2), (-1, 2, -1), (-2, 1, 1), (-1, -1, 2), (1, -2, 1)]
        for dx, dy, dz in directions:
            x, y, z = self.x, self.y, self.z
            while True:
                x, y, z = x + dx, y + dy, z + dz
                if not board.is_on_board(x, y, z): break
                if (x, y, z) in occupied:
                    if occupied[(x, y, z)].color != self.color: moves.append((x, y, z))
                    break
                moves.append((x, y, z))
        return moves

class Rook(Piece):
    def __init__(self, color, x, y, z):
        super().__init__(color, x, y, z, 'R')
    def get_moves(self, board, occupied):
        moves = []
        directions = [(1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1), (0, -1, 1)]
        for dx, dy, dz in directions:
            x, y, z = self.x, self.y, self.z
            while True:
                x, y, z = x + dx, y + dy, z + dz
                if not board.is_on_board(x, y, z): break
                if (x, y, z) in occupied:
                    if occupied[(x, y, z)].color != self.color: moves.append((x, y, z))
                    break
                moves.append((x, y, z))
        return moves

class Queen(Piece):
    def __init__(self, color, x, y, z):
        super().__init__(color, x, y, z, 'Q')
    def get_moves(self, board, occupied):
        return Rook.get_moves(self, board, occupied) + Bishop.get_moves(self, board, occupied)

class King(Piece):
    def __init__(self, color, x, y, z):
        super().__init__(color, x, y, z, 'K')
    def get_moves(self, board, occupied):
        moves = []
        directions = [(1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1), (0, -1, 1)]
        for dx, dy, dz in directions:
            nx, ny, nz = self.x + dx, self.y + dy, self.z + dz
            if board.is_on_board(nx, ny, nz):
                if (nx, ny, nz) not in occupied or occupied[(nx, ny, nz)].color != self.color:
                    moves.append((nx, ny, nz))
        return moves

# ----------------------------------------------------------------------
# Доска и Логика
# ----------------------------------------------------------------------
class Board:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1000, 800
        self.BACKGROUND = (35, 35, 35)
        self.COLORS = [BOARD_LIGHT, BOARD_MIDDLE, BOARD_DARK]
        self.PLAYER_COLORS = {'white': (255, 255, 255), 'black': (15, 15, 15), 'orange': (255, 120, 0)}
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.SQRT3 = math.sqrt(3)
        self.ANGLES = [math.pi/2 + i * math.pi/3 for i in range(6)]
        self.hexes = []
        for x in range(-7, 9):
            for y in range(-8, 8):
                z = -x - y
                if -7 <= z <= 8: self.hexes.append((x, y, z))
        self._compute_scale_and_offset()

    def _compute_scale_and_offset(self):
        coords = []
        for (x, y, z) in self.hexes:
            px = self.SQRT3 * (x + z / 2.0)
            py = 1.5 * z
            coords.append((px, py))
        xs, ys = [p[0] for p in coords], [p[1] for p in coords]
        min_x, max_x, min_y, max_y = min(xs), max(xs), min(ys), max(ys)
        self.SIDE = min((self.WIDTH-120)/((max_x-min_x)+2), (self.HEIGHT-120)/((max_y-min_y)+2))
        self.offset_x = self.WIDTH // 2 - (self.SIDE * (min_x + max_x) // 2)
        self.offset_y = self.HEIGHT // 2 - (self.SIDE * (min_y + max_y) // 2)

    def is_on_board(self, x, y, z): return (x, y, z) in self.hexes
    def cube_to_pixel(self, x, y, z):
        px = self.SIDE * self.SQRT3 * (x + z / 2.0) + self.offset_x
        py = self.SIDE * 1.5 * z + self.offset_y
        return int(px), int(py)

    def get_hex_at(self, screen_x, screen_y):
        best_hex, min_dist = None, float('inf')
        for (x, y, z) in self.hexes:
            cx, cy = self.cube_to_pixel(x, y, z)
            dist = math.hypot(screen_x - cx, screen_y - cy)
            if dist < self.SIDE and dist < min_dist: min_dist, best_hex = dist, (x, y, z)
        return best_hex

    def draw_hex(self, surface, x, y, z, color):
        cx, cy = self.cube_to_pixel(x, y, z)
        vertices = [(cx + self.SIDE * math.cos(a), cy + self.SIDE * math.sin(a)) for a in self.ANGLES]
        pygame.draw.polygon(surface, color, vertices)
        pygame.draw.polygon(surface, (40, 40, 40), vertices, 1)

    def draw_piece(self, surface, piece):
        cx, cy = self.cube_to_pixel(piece.x, piece.y, piece.z)
        color = self.PLAYER_COLORS[piece.color]
        radius = int(self.SIDE * 0.55)
        if piece.color == 'black':
            pygame.draw.circle(surface, (50, 50, 50), (cx, cy), radius)
            txt_c = (255, 255, 255)
        else:
            pygame.draw.circle(surface, color, (cx, cy), radius)
            txt_c = (0, 0, 0)
        pygame.draw.circle(surface, (0, 0, 0), (cx, cy), radius, 2)
        font = pygame.font.Font(None, int(radius * 1.5))
        text = font.render(piece.symbol, True, txt_c)
        surface.blit(text, text.get_rect(center=(cx, cy)))

def create_initial_pieces(board):
    pieces = []
    figs = [Rook, Bishop, Knight, Queen, King, Knight, Bishop, Rook]
    # White
    z_max = 8
    row1 = sorted([h for h in board.hexes if h[2] == z_max], key=lambda h: h[0])
    for i, h in enumerate(row1): pieces.append(figs[i]('white', *h))
    row2 = sorted([h for h in board.hexes if h[2] == z_max-1], key=lambda h: h[0])
    for i, h in enumerate(row2):
        if i == len(row2)//2: pieces.append(Bishop('white', *h))
        else: pieces.append(Pawn('white', *h))
    row3 = sorted([h for h in board.hexes if h[2] == z_max-2], key=lambda h: h[0])
    for i, h in enumerate(row3):
        if 0 < i < len(row3)-1: pieces.append(Pawn('white', *h))
    # Black
    y_max = 7
    row1 = sorted([h for h in board.hexes if h[1] == y_max], key=lambda h: h[0])
    for i, h in enumerate(row1): pieces.append(figs[i]('black', *h))
    row2 = sorted([h for h in board.hexes if h[1] == y_max-1], key=lambda h: h[0])
    for i, h in enumerate(row2):
        if i == len(row2)//2: pieces.append(Bishop('black', *h))
        else: pieces.append(Pawn('black', *h))
    row3 = sorted([h for h in board.hexes if h[1] == y_max-2], key=lambda h: h[0])
    for i, h in enumerate(row3):
        if 0 < i < len(row3)-1: pieces.append(Pawn('black', *h))
    # Orange
    x_max = 8
    row1 = sorted([h for h in board.hexes if h[0] == x_max], key=lambda h: -h[1])
    for i, h in enumerate(row1): pieces.append(figs[i]('orange', *h))
    row2 = sorted([h for h in board.hexes if h[0] == x_max-1], key=lambda h: -h[1])
    for i, h in enumerate(row2):
        if i == len(row2)//2: pieces.append(Bishop('orange', *h))
        else: pieces.append(Pawn('orange', *h))
    row3 = sorted([h for h in board.hexes if h[0] == x_max-2], key=lambda h: -h[1])
    for i, h in enumerate(row3):
        if 0 < i < len(row3)-1: pieces.append(Pawn('orange', *h))
    return pieces

def main():
    board = Board()
    pieces = create_initial_pieces(board)
    occupied = {(p.x, p.y, p.z): p for p in pieces}
    current_player, selected_piece, possible_moves = 'white', None, []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                coord = board.get_hex_at(*pygame.mouse.get_pos())
                if coord:
                    if selected_piece and coord in possible_moves:
                        if coord in occupied: pieces.remove(occupied[coord])
                        del occupied[(selected_piece.x, selected_piece.y, selected_piece.z)]
                        selected_piece.x, selected_piece.y, selected_piece.z = coord
                        
                        # КЛЮЧЕВОЙ МОМЕНТ: фиксируем, что фигура сделала ход
                        selected_piece.has_moved = True
                        
                        occupied[coord] = selected_piece
                        selected_piece, possible_moves = None, []
                        current_player = {'white':'black', 'black':'orange', 'orange':'white'}[current_player]
                    elif coord in occupied and occupied[coord].color == current_player:
                        selected_piece = occupied[coord]
                        possible_moves = selected_piece.get_moves(board, occupied)
                    else: selected_piece, possible_moves = None, []

        board.screen.fill(board.BACKGROUND)
        for x, y, z in board.hexes:
            board.draw_hex(board.screen, x, y, z, board.COLORS[(x - y) % 3])
        for m in possible_moves:
            cx, cy = board.cube_to_pixel(*m)
            pygame.draw.circle(board.screen, (255, 255, 0), (cx, cy), int(board.SIDE*0.3), 3)
        if selected_piece:
            cx, cy = board.cube_to_pixel(selected_piece.x, selected_piece.y, selected_piece.z)
            pygame.draw.circle(board.screen, (0, 255, 255), (cx, cy), int(board.SIDE*0.6), 2)
        for p in pieces: board.draw_piece(board.screen, p)
        
        # Инфо-панель
        font = pygame.font.Font(None, 40)
        txt_col = board.PLAYER_COLORS[current_player] if current_player != 'black' else (200, 200, 200)
        label = font.render(f"TURN: {current_player.upper()}", True, txt_col)
        board.screen.blit(label, (20, 20))
        
        pygame.display.flip()
        board.clock.tick(60)

if __name__ == "__main__": main()