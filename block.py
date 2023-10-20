import pygame
from colors import Colors
from position import Position

SRS:{int:{str:{int:(int,int)}}} = {
        0:{
            'clockwise':{0:(0,0),1:(0,-1),2:(1,-1),3:(2,0),4:(2,-1)},
            'anticlockwise':{0:(0,0),1:(0,1),2:(-1,1),3:(2,0),4:(2,1)}
        },
        1:{
            'clockwise':{0:(0,0),1:(0,1),2:(1,1),3:(-2,0),4:(-2,1)},
            'anticlockwise':{0:(0,0),1:(0,1),2:(1,1),3:(-2,0),4:(-2,1)}
        },    
        2:{
            'clockwise':{0:(0,0),1:(0,1),2:(-1,1),3:(2,0),4:(2,1)},
            'anticlockwise':{0:(0,0),1:(0,-1),2:(-1,-1),3:(2,0),4:(2,-1)}
        },
        3:{
            'clockwise':{0:(0,0),1:(0,-1),2:(1,-1),3:(-2,0),4:(-2,-1)},
            'anticlockwise':{0:(0,0),1:(0,-1),2:(1,-1),3:(-2,0),4:(-2,-1)}
        },    
    }

SRSI:{int:{str:{int:(int,int)}}} = {
        0:{
            'clockwise':{0:(0,0),1:(0,-2),2:(0,1),3:(1,-2),4:(-2,1)},
            'anticlockwise':{0:(0,0),1:(0,-1),2:(0,2),3:(-2,-1),4:(1,2)}
        },
        1:{
            'clockwise':{0:(0,0),1:(0,-1),2:(0,2),3:(-2,-1),4:(1,2)},
            'anticlockwise':{0:(0,0),1:(0,2),2:(0,-1),3:(-1,2),4:(2,-1)}
        },    
        2:{
            'clockwise':{0:(0,0),1:(0,2),2:(0,-1),3:(-1,2),4:(2,-1)},
            'anticlockwise':{0:(0,0),1:(0,1),2:(0,-2),3:(2,1),4:(-1,-2)}
        },
        3:{
            'clockwise':{0:(0,0),1:(0,1),2:(0,-2),3:(2,1),4:(-1,-2)},
            'anticlockwise':{0:(0,0),1:(0,-2),2:(0,1),3:(1,-2),4:(-2,1)}
        },    
    }

class Block:
    def __init__(self, id:int)->None:
        self.id = id
        self.cells: {int:[Position]} = {}
        self.cell_size: int = 30
        self.colors = Colors.get_cell_colors()
        self.draw_offset: int = 1
        self.reset()
    
    def reset(self)->None:
        self.rotation_states:[int] = [0,1,2,3]
        self.column_offset:int = 3
        self.row_offset:int = -2
    
    def move(self, rows:int, cols: int)->None:
        self.row_offset += rows
        self.column_offset += cols
        
    def get_cell_positions(self)->[Position]:
        tiles:[Position] = self.cells[self.rotation_states[0]]
        return [Position(position.row + self.row_offset, position.column + self.column_offset) for position in tiles]
        
    def rotate_clockwise(self)->None:
        self.rotation_states = self.rotation_states[1:] + self.rotation_states[:1]
        
    def rotate_anticlockwise(self)->None:
        self.rotation_states = self.rotation_states[-1:] + self.rotation_states[:-1]
        
    def wall_kick(self,test_number:int,direction:str)->(int,int):
        if id == 4: return (0,0)
        elif id == 3: return SRSI[self.rotation_states[0]][direction][test_number]
        else:
            return SRS[self.rotation_states[0]][direction][test_number]
        
    def draw(self, screen:pygame.Surface, offset_x, offset_y, fill:int = 0)->None:
        tiles:[Position] = self.get_cell_positions()
        for tile in tiles:
            if tile.is_in_screen():
                tile_rect = pygame.Rect(tile.column * self.cell_size + self.draw_offset + offset_x,
                                    tile.row * self.cell_size + self.draw_offset + offset_y,
                                    self.cell_size - self.draw_offset,
                                    self.cell_size - self.draw_offset)
                pygame.draw.rect(screen, self.colors[self.id], tile_rect,fill,5)