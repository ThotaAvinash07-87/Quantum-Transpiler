import serial
import time
from quantum_synth import a_star_synthesizer, apply_gate, IDENTITY_STATE, GATE_LIBRARY

# --- 1. SET UP THE TARGET CIRCUIT ---
# We will use the Half-Adder as our test case
t1 = apply_gate(IDENTITY_STATE, GATE_LIBRARY["CCX_0_1_2"]) 
HALF_ADDER_STATE = apply_gate(t1, GATE_LIBRARY["CX_0_1"])

# --- 2. CONNECT TO ARDUINO ---
# UPDATE "COM3" TO MATCH YOUR ARDUINO'S PORT!
arduino_port = "COM10" 
baud_rate = 9600

try:
    print(f"Opening Serial Connection to {arduino_port}...")
    hardware = serial.Serial(arduino_port, baud_rate, timeout=1)
    
    # Arduino resets when serial is opened. We must wait for it to wake up.
    time.sleep(2) 
    
    # Read the ready signal
    while hardware.in_waiting > 0:
        print("Hardware says:", hardware.readline().decode().strip())
        
except Exception as e:
    print(f"Failed to connect to Arduino: {e}")
    exit()

def send_circuit_to_hardware(circuit_name, gate_list):
    print(f"\nExecuting {circuit_name} on Physical Hardware...")
    print(f"Gate Sequence: {gate_list}")
    
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
    print(f"\n=> {circuit_name} Execution Time: {round(end_time - start_time, 2)} seconds")

if __name__ == "__main__":
    # Synthesize the optimal circuit
    print("Synthesizing Optimal Circuit...")
    optimal_circuit = a_star_synthesizer(HALF_ADDER_STATE)
    
    # Unoptimized Baseline Bennett Circuit (for comparison)
    # This represents what happens when a bad compiler adds redundant gates
    unoptimized_circuit = ["X1", "X1", "CCX_0_1_2", "CX_2_1", "CX_2_1", "CX_0_1"]

    input("\nPress ENTER to run the UNOPTIMIZED circuit on hardware...")
    send_circuit_to_hardware("Unoptimized Half-Adder", unoptimized_circuit)
    
    input("\nPress ENTER to run YOUR OPTIMIZED circuit on hardware...")
    send_circuit_to_hardware("Optimized Half-Adder", optimal_circuit)
    
    hardware.close()