import matplotlib.pyplot as plt
import numpy as np

# Sample dataset from histogram equalization example
# Actually, this will not be a histogram since we use the discrete probability distribution
rounded_values = np.array([1, 4, 8, 10, 13, 15])
obs = np.array([15, 70, 110, 45, 80, 40])

# Plot the frequency distribution
plt.bar(
    rounded_values, obs, width=0.8, align="center", color="skyblue", edgecolor="black"
)
plt.xlabel("Rounded value")
plt.ylabel("Observations")
plt.ylim(0, obs.max() + 10)
plt.title("Discrete Histogram (Frequency Distribution)")
plt.show()
