import numpy as np
import heapq 
from qiskit import QuantumCircuit

# --- CONSTANTS AND LIBRARY DEFINITIONS ---

# A 3-qubit system has 8 states: 000(0) to 111(7)
# The identity state (a wire doing nothing) is:
IDENTITY_STATE = (0, 1, 2, 3, 4, 5, 6, 7)

# Format: "Gate_Name": [(swap_index_1, swap_index_2), ...]
GATE_LIBRARY = {
    # NOT GATES (X) - flips a specific bit
    # X0 flips the least significant bit (LSB)
    "X0": [(0, 1), (2, 3), (4, 5), (6, 7)],
    "X1": [(0, 2), (1, 3), (4, 6), (5, 7)],
    "X2": [(0, 4), (1, 5), (2, 6), (3, 7)],

    # CNOT GATES (CX) - flips target IF control is 1
    # CX_c_t: c = control qubit, t = target qubit
    "CX_1_0": [(2, 3), (6, 7)], # Control q1, Target q0
    "CX_2_0": [(4, 5), (6, 7)],
    "CX_0_1": [(1, 3), (5, 7)],
    "CX_2_1": [(4, 6), (5, 7)],
    "CX_0_2": [(1, 5), (3, 7)],
    "CX_1_2": [(2, 6), (3, 7)],

    # TOFFOLI GATES (CCX) - flips target IF both controls are 1
    # CCX_c1_c2_t: c1, c2 = controls, t = target
    "CCX_1_2_0": [(6, 7)],      # Controls q1,q2, Target q0
    "CCX_0_2_1": [(5, 7)],
    "CCX_0_1_2": [(3, 7)]
}

# To minimize "costly CNOT and Toffoli gates", we assign weights.
# A standard IBM Qiskit hardware cost model:
GATE_COSTS = {
    "X": 1,     # Single qubit gates are cheap
    "CX": 10,   # Two-qubit gates are expensive
    "CCX": 50   # Toffolis require decomposition into multiple CX gates
}

# --- HELPER FUNCTIONS ---

def apply_gate(state, gate_swaps):
    """
    Applies a quantum gate to a state vector. 
    gate_swaps is a list of tuples representing state indices to swap.
    """
    state_list = list(state)
    for i, j in gate_swaps:
        state_list[i], state_list[j] = state_list[j], state_list[i]
    return tuple(state_list)

def get_cost(gate_name):
    if "CCX" in gate_name: return GATE_COSTS["CCX"]
    if "CX" in gate_name: return GATE_COSTS["CX"]
    return GATE_COSTS["X"]

def hamming_heuristic(state):
    """
    Calculates the Hamming distance.
    Counts how many truth table outputs are not in their target identity position.
    """
    return sum(1 for i, v in enumerate(state) if i != v)

# --- CORE ALGORITHMS ---

def a_star_synthesizer(target_state):
    """
    A* search to find the optimal gate sequence to build the target_state.
    """
    print(f"Starting A* Search for state: {target_state}")
    
    # Priority queue entries: (f_score, g_score, current_state, gate_path)
    # f_score = g_score (cost so far) + h_score (heuristic to goal)
    pq = [(hamming_heuristic(target_state), 0, target_state, [])]
    
    # Track the lowest cost to reach a state to avoid redundant work
    visited_costs = {target_state: 0}
    
    nodes_explored = 0
    
    while pq:
        f, g, current_state, path = heapq.heappop(pq)
        nodes_explored += 1
        
        # Did we synthesize the circuit? (Reached the Identity state)
        if current_state == IDENTITY_STATE:
            print(f"Synthesis successful! Nodes explored: {nodes_explored}")
            
            # Important Quantum Property: Our gate library consists entirely of 
            # self-inverse gates (Hermitian). Reversing the path found from 
            # Target -> Identity gives us the exact sequence to build Identity -> Target.
            return path[::-1] 
        
        # Explore all possible next gates
        for gate_name, gate_swaps in GATE_LIBRARY.items():
            next_state = apply_gate(current_state, gate_swaps)
            gate_cost = get_cost(gate_name)
            
            new_g = g + gate_cost
            
            # If we found a cheaper path to this state, queue it up
            if next_state not in visited_costs or new_g < visited_costs[next_state]:
                visited_costs[next_state] = new_g
                new_f = new_g + hamming_heuristic(next_state)
                heapq.heappush(pq, (new_f, new_g, next_state, path + [gate_name]))
                
    return None

def export_to_qiskit(gate_sequence, num_qubits=3):
    """
    Translates the internal gate sequence into a Qiskit QuantumCircuit.
    """
    print("\n--- Phase 4: Exporting to Qiskit ---")
    qc = QuantumCircuit(num_qubits)
    
    for gate in gate_sequence:
        parts = gate.split('_')
        gate_type = parts[0]
        
        # Single Qubit Gates (e.g., X0)
        if gate_type.startswith("X") and len(parts) == 1:
            target = int(gate_type[1])
            qc.x(target)
            
        # Two Qubit Gates (e.g., CX_0_1)
        elif gate_type == "CX":
            control = int(parts[1])
            target = int(parts[2])
            qc.cx(control, target)
            
        # Three Qubit Gates (e.g., CCX_0_1_2)
        elif gate_type == "CCX":
            control1 = int(parts[1])
            control2 = int(parts[2])
            target = int(parts[3])
            qc.ccx(control1, control2, target)
            
    return qc

# --- EXECUTION BLOCK ---

if __name__ == "__main__":
    # Simulate generating a Half-Adder target state
    temp_state = apply_gate(IDENTITY_STATE, GATE_LIBRARY["CCX_0_1_2"]) 
    target_half_adder = apply_gate(temp_state, GATE_LIBRARY["CX_0_1"]) 
    
    # Run the exact synthesis engine
    optimal_circuit = a_star_synthesizer(target_half_adder)
    
    print("\nOptimized Gate Sequence:")
    for step, gate in enumerate(optimal_circuit):
        print(f"Step {step + 1}: {gate} (Cost: {get_cost(gate)})")
    
    # Export and visualize
    if optimal_circuit:
        qiskit_circuit = export_to_qiskit(optimal_circuit)
        
        print("\nQiskit Circuit Representation:")
        print(qiskit_circuit.draw(output='text'))
        
        print("\nQiskit Native Gate Metrics:")
        gate_metrics = qiskit_circuit.count_ops()
        for gate, count in gate_metrics.items():
            print(f"- {gate.upper()} gates: {count}")
        print(f"Total Circuit Depth: {qiskit_circuit.depth()}")