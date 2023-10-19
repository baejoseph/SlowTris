import pygame

from grid import Grid
from position import Position
from block import Block
from blocks import LBlock,IBlock,SBlock,JBlock,OBlock,TBlock,ZBlock
import random
from copy import copy


class Game:
    def __init__(self, offset:int = 10)->None:
        self.grid:Grid = Grid(offset)
        self.screen_offset = offset
        self.rotate_sound = pygame.mixer.Sound('Sound/rotate-piece.wav')
        self.move_sound = pygame.mixer.Sound('Sound/move-piece.wav')
        self.clear_sound = pygame.mixer.Sound('Sound/line-clear.wav')
        self.tetris_sound = pygame.mixer.Sound('Sound/tetris-clear.wav')
        self.game_over_sound = pygame.mixer.Sound('Sound/game-over.wav')
        self.landing_sound = pygame.mixer.Sound('Sound/piece-landed.wav')
        self.harddrop_sound = pygame.mixer.Sound('Sound/harddrop.wav')
        pygame.mixer.music.load('Sound/tetris-gameboy-02.mp3')
        pygame.mixer.music.play(-1)
        self.reset()

    def reset(self)->None:
        self.grid.reset()
        self.refill_bag()
        self.current_block: Block = self.get_random_block()
        self.get_current_ghost()
        self.next_block: Block = self.get_random_block()
        self.hold_block: Block = None
        self.score: int = 0
        self.game_over: bool = False

    def update_score(self, lines_cleared:str, move_down_points:int=0)->None:
        self.score += move_down_points
        if lines_cleared == 'single': self.score += 100
        if lines_cleared == 'double': self.score += 300
        if lines_cleared == 'triple': self.score += 500
        if lines_cleared == 'tetris': self.score += 800
        if lines_cleared == 'single T-spin': self.score += 800
        if lines_cleared == 'double T-spin': self.score += 1200
        if lines_cleared == 'triple T-spin': self.score += 1600
        
    def get_random_block(self)->Block:
            if len(self.blocks)==0: 
                self.refill_bag()
            return self.blocks.pop()
        
    def refill_bag(self)->None:
        self.blocks:[Block] = [LBlock(),JBlock(),IBlock(),OBlock(),SBlock(),TBlock(),ZBlock()]
        random.shuffle(self.blocks)

    def get_current_ghost(self)->None:
        self.current_ghost: Block = copy(self.current_block)
        self.ghost_fits()
    
    def ghost_fits(self)->None:
        for row in range(max(self.current_block.row_offset,2), self.grid.num_rows):
            self.current_ghost.row_offset = row
            self.current_ghost.move(1,0)
            if self.block_fits(self.current_ghost) == False:
                self.current_ghost.move(-1,0)
                break
    
    def hold_piece(self)->None:
        self.temp_block = copy(self.current_block)
        self.temp_block.reset()
        if self.temp_block.id == 4: self.temp_block.column_offset = 4
        if self.hold_block is not None:
            self.current_block = self.hold_block
        else:
            self.current_block = self.next_block
            self.next_block = self.get_random_block()
        self.get_current_ghost()
        self.hold_block = self.temp_block
            
    def move_left(self)->None:
        self.current_block.move(0,-1)
        self.current_ghost.move(0,-1)
        if self.block_fits()==False:
            self.current_block.move(0,1)
            self.current_ghost.move(0,1)
        self.move_sound.play()
        self.ghost_fits()
        
    def move_right(self)->None:
        self.current_block.move(0,1)
        self.current_ghost.move(0,1)
        if self.block_fits()==False:
            self.current_block.move(0,-1)
            self.current_ghost.move(0,-1)
        self.move_sound.play()
        self.ghost_fits()
        
    def move_down(self)->None:
        self.fall_down()
        self.move_sound.play()
        self.update_score('',1)
        
    def fall_down(self)->None:
        self.current_block.move(1,0)
        if self.block_fits()==False:
            self.current_block.move(-1,0)
            self.lock_block()
            
    def hard_drop(self)->None:
        self.update_score('',2*(self.current_ghost.row_offset - self.current_block.row_offset))
        self.current_block.row_offset = self.current_ghost.row_offset
        self.lock_block()
            
    def lock_block(self)->None:
        self.landing_sound.play()
        tiles:[Position] = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        cleared_rows:int = self.grid.clear_full_rows()
        if cleared_rows > 0:
            self.clear_sound.play()
            if cleared_rows == 1: self.update_score('single')
            if cleared_rows == 2: self.update_score('double')
            if cleared_rows == 3: self.update_score('triple')
            if cleared_rows == 4: 
                self.tetris_sound.play()
                self.update_score('tetris')
        if self.grid.game_over():
            self.game_over_sound.play()
            self.game_over = True
        self.current_block = self.next_block
        self.get_current_ghost()
        self.next_block = self.get_random_block()
        
    def rotate_clockwise(self)->None:
        for test_number in range(5):
            row,col = self.current_block.wall_kick(test_number, 'clockwise')
            self.current_block.move(row,col)
            self.current_block.rotate_clockwise()
            if self.block_fits(): 
                self.rotate_sound.play()
                self.current_ghost.move(row,col)
                self.current_ghost.rotate_clockwise()
                self.ghost_fits()
                break
            else: 
                self.current_block.move(-row,-col)
                self.current_block.rotate_anticlockwise()

    def rotate_anticlockwise(self)->None:
        for test_number in range(5):
            row,col = self.current_block.wall_kick(test_number, 'anticlockwise')
            self.current_block.rotate_anticlockwise()
            self.current_block.move(row,col)
            if self.block_fits():
                self.rotate_sound.play()
                self.current_ghost.rotate_anticlockwise()
                self.current_ghost.move(row,col)
                self.ghost_fits()
                break
            else: 
                self.current_block.move(-row,-col)
                self.current_block.rotate_clockwise()
        
    def block_fits(self, block:Block=None)->bool:
        if block is None: block = self.current_block
        tiles:[Position] = block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True
                
    def draw(self,screen:pygame.Surface):
        self.grid.draw(screen)
        self.current_block.draw(screen,self.screen_offset,self.screen_offset)
        self.current_ghost.draw(screen, self.screen_offset, self.screen_offset, 1)
        
        next_offset_x, next_offset_y = 270, 200
        if self.next_block.id == 3: next_offset_x, next_offset_y = 255, 220
        if self.next_block.id == 4: next_offset_x, next_offset_y = 255, 210
        self.next_block.draw(screen,next_offset_x, next_offset_y)
        
        if self.hold_block is not None:
            hold_offset_x,hold_offset_y = 270, 400
            if self.hold_block.id == 3: hold_offset_x, hold_offset_y = 255, 420
            if self.hold_block.id == 4: hold_offset_x, hold_offset_y = 255, 410
            self.hold_block.draw(screen,hold_offset_x, hold_offset_y)
        