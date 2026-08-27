import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 1. Setup Canvas
fig, ax = plt.subplots(figsize=(14, 6), dpi=300)
fig.patch.set_facecolor('white')
ax.axis('off')

# Helper functions to draw crisp Qiskit-style logic gates
def draw_circuit_lines(x_start, x_end):
    for y in [2, 1, 0]:
        ax.plot([x_start, x_end], [y, y], color='#2c3e50', lw=1.5, zorder=1)
        ax.text(x_start - 0.3, y, f"q_{2-y}", va='center', ha='right', fontsize=14, fontweight='bold', color='#2c3e50')

def draw_x_box(x, y, color='#ebf5fb', text_color='#2980b9'):
    ax.add_patch(patches.Rectangle((x-0.25, y-0.25), 0.5, 0.5, facecolor=color, edgecolor=text_color, lw=2, zorder=3))
    ax.text(x, y, 'X', ha='center', va='center', fontsize=12, fontweight='bold', color=text_color, zorder=4)

def draw_ctrl(x, y, color='#2980b9'):
    ax.add_patch(patches.Circle((x, y), 0.1, facecolor=color, zorder=4))

def draw_vline(x, y1, y2, color='#2980b9'):
    ax.plot([x, x], [y1, y2], color=color, lw=2, zorder=2)

# ==========================================
# LEFT SIDE: UNOPTIMIZED (Your 6 Gates)
# ==========================================
ax.text(3, 3.2, "STANDARD COMPILER OUTPUT\n(Unoptimized)", ha='center', fontsize=15, fontweight='bold', color='#2c3e50')
draw_circuit_lines(1, 5.5)

# q_0 is y=2, q_1 is y=1, q_2 is y=0
draw_x_box(1.5, 1)  # X on q_1
draw_x_box(2.1, 1)  # X on q_1
draw_ctrl(2.7, 2); draw_ctrl(2.7, 1); draw_x_box(2.7, 0); draw_vline(2.7, 0, 2) # Toffoli
draw_ctrl(3.3, 0); draw_x_box(3.3, 1); draw_vline(3.3, 0, 1) # CNOT
draw_ctrl(3.9, 0); draw_x_box(3.9, 1); draw_vline(3.9, 0, 1) # CNOT
draw_ctrl(4.5, 2); draw_x_box(4.5, 1); draw_vline(4.5, 1, 2) # CNOT

# Unoptimized Pulses (6 distinct blocks)
ax.text(3, -0.8, "Microwave Control Pulses (6 Operations)", ha='center', fontsize=12, color='#2c3e50')
ax.plot([1, 5.5], [-1.5, -1.5], color='#2c3e50', lw=2) 
for px in [1.4, 2.0, 2.6, 3.2, 3.8, 4.4]:
    ax.add_patch(patches.Rectangle((px, -1.5), 0.2, 0.5, facecolor='#bdc3c7', edgecolor='#7f8c8d'))

# ==========================================
# CENTER: THE COMPILER ARROW
# ==========================================
ax.arrow(6, 1, 1.5, 0, width=0.4, head_width=0.8, head_length=0.5, facecolor='#27ae60', edgecolor='white')
ax.text(7, 1.8, "Hardware-Aware\nSynthesis", ha='center', fontsize=12, fontweight='bold', color='#27ae60')

# ==========================================
# RIGHT SIDE: OPTIMIZED (Your 2 Gates)
# ==========================================
ax.text(11, 3.2, "QUANTUM-COMPILER OUTPUT\n(Optimized)", ha='center', fontsize=15, fontweight='bold', color='#27ae60')
draw_circuit_lines(9, 13)

# Toffoli & CNOT
draw_ctrl(10.5, 2, '#27ae60'); draw_ctrl(10.5, 1, '#27ae60'); draw_x_box(10.5, 0, '#d5f5e3', '#27ae60'); draw_vline(10.5, 0, 2, '#27ae60')
draw_ctrl(12, 2, '#27ae60'); draw_x_box(12, 1, '#d5f5e3', '#27ae60'); draw_vline(12, 1, 2, '#27ae60')

# Optimized Pulses (2 clean blocks)
ax.text(11, -0.8, "Consolidated Pulses (2 Operations)", ha='center', fontsize=12, color='#27ae60', fontweight='bold')
ax.plot([9, 13], [-1.5, -1.5], color='#2c3e50', lw=2) 
ax.add_patch(patches.Rectangle((10.3, -1.5), 0.4, 0.5, facecolor='#27ae60', edgecolor='#1e8449'))
ax.add_patch(patches.Rectangle((11.8, -1.5), 0.4, 0.5, facecolor='#27ae60', edgecolor='#1e8449'))

# Save Graphic
plt.tight_layout()
plt.savefig("slide10_exact_circuit.png", bbox_inches='tight', facecolor='white')
print("Graphic generated successfully as slide10_exact_circuit.png!")