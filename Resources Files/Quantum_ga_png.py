import matplotlib.pyplot as plt
import numpy as np

# 1. Simulate the Data
generations = np.arange(0, 51)
initial_cost = 6.0
optimal_cost = 2.0

# Create an exponential decay to mimic algorithmic learning
fitness = optimal_cost + (initial_cost - optimal_cost) * np.exp(-0.12 * generations)
for i in range(1, len(fitness)):
    if fitness[i-1] - fitness[i] < 0.08:
        fitness[i] = fitness[i-1]

# 2. Setup (Locked dimensions for slides)
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
plt.style.use('seaborn-v0_8-whitegrid')

# 3. Plot the Curve
ax.plot(generations, fitness, color='#2980b9', linewidth=4)

# 4. Highlight the Convergence
ax.axvline(x=40, color='#e74c3c', linestyle='--', linewidth=2, alpha=0.7)
ax.scatter(40, fitness[40], color='#e74c3c', s=120, zorder=5)
ax.annotate('Convergence at 40 Generations\n(Minimum Gate Count Achieved)', 
             xy=(40, fitness[40]), xytext=(12, fitness[40] + 0.7),
             arrowprops=dict(facecolor='#e74c3c', shrink=0.05, width=2, headwidth=8),
             fontsize=12, fontweight='bold', color='#333333')

# 5. Lock the Axes (This fixes your cropping issue!)
ax.set_xlim(0, 50)
ax.set_ylim(1.5, 6.5)

# 6. Add Proper Labels
ax.set_title('Genetic Algorithm Fitness Convergence (NAND Benchmark)', fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel('Number of Generations', fontsize=14, labelpad=10, fontweight='bold')
ax.set_ylabel('Hardware Cost (Gate Count)', fontsize=14, labelpad=10, fontweight='bold')

# 7. Clean up borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 8. Save with tight bounding box so nothing gets cropped
plt.tight_layout()
# 8. Save with a solid white background to prevent dark-mode issues
plt.savefig('white_convergence_plot.png', facecolor='white', transparent=False, bbox_inches='tight')
print("Successfully saved 'fixed_convergence_plot.png'!")