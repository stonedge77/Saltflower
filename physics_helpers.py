# physics_helpers.py
"""
Physics helpers for Saltflower — companion to emergent_laws_db.json
Focus: magnetic fields, Lorentz force, simple vortex indicators.
Minimal dependencies (numpy only for core math; matplotlib optional for viz).

Ties to laws:
- HELICAL_REALM: dipole field lines, Lorentz trajectories
- TORQUE: magnetic moments, cross-product forces
- HORIZON_INTEGRITY: field strength in gap (eye), boundary exclusion
"""

import numpy as np

def dipole_field_2d(x: np.ndarray, y: np.ndarray, dipole_pos: tuple = (-1,0), moment: tuple = (0,1), strength: float = 1.0):
    """Magnetic field from single dipole at position (px, py) with moment (mx, my)."""
    px, py = dipole_pos
    mx, my = moment
    dx = x - px
    dy = y - py
    r2 = dx**2 + dy**2 + 1e-10  # avoid singularity
    r3 = r2 ** 1.5
    r5 = r2 ** 2.5
    
    Bx = strength * (3 * dx * (mx * dx + my * dy) / r5 - mx / r3)
    By = strength * (3 * dy * (mx * dx + my * dy) / r5 - my / r3)
    return Bx, By


def parallel_dipole_gap_field(x: np.ndarray, y: np.ndarray):
    """Field between two parallel dipoles (gap 'eye' where phase threads)."""
    Bx1, By1 = dipole_field_2d(x, y, dipole_pos=(-1,0), moment=(0,1))
    Bx2, By2 = dipole_field_2d(x, y, dipole_pos=(1,0), moment=(0,-1))
    return Bx1 + Bx2, By1 + By2


def lorentz_accel_2d(vel: np.ndarray, E: np.ndarray = np.array([0.5,0]), B: np.ndarray = np.array([0,0,1])):
    """Lorentz acceleration on unit charge/mass particle: a = E + v × B (2D slice)"""
    vx, vy = vel
    # v × B (z-component only matters in 2D)
    v_cross_Bx = vy * B[2]
    v_cross_By = -vx * B[2]
    ax = E[0] + v_cross_Bx
    ay = E[1] + v_cross_By
    return np.array([ax, ay])


def simple_vortex_indicator(pos_history: np.ndarray):
    """Basic metric: angular momentum proxy around origin.
    Higher = more coherent vortex behavior."""
    x, y = pos_history[:,0], pos_history[:,1]
    r2 = x**2 + y**2 + 1e-10
    angular_momentum = np.mean(x * y.diff() - y * x.diff())  # crude discrete Lz proxy
    return abs(angular_momentum) / np.mean(r2)


# Optional visualization helper (matplotlib)
def plot_dipole_gap():
    import matplotlib.pyplot as plt
    
    x = np.linspace(-2, 2, 30)
    y = np.linspace(-2, 2, 30)
    X, Y = np.meshgrid(x, y)
    
    Bx, By = parallel_dipole_gap_field(X, Y)
    Bmag = np.sqrt(Bx**2 + By**2)
    
    fig, ax = plt.subplots(figsize=(7,6))
    strm = ax.streamplot(X, Y, Bx, By, density=1.8, color=Bmag, cmap='inferno')
    ax.set_title("Magnetic Field in Parallel Dipole Gap\n('Eye' region for phase threading)")
    ax.set_aspect('equal')
    plt.colorbar(strm.lines, label='|B|')
    plt.show()
