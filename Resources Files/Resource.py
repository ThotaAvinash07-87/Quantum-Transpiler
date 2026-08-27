import matplotlib.pyplot as plt
import qrcode
import textwrap

# 1. Generate the single QR Code
qr_text = (
    "GitHub Repo: https://github.com/ThotaAvinash07-87/Quantum-Transpiler\n"
    "Hardware Demo: https://drive.google.com/file/d/1MLix5iM5_9OUbVUZs1IdtXtiGdUfQK8s/view?usp=drivesdk\n"
    "Research Paper: https://drive.google.com/file/d/13lsqK_YGEU7p7LzTCeN6h1hipiqhYjW-/view?usp=sharing" 
)

qr = qrcode.QRCode(version=1, box_size=10, border=2)
qr.add_data(qr_text)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="#2c3e50", back_color="white")

# 2. Setup Canvas (16:9 Standard PowerPoint Ratio)
fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
fig.patch.set_facecolor('white')
ax.axis('off')

# 3. Slide Title & Divider
ax.text(0.05, 0.92, "Resources & References", fontsize=28, fontweight='bold', color='#2c3e50')
ax.plot([0.05, 0.95], [0.87, 0.87], color='#2980b9', lw=2)

# 4. Top Section: QR Code (Shifted right for proper margins)
ax_qr = fig.add_axes([0.08, 0.48, 0.25, 0.35]) # [x, y, width, height]
ax_qr.imshow(qr_img)
ax_qr.axis('off')

# 5. Top Section: Bullets (Aligned with QR code)
ax.text(0.38, 0.77, "Scan for Project Assets:", fontsize=20, fontweight='bold', color='#2980b9')

bullets = [
    "1. Full Qiskit Source Code (GitHub Repository)",
    "2. Physical Hardware Demo (Arduino Uno Implementation)",
    "3. Complete Research Publication (PDF)"
]

y_pos = 0.67
for bullet in bullets:
    ax.text(0.38, y_pos, bullet, fontsize=16, color='#2c3e50', fontweight='bold')
    y_pos -= 0.08

# 6. References Section Header
ax.text(0.05, 0.40, "Key Academic References", fontsize=18, fontweight='bold', color='#2980b9')
ax.plot([0.05, 0.95], [0.37, 0.37], color='#ecf0f1', lw=1.5)

# 7. Smart Text Wrapping Function for References
def print_refs(ax, refs, x_start, y_start, wrap_width):
    y = y_start
    for ref in refs:
        # Automatically break lines so they don't overlap columns
        wrapped_text = textwrap.fill(ref, width=wrap_width)
        ax.text(x_start, y, wrapped_text, fontsize=10.5, color='#34495e', va='top')
        # Calculate how much space to drop down based on the number of lines
        lines = wrapped_text.count('\n') + 1
        y -= (0.025 * lines) + 0.025 # Proper line spacing

# Reference Data
refs_col1 = [
    "[1] F. Arute, K. Arya, R. Babbush, et al., \"Quantum supremacy using a programmable superconducting processor,\" Nature, 2019.",
    "[2] A. Aleksandrowicz, T. Alexander, et al., \"Qiskit: An open-source framework for quantum computing,\" 2019.",
    "[3] T. Toffoli, \"Reversible computing,\" in Automata, Languages and Programming, Springer, 1980, pp. 632–644.",
    "[4] A. V. Aho, M. S. Lam, R. Sethi, and J. D. Ullman, Compilers: Principles, Techniques, and Tools, 2nd ed. 2007.",
    "[5] C. H. Bennett, \"Logical reversibility of computation,\" IBM Journal of Research and Development, 1973."
]

refs_col2 = [
    "[6] S. S. Tannu and M. K. Qureshi, \"Not all qubits are created equal: A case for variability-aware policies,\" ASPLOS, 2019.",
    "[7] F.-M. De Rainville et al., \"DEAP: Evolutionary algorithms made easy,\" Journal of Machine Learning Research, 2012.",
    "[8] Qiskit Development Team, \"Qiskit transpiler documentation,\" 2024.",
    "[9] P. E. Hart, N. J. Nilsson, and B. Raphael, \"A formal basis for the heuristic determination of minimum cost paths,\" 1968.",
    "[10] A. Thota, \"Quantum-Compiler: Hardware-aware quantum circuit synthesis,\" GitHub, 2025."
]

# Print columns with a strict max width of 65 characters per line
print_refs(ax, refs_col1, x_start=0.05, y_start=0.33, wrap_width=65)
print_refs(ax, refs_col2, x_start=0.52, y_start=0.33, wrap_width=65)

# 8. Save the perfect layout
plt.savefig("slide11_perfect_resources.png", bbox_inches='tight', facecolor='white')
print("Slide 11 graphic generated successfully as 'slide11_perfect_resources.png'!")