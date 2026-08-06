import random
import numpy as np
from deap import base, creator, tools, algorithms

# --- REUSE CORE COMPONENTS ---
IDENTITY_STATE = (0, 1, 2, 3, 4, 5, 6, 7)

GATE_LIBRARY = {
    "X0": [(0, 1), (2, 3), (4, 5), (6, 7)],
    "X1": [(0, 2), (1, 3), (4, 6), (5, 7)],
    "X2": [(0, 4), (1, 5), (2, 6), (3, 7)],
    "CX_1_0": [(2, 3), (6, 7)], "CX_2_0": [(4, 5), (6, 7)],
    "CX_0_1": [(1, 3), (5, 7)], "CX_2_1": [(4, 6), (5, 7)],
    "CX_0_2": [(1, 5), (3, 7)], "CX_1_2": [(2, 6), (3, 7)],
    "CCX_1_2_0": [(6, 7)], "CCX_0_2_1": [(5, 7)], "CCX_0_1_2": [(3, 7)]
}
GATE_NAMES = list(GATE_LIBRARY.keys())

def apply_gate(state, gate_swaps):
    state_list = list(state)
    for i, j in gate_swaps:
        state_list[i], state_list[j] = state_list[j], state_list[i]
    return tuple(state_list)

def get_cost(gate_name):
    if "CCX" in gate_name: return 50
    if "CX" in gate_name: return 10
    return 1

# --- DEAP GENETIC ALGORITHM SETUP (SINGLE OBJECTIVE) ---

# We now use a SINGLE objective (minimizing one combined score)
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_gate", random.choice, GATE_NAMES)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_gate, n=random.randint(2, 10))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

TARGET_STATE = (0, 7, 2, 1, 4, 3, 6, 5)

def evaluate_circuit(individual):
    """
    Returns a SINGLE score: (Logic Error * 1000) + Cost
    """
    current_state = IDENTITY_STATE
    total_cost = 0
    
    for gate in individual:
        current_state = apply_gate(current_state, GATE_LIBRARY[gate])
        total_cost += get_cost(gate)
        
    logic_error = sum(1 for i, v in enumerate(current_state) if v != TARGET_STATE[i])
    
    # Massive penalty for wrong logic
    final_score = (logic_error * 1000) + total_cost
    return (final_score,) # DEAP requires a tuple return

def mutate_circuit(individual):
    if len(individual) == 0:
        return individual,
    
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
# Switched from NSGA2 to Tournament selection for single-objective
toolbox.register("select", tools.selTournament, tournsize=3) 

def peephole_optimizer(circuit):
    """Scans the circuit and cancels out adjacent identical gates."""
    optimized_stack = []
    for gate in circuit:
        if optimized_stack and optimized_stack[-1] == gate:
            optimized_stack.pop() 
        else:
            optimized_stack.append(gate)
    return optimized_stack

def run_ga():
    print("--- Starting Genetic Algorithm Synthesis ---")
    
    pop = toolbox.population(n=200)
    
    # Run evolution
    algorithms.eaMuPlusLambda(pop, toolbox, mu=200, lambda_=400, cxpb=0.5, mutpb=0.3, ngen=50, verbose=False)
    
    # Extract the absolute best circuits based on our single combined score
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