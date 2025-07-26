import numpy as np
import matplotlib.pyplot as plt

num_requests = 10000

# Generate loads for four different distributions
normal_loads = np.random.normal(1.0, 0.5, num_requests)
lognormal_loads = np.random.lognormal(0.0, 0.5, num_requests)
exponential_loads = np.random.exponential(1.0, num_requests)
uniform_loads = np.random.uniform(0.5, 1.5, num_requests)

# Create histogram plots
plt.figure(figsize=(20, 5))

plt.subplot(1, 4, 1)
plt.hist(normal_loads, bins=50, color='skyblue', edgecolor='black')
plt.title('Normal Distribution\n(mean=1.0, std=0.5)')
plt.xlabel('Request Load')
plt.ylabel('Frequency')

plt.subplot(1, 4, 2)
plt.hist(lognormal_loads, bins=50, color='orange', edgecolor='black')
plt.title('Lognormal Distribution\n(mean=0.0, sigma=0.5)')
plt.xlabel('Request Load')

plt.subplot(1, 4, 3)
plt.hist(exponential_loads, bins=50, color='salmon', edgecolor='black')
plt.title('Exponential Distribution\n(scale=1.0)')
plt.xlabel('Request Load')

plt.subplot(1, 4, 4)
plt.hist(uniform_loads, bins=50, color='lightgreen', edgecolor='black')
plt.title('Uniform Distribution\n(low=0.5, high=1.5)')
plt.xlabel('Request Load')

plt.tight_layout()
plt.show()

# Print statistics
print("Distribution Statistics:")
print(f"Normal - Mean: {np.mean(normal_loads):.3f}, Std: {np.std(normal_loads):.3f}, Min: {np.min(normal_loads):.3f}, Max: {np.max(normal_loads):.3f}")
print(f"Lognormal - Mean: {np.mean(lognormal_loads):.3f}, Std: {np.std(lognormal_loads):.3f}, Min: {np.min(lognormal_loads):.3f}, Max: {np.max(lognormal_loads):.3f}")
print(f"Exponential - Mean: {np.mean(exponential_loads):.3f}, Std: {np.std(exponential_loads):.3f}, Min: {np.min(exponential_loads):.3f}, Max: {np.max(exponential_loads):.3f}")
print(f"Uniform - Mean: {np.mean(uniform_loads):.3f}, Std: {np.std(uniform_loads):.3f}, Min: {np.min(uniform_loads):.3f}, Max: {np.max(uniform_loads):.3f}")

# Check for negative values
print(f"\nNegative values check:")
print(f"Normal distribution has {np.sum(normal_loads < 0)} negative values")
print(f"Lognormal distribution has {np.sum(lognormal_loads < 0)} negative values")
print(f"Exponential distribution has {np.sum(exponential_loads < 0)} negative values")
print(f"Uniform distribution has {np.sum(uniform_loads < 0)} negative values")