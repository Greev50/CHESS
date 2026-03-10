from src.figure import *
from src.cells import Cell
from src.helper import Colors, Position
from gpColor import colorize

class TableTypes:
    BASIC = "basic"
    MODERN = "modern"
    CHECKERS = "checkers"

class Table:
    def __init__(self, type=TableTypes.BASIC, size=(8,8)):
        self.type, self.size, self.table = type, size, []

    def generate_table(self):
        self.table = [[Cell(Colors.DARK if (x+y)%2 else Colors.LIGHT) for y in range(8)] for x in range(8)]
        if self.type in [TableTypes.BASIC, TableTypes.MODERN]:
            p = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
            if self.type == TableTypes.MODERN:
                p = [Tank, Jester, Ghost, Queen, King, Ghost, Jester, Tank]
            for i in range(8):
                self.table[0][i].set_figure(p[i](Colors.BLACK))
                self.table[1][i].set_figure(Pawn(Colors.BLACK))
                self.table[6][i].set_figure(Pawn(Colors.WHITE))
                self.table[7][i].set_figure(p[i](Colors.WHITE))
        elif self.type == TableTypes.CHECKERS:
            for x in range(8):
                for y in range(8):
                    if (x + y) % 2 != 0:
                        if x < 3: self.table[x][y].set_figure(Checker(Colors.BLACK))
                        elif x > 4: self.table[x][y].set_figure(Checker(Colors.WHITE))

    def print_table(self):
        print("    a  b  c  d  e  f  g  h")
        for i, line in enumerate(self.table):
            print(f"{8-i} ", end="")
            for cell in line: print(cell, end="")
            print(f" {8-i}")
        print("    a  b  c  d  e  f  g  h")


    def _execute_jump(self, p1: Position, p2: Position):
        """Универсальное перемещение с удалением фигуры на пути"""
        # Определяем направление движения
        dx = 1 if p2.x > p1.x else -1
        dy = 1 if p2.y > p1.y else -1
        
        # Проходим по клеткам между стартом и финишем
        curr_x, curr_y = p1.x + dx, p1.y + dy
        while (curr_x, curr_y) != (p2.x, p2.y):
            # Если наткнулись на фигуру — удаляем её (это враг)
            if self.table[curr_x][curr_y].has_figure():
                self.table[curr_x][curr_y].remove_figure()
                # В шашках за один прыжок съедаем одну фигуру, 
                # поэтому после удаления первой встречной выходим из цикла
                break 
            curr_x += dx
            curr_y += dy

        # Переставляем саму шашку
        fig = self.table[p1.x][p1.y].extract_figure()
        self.table[p2.x][p2.y].set_figure(fig)


    def get_available_jumps(self, pos: Position) -> list:
        """Поиск прыжков: для дамки — через всё поле, для шашки — на 2 клетки"""
        jumps = []
        figure = self.table[pos.x][pos.y].get_figure()
        if not figure: return jumps

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        if isinstance(figure, Queen):
            # Логика "летающей" дамки
            for dx, dy in directions:
                found_enemy = False
                curr_x, curr_y = pos.x + dx, pos.y + dy
                
                while 0 <= curr_x < 8 and 0 <= curr_y < 8:
                    if not found_enemy:
                        if self.table[curr_x][curr_y].has_figure():
                            if self.table[curr_x][curr_y].get_figure().color == figure.color:
                                break # Свой блокирует путь
                            else:
                                found_enemy = True # Нашли врага, смотрим клетки ЗА ним
                    else:
                        # Мы уже перепрыгнули врага
                        if not self.table[curr_x][curr_y].has_figure():
                            jumps.append(Position(curr_x, curr_y))
                        else:
                            break # Путь закрыт другой фигурой
                    curr_x += dx
                    curr_y += dy
        else:
            # Логика обычной шашки
            for dx, dy in directions:
                mid_x, mid_y = pos.x + dx, pos.y + dy
                end_x, end_y = pos.x + 2 * dx, pos.y + 2 * dy
                if 0 <= end_x < 8 and 0 <= end_y < 8:
                    mid_cell = self.table[mid_x][mid_y]
                    end_cell = self.table[end_x][end_y]
                    if mid_cell.has_figure() and mid_cell.get_figure().color != figure.color and not end_cell.has_figure():
                        jumps.append(Position(end_x, end_y))
        return jumps

    def continue_jump(self, pos: Position):
        """Рекурсивная серия прыжков (комбо)"""
        jumps = self.get_available_jumps(pos)
        if not jumps: return
            
        if len(jumps) == 1:
            next_pos = jumps[0]
            self._execute_jump(pos, next_pos)
            print(colorize(f" АВТО-ПРЫЖОК: {pos.position} -> {next_pos.position} ", font=Colors.ORANGE))
            # После прыжка проверяем — не стали ли мы дамкой прямо сейчас
            fig = self.table[next_pos.x][next_pos.y].get_figure()
            self.check_promotion(fig, next_pos)
            self.continue_jump(next_pos) 
            
        else:
            self.print_table()
            jump_names = [j.position for j in jumps]
            print(colorize(f"\n Развилка! Можно прыгнуть на: {', '.join(jump_names)} ", font=Colors.GREEN))
            while True:
                choice = input("Ваш выбор: ").lower().strip()
                selected = next((j for j in jumps if j.position == choice), None)
                if selected:
                    self._execute_jump(pos, selected)
                    fig = self.table[selected.x][selected.y].get_figure()
                    self.check_promotion(fig, selected)
                    self.continue_jump(selected) 
                    break
                print(colorize(" Неверный ход! ", font=Colors.RED))


    def move_figure(self, position1: Position, position2: Position) -> bool:
        cell1 = self.table[position1.x][position1.y]
        figure = cell1.get_figure()
        
        if not figure: 
            return False

        # Получаем вердикт от фигуры (Checker или Queen)
        check = figure.check_move(position1, position2, self.table)

        if check == 'move':
            fig = cell1.extract_figure()
            self.table[position2.x][position2.y].set_figure(fig)
            self.check_promotion(fig, position2)
            return True # ХОД УСПЕШЕН -> Смена очереди
                
        elif check in ['eat', 'eat_checker']: 
            # 1. Выполняем само взятие (удаление врага)
            self._execute_jump(position1, position2)
            
            # 2. Берем фигуру в новой точке
            current_fig = self.table[position2.x][position2.y].get_figure()
            
            # 3. Проверяем превращение в дамку
            self.check_promotion(current_fig, position2)
            
            # 4. Проверяем на серию прыжков (комбо)
            # Даже если серия продолжается, текущий ввод d4 b6 УЖЕ ВАЛИДЕН
            self.continue_jump(position2)
            
            # САМОЕ ВАЖНОЕ: возвращаем True, чтобы Gamemanager увидел успех
            return True # ХОД УСПЕШЕН -> Смена очереди

        # Если дошли до этой строки, значит ход реально невозможен
        return False
    

    def check_promotion(self, figure, pos: Position):
        """Превращает в дамку (Queen)"""
        if not figure or isinstance(figure, Queen): return
        
        is_white_promo = (figure.color == Colors.WHITE and pos.x == 0)
        is_black_promo = (figure.color == Colors.BLACK and pos.x == 7)

        if is_white_promo or is_black_promo:
            self.table[pos.x][pos.y].change_figure(Queen)
            color_name = "БЕЛАЯ" if figure.color == Colors.WHITE else "ЧЕРНАЯ"
            # ЗАМЕНИ Colors.CYAN на Colors.GREEN (или проверь свои Colors в helper.py)
            print(colorize(f" {color_name} ШАШКА СТАЛА ДАМКОЙ! ", font=Colors.GREEN))

    # --- Остальные шахматные методы (try_check, is_checkmate) оставляем как есть ---
    def try_check(self):
        kings = []
        for x in range(8):
            for y in range(8):
                f = self.table[x][y].get_figure()
                if isinstance(f, King): kings.append((f, Position(x, y)))
        
        under_check = []
        for king, pos in kings:
            attackers = []
            for rx in range(8):
                for ry in range(8):
                    f = self.table[rx][ry].get_figure()
                    if f and f.color != king.color:
                        if f.check_move(Position(rx, ry), pos, self.table) in ['move', 'eat']:
                            attackers.append(Position(rx, ry))
            if attackers: under_check.append((king, pos, attackers))
        return under_check

    def is_checkmate(self, color: Colors) -> bool:
        checks = self.try_check()
        if not any(king.color == color for king, pos, attackers in checks): return False

        for fx in range(8):
            for fy in range(8):
                c_from = self.table[fx][fy]
                if c_from.has_figure() and c_from.get_figure().color == color:
                    p1 = Position(fx, fy)
                    for tx in range(8):
                        for ty in range(8):
                            p2 = Position(tx, ty)
                            if c_from.get_figure().check_move(p1, p2, self.table) in ['move', 'eat']:
                                c_to = self.table[tx][ty]
                                old_fig, mover = c_to.get_figure(), c_from.get_figure()
                                c_to.figure, c_from.figure = mover, None
                                still_check = any(k.color == color for k, p, a in self.try_check())
                                c_from.figure, c_to.figure = mover, old_fig
                                if not still_check: return False
        return True

    def get_longest_capture_path(self, pos: Position, current_path: list = None) -> list:
        if current_path is None: 
            current_path = []
        
        longest_path = []
        figure = self.table[pos.x][pos.y].get_figure()
        if not figure: 
            return longest_path

        # Проверяем 4 диагонали (шашки могут бить назад)
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dx, dy in directions:
            mid_x, mid_y = pos.x + dx, pos.y + dy
            end_x, end_y = pos.x + 2 * dx, pos.y + 2 * dy
            
            # Если прыжок не выходит за границы доски
            if 0 <= end_x < 8 and 0 <= end_y < 8:
                mid_cell = self.table[mid_x][mid_y]
                end_cell = self.table[end_x][end_y]
                
                # Если на пути враг, а за ним пусто — можно прыгать
                if mid_cell.has_figure() and mid_cell.get_figure().color != figure.color and not end_cell.has_figure():
                    
                    # 1. СИМУЛЯЦИЯ ПРЫЖКА (делаем ход)
                    eaten_fig = mid_cell.extract_figure()
                    self.table[end_x][end_y].set_figure(figure)
                    self.table[pos.x][pos.y].remove_figure()
                    
                    # 2. РЕКУРСИЯ (ищем прыжки дальше из новой точки)
                    new_path = current_path + [Position(end_x, end_y)]
                    path_from_here = self.get_longest_capture_path(Position(end_x, end_y), new_path)
                    
                    # Запоминаем самый длинный путь
                    if len(path_from_here) > len(longest_path):
                        longest_path = path_from_here
                        
                    # 3. ОТКАТ СИМУЛЯЦИИ (возвращаем доску как было для проверки других веток)
                    self.table[pos.x][pos.y].set_figure(figure)
                    self.table[end_x][end_y].remove_figure()
                    mid_cell.set_figure(eaten_fig)
                    
        # Если дальше прыгать некуда, возвращаем то, что накопили
        if not longest_path:
            longest_path = current_path
            
        return longest_path