import matplotlib.pyplot as plt

# 1. Exact Data from Table II of your paper
columns = ['Metric', 'Unoptimized', 'Optimized', 'Reduction']
data = [
    ['Total Gate Count', '6', '2', '67%'],
    ['Circuit Depth', '6', '2', '67%'],
    ['Two-Qubit Gates', '4', '1', '75%']
]

# 2. Presentation-Ready Setup
fig, ax = plt.subplots(figsize=(9, 3.5), dpi=300)
fig.patch.set_facecolor('white')
ax.axis('off') # Hide standard graph axes
ax.axis('tight')

# 3. Build the Table
table = ax.table(cellText=data, colLabels=columns, cellLoc='center', loc='center')

# 4. Modern Styling and Typography
table.auto_set_font_size(False)
table.set_fontsize(14)
table.scale(1.2, 2.5) # Stretch the table to look breathable and clean

for (row, col), cell in table.get_celld().items():
    cell.set_edgecolor('#ecf0f1') # Super subtle, clean borders
    
    # Header Row Styling
    if row == 0:
        cell.set_text_props(weight='bold', color='white', size=15)
        cell.set_facecolor('#2980b9') # Crisp blue header
    else:
        # Highlight the 'Optimized' and 'Reduction' columns to make the impact pop
        if col in [2, 3]:
            cell.set_text_props(weight='bold', color='#27ae60') # Bright green text
            cell.set_facecolor('#f4fdf8') # Very faint green background
        else:
            cell.set_facecolor('white')
            
        # Bold the metric names on the left
        if col == 0:
            cell.set_text_props(weight='bold', color='#2c3e50')

# 5. Add a Presentation Title
plt.title("Circuit Metrics for the NAND Benchmark", 
          fontsize=18, fontweight='bold', color='#2c3e50', pad=20)

# 6. Save as a High-Res Image
plt.tight_layout()
plt.savefig('slide9_metric_table.png', facecolor='white', bbox_inches='tight')
print("Successfully saved 'slide9_metric_table.png'!")