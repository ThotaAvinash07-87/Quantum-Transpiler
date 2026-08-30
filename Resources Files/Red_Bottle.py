import matplotlib.pyplot as plt
from qiskit import QuantumCircuit

# 1. Create the Unoptimized Circuit (6 Gates)
qc_unoptimized = QuantumCircuit(3)
qc_unoptimized.x(0)
qc_unoptimized.x(1)
qc_unoptimized.ccx(0, 1, 2)  # Toffoli gate
qc_unoptimized.x(0)
qc_unoptimized.x(1)
qc_unoptimized.x(2)

# 2. Create the Optimized Circuit (2 Gates)
qc_optimized = QuantumCircuit(3)
qc_optimized.ccx(0, 1, 2)    # Toffoli gate
qc_optimized.x(2)

# 3. Setup the Matplotlib Figure
fig = plt.figure(figsize=(12, 4))

# Plot Unoptimized Circuit on the left
ax1 = fig.add_subplot(1, 2, 1)
qc_unoptimized.draw(output='mpl', ax=ax1, plot_barriers=False)
ax1.set_title("Standard Heuristic Output (6 Gates)", fontsize=14, pad=10)

# Plot Optimized Circuit on the right
ax2 = fig.add_subplot(1, 2, 2)
qc_optimized.draw(output='mpl', ax=ax2, plot_barriers=False)
ax2.set_title("Ideal Physical Circuit (2 Gates)", fontsize=14, pad=10)

# Add an arrow in the middle to represent the gap (Notice the 'r' before the string)
fig.text(0.5, 0.5, r'$\Rightarrow$', fontsize=40, ha='center', va='center')
fig.text(0.5, 0.58, '?', fontsize=24, ha='center', va='center', color='red')

# Adjust layout and save the image to paste into your slide
plt.tight_layout()
plt.savefig("redundancy_bottleneck.png", dpi=300, bbox_inches="tight")
print("Image successfully saved as 'redundancy_bottleneck.png'")