import numpy as np
import matplotlib.pyplot as plt

def plot_ideal_forms(max_accel, total_time):
    """Plot ideal forms of acceleration, velocity, and position with equations."""
    dt = 0.01
    t = np.arange(0, total_time + dt, dt)
    half_time = total_time / 2
    
    # Calculate ideal profiles
    a = np.zeros_like(t)
    a[t <= half_time] = max_accel
    a[t > half_time] = -max_accel
    
    v = np.zeros_like(t)
    for i, time in enumerate(t):
        if time <= half_time:
            v[i] = max_accel * time
        else:
            v[i] = max_accel * half_time - max_accel * (time - half_time)
    
    s = np.zeros_like(t)
    for i, time in enumerate(t):
        if time <= half_time:
            s[i] = 0.5 * max_accel * time**2
        else:
            s_half = 0.5 * max_accel * half_time**2
            v_half = max_accel * half_time
            dt = time - half_time
            s[i] = s_half + v_half * dt - 0.5 * max_accel * dt**2
    
    # Create figure
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12))
    
    # Acceleration plot
    ax1.plot(t, a, 'k-', linewidth=2)
    ax1.set_ylabel('Acceleration (m/s²)')
    ax1.grid(True)
    ax1.set_title('Ideal Acceleration Profile')
    ax1.text(total_time * 1.05, 0,
             'a(t) = aₘₐₓ     for 0 ≤ t ≤ T/2\n'
             'a(t) = -aₘₐₓ    for T/2 < t ≤ T',
             verticalalignment='center')
    
    # Velocity plot
    ax2.plot(t, v, 'k-', linewidth=2)
    ax2.set_ylabel('Velocity (m/s)')
    ax2.grid(True)
    ax2.set_title('Ideal Velocity Profile')
    ax2.text(total_time * 1.05, max(v)/2,
             'v(t) = aₘₐₓ·t           for 0 ≤ t ≤ T/2\n'
             'v(t) = aₘₐₓ·T/2 - aₘₐₓ·(t-T/2)   for T/2 < t ≤ T',
             verticalalignment='center')
    
    # Position plot
    ax3.plot(t, s, 'k-', linewidth=2)
    ax3.set_ylabel('Position (m)')
    ax3.set_xlabel('Time (s)')
    ax3.grid(True)
    ax3.set_title('Ideal Position Profile')
    ax3.text(total_time * 1.05, max(s)/2,
             's(t) = ½·aₘₐₓ·t²        for 0 ≤ t ≤ T/2\n'
             's(t) = s(T/2) + v(T/2)·(t-T/2) - ½·aₘₐₓ·(t-T/2)²   for T/2 < t ≤ T',
             verticalalignment='center')
    
    # Add key results
    max_velocity = max_accel * half_time
    final_position = max_accel * total_time**2 / 8
    
    plt.figtext(0.02, 0.02, 
                f"Key Results:\n"
                f"Maximum Velocity = {max_velocity:.1f} m/s (at t = T/2)\n"
                f"Final Position = {final_position:.1f} m (at t = T)",
                fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Parameters
    max_accel = 10.0  # m/s²
    total_time = 5.0  # seconds
    
    plot_ideal_forms(max_accel, total_time)
