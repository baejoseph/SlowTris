class Position:
    def __init__(self, row:int, col:int)-> None:
        self.row = row
        self.column = col
    def is_in_screen(self)->bool:
        return self.row >= 0