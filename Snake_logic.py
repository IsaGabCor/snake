
GRID_SIZE = 20
MAX_STEPS = 200

def run_game(brain):
    """
    Runs one full snake game controlled by the given brain.
    Returns a fitness score (float).
    """

    #Initialize game objects
    snake = Snake(grid_size=GRID_SIZE)
    agent = Agent(brain)

    food = spawn_food(snake)
    steps = 0
    score = 0

    while True:
        steps += 1
        steps_since_food += 1

        #Get state
        state = agent.get_state(snake, food)
        state = np.array(state, dtype=float)

        #Brain decides action
        output = brain.forward(state)
        action = np.argmax(output)

        #Apply action
        snake.change_direction(action)
        snake.move()

        #Check collisions
        if collision_with_boundaries(snake.body[0]) or collision_with_self(snake.body):
            break

        #Check food
        # Check if snake has eaten the food
        food_spawn = not has_eaten_food(snake.body[0], food_pos)
        #spawn food
        if not food_spawn:
            food_pos = spawn_food(snake)

        #Starvation cutoff (prevents infinite loops)
        if steps_since_food > 100:
            break

        #Absolute step limit
        if steps >= MAX_STEPS:
            break

    # 8. Fitness calculation
    fitness = score * 100 + steps

    return fitness