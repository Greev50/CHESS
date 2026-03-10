from typing import List
from gpColor import colorize
from src.figure import Pawn
from src.helper import Colors, Position
from src.table import Table, TableTypes
from src.player import Player

class Gamemanager:
    def __init__(self):
        self.current_table = None
        self.players: List[Player] = []
        self.current_player = None
        self.is_working = True

    def temp_start(self, table_type: TableTypes = TableTypes.BASIC):
        try:
            self.current_table = Table(type=table_type)
            self.current_table.generate_table()
            self.players = [Player(1, Colors.WHITE), Player(2, Colors.BLACK)]
            self.current_player = self.players[0]
            self.life_cycle()
        except KeyboardInterrupt:
            self._quit()


    def move(self) -> bool:
        try:
            prompt = f"Ход ({self.current_player.return_name()}): "
            inp = input(prompt).lower().split()
            
            if len(inp) < 2: 
                return False
            
            p1, p2 = Position(inp[0]), Position(inp[1])
            cell = self.current_table.table[p1.x][p1.y]
            fig = cell.get_figure()
            
            if not fig or fig.color != self.current_player.color: 
                print("Это не твоя фигура или клетка пуста!")
                return False
            
            # Вызываем перемещение
            res = self.current_table.move_figure(p1, p2)
            
            # ОТЛАДКА: если тут False при визуальном прыжке — беда в table.py
            # print(f"DEBUG: move_figure returned {res}") 
            
            return res 
            
        except Exception as e:
            print(f"Критическая ошибка в move: {e}")
            return False


    def life_cycle(self):
        while self.is_working:
            # 1. Печатаем доску
            self.current_table.print_table()
            
            # 2. Ждем валидного хода
            is_moved = False
            while not is_moved:
                # Вызываем твой новый move(), который мы только что поправили
                if self.move(): 
                    is_moved = True
                else:
                    print("ОШИБКА ХОДА! Попробуй еще раз.")

            # 3. Как только вышли из цикла — СРАЗУ меняем игрока
            self._next_player()
            print(f"--- Очередь перешла к: {self.current_player.return_name()} ---")


    def round_check(self):
        # Превращение пешек на крайних линиях
        for i, row_idx in enumerate([0, 7]):
            color = Colors.WHITE if i == 0 else Colors.BLACK
            for cell in self.current_table.table[row_idx]:
                fig = cell.get_figure()
                if isinstance(fig, Pawn) and fig.color == color:
                    cell.change_figure(fig.last_cell_transform())
        
        # Проверка шаха и мата
        checks = self.current_table.try_check()
        if checks:
            for king, pos, attackers in checks:
                enemy_color = king.color
                print(colorize(f"\n ШАХ {Colors.color_to_name(enemy_color)}! ", font=Colors.ORANGE))
                
                # Вызываем проверку на мат для короля, которому объявили шах
                if self.current_table.is_checkmate(enemy_color):
                    print(colorize(f"\n МАТ! Игрок {self.current_player.return_name()} побеждает! ", font=Colors.RED))
                    self.is_working = False # Останавливаем игру

    def _next_player(self):
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def _quit(self):
        self.is_working = False
        print(colorize("\nВыход!", font=Colors.GREEN))