import random
import numpy as np
from deap import base, creator, tools, algorithms

# --- REUSE CORE COMPONENTS ---
# We redefine the core library here for the 3-qubit proof of concept.
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

# --- DEAP GENETIC ALGORITHM SETUP ---

# We want to MINIMIZE two objectives: (1) Logic Error, (2) Gate Cost
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator: pick a random gate
toolbox.register("attr_gate", random.choice, GATE_NAMES)

# Structure initializers: an individual is a list of random gates (max length 10)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_gate, n=random.randint(2, 10))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# The Target State we want to synthesize (e.g., Half-Adder)
TARGET_STATE = (0, 7, 2, 1, 4, 3, 6, 5)

def evaluate_circuit(individual):
    """
    Runs the circuit and returns (Logic Error, Total Cost)
    """
    current_state = IDENTITY_STATE
    total_cost = 0
    
    for gate in individual:
        current_state = apply_gate(current_state, GATE_LIBRARY[gate])
        total_cost += get_cost(gate)
        
    # Logic Error = Hamming distance to the TARGET_STATE
    logic_error = sum(1 for i, v in enumerate(current_state) if v != TARGET_STATE[i])
    
    return (logic_error, total_cost)

def mutate_circuit(individual):
    """
    Custom Mutation: Randomly add, remove, or replace a gate
    """
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
    """
    Safe Crossover: Only splice if both circuits have at least 2 gates
    """
    if len(ind1) >= 2 and len(ind2) >= 2:
        return tools.cxTwoPoint(ind1, ind2)
    return ind1, ind2  # If too short, return them unaltered

# Register genetic operators
toolbox.register("evaluate", evaluate_circuit)
toolbox.register("mate", mate_circuit) 
toolbox.register("mutate", mutate_circuit)
toolbox.register("select", tools.selNSGA2) # NSGA-II is great for multi-objective optimization

def run_ga():
    print("--- Starting Genetic Algorithm Synthesis ---")
    
    # Create a population of 200 random circuits
    pop = toolbox.population(n=200)
    
    # Run evolution for 50 generations
    # cxpb = probability of mating (crossover)
    # mutpb = probability of mutation
    algorithms.eaMuPlusLambda(pop, toolbox, mu=200, lambda_=400, cxpb=0.5, mutpb=0.3, ngen=50, verbose=False)
    
    # Extract the best circuits
    fronts = tools.sortNondominated(pop, len(pop), first_front_only=True)
    best_circuits = fronts[0]
    
    print("\nBest circuits found (Logic Error, Total Cost):")
    for circuit in best_circuits[:3]:
        fitness = evaluate_circuit(circuit)
        print(f"Metrics: {fitness} | Circuit: {circuit}")

if __name__ == "__main__":
    run_ga()