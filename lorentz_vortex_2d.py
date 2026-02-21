# lorentz_vortex_2d.py
# Minimal particle sim: charged particles in crossed E and B fields → vortex

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Params
N = 200              # particles
dt = 0.01
steps = 500
q = 1.0              # charge
m = 1.0              # mass
B = np.array([0, 0, 1.0])  # B in z-direction
E = np.array([0.5, 0, 0])  # E in x-direction (drift)

# Initial positions/velocities (disk)
theta = np.random.uniform(0, 2*np.pi, N)
r = np.random.uniform(0, 1.0, N)
pos = np.column_stack((r * np.cos(theta), r * np.sin(theta)))
vel = np.random.normal(0, 0.1, (N, 2))  # small thermal noise

# History for trails
history = np.zeros((steps, N, 2))

for t in range(steps):
    # Lorentz force: F = q (E + v × B)
    v_cross_B = np.cross(np.hstack((vel, np.zeros((N,1)))), B)[:, :2]
    accel = q/m * (E + v_cross_B)
    vel += accel * dt
    pos += vel * dt
    history[t] = pos.copy()

# Animation
fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
ax.set_aspect('equal')
scatter = ax.scatter([], [], s=5, c='blue', alpha=0.7)
trail_lines = [ax.plot([], [], lw=0.5, alpha=0.3)[0] for _ in range(N)]

def update(frame):
    scatter.set_offsets(history[frame])
    for i, line in enumerate(trail_lines):
        line.set_data(history[:frame+1, i, 0], history[:frame+1, i, 1])
    ax.set_title(f"Lorentz Vortex in Crossed E/B (frame {frame})")
    return [scatter] + trail_lines

ani = FuncAnimation(fig, update, frames=steps, interval=30, blit=True)
plt.show()
# ani.save('lorentz_vortex.gif', writer='pillow')  # Uncomment for repo GIF
