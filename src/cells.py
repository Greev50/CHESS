from enum import Enum
from gpColor import colorize

from src.figure import *
from src.helper import Colors


class Cell():
    def __init__(self, color: Colors, figure: Figure = None):
        self.color = color
        self.figure = figure
        self.can_move_on = True

    def __str__(self):
        if self.figure and not isinstance(self.figure, NoneFigure):
            figure_color = self.figure.color
            bold_text = f"\033[1m {self.figure.icon} \033[0m"

            return colorize(text=bold_text, font=figure_color, back=self.color)
        else:
            return colorize(text="   ", back=self.color)

    
    def get_figure(self):
        return self.figure
    
    def set_figure(self, figure: Figure):
        if not isinstance(self.figure, NoneFigure):
            self.figure = figure
    
    def remove_figure(self):
        self.figure = None

    def extract_figure(self) -> Figure:
        figure = self.figure
        self.remove_figure()

        return figure
        

    def has_figure(self):
        return self.figure != None        

class NoneCell(Cell):
    def __init__(self):
        super().__init__(None, None)
        self.can_move_on = False

    def __str__(self):
        return "   "