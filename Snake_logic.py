import numpy as np
import random 
from Agent import Agent
from Snake import Snake


GRID_SIZE = 20
MAX_STEPS = 200

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

    while True:
        steps += 1
        steps_since_food += 1

        #Get state
        state = agent.get_state(snake, food, 'RIGHT')
        state = np.array(state, dtype=float)

        #Brain decides action
        output = brain.forward(state)
        action = np.argmax(output)

        #Apply action
        new_dir = get_new_direction(snake.direction, action)
        snake.change_direction(new_dir)
        snake.move()

        #Check collisions
        if hit_wall(snake, GRID_SIZE) or hit_self(snake):
            break

        #Check food
        # Check if snake has eaten the food
        if snake.body[0] == food:
            snake.grow()
            food = spawn_food(snake)
            score += 1
            steps_since_food = 0

        #Starvation cutoff (prevents infinite loops)
        if steps_since_food > 100:
            break

        #Absolute step limit
        if steps >= MAX_STEPS:
            break

    # 8. Fitness calculation
    fitness = score * 100 + steps

    ##print(fitness)
    return fitness