from src.errors import *

class Position:
    def __init__(self, *position):
        print(position)
        if len(position) == 1:
            x, y = self._convert_xy(position[0])

            if self._validate_pos((x, y)) == True:
                self.x, self.y = x, y
                self.position = position[0]
            else:
                raise WrongPositionError()
        if len(position) == 2:
            x, y = [int(x) for x in position]

            if self._validate_pos((x, y)) == True:
                self.x, self.y = x, y
                self.position = self._convert_a(x, y)
            else:
                raise WrongPositionError()
        else:
            raise WrongPositionError()

    def __str__(self):
        return f"{self.position} ({self.x}, {self.y})"


    def _validate_pos(self, pos: tuple):
        if len(pos) == 2 and all(isinstance(x, int) and x > -1 for x in pos):
            return True
        return False
    
    def _convert_xy(self, position: str):
        letter = position[0]
        number = position[1]

        y = ord(letter) - ord('a')
    
        x = 8 - int(number)
        
        return (x, y)
    
    def _convert_a(self, x: int, y: int) -> str:
        if not (0 <= x < 8 and 0 <= y < 8):
            raise WrongPositionError()
        
        letter = chr(ord('a') + y)
        
        number = str(8 - x)
        
        return f"{letter}{number}"
        
    
    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.position == other.position
    
    def __ne__(self, other):
        if not isinstance(other, Position):
            return True
        return self.position != other.position





    
class Colors():
    BLACK = "#000000"
    WHITE = "#FFFFFF"

    DARK = "#7b6c55"
    MIDDLE = "#a28355"
    LIGHT = "#d8b984"

    GREEN = "#16D408"
    RED = "#FF4343"
