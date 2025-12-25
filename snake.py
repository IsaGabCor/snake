class snake:

    def __init__(self, length=3, direction='RIGHT', position = (0,0)):
        self.length = length
        self.direction = direction
        self.position = position
        self.body = [position]
        for i in range(1, length):
            if direction == 'RIGHT':
                self.body.append((position[0] - i, position[1]))
            elif direction == 'LEFT':
                self.body.append((position[0] + i, position[1]))
            elif direction == 'UP':
                self.body.append((position[0], position[1] + i))
            elif direction == 'DOWN':
                self.body.append((position[0], position[1] - i))
    
    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == 'RIGHT':
            new_head = (head_x + 1, head_y)
        elif self.direction == 'LEFT':
            new_head = (head_x - 1, head_y)
        elif self.direction == 'UP':
            new_head = (head_x, head_y - 1)
        elif self.direction == 'DOWN':
            new_head = (head_x, head_y + 1)
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        tail = self.body[-1]
        self.body.append(tail)

    def change_direction(self, new_direction):
        opposite_directions = {'RIGHT' : 'LEFT', 'LEFT' : 'RIGHT', 'UP' : 'DOWN', 'DOWN' : 'UP'}
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction
    
    
