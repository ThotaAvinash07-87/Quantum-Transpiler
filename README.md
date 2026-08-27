# Hardware-Aware Quantum Circuit Synthesis (Quantum-Compiler)

An end-to-end quantum transpiler pipeline designed to actively minimize expensive two-qubit hardware gates and mitigate quantum gate bloat. This project leverages A* search and Genetic Algorithms (GA) to synthesize optimal quantum circuits, achieving up to a 53% reduction in gate costs compared to baseline synthesis methods.

## 📂 Repository Structure

* **`/Resources Files/`**: Python (Matplotlib) scripts utilized to generate mathematically exact, high-resolution circuit diagrams and algorithmic flowcharts for presentation graphics.
* **`/hardware_demo/`**: Contains the Embedded C implementation (`Pulse_Controller.cpp`) and the serial bridge (`arduino_bridge.py`) for physical pulse execution on an Arduino Uno.
* **Core Synthesizers**: 
  * `quantum_synth.py`: Foundational script defining state spaces and executing A* search optimization.
  * `quantum_ga.py`: Genetic Algorithm (GA) synthesizer scaling optimization to 4-qubit systems.

## ⚙️ Key Features

* **Advanced State Space Support:** Defines a strict NOT, CNOT, and Toffoli (CCX) gate library for 3-qubit states, and programmatically generates permutations for 4-qubit systems (handling ~20.9 trillion state permutations) using bitwise logic.
* **Exact A* Search Optimization:** Uses a shortest-path A* algorithm combined with a Hamming-distance heuristic to systematically guarantee the absolute cheapest sequence of hardware operations.
* **Genetic Algorithm (GA) Scaling:** Scales to massive search spaces where exact algorithms hit memory limits. Evolves circuits using the `deap` library with a single-objective fitness function: `Score = (Logic Error * 1000) + Gate Cost`.
* **Peephole Optimizer:** A fast, classical EDA-style post-synthesis pass that scans the generated netlist and collapses localized redundant gate pairs (e.g., X -> Toffoli -> X).
* **Qiskit Integration:** Natively exports synthesized logical outputs to Qiskit for circuit rendering and physical coupling map analysis.

## 📊 Benchmark Results

The benchmarking suite compares our optimal transpiled netlists against baseline naive translation costs:

| Circuit | Baseline Cost | Optimized Cost | Reduction | Gate Composition | Optimal Netlist |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Half-Adder** | 110 | 60 | **45.45%** | 1 CX, 1 CCX | `CCX_0_1_2 -> CX_0_1` |
| **Feynman Fan-out** | 40 | 20 | **50.00%** | 2 CX, 0 CCX | `CX_0_1 -> CX_0_2` |
| **Toffoli-Swap** | 150 | 70 | **53.33%** | 2 CX, 1 CCX | `CX_2_1 -> CCX_0_1_2 -> CX_2_1` |

## 🎛️ Physical Hardware Deployment

The optimized circuits are deployed via `arduino_bridge.py` via `pyserial` to validate execution logic on physical hardware. For the Half-Adder circuit benchmark, the wall-clock execution time was drastically improved:
* **Unoptimized Execution Time:** 8.31 seconds
* **Optimized Execution Time:** 6.06 seconds

## 🚀 Usage

Execute the A* synthesis to generate exact optimal gate sequences:
```bash
python quantum_synth.py
```

Execute the Genetic Algorithm to synthesize larger (4-qubit) multi-state circuits:
```bash
python quantum_ga.py
```

Run the hardware validation to transmit microwave control pulses to the serial board:
```bash
python arduino_bridge.py
```

---
### 🎓 Academic Context
**Author:** Thota Venkata Avinash Naidu  
**Affiliation:** Department of Electronics and Communication Engineering, Andhra University  
**Presentation:** QUEST-AI 2026
