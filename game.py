import pygame

from grid import Grid
from score import Tally
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
        self.reset()

    def reset(self)->None:
        pygame.mixer.music.load('Sound/tetris-gameboy-02.mp3')
        pygame.mixer.music.play(-1)
        self.grid.reset()
        self.refill_bag()
        self.current_block: Block = self.get_random_block()
        self.get_current_ghost()
        self.next_block: Block = self.get_random_block()
        self.hold_block: Block = None
        self.move_count: int = 0
        self.game_over: bool = False
        self.swapped_out: bool = False
        self.score: Tally = Tally()
        
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
    
    def block_fits(self, block:Block=None)->bool:
        if block is None: block = self.current_block
        tiles:[Position] = block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        for tile in [x for x in tiles if x.is_in_screen()]:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True
    
    def ghost_fits(self)->None:
        for row in range(max(self.current_block.row_offset,-2), self.grid.num_rows):
            self.current_ghost.row_offset = row
            self.current_ghost.move(1,0)
            if self.block_fits(self.current_ghost) == False:
                self.current_ghost.move(-1,0)
                break
    
    def hold_piece(self)->None:
        if self.swapped_out:
            return None
        else:
            self.swap_out_piece()
            self.swapped_out = True
        
    def swap_out_piece(self)->None:
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
        self.score.move_down_points(1)
        
    def fall_down(self)->None:
        self.current_block.move(1,0)
        if self.block_fits()==False:
            self.current_block.move(-1,0)
            self.lock_block()
        self.score.tspin = False
            
    def hard_drop(self)->None:
        lines_dropped = (self.current_ghost.row_offset - self.current_block.row_offset)
        if lines_dropped > 0: self.score.tspin = False
        self.score.move_down_points(2*lines_dropped)
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
            self.score.increment_combo()
            self.score.update(cleared_rows)
            self.move_count += 1
            if cleared_rows == 4:
                self.tetris_sound.play()
            self.score.tspin = False
        else: self.score.reset_combo()
        if self.grid.game_over():
            self.game_over_sound.play()
            pygame.mixer.music.stop()
            pygame.mixer.music.load('Sound/tetris-gameboy-05.mp3')
            pygame.mixer.music.play(-1)
            self.game_over = True
        self.swapped_out = False
        self.current_block = self.next_block
        self.get_current_ghost()
        self.next_block = self.get_random_block()
        
    def rotate_clockwise(self)->None:
        for test_number in range(5):
            row,col = self.current_block.wall_kick(test_number, 'clockwise')
            self.current_block.move(row,col)
            self.current_block.rotate_clockwise()
            if self.block_fits(): 
                if self.current_block.id == 6:
                    self.score.is_tspin()
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
                if self.current_block.id == 6:
                    self.score.is_tspin()
                self.rotate_sound.play()
                self.current_ghost.rotate_anticlockwise()
                self.current_ghost.move(row,col)
                self.ghost_fits()
                break
            else: 
                self.current_block.move(-row,-col)
                self.current_block.rotate_clockwise()
                
    def draw(self,screen:pygame.Surface)->None:
        self.grid.draw(screen)
        self.current_block.draw(screen,self.screen_offset,self.screen_offset)
        self.current_ghost.draw(screen, self.screen_offset, self.screen_offset, 1)
        
        next_offset_x, next_offset_y = 270, 260
        if self.next_block.id == 3: next_offset_x, next_offset_y = 255, 280
        if self.next_block.id == 4: next_offset_x, next_offset_y = 255, 270
        self.next_block.draw(screen,next_offset_x, next_offset_y)
        
        if self.hold_block is not None:
            hold_offset_x,hold_offset_y = 270, 460
            if self.hold_block.id == 3: hold_offset_x, hold_offset_y = 255, 480
            if self.hold_block.id == 4: hold_offset_x, hold_offset_y = 255, 470
            self.hold_block.draw(screen,hold_offset_x, hold_offset_y)