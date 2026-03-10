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
            return colorize(text=self.figure, back=self.color)
        else:
            return colorize(text="   ", back=self.color)
    
    def get_figure(self):
        return self.figure
    
    def set_figure(self, figure: Figure):
        self.figure = figure


    def change_figure(self, figure_class): 
        if not self.has_figure(): return False
        
        self.figure = figure_class(color = self.figure.color)
        print(f"ФИГУРА ПРЕВРАТИЛАСЬ В {self.figure.name}")
        return True
    
    
    def remove_figure(self):
        self.figure = None

    def extract_figure(self) -> Figure:
        figure = self.figure
        self.remove_figure()
        return figure

    def has_figure(self):
        return self.figure is not None     

class NoneCell(Cell):
    def __init__(self):
        super().__init__(None, None)
        self.can_move_on = False

    def __str__(self):
        return "   "