import matplotlib.pyplot as plt
import networkx as nx

# 1. Set up the A* Search Tree graph
G = nx.DiGraph()

# Add nodes (Circuit States)
nodes = {
    "Root": (0, 0),
    "A1": (-2, -1), "A2": (0, -1), "A3": (2, -1),
    "B1": (-3, -2), "B2": (-1, -2), "Goal": (1, -2), "B4": (3, -2)
}

# Add edges (Quantum Gates applied)
edges = [
    ("Root", "A1", "CNOT\n(Cost: 10)"), 
    ("Root", "A2", "X Gate\n(Cost: 1)"), 
    ("Root", "A3", "H Gate\n(Cost: 1)"),
    ("A1", "B1", "X Gate"), ("A1", "B2", "Toffoli"),
    ("A2", "Goal", "Toffoli\n(Target Reached)"), 
    ("A3", "B4", "CNOT")
]

G.add_nodes_from(nodes.keys())
for edge in edges:
    G.add_edge(edge[0], edge[1], label=edge[2])

# 2. Presentation-Ready Setup (Clean White/Tech Theme)
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Define colors matching the convergence plot
default_node_color = "#ebf5fb" # Light blue fill
optimal_node_color = "#d5f5e3" # Light green fill
default_edge_color = "#bdc3c7" # Light grey for abandoned paths
optimal_path_color = "#27ae60" # Strong green for the winning path
text_color = "#2c3e50"         # Dark slate grey for readable text

# Apply colors
node_colors = [optimal_node_color if node in ["Root", "A2", "Goal"] else default_node_color for node in G.nodes()]
edge_colors_nodes = ["#27ae60" if node in ["Root", "A2", "Goal"] else "#2980b9" for node in G.nodes()]

# 3. Draw the graph
nx.draw_networkx_nodes(G, nodes, node_size=2500, node_color=node_colors, edgecolors=edge_colors_nodes, linewidths=2.5)
nx.draw_networkx_labels(G, nodes, font_size=12, font_family="sans-serif", font_weight="bold", font_color=text_color)

# Draw standard edges (abandoned/expensive paths)
standard_edges = [(u, v) for u, v in G.edges() if not (u in ["Root", "A2"] and v in ["A2", "Goal"])]
nx.draw_networkx_edges(G, nodes, edgelist=standard_edges, edge_color=default_edge_color, width=2, arrows=True, arrowsize=20, style="dashed")

# Draw optimal A* path edges (highlighted)
optimal_edges = [("Root", "A2"), ("A2", "Goal")]
nx.draw_networkx_edges(G, nodes, edgelist=optimal_edges, edge_color=optimal_path_color, width=4, arrows=True, arrowsize=25)

# Add edge labels (Gate costs) with white backgrounds so they don't overlap lines
edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, nodes, edge_labels=edge_labels, font_size=10, font_color=text_color, label_pos=0.5, bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=0.5))

# 4. Final Polish
plt.title("Phase 2: Exact Optimization via A* Search\n(Finding the Mathematically Minimal Circuit)", 
          fontsize=18, fontweight='bold', color=text_color, pad=20)
plt.axis("off") # Removes the background grid/box completely
plt.tight_layout()

# Save for the slide deck
plt.savefig("astar_clean_theme_slide5.png", facecolor='white', bbox_inches='tight')
print("Successfully saved 'astar_clean_theme_slide5.png'!")