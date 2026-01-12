import numpy as np

GRID_WIDTH = 20
GRID_HEIGHT = 20

VISION_RADIUS = 2

#direction vectors
DIR_VECTORS = {
            'UP': (0, -1),
            'DOWN': (0, 1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0)
            }

def turn_left(dx, dy):
    return dy, -dx
    
def turn_right(dx, dy):
    return -dy, dx

#rotate function for grid
def rotate_right(mat):  # 90° clockwise
    return [list(row) for row in zip(*mat[::-1])]
#rotate function for grid
def rotate_left(mat):   # 90° counter-clockwise
    return [list(row) for row in zip(*mat)][::-1]
#rotate function for grid
def rotate_180(mat):
    return [row[::-1] for row in mat[::-1]]

def manhattan_distance(point1, point2):
    """
    Calculates the Manhattan distance between two NumPy arrays.
    """
    # Convert to numpy arrays if they aren't already
    p1 = np.array(point1)
    p2 = np.array(point2)
    
    # Calculate the sum of absolute differences
    distance = np.sum(np.abs(p1 - p2))
    return distance
        
def get_local_grid(snake, head, food):

    head_x, head_y = head
    grid = []

    for dy in range(-VISION_RADIUS, VISION_RADIUS + 1):
        for dx in range(-VISION_RADIUS, VISION_RADIUS + 1):
            x = head_x + dx
            y = head_y + dy

            if x > GRID_WIDTH or x < 0 or y > GRID_WIDTH or y < 0:
                grid.append(-1) #wall
            elif (x, y) in snake.body:
                grid.append(-0.5) #body
            elif (x, y) == food:
                grid.append(1) #food
            else:
                grid.append(0) #empty


    return grid
    
def rotate_grid(snake, grid):
    size = 2 * VISION_RADIUS + 1
    grid2d = [grid[i*size:(i + 1)*size] for i in range(size)]

    #rotate grid based on direction headed
    if snake.direction == 'UP':
        rotated = grid2d
    elif snake.direction == 'RIGHT':
        rotated = rotate_left(grid2d)
    elif snake.direction == 'DOWN':
        rotated = rotate_180(grid2d)
    elif snake.direction == 'LEFT':
        rotated = rotate_right(grid2d)

    rotated_flat = [cell for row in rotated for cell in row]
    return rotated_flat

def relative_to_absolute(current_dir, action):
    # 0 = straight, 1 = left, 2 = right
    dirs = ["UP", "RIGHT", "DOWN", "LEFT"]
    i = dirs.index(current_dir)

    if action == 0:      # straight
        return dirs[i]
    elif action == 1:    # left
        return dirs[(i - 1) % 4]
    elif action == 2:    # right
        return dirs[(i + 1) % 4]


class Agent:
    def __init__(self, brain):
        pass
    
    def get_danger_zone(self, head, snake_body, current_direction):
        danger = [0, 0, 0]  # NEW list every frame

        dx, dy = DIR_VECTORS[current_direction]

        directions = [
            (dx, dy),                 # front
            turn_left(dx, dy),        # left
            turn_right(dx, dy)        # right
        ]

        for i, (vx, vy) in enumerate(directions):
            nx = head[0] + vx
            ny = head[1] + vy

            if (
                nx < 0 or nx >= GRID_WIDTH or
                ny < 0 or ny >= GRID_HEIGHT or
                (nx, ny) in snake_body[1:]
            ):
                danger[i] = 1

        return danger

    def get_food_dir(self, head, food_pos):
        return [

        int(food_pos[1] < head[1]), #up
        int(food_pos[1] > head[1]), #down
        int(food_pos[0] < head[0]), #left
        int(food_pos[0] > head[0]) #right

        ]
    
    def get_moving_direction(self, current_direction):
        if current_direction == 'UP':
            return [1, 0, 0, 0]
        elif current_direction == 'DOWN':
            return [0, 1, 0, 0]
        elif current_direction == 'LEFT':
            return [0, 0, 1, 0]
        else:
            return [0, 0, 0, 1] #right
    
    def get_state(self, snake, food_pos, current_direction):
        head = snake.body[0]

        #create local grid and rotate based on current direction
        grid = get_local_grid(snake, head, food_pos)
        grid = rotate_grid(snake, grid)
        

        #danger zone (no longer needed because of local grid implementation)
        #new_danger_zone = self.get_danger_zone(head, snake.body, current_direction)

        #food direction
        #new_food_dir = self.get_food_dir(head, food_pos)

        #moving direction
        new_moving_dir = self.get_moving_direction(current_direction)

        """
        dist = (
            abs(head[0] - food_pos[0]) +
            abs(head[1] - food_pos[1])
            ) / (2 * GRID_HEIGHT)
        #state.append(dist / (2 * GRID_SIZE))
        """

        #return new_danger_zone + grid + new_food_dir + new_moving_dir + [dist]
        return grid + new_moving_dir 
    
    def act(self, state):
        danger_front, danger_left, danger_right = state[0:3] #[f, l, r] danger zone
        #print(state) #debug line
        if danger_front:
            if not danger_left:
                return 'LEFT'
            elif not danger_right:
                return 'RIGHT'
            else:
                return 'LEFT' #if all else fails (trapped) just turn
        else:
            return 'STRAIGHT'
        

   