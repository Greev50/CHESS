from typing import List
from gpColor import colorize

from src.helper import Colors, Position
from src.table import Table, TableTypes
from src.player import Player
from src.errors import *

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
    
    def move(self) -> bool:
        """ a1 b2 (начало, конец)
        """
        try:
            inp = str(input(f"Ход игрока {self.current_player.return_name()}: ")).lower().split(" ")

            position1 = Position(inp[0])
            position2 = Position(inp[1])

            self.current_table.move_figure(position1, position2)

            return True
        
        except WrongPositionError:
            return False





    def life_cycle(self):
        while self.is_working == True:
            try:

                self.current_table.print_table()

                is_moved = False
                while is_moved != True:
                    is_moved = self.move()

                print()
                self._next_player() #! ВЕРНУТЬ

            except Exception as e:
                print(f"{colorize("ОШИБКА!", font = Colors.RED)} ({e})")
                continue



    def _next_player(self):
        next_id = self.current_player.id

        if len(self.players) > next_id:
            self.current_player = self.players[next_id]
        else:
            self.current_player = self.players[0]

    def _quit(self):
        self.is_working = False
        print(colorize("\nВыход из шахмат!", font = Colors.GREEN))


        