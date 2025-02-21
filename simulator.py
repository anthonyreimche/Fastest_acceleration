import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class AccelerationProfile:
    """Defines a smooth acceleration profile for optimal motion."""
    
    def __init__(self, max_accel, total_time, transition_time=0.1):
        """
        Args:
            max_accel (float): Maximum acceleration in m/s²
            total_time (float): Total time for the motion in seconds
            transition_time (float): Time constant for smooth transitions in seconds
        """
        self.max_accel = max_accel
        self.total_time = total_time
        
        # Calculate maximum allowable transition time
        max_transition = self.calculate_max_transition_time(total_time)
        if transition_time > max_transition:
            raise ValueError(f"Transition time {transition_time}s exceeds maximum allowable time {max_transition}s for total time {total_time}s")
        
        self.transition_time = transition_time
        
    @staticmethod
    def calculate_max_transition_time(total_time):
        """Calculate the maximum allowable transition time for a given total time.
        
        Args:
            total_time (float): Total time for the motion in seconds
            
        Returns:
            float: Maximum allowable transition time in seconds
        """
        return total_time / 4.0
    
    def smooth_step(self, t, t0, direction=1):
        """Create a smooth step function using tanh.
        
        Args:
            t (float or array): Time points
            t0 (float): Time of transition
            direction (int): 1 for up-step, -1 for down-step
        """
        k = 4.0 / self.transition_time  # Controls transition steepness
        return 0.5 * (1 + np.tanh(k * (t - t0))) * direction
        
    def acceleration(self, t):
        """Compute acceleration at time t.
        
        Args:
            t (float or array): Time points
            
        Returns:
            float or array: Acceleration values
        """
        # First transition from 0 to max_accel
        step1 = self.smooth_step(t, self.transition_time)
        
        # Second transition from max_accel to -max_accel at T/2
        step2 = self.smooth_step(t, self.total_time/2, direction=-2)
        
        # Final transition from -max_accel to 0
        step3 = self.smooth_step(t, self.total_time - self.transition_time)
        
        return self.max_accel * (step1 + step2 + step3)

class AccelerationSimulator:
    """A MATLAB-style acceleration simulator."""
    
    def __init__(self):
        self.initial_velocity = 0
        self.initial_position = 0
        self.acceleration_profile = None
        
    def set_initial_conditions(self, initial_velocity=0, initial_position=0):
        """Set initial conditions for the simulation.
        
        Args:
            initial_velocity (float): Initial velocity in m/s
            initial_position (float): Initial position in m
        """
        self.initial_velocity = initial_velocity
        self.initial_position = initial_position
        
    def set_acceleration_profile(self, max_accel, total_time, transition_time=0.1):
        """Set the acceleration profile for the simulation.
        
        Args:
            max_accel (float): Maximum acceleration in m/s²
            total_time (float): Total time for the motion in seconds
            transition_time (float): Time constant for smooth transitions in seconds
        """
        self.acceleration_profile = AccelerationProfile(max_accel, total_time, transition_time)
            
    def _system(self, state, t):
        """System of differential equations.
        
        Args:
            state (array): Current state [position, velocity]
            t (float): Current time
            
        Returns:
            array: State derivatives [velocity, acceleration]
        """
        position, velocity = state
        acceleration = self.acceleration_profile.acceleration(t)
        return [velocity, acceleration]
    
    def simulate(self, dt=0.01):
        """Run the simulation.
        
        Args:
            dt (float): Time step in seconds
            
        Returns:
            tuple: Arrays of (time, position, velocity, acceleration)
        """
        if self.acceleration_profile is None:
            raise ValueError("Acceleration profile must be set before simulation")
            
        t = np.arange(0, self.acceleration_profile.total_time + dt, dt)
        initial_state = [self.initial_position, self.initial_velocity]
        
        # Solve the system of differential equations
        solution = odeint(self._system, initial_state, t)
        
        position = solution[:, 0]
        velocity = solution[:, 1]
        acceleration = self.acceleration_profile.acceleration(t)
        
        return t, position, velocity, acceleration
    
    def plot_results(self, t, position, velocity, acceleration):
        """Plot simulation results.
        
        Args:
            t (array): Time points
            position (array): Position values
            velocity (array): Velocity values
            acceleration (array): Acceleration values
        """
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
        
        ax1.plot(t, position)
        ax1.set_ylabel('Position (m)')
        ax1.grid(True)
        
        ax2.plot(t, velocity)
        ax2.set_ylabel('Velocity (m/s)')
        ax2.grid(True)
        
        ax3.plot(t, acceleration)
        ax3.set_ylabel('Acceleration (m/s²)')
        ax3.set_xlabel('Time (s)')
        ax3.grid(True)
        
        plt.tight_layout()
        plt.show()
