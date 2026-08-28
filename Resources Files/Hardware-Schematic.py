import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 1. Setup Canvas (Expanded size for breathing room)
fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
fig.patch.set_facecolor('#f2f6f9')
ax.set_facecolor('#f2f6f9')
ax.set_xlim(0, 14)
ax.set_ylim(0, 9.5)
ax.axis('off')

# 2. Colors and Styles
line_color = '#34495e'
bg_card = '#ffffff'
text_color = '#1a252f'
blue_accent = '#2980b9'

# 3. Helper Functions for Components
def draw_box(x, y, w, h, title, subtitle=""):
    # Box
    ax.add_patch(patches.Rectangle((x, y), w, h, facecolor=bg_card, edgecolor=line_color, lw=2.5, zorder=3))
    # Title and subtitle placed dynamically based on box height to prevent overlap
    ax.text(x + w/2, y + h - 0.4, title, ha='center', va='top', fontsize=15, fontweight='bold', color=text_color, zorder=4)
    if subtitle:
        ax.text(x + w/2, y + h - 0.9, subtitle, ha='center', va='top', fontsize=11, color='#7f8c8d', zorder=4)

def draw_resistor(x_start, y, length):
    """Draws a zigzag resistor symbol"""
    x_pts = [x_start, x_start+0.2, x_start+0.3, x_start+0.5, x_start+0.7, x_start+0.9, x_start+1.0, x_start+1.2]
    y_pts = [y, y, y+0.2, y-0.2, y+0.2, y-0.2, y, y]
    ax.plot(x_pts, y_pts, color=line_color, lw=2, zorder=2)
    ax.text(x_start + 0.6, y + 0.35, "330 \u03A9", ha='center', fontsize=10, fontweight='bold', color=line_color)

def draw_led(x, y, color, label):
    """Draws a diode symbol with light arrows"""
    # Triangle
    triangle = patches.Polygon([[x, y+0.2], [x, y-0.2], [x+0.4, y]], closed=True, facecolor=color, edgecolor=line_color, lw=2, zorder=3)
    ax.add_patch(triangle)
    # Vertical line
    ax.plot([x+0.4, x+0.4], [y+0.2, y-0.2], color=line_color, lw=2, zorder=3)
    # Wire through
    ax.plot([x-0.2, x], [y, y], color=line_color, lw=2, zorder=2)
    ax.plot([x+0.4, x+0.6], [y, y], color=line_color, lw=2, zorder=2)
    # Light arrows
    ax.plot([x+0.2, x+0.4], [y+0.3, y+0.5], color=color, lw=2, zorder=3)
    ax.plot([x+0.3, x+0.5], [y+0.2, y+0.4], color=color, lw=2, zorder=3)
    # Label (lowered to avoid hitting wires)
    ax.text(x+0.2, y-0.5, label, ha='center', fontsize=11, fontweight='bold', color=line_color)

# 4. Draw Main Components (Y-coordinates adjusted massively)
draw_box(2.5, 6.5, 3.5, 1.5, "LAPTOP", "Quantum-Compiler (Python)")
draw_box(2.5, 1.0, 3.5, 4.5, "ARDUINO UNO", "Hardware Serial Bridge")

# 5. Draw Wires and Connections
# USB Connection
ax.plot([4.25, 4.25], [5.5, 6.5], color=blue_accent, lw=3, zorder=2)
ax.text(4.4, 6.0, "USB (Serial 9600)", fontsize=11, color=blue_accent, fontweight='bold', va='center')

# Pin Labels on Arduino (Spaced out nicely)
ax.text(5.8, 4.0, "Pin 10", ha='right', va='center', fontsize=11, fontweight='bold', color=text_color)
ax.text(5.8, 2.8, "Pin 9", ha='right', va='center', fontsize=11, fontweight='bold', color=text_color)
ax.text(5.8, 1.6, "Pin 8", ha='right', va='center', fontsize=11, fontweight='bold', color=text_color)
ax.text(2.7, 1.6, "GND", ha='left', va='center', fontsize=11, fontweight='bold', color=text_color)

# Signal Wires from Arduino to Resistors
ax.plot([6.0, 7.5], [4.0, 4.0], color=line_color, lw=2, zorder=1)
ax.plot([6.0, 7.5], [2.8, 2.8], color=line_color, lw=2, zorder=1)
ax.plot([6.0, 7.5], [1.6, 1.6], color=line_color, lw=2, zorder=1)

# Draw Resistors
draw_resistor(7.5, 4.0, 1.2)
draw_resistor(7.5, 2.8, 1.2)
draw_resistor(7.5, 1.6, 1.2)

# Wires from Resistors to LEDs
ax.plot([8.7, 9.8], [4.0, 4.0], color=line_color, lw=2, zorder=1)
ax.plot([8.7, 9.8], [2.8, 2.8], color=line_color, lw=2, zorder=1)
ax.plot([8.7, 9.8], [1.6, 1.6], color=line_color, lw=2, zorder=1)

# Draw LEDs (Matching C++ code colors)
draw_led(10.0, 4.0, '#e74c3c', "CCX Gate") # Red
draw_led(10.0, 2.8, '#f1c40f', "CX Gate")  # Yellow
draw_led(10.0, 1.6, '#2ecc71', "X Gate")   # Green

# Common Ground Lines
# From CCX down to bottom line, then across and up into Arduino GND
ax.plot([10.6, 12.0, 12.0, 1.5, 1.5, 2.5], [4.0, 4.0, 0.6, 0.6, 1.6, 1.6], color=line_color, lw=2, zorder=1)
# Connecting CX to vertical ground rail
ax.plot([10.6, 12.0], [2.8, 2.8], color=line_color, lw=2, zorder=1)
# Connecting X to vertical ground rail
ax.plot([10.6, 12.0], [1.6, 1.6], color=line_color, lw=2, zorder=1)

# Ground Label
ax.text(1.2, 1.0, "Common Ground (GND)", fontsize=11, fontweight='bold', color=line_color, rotation=90, va='bottom')

# Title (Shifted way up so it clears the laptop box entirely)
ax.text(7.0, 8.8, "Quantum Hardware Pulse Simulation Circuit", ha='center', fontsize=22, fontweight='bold', color=text_color)
ax.plot([3.5, 10.5], [8.5, 8.5], color=blue_accent, lw=2.5)

# Save
plt.savefig("hardware_schematic.png", bbox_inches='tight', dpi=300)
print("Schematic generated successfully as 'hardware_schematic.png'!")