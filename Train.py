import numpy as np
import pickle

from Model import NeuralNetwork
from Genetic import GeneticAlgorithm
from Snake_logic import run_game

POPULATION_SIZE = 500 #more agents smooth mutation, lesser create more noise but evolve faster
GENERATIONS = 2000

INPUT_SIZE = 29 #state vector
HIDDEN_SIZE = 16
OUTPUT_SIZE = 3 #direction choices

ELITE_FRACTION = 0.08 #number of elites chosen
MUTATION_RATE = 0.35 #rate of change
MUTATION_STRENGTH = 0.6 #strength of change


def main():
    #Create initial population
    #all brains are created randomly and start bad (on purpose)
    population = [
        NeuralNetwork(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE)
        for _ in range(POPULATION_SIZE)
    ]

    ga = GeneticAlgorithm(
        #this stores evol. rules, and nothing else
        population_size=POPULATION_SIZE,
        elite_fraction=ELITE_FRACTION,
        mutation_rate=MUTATION_RATE,
        mutation_strength=MUTATION_STRENGTH
    )

    #Training loop
    #each loop is another gen.
    best_ever = -float("inf")
    best_brain = None

    best_history = []
    avg_history = []

    for generation in range(GENERATIONS):
        fitnesses = []

        #Evaluate each agent
        for brain in population:
            fitness = run_game(brain)
            fitnesses.append(fitness)

        fitnesses = np.array(fitnesses)

        #Logging
        best = np.max(fitnesses)
        avg = np.mean(fitnesses)
        avg_history.append(avg)

        if generation > 0:
            if avg_history[-1] - avg_history[-2] < 1:
                ga.mutation_rate = min(0.5, ga.mutation_rate * 1.1)
                ga.mutation_strength = min(1.0, ga.mutation_strength * 1.05)


        print(
            f"Generation {generation:3d} | "
            f"Best: {best:6.1f} | "
            f"Avg: {avg:6.2f}"
        )

        #save best model
        best_index = np.argmax(fitnesses)
        best_brain = population[best_index].copy()

        if best > best_ever:
            best_ever = best
            best_brain = population[best_index]
            best_history.append(best_ever)

        #Evolve population
        population = ga.evolve(population, fitnesses)


    print("Best Score: ", best_ever)

    np.save("best_W1.npy", best_brain.w1)
    np.save("best_W2.npy", best_brain.w2)
    np.save("best_history.npy", best_history)
    np.save("avg_history.npy", avg_history)

    with open("gen_logs/best_brain.pkl", "wb") as f:
        pickle.dump(best_brain, f)


if __name__ == "__main__":
    main()
