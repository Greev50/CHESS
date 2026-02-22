from src.helper import Colors, Position


class Figure:
    def __init__(self, color: Colors = Colors.BLACK):
        self.name = None
        self.icon = " "
        self.color = color

    def check_move(self, old_pos: Position, new_pos: Position) -> bool:
        return True

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

    # def check_move(self, old_pos: Position, new_pos: Position) -> bool:
    #     return True

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

    # def check_move(self, old_pos: Position, new_pos: Position) -> bool:
