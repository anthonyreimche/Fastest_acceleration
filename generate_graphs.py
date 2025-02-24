import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def a(t, k, epsilon, half_time, total_time, max_accel):
    """Calculate acceleration at time t using a smooth approximation of bang-bang profile.
    
    Args:
        t: Time points to evaluate acceleration at
        k: Steepness factor for transitions (k = 4/epsilon)
        epsilon: Transition time parameter
        half_time: Time at which to switch from positive to negative acceleration
        total_time: Total duration of motion
        max_accel: Maximum acceleration magnitude
    
    Returns:
        Array of acceleration values at each time point
    """
    # Smooth acceleration using hyperbolic tangent functions
    step1 = 0.5 * (1 + np.tanh(k * (t - epsilon)))
    step2 = -1.0 * (1 + np.tanh(k * (t - half_time)))
    step3 = 0.5 * (1 + np.tanh(k * (t - (total_time - epsilon))))
    return max_accel * (step1 + step2 + step3)

# Parameters
max_accel = 0.25  # m/s²
distance = 10.0   # meters
epsilon = 0.001   # Transition time parameter
k = 4.0 / epsilon  # Steepness factor

# Calculate time
base_time = 2 * np.sqrt(2 * distance / max_accel)  # Theoretical minimum time
total_time = base_time * 0.8  # Start with shorter time
target_error = 0.0001  # 0.1mm accuracy
min_time = base_time * 0.7  # Allow more margin below theoretical minimum
max_time = base_time * 0.9  # Allow some margin above theoretical minimum
max_iterations = 50
iteration = 0

while iteration < max_iterations:
    iteration += 1
    # Create time array
    dt = 0.001
    t = np.arange(0, total_time + dt, dt)

    # Calculate acceleration
    accel = a(t, k, epsilon, total_time/2, total_time, max_accel)
    
    # Calculate velocity using trapezoidal integration
    vel = np.zeros_like(t)
    for i in range(1, len(t)):
        vel[i] = vel[i-1] + 0.5 * (accel[i] + accel[i-1]) * dt
    
    # Calculate position using trapezoidal integration
    pos = np.zeros_like(t)
    for i in range(1, len(t)):
        pos[i] = pos[i-1] + 0.5 * (vel[i] + vel[i-1]) * dt
    
    final_pos = pos[-1]
    error = final_pos - distance
    
    if abs(error) < target_error:
        break
        
    if error > 0:  # Overshot
        max_time = total_time
        total_time = (min_time + total_time) / 2
    else:  # Undershot
        min_time = total_time
        total_time = (max_time + total_time) / 2

print(f"Final position: {final_pos:.6f} m")
print(f"Error: {error:.6f} m")
print(f"Time: {total_time:.6f} s")
print(f"Iterations: {iteration}")
print(f"Maximum acceleration: {np.max(np.abs(accel)):.6f} m/s²")

# Create figure
fig = plt.figure(figsize=(15, 12))
gs = plt.GridSpec(3, 1, hspace=0.3)
fig.suptitle('Continuous Motion Profiles', fontsize=14)

# Acceleration subplot
ax1 = fig.add_subplot(gs[0])
ax1.plot(t, accel, 'k-', linewidth=2)
ax1.set_ylabel('Acceleration (m/s²)')
ax1.grid(True)
ax1.set_title('Acceleration Profile')
ax1.set_ylim(-0.3, 0.3)  # Set y-axis limits to show max acceleration clearly

# Velocity subplot
ax2 = fig.add_subplot(gs[1])
ax2.plot(t, vel, 'k-', linewidth=2)
ax2.set_ylabel('Velocity (m/s)')
ax2.grid(True)
ax2.set_title('Velocity Profile')

# Position subplot
ax3 = fig.add_subplot(gs[2])
ax3.plot(t, pos, 'k-', linewidth=2)
ax3.set_ylabel('Position (m)')
ax3.set_xlabel('Time (s)')
ax3.grid(True)
ax3.set_title('Position Profile')
ax3.set_ylim(0, 11)  # Set y-axis limits to show 0 to 10m range clearly

plt.tight_layout()
plt.savefig('motion_profiles.pdf', bbox_inches='tight')
