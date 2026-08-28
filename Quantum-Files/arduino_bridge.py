import serial
import time
from qiskit import QuantumCircuit
from quantum_synth import a_star_synthesizer, apply_gate, IDENTITY_STATE, GATE_LIBRARY

# --- 1. SET UP THE TARGET CIRCUIT ---
# We will use the Half-Adder as our test case
t1 = apply_gate(IDENTITY_STATE, GATE_LIBRARY["CCX_0_1_2"]) 
HALF_ADDER_STATE = apply_gate(t1, GATE_LIBRARY["CX_0_1"])

# --- 2. CONNECT TO ARDUINO ---
# UPDATE "COM10" TO MATCH YOUR ARDUINO'S PORT!
arduino_port = "COM10" 
baud_rate = 9600

try:
    print(f"Opening Serial Connection to {arduino_port}...")
    hardware = serial.Serial(arduino_port, baud_rate, timeout=1)
    
    # Arduino resets when serial is opened. We must wait for it to wake up.
    time.sleep(2) 
    
    # Read the ready signal
    while hardware.in_waiting > 0:
        # Ignore the ready print to match your clean terminal output
        hardware.readline()
        
except Exception as e:
    print(f"Failed to connect to Arduino: {e}")
    exit()

def print_qiskit_circuit(title, gate_list):
    """Parses the gate list and prints an ASCII Qiskit diagram."""
    print("\n" + "="*50)
    print(title)
    print("="*50)
    print("\n--- Phase 4: Exporting to Qiskit ---\n")
    
    qc = QuantumCircuit(3)
    for gate in gate_list:
        if gate == "X1" or gate == "X_1":
            qc.x(1)
        elif gate.startswith("CCX"):
            parts = gate.split("_")
            qc.ccx(int(parts[1]), int(parts[2]), int(parts[3]))
        elif gate.startswith("CX"):
            parts = gate.split("_")
            qc.cx(int(parts[1]), int(parts[2]))
            
    print(qc.draw(output='text'))
    print("="*50 + "\n")

def send_circuit_to_hardware(circuit_name, gate_list):
    print(f"Executing {circuit_name} on Physical Hardware...")
    
    start_time = time.time()
    
    for gate in gate_list:
        print(f"Firing Pulse for: {gate} ... ", end="")
        
        # Send the gate string to Arduino, terminating with a newline
        hardware.write(f"{gate}\n".encode())
        
        # Wait for the Arduino to finish the physical pulse and reply "DONE"
        while True:
            if hardware.in_waiting > 0:
                response = hardware.readline().decode().strip()
                if response == "DONE":
                    print("Completed.")
                    break
                    
    end_time = time.time()
    print(f"=> {circuit_name} Execution Time: {round(end_time - start_time, 2)} seconds\n")

if __name__ == "__main__":
    # Synthesize the optimal circuit
    print("Synthesizing Optimal Circuit...")
    optimal_circuit = a_star_synthesizer(HALF_ADDER_STATE)
    
    # Unoptimized Baseline Bennett Circuit (for comparison)
    unoptimized_circuit = ["X1", "X1", "CCX_0_1_2", "CX_2_1", "CX_2_1", "CX_0_1"]

    # --- NEW: Print Qiskit Diagrams Before Execution ---
    print_qiskit_circuit("1. UNOPTIMIZED HALF-ADDER CIRCUIT DIAGRAM:", unoptimized_circuit)
    print_qiskit_circuit("2. SYNTHESIZED OPTIMIZED CIRCUIT DIAGRAM:", optimal_circuit)

    input("Press ENTER to run the UNOPTIMIZED circuit on hardware...\n")
    send_circuit_to_hardware("Unoptimized Half-Adder", unoptimized_circuit)
    
    input("Press ENTER to run YOUR OPTIMIZED circuit on hardware...\n")
    send_circuit_to_hardware("Optimized Half-Adder", optimal_circuit)
    
    hardware.close()