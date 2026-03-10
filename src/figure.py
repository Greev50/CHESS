from gpColor import colorize
from src.helper import Colors, Position

class Figure:
    def __init__(self, color: Colors = Colors.BLACK):
        self.name = "Фигура"
        self.icon = "●"
        self.color = color

    def check_move(self, old_pos: Position, new_pos: Position, table) -> str:
        return 'false'
    
    def __str__(self):
        return colorize(f"\033[1m {self.icon} \033[0m", font = self.color)
    
class NoneFigure(Figure):
    def __init__(self):
        self.icon = " "
    def check_move(self, *args) -> str:
        return 'false'
    

class Pawn(Figure): 
    def __init__(self, color: Colors = Colors.BLACK):
        super().__init__(color)
        self.name = "Пешка"
        self.icon = "P"  

    def check_move(self, old_pos: Position, new_pos: Position, table) -> str:
        dx = new_pos.x - old_pos.x
        dy = new_pos.y - old_pos.y
        
        
        if self.color == Colors.WHITE:
            
            if dx != -1 and dx != -2:  
                return 'false'
            direction = -1
        else:  
            
            if dx != 1 and dx != 2:  
                return 'false'
            direction = 1
        
        
        is_first_move = (self.color == Colors.WHITE and old_pos.x == 6) or \
                        (self.color == Colors.BLACK and old_pos.x == 1)
        
        
        if dx == direction and dy == 0:
            if not table[new_pos.x][new_pos.y].has_figure():
                return 'move'
        
        
        if dx == 2 * direction and dy == 0 and is_first_move:
            
            mid_x = old_pos.x + direction
            if not table[mid_x][old_pos.y].has_figure() and not table[new_pos.x][new_pos.y].has_figure():
                return 'move'
        
        
        if dx == direction and abs(dy) == 1:
            if table[new_pos.x][new_pos.y].has_figure() and \
               table[new_pos.x][new_pos.y].get_figure().color != self.color:
                return 'eat'
        
        return 'false'
    

class King(Figure):
    def __init__(self, color: Colors = Colors.BLACK):
        super().__init__(color)
        self.name = "Король"
        self.icon = "K"

    def check_move(self, old_pos: Position, new_pos: Position, table) -> str:
        if abs(old_pos.x - new_pos.x) <= 1 and abs(old_pos.y - new_pos.y) <= 1:
            if table[new_pos.x][new_pos.y].has_figure():
                return 'eat' if table[new_pos.x][new_pos.y].get_figure().color != self.color else 'false'
            return 'move'
        return 'false'


class Queen(Figure): 
    def __init__(self, color: Colors = Colors.BLACK):
        super().__init__(color)
        self.name = "Ферзь"
        self.icon = "Q"

    def check_move(self, old_pos: Position, new_pos: Position, table) -> str:
        dx = new_pos.x - old_pos.x
        dy = new_pos.y - old_pos.y
        
        
        if not (dx == 0 or dy == 0 or abs(dx) == abs(dy)):
            return 'false'
        
        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
        
        curr_x, curr_y = old_pos.x + step_x, old_pos.y + step_y
        while (curr_x, curr_y) != (new_pos.x, new_pos.y):
            if table[curr_x][curr_y].has_figure():
                return 'false'
            curr_x += step_x
            curr_y += step_y
        
        if table[new_pos.x][new_pos.y].has_figure():
            return 'eat' if table[new_pos.x][new_pos.y].get_figure().color != self.color else 'false'
        return 'move'
    

class Rook(Figure):
    def __init__(self, color: Colors = Colors.BLACK):
        super().__init__(color)
        self.name = "Ладья"
        self.icon = "R"

    def check_move(self, old_pos: Position, new_pos: Position, table) -> str:
        if not (old_pos.x == new_pos.x or old_pos.y == new_pos.y): 
            return 'false'
        step_x = (new_pos.x > old_pos.x) - (new_pos.x < old_pos.x)
        step_y = (new_pos.y > old_pos.y) - (new_pos.y < old_pos.y)
        curr_x, curr_y = old_pos.x + step_x, old_pos.y + step_y
        while (curr_x, curr_y) != (new_pos.x, new_pos.y):
            if table[curr_x][curr_y].has_figure(): 
                return 'false'
            curr_x += step_x
            curr_y += step_y
        if table[new_pos.x][new_pos.y].has_figure():
            return 'eat' if table[new_pos.x][new_pos.y].get_figure().color != self.color else 'false'
        return 'move'

class Bishop(Figure):
    def __init__(self, color: Colors = Colors.BLACK):
        super().__init__(color)
        self.name = "Слон"
        self.icon = "B"

    def check_move(self, old_pos: Position, new_pos: Position, table) -> str:
        if abs(old_pos.x - new_pos.x) != abs(old_pos.y - new_pos.y): 
            return 'false'
        step_x = (new_pos.x > old_pos.x) - (new_pos.x < old_pos.x)
        step_y = (new_pos.y > old_pos.y) - (new_pos.y < old_pos.y)
        curr_x, curr_y = old_pos.x + step_x, old_pos.y + step_y
        while (curr_x, curr_y) != (new_pos.x, new_pos.y):
            if table[curr_x][curr_y].has_figure(): 
                return 'false'
            curr_x += step_x
            curr_y += step_y
        if table[new_pos.x][new_pos.y].has_figure():
            return 'eat' if table[new_pos.x][new_pos.y].get_figure().color != self.color else 'false'
        return 'move'

class Knight(Figure):
    def __init__(self, color: Colors = Colors.BLACK):
        super().__init__(color)
        self.name = "Конь"
        self.icon = "N"

    def check_move(self, old_pos: Position, new_pos: Position, table) -> str:
        if sorted([abs(old_pos.x - new_pos.x), abs(old_pos.y - new_pos.y)]) == [1, 2]:
            if table[new_pos.x][new_pos.y].has_figure():
                return 'eat' if table[new_pos.x][new_pos.y].get_figure().color != self.color else 'false'
            return 'move'
        return 'false'

class Jester(Figure):
    def __init__(self, color: Colors = Colors.BLACK):
        super().__init__(color)
        self.name = "Шут"
        self.icon = "J"

    def check_move(self, old_pos: Position, new_pos: Position, table) -> str:
        if sorted([abs(old_pos.x - new_pos.x), abs(old_pos.y - new_pos.y)]) == [1, 2]:
            if table[new_pos.x][new_pos.y].has_figure() and table[new_pos.x][new_pos.y].get_figure().color != self.color:
                return 'eat'
        return 'false'

class Tank(Figure):
    def __init__(self, color: Colors = Colors.BLACK):
        super().__init__(color)
        self.name = "Танк"
        self.icon = "T"

    def check_move(self, old_pos: Position, new_pos: Position, table) -> str:
        if abs(old_pos.x - new_pos.x) <= 1 and abs(old_pos.y - new_pos.y) <= 1:
            if table[new_pos.x][new_pos.y].has_figure():
                return 'eat' if table[new_pos.x][new_pos.y].get_figure().color != self.color else 'false'
            return 'move'
        return 'false'

class Ghost(Figure):
    def __init__(self, color: Colors = Colors.BLACK):
        super().__init__(color)
        self.name = "Призрак"
        self.icon = "G"

    def check_move(self, old_pos: Position, new_pos: Position, table) -> str:
        dist_x, dist_y = abs(old_pos.x - new_pos.x), abs(old_pos.y - new_pos.y)
        if (dist_x in [2, 3] and dist_y == 0) or (dist_y in [2, 3] and dist_x == 0):
            if table[new_pos.x][new_pos.y].has_figure():
                return 'eat' if table[new_pos.x][new_pos.y].get_figure().color != self.color else 'false'
            return 'move'
        return 'false'

class Checker(Figure): 
    def __init__(self, color):
        super().__init__(color)
        self.name = "Шашка"
        self.icon = "●" 

    def check_move(self, old_pos, new_pos, table):
        dx = new_pos.x - old_pos.x
        dy = abs(new_pos.y - old_pos.y)
        
        direction = 1 if self.color == Colors.BLACK else -1
        
        if dx == direction and dy == 1:
            if not table[new_pos.x][new_pos.y].has_figure():
                return 'move'
            
        if abs(dx) == 2 and dy == 2:
            mid_x, mid_y = (old_pos.x + new_pos.x) // 2, (old_pos.y + new_pos.y) // 2
            mid_cell = table[mid_x][mid_y]
            
            if mid_cell.has_figure() and mid_cell.get_figure().color != self.color:
                if not table[new_pos.x][new_pos.y].has_figure():
                    return 'eat'

        return 'false'