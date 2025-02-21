import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulator import AccelerationSimulator

def run_basic_simulation():
    # Create simulation instance
    sim = AccelerationSimulator()
    
    # Set parameters (mass=1kg, force=10N)
    sim.set_parameters(mass=1.0, force=10.0)
    
    # Set initial conditions
    sim.set_initial_conditions(initial_velocity=0, initial_position=0)
    
    # Run simulation for 5 seconds
    t, pos, vel, acc = sim.simulate(duration=5.0)
    
    # Plot results
    sim.plot_results(t, pos, vel, acc)

if __name__ == "__main__":
    run_basic_simulation()
