import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulator import AccelerationSimulator

def run_optimal_motion_simulation():
    # Create simulation instance
    sim = AccelerationSimulator()
    
    # Set parameters for motion
    max_accel = 10.0  # m/s²
    total_time = 5.0  # seconds
    transition_time = 0.2  # seconds
    
    # Configure simulation
    sim.set_initial_conditions(initial_velocity=0, initial_position=0)
    sim.set_acceleration_profile(max_accel, total_time, transition_time)
    
    # Run simulation
    t, pos, vel, acc = sim.simulate(dt=0.01)
    
    # Plot results
    sim.plot_results(t, pos, vel, acc)

if __name__ == "__main__":
    run_optimal_motion_simulation()
