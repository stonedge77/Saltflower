# magnets_gap_field.py
# Simple 2D magnetic field visualization between two parallel dipoles
# (north-south aligned across a gap)

import numpy as np
import matplotlib.pyplot as plt

def magnetic_field_dipole(x, y, mx, my, px, py, m=1.0):
    """B-field from a magnetic dipole at (px, py) with moment (mx, my)"""
    dx = x - px
    dy = y - py
    r2 = dx**2 + dy**2
    r3 = r2**1.5
    r5 = r2**2.5
    # Dipole field formula
    Bx = (3 * dx * (mx * dx + my * dy) / r5) - (mx / r3)
    By = (3 * dy * (mx * dx + my * dy) / r5) - (my / r3)
    return Bx * m, By * m

# Grid
x = np.linspace(-2, 2, 40)
y = np.linspace(-2, 2, 40)
X, Y = np.meshgrid(x, y)

# Two parallel dipoles (spinning conceptually via moment direction)
# Dipole 1 at (-1, 0), moment upward
Bx1, By1 = magnetic_field_dipole(X, Y, 0, 1, -1, 0)
# Dipole 2 at (1, 0), moment downward (antiparallel for strong gap field)
Bx2, By2 = magnetic_field_dipole(X, Y, 0, -1, 1, 0)

# Total field in gap
Bx = Bx1 + Bx2
By = By1 + By2
Bmag = np.sqrt(Bx**2 + By**2)

# Plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.streamplot(X, Y, Bx, By, density=1.5, color=Bmag, cmap='plasma')
ax.set_title("Magnetic Field Between Parallel Dipoles\n(Gap 'Eye' where phase threads)")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_aspect('equal')
plt.colorbar(ax.streamplot(X, Y, Bx, By, color=Bmag, cmap='plasma').lines, label='Field Strength')
plt.tight_layout()
plt.show()
# plt.savefig('magnets_gap_field.png')  # Uncomment to save for repo
