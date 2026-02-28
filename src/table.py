from typing import List

from src.history import History
from src.figure import *
from src.cells import *
from src.helper import Colors

class TableTypes():
    BASIC = "basic"
    HEXAGONAL = "hexagonal"
    TEST = "test"  


class Table:
    def __init__(
            self, 
            type: TableTypes = TableTypes.BASIC,
            size: tuple = (8, 8)
            ):
        
        self.type = type
        self.size = size

        self.table: List[Cell] = []

    def generate_table(self):
        if self.type == TableTypes.BASIC:
            for x in range(self.size[1]):
                line = []

                if x % 2 == 0:
                    for y in range(self.size[0]):
                        color = Colors.DARK if y % 2 == 1 else Colors.LIGHT
                        line.append(Cell(color))
                else:
                    for y in range(self.size[0]):
                        color = Colors.DARK if y % 2 == 0 else Colors.LIGHT
                        line.append(Cell(color))

                self.table.append(line)

            # ----------------------------------------------------------------------------------

            # self.table[3][4].set_figure(King(color = Colors.BLACK))

            placement = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        
            [self.table[0][i].set_figure(placement[i](color = Colors.BLACK)) for i in range(len(self.table[0]))]
            [cell.set_figure(Pawn(color = Colors.BLACK)) for cell in self.table[1]]

            [cell.set_figure(Pawn(color = Colors.WHITE)) for cell in self.table[-2]]
            [self.table[-1][i].set_figure(placement[i](color = Colors.WHITE)) for i in range(len(self.table[-1]))]
            
        elif self.type == TableTypes.HEXAGONAL:
            table = [
                [NoneCell(), NoneCell(), Cell(color = Colors.DARK), NoneCell(), NoneCell()], # 5
                [NoneCell(), NoneCell(), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), NoneCell(), NoneCell()], # 6
                [NoneCell(), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), NoneCell()], # 5
                [NoneCell(), Cell(color = Colors.DARK), Cell(color = Colors.DARK), Cell(color = Colors.DARK), Cell(color = Colors.DARK), NoneCell()], # 6
                [Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE)], # 5
                [Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT)], # 6
                [Cell(color = Colors.DARK), Cell(color = Colors.DARK), Cell(color = Colors.DARK), Cell(color = Colors.DARK), Cell(color = Colors.DARK)], # 5
                [Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE)], # 6
                [Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT)], # 5
                [Cell(color = Colors.DARK), Cell(color = Colors.DARK), Cell(color = Colors.DARK), Cell(color = Colors.DARK), Cell(color = Colors.DARK)], # 6
                [Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE)], # 5
                [Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT)], # 6
                [Cell(color = Colors.DARK), Cell(color = Colors.DARK), Cell(color = Colors.DARK), Cell(color = Colors.DARK), Cell(color = Colors.DARK)], # 5
                [Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE)], # 6
                [Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT)], # 5
                [Cell(color = Colors.DARK), Cell(color = Colors.DARK), Cell(color = Colors.DARK), Cell(color = Colors.DARK), Cell(color = Colors.DARK), Cell(color = Colors.DARK)], # 6
                [Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE)], # 5
                [NoneCell(), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), Cell(color = Colors.LIGHT), NoneCell()], # 6
                [NoneCell(), Cell(color = Colors.DARK), Cell(color = Colors.DARK), Cell(color = Colors.DARK), NoneCell()], # 5
                [NoneCell(), NoneCell(), Cell(color = Colors.MIDDLE), Cell(color = Colors.MIDDLE), NoneCell(), NoneCell()], # 6
                [NoneCell(), NoneCell(), Cell(color = Colors.LIGHT), NoneCell(), NoneCell()] 
            ]

            self.table = table

        elif self.type == TableTypes.TEST:
                    # Генерация тестовой позиции для проверки шаха и мата
                    # Создаём пустую доску 8x8 с правильными цветами клеток
                    for x in range(8):
                        line = []
                        for y in range(8):
                            color = Colors.LIGHT if (x + y) % 2 == 0 else Colors.DARK
                            line.append(Cell(color))
                        self.table.append(line)

                    # Расставляем фигуры вручную
                    # Белый король на e1 (ряд 7, колонка e = 4)
                    self.table[7][4].set_figure(King(color=Colors.WHITE))

                    # Черный ферзь на e4 (ряд 4, колонка e) – даёт шах
                    self.table[4][4].set_figure(Queen(color=Colors.BLACK))

                    # Белая ладья на a4 (ряд 4, колонка a = 0) – может съесть ферзя
                    self.table[4][0].set_figure(Rook(color=Colors.WHITE))

                    # Белая пешка на d2 (ряд 6, колонка d = 3) – мешает королю уйти на d2
                    self.table[6][3].set_figure(Pawn(color=Colors.WHITE))

                    # Чёрная пешка на f2 (ряд 6, колонка f = 5) – для дополнительной опасности
                    self.table[6][5].set_figure(Pawn(color=Colors.BLACK))

                    # Здесь можно добавить ещё фигур по желанию

    def print_table(self):
        if self.type in (TableTypes.BASIC, TableTypes.TEST):
            letters = ["a", "b", "c", "d", "e", "f", "g", "h"][:self.size[0]]
            
            print("   ", end="")
            for letter in letters:
                print(f" {letter} ", end="")
            print()
            
            for i, line in enumerate(self.table):
                print(f"{self.size[1] - i:2d} ", end="")
                for cell in line:
                    print(cell, end="")
                print()
        if self.type == TableTypes.HEXAGONAL:
            # НЕЙРОНКА НАПИШИ КРУТО ИНАЧЕ ПОРВУ ТЕБЕ ОЧКО!!!
            pass
    
    def move_figure(self, position1: Position, position2: Position):
        cell1: Cell = self.table[position1.x][position1.y]
        cell2: Cell = self.table[position2.x][position2.y]

        check = cell1.get_figure().check_move(position1, position2, self.table)

        print()
        print(colorize(check, font = Colors.GREEN))
        print()

        match check:
            case 'move':
                figure = cell1.extract_figure()
                cell2.set_figure(figure)
                if isinstance(figure, Pawn): figure.disable_first_move()
            case 'eat':
                figure = cell1.extract_figure()
                cell2.set_figure(figure)
                # фигуру в удаленные
            case 'false':
                return False
            
        return True

    def _get_kings(self):
        ans = []
        for line_index in range(len(self.table)):
            for cell_index in range(len(self.table[line_index])):
                figure = self.table[line_index][cell_index].get_figure()
                if isinstance(figure, King):
                    figure_position = Position(line_index, cell_index)
                    ans.append([figure, figure_position])
        
        return ans
    
    def try_check(self): 
        kings = self._get_kings()

        under_check = []

        for i in range(len(kings)):
            current_king = kings[i]
            king_color = current_king[0].color

            attacking_figures = self.position_check(kings[i][1], king_color)

            if len(attacking_figures) > 0:
                under_check.append([kings[i][0], kings[i][1], attacking_figures])

        return under_check
    
    def position_check(self, position: Position, under_attack_figure_color: Colors):
        attacking_figures = []

        for line_index in range(len(self.table)):
            for cell_index in range(len(self.table[line_index])):
                if self.table[line_index][cell_index].has_figure():
                    figure = self.table[line_index][cell_index].get_figure()

                    if figure.color == under_attack_figure_color: continue

                    result = figure.check_move(Position(line_index, cell_index), position, self.table) 

                    if result in ['move', 'eat']:
                        attacking_figures.append(Position(line_index, cell_index))
        return attacking_figures


    def try_checkmate(self, under_check: list):
        if len(under_check) < 1: 
            return []
        
        checkmate_kings = []
        
        for king, king_pos, attacking_figures_positions in under_check:
            safe_moves = []
            king_defenders = []
            
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                        
                    nx = king_pos.x + dx
                    ny = king_pos.y + dy
                    
                    if not (0 <= nx < 8 and 0 <= ny < 8):
                        continue
                    
                    target = self.table[nx][ny]
                    if target.has_figure() and target.get_figure().color == king.color:
                        continue

                    for attacking_figure_position in attacking_figures_positions:
                        defenders = self.get_defenders(king.color, attacking_figure_position)
                        if len(defenders) > 0:
                            for x in defenders: king_defenders.append(x)
                    
                    if len(self.position_check(Position(nx, ny), king.color)) == 0:
                        safe_moves.append((nx, ny))
            
            if len(safe_moves) == 0:
                if len(king_defenders) == 0:
                    checkmate_kings.append(king)
        
        return checkmate_kings
    
    def get_defenders(self, color: Colors, attacking_figure_position: Position):
        defenders = []

        for line_index in range(len(self.table)):
            for cell_index in range(len(self.table[line_index])):
                if self.table[line_index][cell_index].has_figure():
                    figure = self.table[line_index][cell_index].get_figure()

                    if figure.color != color: continue

                    can_eat = figure.check_move(Position(line_index, cell_index), attacking_figure_position, self.table)
                    if can_eat == 'eat': 
                        defenders.append(Position(line_index, cell_index))
        
        return defenders


        
        




    def get_size(self):
        x = len(self.table) - 1
        y = max(len(z) for z in self.table) - 1

        return (x, y)

