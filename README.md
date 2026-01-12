# Self-Learning Snake (Genetic Algorithm + Neural Network)

This project is a reinforcement learning experiment where a Snake agent learns to survive and collect food using a neural network evolved via a genetic algorithm.

Unlike traditional Snake AIs that use hand-written rules, this agent learns entirely from reward signals and environment feedback.

---

## How It Works

Each snake is controlled by a small neural network.  
The network receives a **local grid centered on the snake’s head**, rotated so that the snake always perceives “forward” in the same direction.  

This makes learning orientation-independent.

The network outputs **relative movement commands**:
- Turn left
- Go straight
- Turn right

These relative actions are converted into absolute world directions at runtime.

---

## Evolution

A population of neural networks is evolved using a **genetic algorithm**:

- Elitism preserves the best-performing snakes
- Crossover combines weights from two parents
- Mutation introduces controlled randomness
- Fitness is based on:
  - Food collected
  - Distance to food
  - Survival time
  - Penalties for collisions

Over generations, the population gradually improves its behavior.

---

## Visualization

The best-performing neural network can be loaded into a Pygame visualization to watch how the trained agent behaves in real time.
This was defintely my favorite part and the one feature that I was anticipating the most. It was a bit funny to watch my snake head straight into the wall at first.
The most rewarding part was watching the snake go for food for the first time.

---

## What I Learned

This project was designed as a hands-on introduction to machine learning and reinforcement learning. It taught me:

- How state representations affect learning
- Why action encoding matters
- How reward shaping changes behavior
- How genetic algorithms explore solution spaces
- How ML systems fail in non-obvious ways

---

## Technologies Used

- Python  
- NumPy  
- Pygame
- Matplotlib
- Genetic Algorithms  
- Feed-forward Neural Networks  

---

## Notes

This is an experimental learning project, not a polished product.  
It was intentionally built from scratch to understand how ML systems behave, break, and improve.
This was my first exposure to ML systems and I mostly implemented and debugged.
