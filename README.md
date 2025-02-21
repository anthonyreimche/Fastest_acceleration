# Continuous Motion Profile Generator

This project implements a continuous motion profile generator that creates smooth trajectories with constrained acceleration. It uses hyperbolic tangent functions to ensure continuous and differentiable motion profiles while respecting physical constraints. The implementation aims to find the fastest possible trajectory by minimizing transition times while maintaining continuity.

## Features

- Generates continuous and differentiable motion profiles (s(t), v(t), a(t))
- Ensures acceleration stays within specified bounds (≤ 0.25 m/s²)
- Automatically finds optimal time T to reach target distance
- Approaches optimal bang-bang trajectory as transition time ε → 0
- Interactive visualization of position, velocity, and acceleration profiles
- Mathematical equations displayed alongside plots

## Optimality

The fastest possible trajectory is theoretically achieved when:
- The transition time parameter ε approaches zero (k = 4/ε → ∞)
- The acceleration profile approaches a bang-bang trajectory
- Continuity is maintained throughout the motion

In practice, we use a small but non-zero ε (default: 0.001) to maintain numerical stability while approximating the optimal solution.

## Prerequisites

- Python 3.8 or higher
- Required packages:
  - NumPy >= 1.24.0 (numerical computations)
  - Matplotlib >= 3.7.0 (plotting and visualization)
  - SciPy >= 1.10.0 (scientific computing)
  - Pandas >= 2.0.0 (data manipulation)

## Constraints

The generated motion profiles satisfy the following constraints:
- s(t), v(t) and a(t) are continuous
- s(t), v(t) and a(t) are differentiable (except possibly at endpoints)
- |a(t)| ≤ 0.25 m/s² at all times
- s(0) = 0 m
- s(T) = 10 m
- v(0) = v(T) = 0 m/s
- a(0) = a(T) = 0 m/s²

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic example:
```python
from examples.continuous_forms import plot_continuous_forms

# Generate and display motion profiles
# Default parameters: max_accel=0.25 m/s², distance=10.0 m
plot_continuous_forms()

# Custom parameters
plot_continuous_forms(max_accel=0.2, distance=8.0, epsilon=0.001)
```

## Documentation

For detailed mathematical analysis and implementation details, see:
- `documentation.tex`: Complete mathematical derivation and analysis
- `examples/continuous_forms.py`: Implementation with detailed comments

## Project Structure

- `examples/continuous_forms.py`: Main implementation of continuous motion profiles
- `documentation.tex`: Mathematical analysis and derivations
- `requirements.txt`: Project dependencies
