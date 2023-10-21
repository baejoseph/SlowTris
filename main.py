import pygame, sys, time

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
initial_hold_key_delay: int = 200
down_key_down:bool = False
left_key_down:bool = False
right_key_down:bool = False
display_move_name:int = 1500
last_move_count = 0
move_name_timer = time.time()

screen:pygame.Surface = pygame.display.set_mode((width, height))
pygame.display.set_caption("baejoseph’s Slowtris")

clock:pygame.Clock = pygame.time.Clock()
game:Game = Game(screen_offset)

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, fall_delay)

while True:
    
    for event in pygame.event.get():
        if event.type == GAME_UPDATE:
            game.fall_down()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            hold_key_delay = initial_hold_key_delay
            if game.game_over == True:
                game.game_over = False
                game.reset()
            if event.key == pygame.K_LEFT: 
                game.move_left()
                left_key_timer = time.time()
                left_key_down = True
            if event.key == pygame.K_RIGHT: 
                game.move_right()
                right_key_timer = time.time()
                right_key_down = True
            if event.key == pygame.K_DOWN and not down_key_down: 
                game.move_down()
                down_key_timer = time.time()
                down_key_down = True
            if event.key == pygame.K_UP: game.rotate_clockwise()
            if event.key == pygame.K_x: game.rotate_clockwise()
            if event.key == pygame.K_z: game.rotate_anticlockwise()
            if event.key == pygame.K_SPACE: game.hard_drop()
            if event.key == pygame.K_RSHIFT: game.hold_piece()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN: 
                down_key_down = False
            if event.key == pygame.K_LEFT: 
                left_key_down = False
            if event.key == pygame.K_RIGHT: 
                right_key_down = False
    if  (down_key_down == True) and (1000*(time.time() - down_key_timer) > hold_key_delay): 
        game.move_down()
        down_key_timer = time.time()
        hold_key_delay = 0.2 * initial_hold_key_delay
    if  (left_key_down == True) and (1000*(time.time() - left_key_timer) > hold_key_delay): 
        game.move_left()
        left_key_timer = time.time()
        hold_key_delay = 0.2 * initial_hold_key_delay
    if  (right_key_down == True) and (1000*(time.time() - right_key_timer) > hold_key_delay): 
        game.move_right()
        right_key_timer = time.time()
        hold_key_delay = 0.2 * initial_hold_key_delay
    
    #Drawing: Score
    score_value_surface = title_font.render(str(game.score.get_score()), True, Colors.white)
    screen.blit(score_surface, (365,20,50,50))
    
    pygame.draw.rect(screen,Colors.light_blue, score_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(
                                                        centerx = score_rect.centerx,
                                                        centery = score_rect.centery
                                                        ))
    
    #Displaying Move Name for display_move_name ms.
    b2b_display, move_name_display = game.score.get_move_name()
    
    b2b_surface = title_font.render(b2b_display, True, Colors.white)
    move_name_surface = title_font.render(move_name_display, True, Colors.white)
    
    if game.move_count > last_move_count:
        last_move_count = game.move_count
        move_name_timer = time.time()
    
    if 1000*(time.time() - move_name_timer) < display_move_name:
        screen.blit(b2b_surface, move_name_surface.get_rect(centerx = 375, centery = 520))
        screen.blit(move_name_surface, move_name_surface.get_rect(centerx = 375, centery = 550))
    
    #Drawing
    screen.fill(Colors.dark_blue)
    
    screen.blit(next_surface, (375,130,50,50))
    screen.blit(hold_surface, (375,330,50,50))
    pygame.draw.rect(screen,Colors.light_blue, next_rect, 0, 10)
    pygame.draw.rect(screen,Colors.light_blue, hold_rect, 0, 10)
    
    game.draw(screen)
    
    if game.game_over == True:
        screen.blit(game_over_surface, (35,250,50,50))
    
    pygame.display.update()
    clock.tick(fps)
    
    