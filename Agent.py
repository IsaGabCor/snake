GRID_WIDTH = 20
GRID_HEIGHT = 20

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

class Agent:
    def __init__(self, brain):
        pass

    # def __init__(self):
    #     pass
    
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

        #danger zone
        new_danger_zone = self.get_danger_zone(head, snake.body, current_direction)
        #food direction
        new_food_dir = self.get_food_dir(head, food_pos)
        #moving direction
        new_moving_dir = self.get_moving_direction(current_direction)

        return new_danger_zone + new_food_dir + new_moving_dir
    
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