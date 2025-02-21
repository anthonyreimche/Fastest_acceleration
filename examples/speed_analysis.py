import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulator import AccelerationSimulator
import numpy as np
import matplotlib.pyplot as plt

def analytical_solution(t, max_accel, total_time):
    """Calculate the analytical solution for instantaneous transitions."""
    half_time = total_time / 2
    
    # Acceleration calculation (perfect step function)
    a = np.zeros_like(t)
    a[t <= half_time] = max_accel
    a[t > half_time] = -max_accel
    
    # Velocity calculation (piecewise linear)
    v = np.zeros_like(t)
    for i, time in enumerate(t):
        if time <= half_time:
            v[i] = max_accel * time
        else:
            v[i] = max_accel * half_time - max_accel * (time - half_time)
    
    # Position calculation (piecewise quadratic)
    s = np.zeros_like(t)
    for i, time in enumerate(t):
        if time <= half_time:
            s[i] = 0.5 * max_accel * time**2
        else:
            s_half = 0.5 * max_accel * half_time**2
            v_half = max_accel * half_time
            dt = time - half_time
            s[i] = s_half + v_half * dt - 0.5 * max_accel * dt**2
    
    return s, v, a

def compare_solutions():
    # Parameters
    max_accel = 10.0  # m/s²
    total_time = 5.0  # seconds
    
    # Create time array
    dt = 0.01
    t = np.arange(0, total_time + dt, dt)
    
    # Get analytical solution
    s_analytical, v_analytical, a_analytical = analytical_solution(t, max_accel, total_time)
    
    # Get numerical solutions with different transition times
    transition_times = [0.001, 0.01, 0.1]
    numerical_results = []
    
    for t_time in transition_times:
        sim = AccelerationSimulator()
        sim.set_acceleration_profile(max_accel, total_time, t_time)
        _, pos, vel, acc = sim.simulate(dt=dt)
        numerical_results.append((pos, vel, acc))
    
    # Calculate maximum velocities and final positions
    v_max_analytical = max(v_analytical)
    s_final_analytical = s_analytical[-1]
    
    print(f"\nAnalytical Solution (transition_time → 0):")
    print(f"Maximum velocity: {v_max_analytical:.3f} m/s")
    print(f"Final position: {s_final_analytical:.3f} m")
    print("\nNumerical Solutions:")
    
    for t_time, (pos, vel, acc) in zip(transition_times, numerical_results):
        print(f"\nTransition time: {t_time:.3f}s")
        print(f"Maximum velocity: {max(vel):.3f} m/s")
        print(f"Final position: {pos[-1]:.3f} m")
        print(f"Velocity difference from ideal: {(v_max_analytical - max(vel))/v_max_analytical*100:.3f}%")
        print(f"Position difference from ideal: {(s_final_analytical - pos[-1])/s_final_analytical*100:.3f}%")
    
    # Plotting
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12))
    
    # Acceleration plot
    ax1.plot(t, a_analytical, 'k--', label='Analytical (ideal)', linewidth=2)
    for t_time, (_, _, acc) in zip(transition_times, numerical_results):
        ax1.plot(t, acc, label=f'Transition time = {t_time:.3f}s')
    ax1.set_ylabel('Acceleration (m/s²)')
    ax1.grid(True)
    ax1.legend()
    ax1.set_title('Acceleration Profiles')
    
    # Velocity plot
    ax2.plot(t, v_analytical, 'k--', label='Analytical (ideal)', linewidth=2)
    for t_time, (_, vel, _) in zip(transition_times, numerical_results):
        ax2.plot(t, vel, label=f'Transition time = {t_time:.3f}s')
    ax2.set_ylabel('Velocity (m/s)')
    ax2.grid(True)
    ax2.legend()
    ax2.set_title('Velocity Profiles')
    
    # Position plot
    ax3.plot(t, s_analytical, 'k--', label='Analytical (ideal)', linewidth=2)
    for t_time, (pos, _, _) in zip(transition_times, numerical_results):
        ax3.plot(t, pos, label=f'Transition time = {t_time:.3f}s')
    ax3.set_ylabel('Position (m)')
    ax3.set_xlabel('Time (s)')
    ax3.grid(True)
    ax3.legend()
    ax3.set_title('Position Profiles')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    compare_solutions()
