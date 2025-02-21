import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulator import AccelerationSimulator, AccelerationProfile
import numpy as np
import matplotlib.pyplot as plt

def analyze_transition_times():
    # Parameters
    max_accel = 10.0  # m/s²
    total_time = 5.0  # seconds
    
    # Calculate maximum transition time
    max_transition = AccelerationProfile.calculate_max_transition_time(total_time)
    print(f"For total time {total_time}s:")
    print(f"Maximum allowable transition time: {max_transition:.2f}s")
    
    # Test different transition times
    transition_times = [0.1, max_transition/2, max_transition, max_transition*1.1]
    
    fig, axes = plt.subplots(len(transition_times), 1, figsize=(10, 12))
    fig.suptitle('Effect of Different Transition Times on Acceleration Profile')
    
    for i, t_time in enumerate(transition_times):
        sim = AccelerationSimulator()
        try:
            sim.set_acceleration_profile(max_accel, total_time, t_time)
            t, pos, vel, acc = sim.simulate(dt=0.01)
            
            axes[i].plot(t, acc)
            axes[i].set_ylabel('Acceleration (m/s²)')
            axes[i].grid(True)
            axes[i].set_title(f'Transition time: {t_time:.2f}s')
            
            if i == len(transition_times) - 1:
                axes[i].set_xlabel('Time (s)')
                
        except ValueError as e:
            axes[i].text(0.5, 0.5, str(e), ha='center', va='center', wrap=True)
            axes[i].set_title(f'Transition time: {t_time:.2f}s (Invalid)')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    analyze_transition_times()
