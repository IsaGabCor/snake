import numpy as np
import random 
from Agent import Agent
from Agent import manhattan_distance
from Snake import Snake


GRID_SIZE = 20
MAX_STEPS = 500

@property
def head(self):
    return self.body[0]

def spawn_food(snake):
    while True:
        pos = (
            random.randint(0, GRID_SIZE - 1),
            random.randint(0, GRID_SIZE - 1),
        )
        if pos not in snake.body:
            return pos

def get_new_direction(current_direction, action):
    directions = ['UP', 'RIGHT', 'DOWN', 'LEFT']
    idx = directions.index(current_direction)

    if action == 0:
        return directions[idx]
    elif action == 1:
        return directions[(idx + 1) % 4]
    elif action == 2:
        return directions[(idx - 1) % 4]

def hit_self(self):
    return self.body[0] in self.body[1:]

def hit_wall(self, grid_size):
    head_x, head_y = self.body[0]
    return head_x < 0 or head_x >= grid_size or head_y < 0 or head_y >= grid_size

def run_game(brain):
    """
    Runs one full snake game controlled by the given brain.
    Returns a fitness score (float).
    """

    #Initialize game objects
    snake = Snake(length=3, direction='RIGHT', position=(10, 10))
    agent = Agent(brain)

    food = spawn_food(snake)
    steps = 0
    score = 0
    steps_since_food = 0
    hunger_limit = GRID_SIZE * 0.75
    turn_penalty = 0.02
    dist_reward = 0.4
    dist_penalty = -0.4
    FOOD_REWARD = 50
    SURVIVAL_REWARD = 0.005
    DEATH_PENALTY = 100
    fitness = 0

    while True:
        steps += 1
        steps_since_food += 1

        #Get state
        state = agent.get_state(snake, food, 'RIGHT')
        state = np.array(state, dtype=float)

        #Brain decides action
        output = brain.forward(state)
        action = np.argmax(output)

        #get distance of food for rewarding before move()
        prev_dist = manhattan_distance(snake.body[0], food)

        #Apply action
        old_dir = snake.direction
        new_dir = get_new_direction(snake.direction, action)
        if new_dir != old_dir :
            fitness -= turn_penalty 
        snake.change_direction(new_dir)
        snake.move()

        #get distance of food for rewarding
        new_dist = manhattan_distance(snake.body[0], food)
        if new_dist < prev_dist:
            fitness += dist_reward
        elif new_dist > prev_dist:
            fitness += dist_penalty

        #Check collisions
        if hit_wall(snake, GRID_SIZE) or hit_self(snake):
            fitness -= DEATH_PENALTY
            break

        #Check food
        # Check if snake has eaten the food
        if snake.body[0] == food:
            snake.grow()
            food = spawn_food(snake)
            fitness += FOOD_REWARD * (score + 1) ** 2
            score += 1
            steps_since_food = 0

        #Starvation cutoff (prevents infinite loops)
        if steps_since_food > hunger_limit:
            fitness -= DEATH_PENALTY
            break

        #Absolute step limit
        if steps >= MAX_STEPS:
            break

        fitness += SURVIVAL_REWARD

    ##print(fitness)
    return fitness