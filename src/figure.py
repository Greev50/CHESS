from gpColor import colorize

from src.helper import Colors, Position

class Figure:
    def __init__(self, color: Colors = Colors.BLACK):
        self.name = None
        self.icon = " "
        self.color = color

    def check_move(self, old_pos: Position, new_pos: Position, table) -> bool:
        return 'move'
    
    def __str__(self):
        return colorize(f"\033[1m {self.icon} \033[0m", font = self.color)

class NoneFigure(Figure):
    def __init__(self):
        self.name = None
        self.icon = " "

    def check_move(self, old_pos: Position, new_pos: Position, table) -> bool:
        return False

class Pawn(Figure): # DONE
    def __init__(self, color: Colors = Colors.BLACK):
        self.name = "Пешка"
        self.icon = "P"
        self.color = color
        
        self.is_first_move = True

    def check_move(self, old_pos: Position, new_pos: Position, table) -> bool:
        if self.color == Colors.WHITE:
            if new_pos.x >= old_pos.x:  # белые не могут идти вниз или оставаться
                return 'false'
        else:  # BLACK
            if new_pos.x <= old_pos.x:  # черные не могут идти вверх или оставаться
                return 'false'

        if abs(new_pos.x - old_pos.x) == 1 and abs(new_pos.y - old_pos.y) == 0:
            if table[new_pos.x][new_pos.y].has_figure() == True:
                figure = table[new_pos.x][new_pos.y].get_figure()

                if figure.color == self.color: 
                    return 'false'
                else:
                    return 'eat'
            else:
                return 'move'
                
        elif abs(new_pos.x - old_pos.x) == 2 and abs(new_pos.y - old_pos.y) == 0:
            if self.is_first_move == False: return 'false'

            if table[new_pos.x][new_pos.y].has_figure() == True:
                figure = table[new_pos.x][new_pos.y].get_figure()

                if figure.color == self.color: 
                    return 'false'
                else:
                    return 'eat'
            else:
                return 'move'
            
        elif abs(new_pos.x - old_pos.x) == 1 and abs(new_pos.y - old_pos.y) == 1:
            if table[new_pos.x][new_pos.y].has_figure() == True:
                figure = table[new_pos.x][new_pos.y].get_figure()

                if figure.color == self.color:
                    return 'false'
                else:
                    return 'eat'
            else:
                return 'false'
                
        else:
            return 'false'
        
    def disable_first_move(self):
        self.is_first_move = False

    def last_cell_transform(self) -> Figure:
        is_selected = False

        figures = {}
        
        for x in transform_figures:
            figures[x.icon] = type(x)

        while is_selected == False:
            print(" | ".join([f"{x.icon} ({x.name})" for x in transform_figures]))
            figure = str(input("Выберите, в какую фигуру превратится пешка: ")).upper()

            if figure in figures.keys():
                return figures[figure]


            



class King(Figure): # DONE
    def __init__(self, color: Colors = Colors.BLACK):
        self.name = "Король"
        self.icon = "K"
        self.color = color

    def check_move(self, old_pos: Position, new_pos: Position, table) -> str:
        if not(abs(old_pos.x - new_pos.x) <= 1 and abs(old_pos.y - new_pos.y) <= 1):
            return 'false'
        
        if table[new_pos.x][new_pos.y].has_figure():
            if table[new_pos.x][new_pos.y].get_figure().color == self.color:
                return 'false'
            else:
                return 'eat'
        
        return 'move'

class Queen(Figure): # DONE
    def __init__(self, color: Colors = Colors.BLACK):
        self.name = "Королева"
        self.icon = "Q"
        self.color = color

    def check_move(self, old_pos: Position, new_pos: Position, table) -> str:
        # Проверка что ход по прямой или диагонали
        if not (abs(old_pos.x - new_pos.x) == abs(old_pos.y - new_pos.y) or 
                old_pos.x == new_pos.x or old_pos.y == new_pos.y):
            return 'false'
        
        # Определяем направление
        step_x = 0
        step_y = 0
        if new_pos.x > old_pos.x: step_x = 1
        elif new_pos.x < old_pos.x: step_x = -1
        if new_pos.y > old_pos.y: step_y = 1
        elif new_pos.y < old_pos.y: step_y = -1
        
        # Проверяем путь (кроме конечной клетки)
        curr_x = old_pos.x + step_x
        curr_y = old_pos.y + step_y
        
        while curr_x != new_pos.x or curr_y != new_pos.y:
            if curr_x < 0 or curr_x >= 8 or curr_y < 0 or curr_y >= 8:
                return 'false'
            if table[curr_x][curr_y].has_figure():
                return 'false'
            curr_x += step_x
            curr_y += step_y
        
        # Проверяем конечную клетку
        target = table[new_pos.x][new_pos.y]
        if target.has_figure():
            if target.get_figure().color != self.color:
                return 'eat'
            return 'false'
        
        return 'move'
    
class Rook(Figure): # DONE
    def __init__(self, color: Colors = Colors.BLACK):
        self.name = "Ладья"
        self.icon = "R"
        self.color = color

    def check_move(self, old_pos: Position, new_pos: Position, table) -> bool:
        if not(old_pos.x == new_pos.x or old_pos.y == new_pos.y):
            return 'false'
        
        step_x = 1 if new_pos.x > old_pos.x else -1
        step_y = 1 if new_pos.y > old_pos.y else -1
        
        curr_x = old_pos.x + step_x
        curr_y = old_pos.y + step_y
        
        path = []

        if new_pos.x != old_pos.x:
            while curr_x != new_pos.x + step_x:
                    
                path.append(table[curr_x][curr_y])
                    
                curr_x += step_x

            for i in range(len(path)):
                if path[i].has_figure() == True:
                    if i != len(path)-1:
                        return 'false'
                    else:
                        if path[i].get_figure().color != self.color:
                            return 'eat'
                        return 'false'
                    
            return 'move'
        
        elif new_pos.y != old_pos.y:
            while curr_y != new_pos.y + step_y:
                    
                path.append(table[curr_x][curr_y])
                    
                curr_y += step_y

            for i in range(len(path)):
                if path[i].has_figure() == True:
                    if i != len(path)-1:
                        return 'false'
                    else:
                        if path[i].get_figure().color != self.color:
                            return 'eat'
                        return 'false'
                    
            return 'move'
        
class Bishop(Figure): # DONE
    def __init__(self, color: Colors = Colors.BLACK):
        self.name = "Слон"
        self.icon = "B"
        self.color = color

    def check_move(self, old_pos: Position, new_pos: Position, table) -> bool:
        if not(abs(old_pos.x - new_pos.x) == abs(old_pos.y - new_pos.y)):
            return 'false'
        
        step_x = 1 if new_pos.x > old_pos.x else -1
        step_y = 1 if new_pos.y > old_pos.y else -1
        
        curr_x = old_pos.x + step_x
        curr_y = old_pos.y + step_y
        
        path = []
        
        while curr_x != new_pos.x + step_x and curr_y != new_pos.y + step_y:
                
            path.append(table[curr_x][curr_y])
            
            # Если на пути есть фигура - ход невозможен
                
            curr_x += step_x
            curr_y += step_y

        for i in range(len(path)):
            if path[i].has_figure() == True:
                if i != len(path)-1:
                    return 'false'
                else:
                    if path[i].get_figure().color != self.color:
                        return 'eat'
                    return 'false'
                
        return 'move'
            
class Knight(Figure): # DONE
    def __init__(self, color: Colors = Colors.BLACK):
        self.name = "Конь"
        self.icon = "N"
        self.color = color

    def check_move(self, old_pos: Position, new_pos: Position, table) -> bool:
        if not any((
            abs(old_pos.x - new_pos.x) == 1 and abs(old_pos.y - new_pos.y) == 2,
            abs(old_pos.x - new_pos.x) == 2 and abs(old_pos.y - new_pos.y) == 1,
        )) == True:
            return 'false'
        
        if table[new_pos.x][new_pos.y].has_figure() == True:
            figure = table[new_pos.x][new_pos.y].get_figure()

            if figure.color == self.color:
                return 'false'
            else:
                return 'eat'
        
        return 'move'
    
transform_figures = [Queen(), Rook(), Bishop(), Knight()]
