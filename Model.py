import numpy as np

#this will act as the snakes brain
#it will produce action scores based on the state vector passed int
class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        """
        input size -> state vector || output_size -> actions (4 directions)
        simple feedforward neural network
        input -> hidden -> output
        hidden layer -> action scores
        """

        #weight matrices
        self.w1 = np.random.randn(input_size, hidden_size)
        self.b1 = np.zeros(hidden_size)

        self.w2 = np.random.randn(hidden_size, output_size)
        self.b2 = np.zeros(output_size)
        
    def forward(self, state):
        #state: 1D array of shape (input_size)
        #return: 1D array of shape (output_size)

        #hidden layer
        # z = xW + b
        z1 = np.dot(state, self.w1) + self.b1
        #relu keeps positive scores and discards negative ones
        a1 = self.relu(z1)

        #output layer: [ score_up, score_down, score_left, score_right ]
        #agent will later choose a action based on these scores
        z2= np.dot(a1, self.w2) + self.b2

        return z2
        
    def relu(self, x):
        return np.maximum(0, x)
        
    def copy(self):
        #create deep copy of the network
        #WE MUST MAKE A DEEP COPY, if not brains will not be independent and will childs will affect parents
        #used by genetic algorithm

        nn = NeuralNetwork(
            input_size = self.w1.shape[0],
            hidden_size = self.w1.shape[1],
            output_size = self.w2.shape[1]
        )

        nn.w1 = np.copy(self.w1)
        nn.b1 = np.copy(self.b1)
        nn.w2 = np.copy(self.w2)
        nn.b2 = np.copy(self.b2)

        return nn