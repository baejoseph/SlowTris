import pygame
from colors import Colors
color = (int,int,int)

class Grid:
    def __init__(self, offset:int = 10)->None:
        self.num_rows:int = 20
        self.num_cols:int = 10
        self.cell_size:int = 30
        self.screen_offset: int = offset
        self.draw_offset: int = 1
        self.reset()
        self.colors:[color] = Colors.get_cell_colors()
        self.piece_falling_after_line_clear_sound = pygame.mixer.Sound('Sound/piece-falling-after-line-clear.wav')
        
    def print_grid(self)->None:
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                print(self.grid[row][col], end=" ")
            print()
            
    def is_inside(self, row:int, col:int)->bool:
        if row >=-3 and row < self.num_rows and col >=0 and col < self.num_cols:
            return True
        return False
    
    def is_empty(self, row:int, col:int)->bool:
        if self.grid[row][col]==0: return True
        else: return False
    
    def is_row_full(self,row:int)->bool:
        for col in range(self.num_cols):
            if self.grid[row][col] == 0: return False
        return True
    
    def clear_row(self,row:int)->None:
        for col in range(self.num_cols):
            self.grid[row][col] = 0
            
    def move_row_down(self,row:int,by:int)->None:
        for col in range(self.num_cols):
            self.grid[row+by][col] = self.grid[row][col]
            self.grid[row][col] = 0
            
    def clear_full_rows(self)->int:
        cleared_rows: int = 0
        for row in range(self.num_rows-1,0,-1):
            if self.is_row_full(row):
                self.clear_row(row)
                cleared_rows += 1
            elif cleared_rows > 0:
                self.move_row_down(row,cleared_rows)
        return cleared_rows
            
    def game_over(self)->bool:
        if self.grid[0][5] > 0 or self.grid[0][6] > 0 : 
            return True
        return False
    
    def reset(self):
        self.grid:[[int]] = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
    
    def draw(self, screen:pygame.Surface)->None:
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell_value = self.grid[row][col]
                cell_rect = pygame.Rect(col*self.cell_size + self.draw_offset + self.screen_offset,
                                        row*self.cell_size + self.draw_offset + self.screen_offset,
                                        self.cell_size - self.draw_offset,
                                        self.cell_size - self.draw_offset)
                pygame.draw.rect(screen, self.colors[cell_value],cell_rect)
                
