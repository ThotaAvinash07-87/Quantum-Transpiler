import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 1. Setup Canvas (Strict 16:9 Ratio with Equal Scaling for Perfect 45-degree Angles)
fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
bg_color = '#f2f6f9' # Soft icy white/blue
trace_color = '#dce4ea' # Subtle circuit gray/blue
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

# 2. Helper Functions for Stylized Elements
def draw_trace(pts, color=trace_color, lw=2.5):
    """Draws a circuit trace from a list of (x,y) tuples."""
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, zorder=1)
    # Add nodes at the joints and ends
    for x, y in pts:
        ax.add_patch(patches.Circle((x, y), 0.06, facecolor=bg_color, edgecolor=color, lw=1.5, zorder=2))

def highlight_trace(pts, color):
    """Adds a thick glowing colored overlay to specific trace segments."""
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=3.5, alpha=0.7, zorder=3)

def draw_microchip(x, y):
    """Draws a stylized microchip icon."""
    chip_color = '#b5c6d6'
    # Pins
    for offset in [-0.25, 0, 0.25]:
        ax.plot([x-0.6, x+0.6], [y+offset, y+offset], color=chip_color, lw=2, zorder=3)
        ax.plot([x+offset, x+offset], [y-0.6, y+0.6], color=chip_color, lw=2, zorder=3)
    # Outer box (FIXED: Removed rx and ry)
    ax.add_patch(patches.Rectangle((x-0.45, y-0.45), 0.9, 0.9, facecolor='#e8eff5', edgecolor=chip_color, lw=2, zorder=4))
    # Inner box
    ax.add_patch(patches.Rectangle((x-0.25, y-0.25), 0.5, 0.5, facecolor='#dce4ea', zorder=4))

def draw_logic_gate(x, y):
    """Draws a stylized NAND gate icon."""
    gate_color = '#b5c6d6'
    # Inputs
    ax.plot([x-0.8, x-0.4], [y+0.2, y+0.2], color=gate_color, lw=2, zorder=3)
    ax.plot([x-0.8, x-0.4], [y-0.2, y-0.2], color=gate_color, lw=2, zorder=3)
    # Output
    ax.plot([x+0.5, x+0.8], [y, y], color=gate_color, lw=2, zorder=3)
    # Gate Body (D-shape)
    arc = patches.Arc((x, y), 0.8, 0.8, angle=0, theta1=-90, theta2=90, color=gate_color, lw=2, zorder=3)
    ax.add_patch(arc)
    ax.plot([x, x-0.4], [y+0.4, y+0.4], color=gate_color, lw=2, zorder=3)
    # Flat back of the NAND gate
    ax.plot([x, x-0.4], [y-0.4, y-0.4], color=gate_color, lw=2, zorder=3)
    ax.plot([x-0.4, x-0.4], [y-0.4, y+0.4], color=gate_color, lw=2, zorder=3)
    # Inversion bubble
    ax.add_patch(patches.Circle((x+0.46, y), 0.08, facecolor=bg_color, edgecolor=gate_color, lw=2, zorder=4))

# 3. Draw Top-Left Diagonal Traces (45-degrees)
draw_trace([(0, 6.5), (1, 6.5), (3, 4.5), (4, 4.5)])
draw_trace([(1.5, 9), (2.5, 8), (4.5, 8)])
draw_trace([(0, 8), (1.5, 8), (2.5, 7), (3.5, 7)])
highlight_trace([(1.5, 8), (2.5, 7)], '#ffaa55') # Orange glow
draw_logic_gate(1.5, 7.5) # The NAND Gate

# 4. Draw Bottom-Left Diagonal Traces
draw_trace([(0, 2.5), (1, 2.5), (3, 4.5), (4.5, 4.5)])
draw_trace([(0, 1), (1.5, 1), (3.5, 3), (4.5, 3)])
draw_trace([(2, 0), (3, 1), (5, 1)])
highlight_trace([(1.5, 1), (2.5, 2)], '#44ccff') # Cyan glow

# 5. Draw Top-Right Diagonal Traces
draw_trace([(16, 7.5), (14, 7.5), (12, 5.5), (11, 5.5)])
draw_trace([(16, 6.5), (14.5, 6.5), (13.5, 5.5)])
draw_trace([(13.5, 9), (12, 7.5), (9.5, 7.5)])
highlight_trace([(14, 7.5), (13, 6.5)], '#44ccff') # Cyan glow
draw_microchip(14.5, 8) # Top Microchip

# 6. Draw Bottom-Right Diagonal Traces
draw_trace([(16, 2), (14.5, 2), (12.5, 4), (11, 4)])
draw_trace([(16, 3), (15, 3), (14, 4), (12.5, 4)])
draw_trace([(14.5, 0), (13, 1.5), (10, 1.5)])
highlight_trace([(14.5, 2), (13.5, 3)], '#ffaa55') # Orange glow
draw_microchip(14.5, 1.5) # Bottom Microchip

# 7. Final Polish & Save
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig("slide_background_stylized.png", bbox_inches='tight', pad_inches=0, dpi=300)
print("Stylized background generated successfully as 'slide_background_stylized.png'!")