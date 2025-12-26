GRID_WIDTH = 10
GRID_HEIGHT = 10
danger_zone = [0, 0, 0] #front, left, right
food_dir = [0, 0, 0, 0] #up, down, left, right
moving_dir = [0, 0, 0, 1] #up, down, left, right
state_vector = []

class Agent:
    def __init__(self):
        self.danger_zone = danger_zone
        self.food_dir = food_dir
        self.moving_dir = moving_dir
        self.state_vector = [self.danger_zone + self.food_dir + self.moving_dir]
        

    def get_state(self, snake_body, food_pos, current_direction):
        head = snake_body[0]
        if current_direction == 'RIGHT':
            self.danger_zone[0] = int(head[0] + 1 >= GRID_WIDTH or (head[0] + 1, head[1]) in snake_body[1:]) #front
            self.danger_zone[1] = int(head[1] - 1 < 0 or (head[0], head[1] - 1) in snake_body[1:]) #left
            self.danger_zone[2] = int(head[1] + 1 >= GRID_HEIGHT or (head[0], head[1] + 1) in snake_body[1:]) #right
        elif current_direction == 'LEFT':
            self.danger_zone[0] = int(head[0] - 1 < 0 or (head[0] - 1, head[1]) in snake_body[1:]) #front
            self.danger_zone[1] = int(head[1] + 1 >= GRID_HEIGHT or (head[0], head[1] + 1) in snake_body[1:]) #left
            self.danger_zone[2] = int(head[1] - 1 < 0 or (head[0], head[1] - 1) in snake_body[1:]) #right
        elif current_direction == 'UP':
            self.danger_zone[0] = int(head[1] - 1 < 0 or (head[0], head[1] - 1) in snake_body[1:]) #front
            self.danger_zone[1] = int(head[0] - 1 < 0 or (head[0] - 1, head[1]) in snake_body[1:]) #left
            self.danger_zone[2] = int(head[0] + 1 >= GRID_WIDTH or (head[0] + 1, head[1]) in snake_body[1:]) #right
        elif current_direction == 'DOWN':
            self.danger_zone[0] = int(head[1] + 1 >= GRID_HEIGHT or (head[0], head[1] + 1) in snake_body[1:]) #front
            self.danger_zone[1] = int(head[0] + 1 >= GRID_WIDTH or (head[0] + 1, head[1]) in snake_body[1:]) #left
            self.danger_zone[2] = int(head[0] - 1 < 0 or (head[0] - 1, head[1]) in snake_body[1:]) #right
        
        #food direction
        self.food_dir[0] = int(food_pos[1] < head[1]) #up
        self.food_dir[1] = int(food_pos[1] > head[1]) #down
        self.food_dir[2] = int(food_pos[0] < head[0]) #left
        self.food_dir[3] = int(food_pos[0] > head[0]) #right

        #moving direction
        if current_direction == 'UP':
            self.moving_dir = [1, 0, 0, 0]
        elif current_direction == 'DOWN':
            self.moving_dir = [0, 1, 0, 0]
        elif current_direction == 'LEFT':
            self.moving_dir = [0, 0, 1, 0]
        elif current_direction == 'RIGHT':
            self.moving_dir = [0, 0, 0, 1]

        self.state_vector = self.danger_zone + self.food_dir + self.moving_dir
        return self.state_vector
    
    def act(self, state_vector):
        #[f, l, r] danger zone[fu, fd, fl, fr][mu, md, ml, mr]moving dir
        #choose direction based on absolute direction + relative turns
        if state_vector[0] == 1 and state_vector[7] == 1: #fd & mu
            if state_vector[1] == 0:
                return 'LEFT'
            else:
                return 'RIGHT'
        elif state_vector[0] == 1 and state_vector[8] == 1: #fd & md
            if state_vector[1] == 0:
                return 'LEFT'
            else:
                return 'RIGHT'
        elif state_vector[0] == 1 and state_vector[9] == 1: #fd & ml
            if state_vector[1] == 0:
                return 'LEFT'
            else:
                return 'RIGHT'
        elif state_vector[0] == 1 and state_vector[10] == 1: #fd & mr
            if state_vector[1] == 0:
                return 'LEFT'
            else:
                return 'RIGHT'
        else:
            return 'STRAIGHT'