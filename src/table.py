from typing import List

from src.history import History
from src.figure import Pawn
from src.cells import *
from src.helper import Colors

class TableTypes():
    BASIC = "basic"
    HEXAGONAL = "hexagonal"


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

            # self.table[3][5].set_figure(Bishop(color = Colors.WHITE))

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


    def print_table(self):
        if self.type == TableTypes.BASIC:
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
    
    def move_figure(self, position1: Position, position2: Position) -> str:

        if self.type == TableTypes.BASIC:
            if all(0 <= x <= 7 for x in (position1.x, position1.y, position2.x, position2.y)) == False:
                raise ValueError("Такой клетки не существует!")
                # return False

        if self.table[position1.x][position1.y].has_figure() == False:
            # raise ValueError("Пустая клетка!")
            return False
        else:
            figure: Figure = self.table[position1.x][position1.y].get_figure()
        
        origin: Cell | NoneCell = self.table[position1.x][position1.y]
        destination: Cell | NoneCell = self.table[position2.x][position2.y]
        
        if isinstance(destination, NoneCell):
            raise ValueError("Такой клетки не существует!")
        
        if position1 == position2: return False 
        
        
        if destination.has_figure() == True:
            if destination.get_figure().color == figure.color:
                return False
            
            self.eat(position1, position2)
            return 'eat'

        else:
            can_move = figure.check_move(position1, position2)

            if can_move == True:
                figure = origin.extract_figure()

                destination.set_figure(figure)

                return 'move'
            else:
                return False
    
    def eat(self, position1: Position, position2: Position) -> bool:
        cell1: Cell | NoneCell = self.table[position1.x][position1.y]
        cell2: Cell | NoneCell = self.table[position2.x][position2.y]

        figure1: Figure = cell1.get_figure()
        figure2: Figure = cell2.get_figure()

        def eat_figure():
            figure = cell1.extract_figure()
            cell2.set_figure(figure)
            History.add_killed(figure)

        if figure1.color == figure2.color: return False

        if isinstance(figure2, King): return False

        if isinstance(figure1, Pawn):
            if abs(position1.y - position2.y) == 1 and (position2.x - position1.x) == (-1 if figure1.color == Colors.WHITE else 1):
                eat_figure()
                return True
        
        eat_figure()
        return True
                


        







        # координаты 1 и 2
        # чем ходить
        # куда ходить (есть ли клетка)
        # есть ли что есть
        
