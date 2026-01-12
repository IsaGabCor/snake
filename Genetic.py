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

    def crossover(self, parent1, parent2):
        child = parent1.copy()

        for p_child, p1, p2 in zip(
            [child.w1, child.b1, child.w2, child.b2],
            [parent1.w1, parent1.b1, parent1.w2, parent1.b2],
            [parent2.w1, parent2.b1, parent2.w2, parent2.b2],
        ):
            mask = np.random.rand(*p_child.shape) < 0.5
            p_child[:] = np.where(mask, p1, p2)

        return child


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
            p1, p2 = np.random.choice(elites, 2, replace=False)
            child = self.crossover(p1, p2)
            self.mutate(child)
            if np.random.rand() < 0.1:
                self.mutate(child)
            new_pop.append(child)


        return new_pop

    def mutate(self, network):
        #mutate the weights of nn in place
        for param in [network.w1, network.b1, network.w2, network.b2]:
            mutation_mask = np.random.rand(*param.shape) < self.mutation_rate
            noise = np.random.randn(*param.shape) * self.mutation_strength
            param += mutation_mask * noise