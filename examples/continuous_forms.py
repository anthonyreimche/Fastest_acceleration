import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_continuous_forms(max_accel=0.25, distance=10.0, epsilon=0.001):
    """Plot continuous forms of acceleration, velocity, and position profiles.
    
    This function generates and plots motion profiles that satisfy the following constraints:
    1. s(t), v(t) and a(t) are continuous
    2. s(t), v(t) and a(t) are differentiable (except possibly at endpoints)
    3. |a(t)| <= max_accel at all times
    4. s(0) = 0
    5. s(T) = distance
    6. v(0) = v(T) = 0
    7. a(0) = a(T) = 0
    
    The implementation uses binary search to find the optimal time T that satisfies
    all constraints while maintaining smooth transitions through hyperbolic tangent functions.
    
    Args:
        max_accel (float): Maximum acceleration in m/s² (default: 0.25)
        distance (float): Target distance to travel in meters (default: 10.0)
        epsilon (float): Transition time for smoothing (default: 0.001)
    """
    # Calculate required time based on distance and acceleration
    # For constant acceleration: distance = 1/2 * a * t^2
    # We need 4x this time due to our acceleration profile (accelerate, decelerate)
    base_time = 2 * np.sqrt(2 * distance / max_accel)  # Base time needed
    total_time = base_time * 1.5  # Initial estimate, will be refined
    
    # Binary search to find correct time
    target_error = 0.001  # 1mm accuracy
    min_time = base_time * 0.5
    max_time = base_time * 2.0
    
    while True:
        # Create time array
        dt = 0.001  # Smaller dt to capture sharp transitions
        t = np.arange(0, total_time + dt, dt)
        half_time = total_time / 2
        k = 4.0 / epsilon  # Steepness factor
        
        # Continuous acceleration function using tanh
        def a(t):
            step1 = 0.5 * (1 + np.tanh(k * (t - epsilon)))
            step2 = -1.0 * (1 + np.tanh(k * (t - half_time)))
            step3 = 0.5 * (1 + np.tanh(k * (t - (total_time - epsilon))))
            return max_accel * (step1 + step2 + step3)
        
        # Calculate acceleration profile
        accel = a(t)
        vel = np.cumsum(accel) * dt
        pos = np.cumsum(vel) * dt
        
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
    
    # Create main window
    root = tk.Tk()
    root.title("Motion Profiles")
    
    # Create figure
    fig = plt.figure(figsize=(15, 12))
    gs = plt.GridSpec(3, 1)
    fig.suptitle('Continuous Motion Profiles', fontsize=14)
    
    # Acceleration subplot
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(t, accel, 'k-', linewidth=2)
    ax1.set_ylabel('Acceleration (m/s²)')
    ax1.grid(True)
    ax1.set_title('Acceleration Profile')
    
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
    
    # Create left and right frames
    left_frame = ttk.Frame(root)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    right_frame = ttk.Frame(root)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
    
    # Add matplotlib figure to left frame
    canvas = FigureCanvasTkAgg(fig, master=left_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    # Add scrolled text to right frame
    text_widget = tk.Text(right_frame, wrap=tk.WORD, width=50, font=('Courier', 10))
    scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    
    # Pack text widget and scrollbar
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Complete equations text with better formatting
    eqs_text = (
        '════════════════════════════════════\n'
        ' Complete Motion Equations\n'
        '════════════════════════════════════\n\n'
        '1. CONTINUOUS FORMS\n'
        '   ――――――――――――――\n\n'
        '   Acceleration:\n'
        '   a(t) = aₘₐₓ × [\n'
        '     + ½(1 + tanh(k(t-ε)))\n'
        '     - (1 + tanh(k(t-T/2)))\n'
        '     + ½(1 + tanh(k(t-(T-ε))))\n'
        '   ]\n'
        '   where k = 4/ε\n\n'
        '   Velocity:\n'
        '   v(t) = ∫₀ᵗ a(τ)dτ\n'
        '   v(t) = aₘₐₓ × [\n'
        '     + t\n'
        '     + ½k⁻¹ln(cosh(k(t-ε))/cosh(-kε))\n'
        '     - k⁻¹ln(cosh(k(t-T/2))/cosh(-kT/2))\n'
        '     + ½k⁻¹ln(cosh(k(t-(T-ε)))/cosh(-kε))\n'
        '   ]\n\n'
        '   Position:\n'
        '   s(t) = ∫₀ᵗ v(τ)dτ\n'
        '   s(t) = aₘₐₓ × [\n'
        '     + ½t²\n'
        '     + ½t·k⁻¹ln(cosh(k(t-ε))/cosh(-kε))\n'
        '     - t·k⁻¹ln(cosh(k(t-T/2))/cosh(-kT/2))\n'
        '     + ½t·k⁻¹ln(cosh(k(t-(T-ε)))/cosh(-kε))\n'
        '     + ¼k⁻²(Li₂(-e^{k(t-ε)}) - Li₂(-e^{-kε}))\n'
        '     - ½k⁻²(Li₂(-e^{k(t-T/2)}) - Li₂(-e^{-kT/2}))\n'
        '     + ¼k⁻²(Li₂(-e^{k(t-(T-ε))}) - Li₂(-e^{-kε}))\n'
        '   ]\n'
        '   where Li₂(z) is the dilogarithm function\n\n'
        '2. LIMIT FORMS (ε → 0)\n'
        '   ――――――――――――――――\n\n'
        '   Acceleration:\n'
        '   a(t) = {\n'
        '     aₘₐₓ       for 0 < t < T/2\n'
        '     -aₘₐₓ      for T/2 < t < T\n'
        '     0          otherwise\n'
        '   }\n\n'
        '   Velocity:\n'
        '   v(t) = {\n'
        '     aₘₐₓt                  for 0 ≤ t < T/2\n'
        '     aₘₐₓT - aₘₐₓ(t-T/2)    for T/2 ≤ t ≤ T\n'
        '     0                      for t < 0\n'
        '   }\n'
        '   where vₘₐₓ = aₘₐₓT/2\n\n'
        '   Position:\n'
        '   s(t) = {\n'
        '     ½aₘₐₓt²                for 0 ≤ t < T/2\n'
        '     vₘₐₓt - ½aₘₐₓ(t-T/2)²  for T/2 ≤ t ≤ T\n'
        '     0                      for t < 0\n'
        '   }\n\n'
        '3. KEY PROPERTIES\n'
        '   ――――――――――――\n\n'
        '   • Maximum velocity: vₘₐₓ = aₘₐₓT/2\n'
        '   • Final position:   s(T) = aₘₐₓT²/4\n'
        '   • Continuous at t = T/2\n'
        '   • Symmetric about t = T/2\n'
        '   • Zero initial/final velocity\n'
        '   • Bounded acceleration: |a(t)| ≤ aₘₐₓ\n\n'
        f'Parameters:\n'
        f'ε = {epsilon:.3f}s\n'
        f'k = {k:.1f}\n'
        f'T = {total_time:.1f}s\n'
        f'aₘₐₓ = {max_accel:.1f} m/s²\n'
        f'd = {distance:.1f} m\n\n'
        f'Results:\n'
        f'Max Velocity = {max(vel):.1f} m/s\n'
        f'Final Position = {pos[-1]:.1f} m'
    )
    
    # Insert text and make read-only
    text_widget.insert(tk.END, eqs_text)
    text_widget.configure(state='disabled')
    
    plt.tight_layout()
    root.mainloop()

if __name__ == "__main__":
    # Fixed parameters
    max_accel = 0.25  # m/s²
    distance = 10.0   # meters
    epsilon = 0.001   # transition time (very small)
    
    plot_continuous_forms(max_accel, distance, epsilon)
