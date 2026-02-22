from gpColor import colorize

from src.helper import Colors

class Player:
    def __init__(self, id: int, color: Colors = Colors.WHITE):
        self.id = id
        self.name: str = f"Игрок {id}"
        self.color: Colors = color

    def set_name(self, name):
        if isinstance(str, name):
            self.name = name

    def set_color(self, color: Colors):
        self.color = color

    def return_name(self):
        return f"{self.name} ({colorize("•", font = self.color)})"

    def return_info(self):
        return colorize(f"Игрок {self.name} ({self.id})", font = self.color)