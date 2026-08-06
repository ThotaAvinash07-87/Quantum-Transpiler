import random
from deap import base, creator, tools, algorithms

# --- DYNAMIC N-QUBIT SYSTEM GENERATOR ---

def build_quantum_system(num_qubits):
    """Programmatically generates the State Space and Gate Library for N qubits."""
    num_states = 2**num_qubits
    identity = tuple(range(num_states))
    gate_lib = {}
    
    # Generate X Gates
    for q in range(num_qubits):
        swaps = []
        for state in range(num_states):
            flipped = state ^ (1 << q)
            if state < flipped: swaps.append((state, flipped))
        gate_lib[f"X{q}"] = swaps
        
    # Generate CX Gates
    for ctrl in range(num_qubits):
        for tgt in range(num_qubits):
            if ctrl == tgt: continue
            swaps = []
            for state in range(num_states):
                if state & (1 << ctrl): # If control bit is 1
                    flipped = state ^ (1 << tgt)
                    if state < flipped: swaps.append((state, flipped))
            gate_lib[f"CX_{ctrl}_{tgt}"] = swaps
            
    # Generate CCX Gates
    for c1 in range(num_qubits):
        for c2 in range(num_qubits):
            for tgt in range(num_qubits):
                if c1 == c2 or c1 == tgt or c2 == tgt: continue
                # To prevent duplicates like CCX_0_1_2 and CCX_1_0_2, enforce order
                if c1 > c2: continue 
                swaps = []
                for state in range(num_states):
                    if (state & (1 << c1)) and (state & (1 << c2)):
                        flipped = state ^ (1 << tgt)
                        if state < flipped: swaps.append((state, flipped))
                gate_lib[f"CCX_{c1}_{c2}_{tgt}"] = swaps
                
    return identity, gate_lib

# Initialize a 4-Qubit System
NUM_QUBITS = 4
IDENTITY_STATE, GATE_LIBRARY = build_quantum_system(NUM_QUBITS)
GATE_NAMES = list(GATE_LIBRARY.keys())

# Let's target a 4-qubit permutation (e.g., flipping the highest bit if the lowest is 1)
# We will create a target state by applying a known sequence, then see if the GA can reverse-engineer it!
def apply_gate(state, gate_swaps):
    state_list = list(state)
    for i, j in gate_swaps:
        state_list[i], state_list[j] = state_list[j], state_list[i]
    return tuple(state_list)

temp = apply_gate(IDENTITY_STATE, GATE_LIBRARY["CX_0_3"])
TARGET_STATE = apply_gate(temp, GATE_LIBRARY["X1"])

def get_cost(gate_name):
    if "CCX" in gate_name: return 50
    if "CX" in gate_name: return 10
    return 1

# --- DEAP GENETIC ALGORITHM SETUP ---

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_gate", random.choice, GATE_NAMES)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_gate, n=random.randint(2, 10))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate_circuit(individual):
    current_state = IDENTITY_STATE
    total_cost = 0
    for gate in individual:
        current_state = apply_gate(current_state, GATE_LIBRARY[gate])
        total_cost += get_cost(gate)
    
    logic_error = sum(1 for i, v in enumerate(current_state) if v != TARGET_STATE[i])
    final_score = (logic_error * 1000) + total_cost
    return (final_score,) 

def mutate_circuit(individual):
    if len(individual) == 0: return individual,
    mutation_type = random.choice(["add", "remove", "replace"])
    if mutation_type == "add":
        individual.insert(random.randint(0, len(individual)), random.choice(GATE_NAMES))
    elif mutation_type == "remove" and len(individual) > 1:
        individual.pop(random.randint(0, len(individual)-1))
    elif mutation_type == "replace":
        individual[random.randint(0, len(individual)-1)] = random.choice(GATE_NAMES)
    return individual,

def mate_circuit(ind1, ind2):
    if len(ind1) >= 2 and len(ind2) >= 2:
        return tools.cxTwoPoint(ind1, ind2)
    return ind1, ind2

toolbox.register("evaluate", evaluate_circuit)
toolbox.register("mate", mate_circuit) 
toolbox.register("mutate", mutate_circuit)
toolbox.register("select", tools.selTournament, tournsize=3) 

def peephole_optimizer(circuit):
    optimized_stack = []
    for gate in circuit:
        if optimized_stack and optimized_stack[-1] == gate:
            optimized_stack.pop() 
        else:
            optimized_stack.append(gate)
    return optimized_stack

def run_ga():
    print(f"--- Starting {NUM_QUBITS}-Qubit GA Synthesis (State Space: {2**NUM_QUBITS}! permutations) ---")
    pop = toolbox.population(n=300) # Increased population for larger space
    
    # Increased generations to give it time to search the 4-qubit space
    algorithms.eaMuPlusLambda(pop, toolbox, mu=300, lambda_=600, cxpb=0.6, mutpb=0.4, ngen=100, verbose=False)
    
    best_circuits = tools.selBest(pop, k=3)
    
    print("\nBest circuits found (Score format: LogicError*1000 + Cost):")
    for circuit in best_circuits:
        raw_score = evaluate_circuit(circuit)[0]
        clean_circuit = peephole_optimizer(circuit)
        clean_score = evaluate_circuit(clean_circuit)[0]
        
        print(f"Raw Score {raw_score}: {circuit}")
        print(f"Opt Score {clean_score}: {clean_circuit}")
        print("-" * 50)

if __name__ == "__main__":
    run_ga()