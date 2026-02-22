from gpColor import colorize

from src.helper import Colors, Position


class Figure:
    def __init__(self, color: Colors = Colors.BLACK):
        self.name = None
        self.icon = " "
        self.color = color

    def check_move(self, old_pos: Position, new_pos: Position) -> bool:
        return True
    
    def __str__(self):
        return colorize(f"\033[1m {self.icon} \033[0m", font = self.color)

class NoneFigure(Figure):
    def __init__(self):
        self.name = None
        self.icon = " "

    def check_move(self, old_pos: Position, new_pos: Position) -> bool:
        return False

class Pawn(Figure):
    def __init__(self, color: Colors = Colors.BLACK):
        self.name = "Пешка"
        self.icon = "P"
        self.color = color
        
        self.is_first_move = True

    def check_move(self, old_pos: Position, new_pos: Position) -> bool:
        direction = -1 if self.color == Colors.WHITE else 1
        
        dx = new_pos.x - old_pos.x
        dy = abs(new_pos.y - old_pos.y)
        
        if dy != 0:
            return False
        
        if dx == direction:
            return True
        
        if self.is_first_move and dx == 2 * direction:
            return True
        
        return False


class King(Figure):
    def __init__(self, color: Colors = Colors.BLACK):
        self.name = "Король"
        self.icon = "K"
        self.color = color

    def check_move(self, old_pos: Position, new_pos: Position) -> bool:
        if abs(old_pos.x - new_pos.x) <= 1 and abs(old_pos.y - new_pos.y) <= 1:
            return True
        
        return False

class Queen(Figure):
    def __init__(self, color: Colors = Colors.BLACK):
        self.name = "Королева"
        self.icon = "Q"
        self.color = color

    def check_move(self, old_pos: Position, new_pos: Position) -> bool:
        if any((
            abs(old_pos.x - new_pos.x) == abs(old_pos.y - new_pos.y),
            old_pos.x == new_pos.x or old_pos.y == new_pos.y
        )) == True:
            return True
        return False

class Rook(Figure):
    def __init__(self, color: Colors = Colors.BLACK):
        self.name = "Ладья"
        self.icon = "R"
        self.color = color

    def check_move(self, old_pos: Position, new_pos: Position) -> bool:
        if old_pos.x == new_pos.x or old_pos.y == new_pos.y:
            return True
        return False

class Bishop(Figure):
    def __init__(self, color: Colors = Colors.BLACK):
        self.name = "Слон"
        self.icon = "B"
        self.color = color

    def check_move(self, old_pos: Position, new_pos: Position) -> bool:
        if abs(old_pos.x - new_pos.x) == abs(old_pos.y - new_pos.y):
            return True
        return False

class Knight(Figure):
    def __init__(self, color: Colors = Colors.BLACK):
        self.name = "Конь"
        self.icon = "N"
        self.color = color

    def check_move(self, old_pos: Position, new_pos: Position) -> bool:
        if any((
            abs(old_pos.x - new_pos.x) == 1 and abs(old_pos.y - new_pos.y) == 2,
            abs(old_pos.x - new_pos.x) == 2 and abs(old_pos.y - new_pos.y) == 1,

        )) == True:
            return True
        return False