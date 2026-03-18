import pygame
import sys
import math


from src.helper import Colors

class Board:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.SIDE = 30
        self.BACKGROUND = (30, 30, 30)
        
        self.COLORS = [Colors.DARK, Colors.MIDDLE, Colors.LIGHT]
        self.LINE_COLOR = Colors.BLACK
        self.PLAYER_COLORS = {
            'white': Colors.WHITE, 
            'black': Colors.BLACK,
            'orange': Colors.ORANGE
        }

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Гексагональные шахматы")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.SQRT3 = math.sqrt(3)
        self.ANGLES = [i * math.pi / 3 for i in range(6)]
        
        self.hexes = []
        for x in range(-5, 6):
            for y in range(-5, 6):
                z = -x - y
                if abs(z) <= 5:
                    self.hexes.append((x, y, z))
        
        self.offset_x = self.WIDTH // 2
        self.offset_y = self.HEIGHT // 2
        self.pieces = []
        self.game_over = False
        self.winner = None

    def cube_to_pixel(self, x, y, z):
        q = x
        r = z
        px = self.SIDE * 1.5 * q + self.offset_x
        py = self.SIDE * self.SQRT3 * (r + q / 2.0) + self.offset_y
        return int(px), int(py)

    def pixel_to_cube(self, px, py):
        x = (px - self.offset_x) / (self.SIDE * 1.5)
        z = (py - self.offset_y) / (self.SIDE * self.SQRT3) - x / 2.0
        y = -x - z
        return x, y, z

    def cube_round(self, x, y, z):
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
        fx, fy, fz = self.pixel_to_cube(px, py)
        x, y, z = self.cube_round(fx, fy, fz)
        if (x, y, z) in self.hexes:
            return (x, y, z)
        return None

    def get_piece_at(self, x, y, z):
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
        text_color = Colors.WHITE if piece.color in ['black', 'orange'] else Colors.BLACK
        
        text = font.render(piece.symbol, True, text_color)
        text_rect = text.get_rect(center=(cx, cy))
        surface.blit(text, text_rect)

    def draw_highlight(self, surface, x, y, z, color=(255, 255, 0, 80)):
        cx, cy = self.cube_to_pixel(x, y, z)
        s = pygame.Surface((self.SIDE*2, self.SIDE*2), pygame.SRCALPHA)
        pygame.draw.circle(s, color[:3] + (80,), (self.SIDE, self.SIDE), int(self.SIDE*0.3))
        surface.blit(s, (cx - self.SIDE, cy - self.SIDE))

    def draw_text(self, text, x_offset=10, y_offset=10, color=(255, 255, 255)):
        text_surf = self.font.render(text, True, color)
        # Устанавливаем положение: x_offset от левого края, y_offset от верхнего
        text_rect = text_surf.get_rect(topleft=(x_offset, y_offset))
        self.screen.blit(text_surf, text_rect)

    def find_king(self, color):
        for piece in self.pieces:
            if piece.color == color and isinstance(piece, King):
                return piece
        return None

    def is_square_attacked(self, x, y, z, attacking_color):
        for piece in self.pieces:
            if piece.color == attacking_color:
                moves = piece.get_moves(self)
                if (x, y, z) in moves:
                    return True
        return False

    def is_in_check(self, color):
        king = self.find_king(color)
        if not king:
            return False
        opponent = 'black' if color == 'white' else 'white'
        return self.is_square_attacked(king.x, king.y, king.z, opponent)

    def move_leaves_king_in_check(self, piece, dest_x, dest_y, dest_z):
        orig_x, orig_y, orig_z = piece.x, piece.y, piece.z
        captured = None
        for p in self.pieces:
            if p.x == dest_x and p.y == dest_y and p.z == dest_z and p != piece:
                captured = p
                break
        if captured:
            self.pieces.remove(captured)
        
        piece.x, piece.y, piece.z = dest_x, dest_y, dest_z
        in_check = self.is_in_check(piece.color)
        
        piece.x, piece.y, piece.z = orig_x, orig_y, orig_z
        if captured:
            self.pieces.append(captured)
        return in_check

    def get_legal_moves(self, piece):
        all_moves = piece.get_moves(self)
        legal = []
        for move in all_moves:
            if not self.move_leaves_king_in_check(piece, *move):
                legal.append(move)
        return legal

    def has_any_legal_moves(self, color):
        for piece in self.pieces:
            if piece.color == color:
                if self.get_legal_moves(piece):
                    return True
        return False

class Piece:
    def __init__(self, color, x, y, z, symbol):
        self.color = color
        self.x = x
        self.y = y
        self.z = z
        self.symbol = symbol
    def get_moves(self, board): return []
    def __repr__(self): return f"{self.color[0]}{self.symbol}"

class Pawn(Piece):
    def __init__(self, color, x, y, z):
        super().__init__(color, x, y, z, 'P')
        self.has_moved = False
    def get_moves(self, board):
        moves = []
        forward = (0, 1, -1) if self.color == 'white' else (0, -1, 1)
        captures = [(-1, 2, -1), (1, 1, -2)] if self.color == 'white' else [(1, -2, 1), (-1, -1, 2)]
        nx, ny, nz = self.x + forward[0], self.y + forward[1], self.z + forward[2]
        if (nx, ny, nz) in board.hexes and board.get_piece_at(nx, ny, nz) is None:
            moves.append((nx, ny, nz))
            if not self.has_moved:
                nx2, ny2, nz2 = self.x + 2*forward[0], self.y + 2*forward[1], self.z + 2*forward[2]
                if (nx2, ny2, nz2) in board.hexes and board.get_piece_at(nx2, ny2, nz2) is None:
                    moves.append((nx2, ny2, nz2))
        for dx, dy, dz in captures:
            nx, ny, nz = self.x + dx, self.y + dy, self.z + dz
            if (nx, ny, nz) in board.hexes:
                p = board.get_piece_at(nx, ny, nz)
                if p and p.color != self.color:
                    moves.append((nx, ny, nz))
        return moves

class Knight(Piece):
    def __init__(self, color, x, y, z): super().__init__(color, x, y, z, 'N')
    def get_moves(self, board):
        moves = []
        knight_dirs = [(1,2,-3), (1,-3,2), (2,1,-3), (2,-3,1), (-3,1,2), (-3,2,1),
                       (-1,-2,3), (-1,3,-2), (-2,-1,3), (-2,3,-1), (3,-1,-2), (3,-2,-1)]
        for dx, dy, dz in knight_dirs:
            nx, ny, nz = self.x + dx, self.y + dy, self.z + dz
            if (nx, ny, nz) in board.hexes:
                p = board.get_piece_at(nx, ny, nz)
                if p is None or p.color != self.color: moves.append((nx, ny, nz))
        return moves

class Bishop(Piece):
    def __init__(self, color, x, y, z): super().__init__(color, x, y, z, 'B')
    def get_moves(self, board):
        moves = []
        diag_dirs = [(2,-1,-1), (-2,1,1), (-1,2,-1), (1,-2,1), (-1,-1,2), (1,1,-2)]
        for dx, dy, dz in diag_dirs:
            step = 1
            while True:
                nx, ny, nz = self.x + step*dx, self.y + step*dy, self.z + step*dz
                if (nx, ny, nz) not in board.hexes: break
                p = board.get_piece_at(nx, ny, nz)
                if p is None: moves.append((nx, ny, nz)); step += 1
                elif p.color != self.color: moves.append((nx, ny, nz)); break
                else: break
        return moves

class Rook(Piece):
    def __init__(self, color, x, y, z): super().__init__(color, x, y, z, 'R')
    def get_moves(self, board):
        moves = []
        orth_dirs = [(1,-1,0), (-1,1,0), (1,0,-1), (-1,0,1), (0,1,-1), (0,-1,1)]
        for dx, dy, dz in orth_dirs:
            step = 1
            while True:
                nx, ny, nz = self.x + step*dx, self.y + step*dy, self.z + step*dz
                if (nx, ny, nz) not in board.hexes: break
                p = board.get_piece_at(nx, ny, nz)
                if p is None: moves.append((nx, ny, nz)); step += 1
                elif p.color != self.color: moves.append((nx, ny, nz)); break
                else: break
        return moves

class Queen(Piece):
    def __init__(self, color, x, y, z): super().__init__(color, x, y, z, 'Q')
    def get_moves(self, board):
        return Rook(self.color, self.x, self.y, self.z).get_moves(board) + \
               Bishop(self.color, self.x, self.y, self.z).get_moves(board)

class King(Piece):
    def __init__(self, color, x, y, z): super().__init__(color, x, y, z, 'K')
    def get_moves(self, board):
        moves = []
        orth_dirs = [(1,-1,0), (-1,1,0), (1,0,-1), (-1,0,1), (0,1,-1), (0,-1,1)]
        for dx, dy, dz in orth_dirs:
            nx, ny, nz = self.x + dx, self.y + dy, self.z + dz
            if (nx, ny, nz) in board.hexes:
                p = board.get_piece_at(nx, ny, nz)
                if p is None or p.color != self.color: moves.append((nx, ny, nz))
        return moves

# --- ОСТАЛЬНАЯ ЛОГИКА (create_initial_pieces, main) ---

def create_initial_pieces():
    white_data = [
        (0, -5, 5, 'B'), (0, -4, 4, 'B'), (0, -3, 3, 'B'),
        (1, -5, 4, 'K'), (2, -5, 3, 'N'), (3, -5, 2, 'R'), (4, -5, 1, 'P'),
        (-1, -4, 5, 'Q'), (-2, -3, 5, 'N'), (-3, -2, 5, 'R'), (-4, -1, 5, 'P'),
        (3, -4, 1, 'P'), (-3, -1, 4, 'P'), (2, -3, 1, 'P'), (-2, -1, 3, 'P'),
        (1, -2, 1, 'P'), (-1, -1, 2, 'P'), (0, -1, 1, 'P')
    ]
    pieces = []
    for x, y, z, sym in white_data:
        for color, mult in [('white', 1), ('black', -1)]:
            cx, cy, cz = x*mult, y*mult, z*mult
            if sym == 'P': pieces.append(Pawn(color, cx, cy, cz))
            elif sym == 'N': pieces.append(Knight(color, cx, cy, cz))
            elif sym == 'B': pieces.append(Bishop(color, cx, cy, cz))
            elif sym == 'R': pieces.append(Rook(color, cx, cy, cz))
            elif sym == 'Q': pieces.append(Queen(color, cx, cy, cz))
            elif sym == 'K': pieces.append(King(color, cx, cy, cz))
    return pieces

def main():
    board = Board()
    board.pieces = create_initial_pieces()
    selected_piece = None
    possible_moves = []
    turn = 'white'
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not board.game_over:
                mx, my = pygame.mouse.get_pos()
                hex_coord = board.get_hex_at(mx, my)
                if hex_coord is None:
                    selected_piece, possible_moves = None, []
                    continue
                hx, hy, hz = hex_coord
                piece_here = board.get_piece_at(hx, hy, hz)

                if selected_piece and (hx, hy, hz) in possible_moves:
                    if piece_here: board.pieces.remove(piece_here)
                    selected_piece.x, selected_piece.y, selected_piece.z = hx, hy, hz
                    if isinstance(selected_piece, Pawn): selected_piece.has_moved = True
                    selected_piece, possible_moves = None, []
                    turn = 'black' if turn == 'white' else 'white'
                    
                    if not board.has_any_legal_moves(turn):
                        board.game_over = True
                        board.winner = 'white' if turn == 'black' else 'black' if board.is_in_check(turn) else None
                else:
                    if piece_here and piece_here.color == turn:
                        selected_piece = piece_here
                        possible_moves = board.get_legal_moves(piece_here)
                    else:
                        selected_piece, possible_moves = None, []

        board.screen.fill(board.BACKGROUND)
        for x, y, z in board.hexes:
            color_index = (x + 2 * y) % 3
            board.draw_hex(board.screen, x, y, z, board.COLORS[color_index])
        for (mx, my, mz) in possible_moves:
            board.draw_highlight(board.screen, mx, my, mz, (0, 0, 0))
        for piece in board.pieces:
            board.draw_piece(board.screen, piece)

        if board.game_over:
            msg = f"Мат! Победили {'Белые' if board.winner == 'white' else 'Чёрные'}" if board.winner else "Пат! Ничья"
            board.draw_text(msg, x_offset=10, y_offset=10)
        else:
            turn_text = f"Ход: {'Белые' if turn == 'white' else 'Чёрные'}"
            color = (255, 100, 100) if board.is_in_check(turn) else (255, 255, 255)
            board.draw_text(turn_text + (" (ШАХ!)" if board.is_in_check(turn) else ""), x_offset=10, y_offset=10, color=color)

        pygame.display.flip()
        board.clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()