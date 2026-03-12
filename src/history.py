import copy
from gpColor import colorize
from src.figure import Figure
from src.helper import Colors, Position
from src.player import Player

class MoveHistory:
    def __init__(self, from_pos: Position, to_pos: Position, figure: Figure, player: Player, move_type: str, table_state):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.figure = figure
        self.player = player
        self.move_type = move_type
        self.table_state = table_state

    def __str__(self):
        return f"[{self.player.name} ({self.player.id})] {colorize(self.figure.name, font = self.figure.color)} ({self.from_pos.position} -> {self.to_pos.position}) | {self.move_type}"

    def return_info(self):
        return str(self)

class History:
    moves = []
    killed = []

    @classmethod
    def add_move(cls, from_pos: Position, to_pos: Position, figure: Figure, player: Player, move_type: str, table_state):
        move = MoveHistory(from_pos, to_pos, figure, player, move_type, table_state)
        cls.moves.append(move)

    @classmethod
    def undo(cls, steps: int):
        state = None
        player = None
        steps = min(steps, len(cls.moves))
        if steps <= 0:
            return None, None
        for _ in range(steps):
            move = cls.moves.pop()
            state = move.table_state
            player = move.player
        return state, player

    @classmethod
    def add_killed(cls, figure):
        if isinstance(figure, Figure):
            cls.killed.append(figure)

    @classmethod
    def get_killed(cls, colors_list):
        if not isinstance(colors_list, list): return False
        return [x for x in cls.killed if x.color in colors_list]
    
    @classmethod
    def get_formatted_history(cls):
        return [f"{i+1}) {cls.moves[i]}\n" for i in range(len(cls.moves))]

    @classmethod
    def get_history(cls):
        return cls.moves
    
    @classmethod
    def last_move(cls):
        return cls.moves[-1].return_info() if cls.moves else None

    @classmethod
    def clear(cls):
        cls.moves.clear()
        cls.killed.clear()