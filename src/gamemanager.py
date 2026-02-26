from typing import List
from gpColor import colorize

from src.figure import Pawn
from src.helper import Colors, Position
from src.table import Table, TableTypes
from src.player import Player
from src.errors import *
from src.history import History

class Gamemanager:
    def __init__(self):
        self.current_table: Table = None

        self.players: List[Player] = []
        self.current_player: Player

        self.is_working = True

    def temp_start(self):
        try:
            self.current_table = Table(type = TableTypes.BASIC)
            self.current_table.generate_table()



            
            self.players.append(Player(id = 1, color = Colors.WHITE))
            self.players.append(Player(id = 2, color = Colors.BLACK))
            
            self.current_player = self.players[0]



            self.life_cycle()



        except KeyboardInterrupt:
            self._quit()
    
    def move(self) -> bool: # если True то меняется игрок
        """ a1 b2 (начало, конец)
        """
        try:
            inp = str(input(f"Ход игрока {self.current_player.return_name()}: ")).lower().split(" ")

            position1 = Position(inp[0])
            position2 = Position(inp[1])

            if self.current_table.table[position1.x][position1.y].get_figure() != None and self.current_table.table[position1.x][position1.y].get_figure().color != self.current_player.color: return False

            move_description = self.current_table.move_figure(position1, position2)

            return move_description
        
        except WrongPositionError:
            return False





    def life_cycle(self):

        def round_check():
            # Пешка в другую фигуру. не динамическое
            # ============================================
            for cell in self.current_table.table[0]:
                figure = cell.get_figure()

                if isinstance(figure, Pawn):
                    if figure.color == Colors.WHITE:
                        cell.change_figure(figure.last_cell_transform())

            for cell in self.current_table.table[-1]:
                figure = cell.get_figure()

                if isinstance(figure, Pawn):
                    if figure.color == Colors.BLACK:
                        cell.change_figure(figure.last_cell_transform())
            # ============================================


            check = self.current_table.try_check()
            checkmate = self.current_table.try_checkmate(check)

            if len(check) != 0:
                if len(checkmate) == 0:
                    print(f"Шах! {check}")
                else:
                    print(f"Мат! {checkmate}")
                    

        while self.is_working == True:
            # try:
                is_moved = False

                while is_moved != True:
                    self.current_table.print_table()
                    is_moved = self.move()

                # print() 
                # print(*History.get_formatted_history(), sep = "") #! ВЕРНУТЬ
                # print()

                # print(self.current_table.try_check())

                round_check()

                self._next_player() #! ВЕРНУТЬ

            # except Exception as e:
            #     print(f"{colorize("ОШИБКА!", font = Colors.RED)} ({e})")
            #     continue



    def _next_player(self):
        next_id = self.current_player.id

        if len(self.players) > next_id:
            self.current_player = self.players[next_id]
        else:
            self.current_player = self.players[0]

    def _quit(self):
        self.is_working = False
        print(colorize("\nВыход из шахмат!", font = Colors.GREEN))


        