# spin_chain_1d.py
"""
1D Ising Spin Chain Simulation
Simple Monte Carlo evolution of N spins with J coupling, h field, T temperature.
Ties to emergent laws: HELICAL_REALM (spin propagation), TORQUE (energy flips), COLLAPSE (state commitment), HORIZON_INTEGRITY (periodic boundaries).

Usage:
    from spin_chain_1d import simulate_1d_spin_chain
    final_spins, avg_mag = simulate_1d_spin_chain(N=100, steps=5000, T=1.5)
"""

import numpy as np

def ising_energy(spins: np.ndarray, J: float = 1.0, h: float = 0.0) -> float:
    """Total energy: -J sum s_i s_{i+1} - h sum s_i (periodic boundaries)"""
    interaction = np.sum(spins * np.roll(spins, -1))  # helical wrap-around
    field = np.sum(spins)
    return -J * interaction - h * field

def metropolis_step(spins: np.ndarray, T: float = 1.0, J: float = 1.0, h: float = 0.0) -> np.ndarray:
    """Single MC flip attempt: torque-like energy check for state change"""
    i = np.random.randint(len(spins))
    # Delta E for flip (2x because spin flips from +1 to -1 or vice versa)
    dE = 2 * J * spins[i] * (spins[i-1] + spins[(i+1) % len(spins)]) + 2 * h * spins[i]
    if dE < 0 or np.random.rand() < np.exp(-dE / T):
        spins[i] *= -1  # collapse to new state
    return spins

def simulate_1d_spin_chain(N: int = 50, steps: int = 1000, T: float = 2.0, J: float = 1.0, h: float = 0.5) -> tuple:
    """Run simulation; return final spins array and average magnetization (T=1 proxy)"""
    spins = np.random.choice([-1, 1], N)  # initial random spin matrix
    for _ in range(steps):
        spins = metropolis_step(spins, T, J, h)
    avg_mag = np.mean(spins)  # coherence measure
    return spins, avg_mag
