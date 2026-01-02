import numpy as np

#this class is going to be responsible for evolving the neural networks
#evolution will be accomplished by selection and mutation
#overview for class: given a group of brains and their fitness, how can they be refined

class GeneticAlgorithm:
    #one instance of GA will mutate multiple brains
    def __init__(
        self,
        population_size, #snakes per gen
        elite_fraction, #% of snakes that survive
        mutation_rate, #probability a weight changes -> how often a change occurs
        mutation_strength #size of change -> how much change
    ):
        self.population_size = population_size
        self.elite_fraction = elite_fraction
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength

    def evolve(self, population, fitnesses):
        #population: list of nn objects
        #fitnesses: list of fitness scores (same length)
        #returns new pop. (same size)

        #sort pop by fitness (descending)
        sorted_indices = np.argsort(fitnesses)[::-1]
        population = [population[i] for i in sorted_indices]
        fitnesses = [fitnesses[i] for i in sorted_indices]

        #select elites
        elite_count = int(self.population_size * self.elite_fraction)
        elites = population[:elite_count]

        #create new pop
        new_pop = []

        #keep elites (no mutation)
        #by choosing elites and creating childs from them ensures snakes not regressing
        for elite in elites:
            new_pop.append(elite.copy())

        #fill rest with mutated copies of elites
        while len(new_pop) < self.population_size:
            parent = np.random.choice(elites)
            child = parent.copy()
            self.mutate(child)
            new_pop.append(child)

        return new_pop

    def mutate(self, network):
        #mutate the weights of nn in place
        for param in [network.w1, network.b1, network.w2, network.b2]:
            mutation_mask = np.random.rand(*param.shape) < self.mutation_rate
            noise = np.random.randn(*param.shape) * self.mutation_strength
            param += mutation_mask * noise