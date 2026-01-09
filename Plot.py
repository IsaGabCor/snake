import numpy as np
import matplotlib.pyplot as plt

best = np.load("best_history.npy")
avg = np.load("avg_history.npy")

plt.plot(best, label="Best")
plt.plot(avg, label="Average")
plt.legend()
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.title("Snake Learning Curve")
plt.show()
