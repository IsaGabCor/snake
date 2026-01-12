import pygame
import random
import sys
import Snake
import Agent
import numpy as np
import pickle
from Snake_logic import get_new_direction
from Agent import relative_to_absolute


#initialize pygame
pygame.init()
pygame.mixer.init()

#open logs
with open("gen_logs/best_brain.pkl", "rb") as f:
    brain = pickle.load(f)

#define constants
SNAKE_SIZE = 20
BORDER_SIZE = 18
FOOD_SIZE = 20
FPS = 5
MAX_WIDTH = 400 #used for window size
MAX_HEIGHT = 400 #used for window size
GRID_WIDTH = 20 #actual game "board"
GRID_HEIGHT = 20 #actual game "board"
GRID_SIZE = 20

#colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (160, 232, 203)

## Initialize game window
pygame.display.set_caption("Snake Game")
screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
clock = pygame.time.Clock()

#load assets
lvlup_sound = pygame.mixer.Sound("assets/lvlup.wav")
game_over_sound = pygame.mixer.Sound("assets/gameover.wav")

#initialize game variables
snake_body = [[10, 10], [9, 10], [8, 10]]
food_pos = [random.randrange(1, GRID_WIDTH), random.randrange(1, GRID_HEIGHT)]
food_spawn = True
direction = 'RIGHT'
score = 0
gameover = False
running = True

#initialize AI agent
ai_mode = False
agent_instance = Agent.Agent(brain)
#initialize snake
snk = Snake.Snake(length=3, direction='RIGHT', position=(10,10))

#define helper functions
def collision_with_boundaries(snake_head):
    if snake_head[0] >= GRID_WIDTH or snake_head[0] < 0 or snake_head[1] >= GRID_HEIGHT or snake_head[1] < 0:
        return True
    return False

def collision_with_self(snake_body):
    head = snake_body[0]
    if head in snake_body[1:]:
        return True
    return False

def has_eaten_food(snake_head, food_pos):
    if snake_head[0] == food_pos[0] and snake_head[1] == food_pos[1]:
        snk.grow()
        lvlup_sound.play()
        global score 
        score += 1
        return True
    return False

def draw_score():
    font = pygame.font.SysFont('Impact', 25)
    score_surface = font.render(f'Score : {score}', True, BLACK)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (10, 10)
    screen.blit(score_surface, score_rect)

def game_over():
    screen.fill(BLACK)
    font = pygame.font.SysFont('Impact', 50)
    game_over_surface = font.render('GAME OVER', True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (MAX_WIDTH / 2, MAX_HEIGHT / 4)
    screen.blit(game_over_surface, game_over_rect)
    score_surface = font.render(f'Score : {score}', True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (MAX_WIDTH / 2, MAX_HEIGHT / 2)
    screen.blit(score_surface, score_rect)
    restart_surface = font.render('Press Y to restart', True, WHITE)
    restart_rect = restart_surface.get_rect()
    restart_rect.midtop = (MAX_WIDTH / 2, MAX_HEIGHT / 1.5)
    screen.blit(restart_surface, restart_rect)

def turn_mapping(action, current_direction):
        #print("Agent State:", action)
        agent_action = agent_instance.act(action)
        #print("Agent Action:", agent_action)
        if action == 'STRAIGHT':
            return current_direction
        if current_direction == 'UP':
            return 'LEFT' if action == 'LEFT' else 'RIGHT'
        if current_direction == 'DOWN':
            return 'RIGHT' if action == 'LEFT' else 'LEFT'
        if current_direction == 'LEFT':
            return 'DOWN' if action == 'LEFT' else 'UP'
        if current_direction == 'RIGHT':
            return 'UP' if action == 'LEFT' else 'DOWN'
        
def spawn_food(snake):
    while True:
        pos = (
            random.randint(0, GRID_SIZE - 1),
            random.randint(0, GRID_SIZE - 1),
        )
        if pos not in snake.body:
            return pos               

#main game loop
while running:
    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if not ai_mode:
                if event.key == pygame.K_w:
                    direction = 'UP'
                elif event.key == pygame.K_s:
                    direction = 'DOWN'
                elif event.key == pygame.K_a:
                    direction = 'LEFT'
                elif event.key == pygame.K_d:
                    direction = 'RIGHT'
            if event.key == pygame.K_f:
                # Toggle AI mode
                print("Toggling AI mode")
                ai_mode = not ai_mode


    #per frame updates
    screen.fill(BACKGROUND_COLOR)  # Fill the screen with background color
    if ai_mode:
        state_vector = agent_instance.get_state(
            snk,
            food_pos,
            snk.direction
        )
        #print(state_vector)
        # get action from the agent's state
        action = np.argmax(brain.forward(state_vector))
        new_direction = relative_to_absolute(snk.direction, action)
        snk.change_direction(new_direction)
        snk.move()
        out = brain.forward(state_vector)
        print("NN:", out, " Action:", np.argmax(out))
    else:
        snk.change_direction(direction)
        snk.move()

    # Check for collisions with walls
    running = running and not collision_with_boundaries(snk.body[0])
    # Check for collisions with itself
    running = running and not collision_with_self(snk.body)
    # Check if snake has eaten the food
    food_spawn = not has_eaten_food(snk.body[0], food_pos)
     #spawn food
    if not food_spawn:
        food_pos = spawn_food(snk)

    #draw snake
    for pos in snk.body:
        pygame.draw.rect(screen, BLACK, pygame.Rect(pos[0] * SNAKE_SIZE, pos[1] * SNAKE_SIZE, SNAKE_SIZE, SNAKE_SIZE))
    
    #draw food
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0] * FOOD_SIZE, food_pos[1] * FOOD_SIZE, FOOD_SIZE, FOOD_SIZE))
    #draw score
    draw_score()
    # Update the display
    pygame.display.update()
    # Control the frame rate
    clock.tick(FPS)
    
    #game over handling
    if not running:
        game_over_sound.play()
        # Game over screen
        game_over()
        pygame.display.update()
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_restart = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        # Reset game variables
                        snake_body = [[10, 10], [9, 10], [8, 10]]
                        snk = Snake.Snake(length=3, direction='RIGHT', position=(10,10))
                        food_pos = [random.randrange(1, GRID_WIDTH), random.randrange(1, GRID_HEIGHT)]
                        food_spawn = True
                        direction = 'RIGHT'
                        score = 0
                        running = True
                        waiting_for_restart = False


pygame.quit()