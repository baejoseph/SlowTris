import pygame, sys

from game import Game
from colors import Colors

pygame.init()

title_font = pygame.font.Font(None, 40)
game_over_font = pygame.font.Font(None, 60)

score_surface = title_font.render("Score",True, Colors.white)
next_surface = title_font.render("Next",True, Colors.white)
hold_surface = title_font.render("Hold",True, Colors.white)
game_over_surface = game_over_font.render("GAME OVER", True, Colors.white)

score_rect = pygame.Rect(320,55,170,60)
next_rect = pygame.Rect(320,165,170,140)
hold_rect = pygame.Rect(320,365,170,140)

width:int = 500
height:int = 620
screen_offset:int = 10
fps:int = 60
fall_delay: int = 600000
hold_key_delay: int = 100

screen:pygame.Surface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Python Tetris")

clock:pygame.Clock = pygame.time.Clock()
game:Game = Game(screen_offset)

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, fall_delay)

KEY_UPDATE = pygame.USEREVENT
pygame.time.set_timer(KEY_UPDATE, hold_key_delay)

down_key_down:bool = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game.game_over == True:
                game.game_over = False
                game.reset()
            if event.key == pygame.K_LEFT: game.move_left()
            if event.key == pygame.K_RIGHT: game.move_right()
            if event.key == pygame.K_DOWN: down_key_down = True
            if event.key == pygame.K_UP: game.rotate_clockwise()
            if event.key == pygame.K_x: game.rotate_clockwise()
            if event.key == pygame.K_z: game.rotate_anticlockwise()
            if event.key == pygame.K_SPACE: game.hard_drop()
            if event.key == pygame.K_RSHIFT: game.hold_piece()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN: down_key_down = False
        #if event.type == GAME_UPDATE and game.game_over == False:
        #    game.move_down()
        if event.type == KEY_UPDATE and down_key_down == True: 
            game.move_down()        
    #Drawing
    score_value_surface = title_font.render(str(game.score), True, Colors.white)
    
    screen.fill(Colors.dark_blue)
    screen.blit(score_surface, (365,20,50,50))
    screen.blit(next_surface, (375,130,50,50))
    screen.blit(hold_surface, (375,330,50,50))
    
    pygame.draw.rect(screen,Colors.light_blue, score_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(
                                                        centerx = score_rect.centerx,
                                                        centery = score_rect.centery
                                                        ))
    pygame.draw.rect(screen,Colors.light_blue, next_rect, 0, 10)
    pygame.draw.rect(screen,Colors.light_blue, hold_rect, 0, 10)
    game.draw(screen)
    
    if game.game_over == True:
        screen.blit(game_over_surface, (35,250,50,50))
    
    pygame.display.update()
    clock.tick(fps)
    
    