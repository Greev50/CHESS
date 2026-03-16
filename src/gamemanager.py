from typing import List
import copy
from gpColor import colorize
from src.figure import Pawn
from src.helper import Colors, Position
from src.table import Table, TableTypes
from src.player import Player
from src.history import History

class Gamemanager:
    def __init__(self):
        self.current_table = None
        self.players: List[Player] = []
        self.current_player = None
        self.is_working = True

    def temp_start(self, table_type: TableTypes = TableTypes.BASIC):
        try:
            History.clear()
            self.current_table = Table(type=table_type)
            self.current_table.generate_table()
            self.players = [Player(1, Colors.WHITE), Player(2, Colors.BLACK)]
            self.current_player = self.players[0]
            self.life_cycle()
        except KeyboardInterrupt:
            self._quit()

    def move(self) -> str:
        try:
            prompt = f"Ход ({self.current_player.return_name()}): "
            inp = input(prompt).lower().split()
            
            if not inp:
                return 'error'

            if len(inp) == 1 and inp[0] == "history":
                hist = History.get_formatted_history()
                if not hist:
                    print("История пуста.")
                else:
                    print("\n--- История ходов ---")
                    for line in hist:
                        print(line.strip())
                    print("---------------------\n")
                return 'info'

            if len(inp) == 2 and inp[0] == "help":
                try:
                    p = Position(inp[1])
                    fig = self.current_table.table[p.x][p.y].get_figure()
                    if not fig or fig.color != self.current_player.color:
                        print("Это не твоя фигура или клетка пуста!")
                        return 'error'
                    self.current_table.show_help(p)
                    return 'info'
                except Exception:
                    return 'error'

            if len(inp) == 2 and inp[0] == "back":
                try:
                    steps = int(inp[1])
                    if steps > 0:
                        state, player = History.undo(steps)
                        if state:
                            self.current_table.table = copy.deepcopy(state)
                            self.current_player = player
                            return 'undone'
                        else:
                            print("Невозможно откатить на столько ходов!")
                            return 'error'
                    else:
                        return 'error'
                except ValueError:
                    return 'error'

            if len(inp) < 2: 
                return 'error'
            
            p1, p2 = Position(inp[0]), Position(inp[1])
            cell = self.current_table.table[p1.x][p1.y]
            fig = cell.get_figure()
            
            if not fig or fig.color != self.current_player.color: 
                print("Это не твоя фигура или клетка пуста!")
                return 'error'
            
            state_before = copy.deepcopy(self.current_table.table)
            
            res = self.current_table.move_figure(p1, p2)

            if res:
                History.add_move(p1, p2, fig, self.current_player, 'move', state_before)
                return 'success'
            
            return 'error'
            
        except Exception as e:
            print(f"Критическая ошибка в move: {e}")
            return 'error'

    def life_cycle(self):
        while self.is_working:
            self.current_table.print_table()
            is_moved = False
            undone = False
            
            while not is_moved:
                res = self.move()
                if res == 'success':
                    is_moved = True
                elif res == 'undone':
                    is_moved = True
                    undone = True
                elif res == 'info':
                    pass
                else:
                    print("ОШИБКА ХОДА!\nПопробуй еще раз.")

            if not undone:
                self.round_check()
                if self.is_working:
                    self._next_player()
                    print(f"--- Очередь перешла к: {self.current_player.return_name()} ---")

    def round_check(self):
        for i, row_idx in enumerate([0, 7]):
            color = Colors.WHITE if i == 0 else Colors.BLACK
            for cell in self.current_table.table[row_idx]:
                fig = cell.get_figure()
                if isinstance(fig, Pawn) and fig.color == color:
                    cell.change_figure(fig.last_cell_transform())
        
        checks = self.current_table.try_check()
        if checks:
            for king, pos, attackers in checks:
                enemy_color = king.color
                print(colorize(f"\n ШАХ {Colors.color_to_name(enemy_color)}! ", font=Colors.ORANGE))
                
                if self.current_table.is_checkmate(enemy_color):
                    print(colorize(f"\n МАТ! Игрок {self.current_player.return_name()} побеждает! ", font=Colors.RED))
                    self.is_working = False 

    def _next_player(self):
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def _quit(self):
        self.is_working = False
        print(colorize("\nВыход!", font=Colors.GREEN))