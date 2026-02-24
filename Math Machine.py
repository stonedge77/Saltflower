#!/usr/bin/env python3
"""
Math Machine v1.0: Translation Surface
Integrates Rotational NAND + Lorentz Vortex + NAND Prime Fractal + Physics Helpers + Spin Chain + Quantum 3-Body
Translates input through helical breath into unified field outputs
Saltflower Embodiment
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec
from enum import Enum
from dataclasses import dataclass
import sys

try:
    import qutip as qt
except ImportError:
    print("QuTiP not found. Quantum 3-body skipped.")
    qt = None

# Rotational NAND Sim (your core code, condensed)
class BreathPhase(Enum):
    IDLE = 0
    INHALE = 1
    HOLD_TORQUE = 2
    EXHALE = 3
    RETURN_ZERO = 4

@dataclass
class HelicalCell:
    phase: float = 0.0
    potential: bool = False
    signal: bool = False
    remainder: bool = False
    violation: bool = False

    def nand(self, a: bool, b: bool) -> bool:
        return not (a and b)

    def apply_torque(self, delta_phase: float = np.pi/4):
        self.phase += delta_phase
        self.phase %= (2 * np.pi)
        return (int(self.phase / (np.pi/4))) % 2 == 1

    def breath_cycle(self, signal_in: bool, admit: bool) -> bool:
        self.potential = signal_in
        has_friction = self.apply_torque()
        if not admit and (self.signal == self.potential):
            self.violation = True
            return False
        self.signal = self.nand(self.potential, self.signal)
        self.remainder = self.signal ^ self.potential
        return self.signal

class HelicalNANDArray:
    def __init__(self, num_cells: int = 8):
        self.cells = [HelicalCell() for _ in range(num_cells)]
        self.num_cells = num_cells
        self.breath_count = 0

    def process(self, data_in: np.ndarray) -> tuple:
        signals = np.zeros(self.num_cells, dtype=bool)
        remainders = np.zeros(self.num_cells, dtype=bool)
        any_violation = False
        for i, cell in enumerate(self.cells):
            sig_in = data_in[i] if i == 0 else signals[i-1]
            admit = sig_in != cell.potential
            sig_out = cell.breath_cycle(sig_in, admit)
            signals[i] = sig_out
            remainders[i] = cell.remainder
            if cell.violation:
                any_violation = True
        self.breath_count += 1
        return signals, remainders, any_violation

    def get_phase_state(self) -> np.ndarray:
        return np.array([cell.phase for cell in self.cells])

class PrimalMathEngine:
    def __init__(self):
        self.helix_a = HelicalNANDArray()
        self.helix_b = HelicalNANDArray()

    def bits_from_int(self, n: int, width: int = 8) -> np.ndarray:
        return np.array([(n >> i) & 1 for i in range(width)], dtype=bool)

    def int_from_bits(self, bits: np.ndarray) -> int:
        return sum(int(b) << i for i, b in enumerate(bits))

    def add(self, a: int, b: int) -> tuple:
        bits_a = self.bits_from_int(a)
        bits_b = self.bits_from_int(b)
        out_a, rem_a, _ = self.helix_a.process(bits_a)
        out_b, rem_b, _ = self.helix_b.process(bits_b)
        result_bits = out_a ^ out_b
        t1_remainder = rem_a | rem_b
        return self.int_from_bits(result_bits), t1_remainder

    def multiply(self, a: int, b: int) -> tuple:
        bits_a = self.bits_from_int(a)
        bits_b = self.bits_from_int(b)
        out_a, rem_a, _ = self.helix_a.process(bits_a)
        out_b, rem_b, _ = self.helix_b.process(bits_b)
        result = 0
        a_int = self.int_from_bits(out_a)
        for i, bit in enumerate(out_b):
            if bit:
                result += (a_int << i)
        return result & 0xFF, rem_a ^ rem_b

    def is_prime_disjoint(self, n: int) -> bool:
        bits = self.bits_from_int(n)
        _, remainders, _ = self.helix_a.process(bits)
        return np.sum(remainders) == np.sum(remainders ^ bits)

# Lorentz Vortex (your snippet)
class LorentzVortex:
    def __init__(self, N=200):
        self.N = N
        theta = np.random.uniform(0, 2*np.pi, N)
        r = np.random.uniform(0, 1.0, N)
        self.pos = np.column_stack((r * np.cos(theta), r * np.sin(theta)))
        self.vel = np.random.normal(0, 0.1, (N, 2))
        self.B = np.array([0, 0, 1.0])
        self.E = np.array([0.5, 0, 0])
        self.history = []

    def step(self, dt=0.01):
        v_cross_B = np.cross(np.hstack((self.vel, np.zeros((self.N,1)))), self.B)[:, :2]
        accel = (self.E[:2] + v_cross_B)
        self.vel += accel * dt
        self.pos += self.vel * dt
        self.history.append(self.pos.copy())

    def run(self, steps=500, dt=0.01):
        self.history = []
        for _ in range(steps):
            self.step(dt)
        return np.array(self.history)

# NAND Prime Fractal (your snippet)
def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def generate_nand_prime_fractal(size=512, max_depth=3):
    img = np.zeros((size, size), dtype=int)
    mask = (1 << max_depth) - 1
    for x in range(size):
        for y in range(size):
            if not ((x & mask) & (y & mask)):
                value = x + y
                if is_prime(value):
                    img[y, x] = 2
                else:
                    img[y, x] = 1
    return img

# Physics Helpers (your snippet)
def dipole_field_2d(x: np.ndarray, y: np.ndarray, dipole_pos: tuple = (-1,0), moment: tuple = (0,1), strength: float = 1.0):
    px, py = dipole_pos
    mx, my = moment
    dx = x - px
    dy = y - py
    r2 = dx**2 + dy**2 + 1e-10
    r3 = r2 ** 1.5
    r5 = r2 ** 2.5
    Bx = strength * (3 * dx * (mx * dx + my * dy) / r5 - mx / r3)
    By = strength * (3 * dy * (mx * dx + my * dy) / r5 - my / r3)
    return Bx, By

def parallel_dipole_gap_field(x: np.ndarray, y: np.ndarray):
    Bx1, By1 = dipole_field_2d(x, y, dipole_pos=(-1,0), moment=(0,1))
    Bx2, By2 = dipole_field_2d(x, y, dipole_pos=(1,0), moment=(0,-1))
    return Bx1 + Bx2, By1 + By2

# Spin Chain (your snippet)
def ising_energy(spins: np.ndarray, J: float = 1.0, h: float = 0.0) -> float:
    interaction = np.sum(spins * np.roll(spins, -1))
    field = np.sum(spins)
    return -J * interaction - h * field

def metropolis_step(spins: np.ndarray, T: float = 1.0, J: float = 1.0, h: float = 0.0) -> np.ndarray:
    i = np.random.randint(len(spins))
    dE = 2 * J * spins[i] * (spins[i-1] + spins[(i+1) % len(spins)]) + 2 * h * spins[i]
    if dE < 0 or np.random.rand() < np.exp(-dE / T):
        spins[i] *= -1
    return spins

def simulate_1d_spin_chain(N: int = 50, steps: int = 1000, T: float = 2.0, J: float = 1.0, h: float = 0.5) -> tuple:
    spins = np.random.choice([-1, 1], N)
    for _ in range(steps):
        spins = metropolis_step(spins, T, J, h)
    avg_mag = np.mean(spins)
    return spins, avg_mag

# Quantum 3-Body (your pasted code, adapted)
def quantum_3body_demo(J=1.0, h=0.5, g=0.2):
    if qt is None:
        return None, None
    sx = qt.sigmax()
    sz = qt.sigmaz()
    I = qt.identity(2)
    sx1 = qt.tensor(sx, I, I)
    sx2 = qt.tensor(I, sx, I)
    sx3 = qt.tensor(I, I, sx)
    sz1 = qt.tensor(sz, I, I)
    sz2 = qt.tensor(I, sz, I)
    sz3 = qt.tensor(I, I, sz)
    sz123 = qt.tensor(sz, sz, sz)
    H = J * (sx1 * sx2 + sx2 * sx3 + sx3 * sx1) + h * (sz1 + sz2 + sz3) + g * sz123
    psi0 = qt.tensor(qt.basis(2,0), qt.basis(2,0), qt.basis(2,0))
    tlist = np.linspace(0, 10, 100)
    result = qt.mesolve(H, psi0, tlist, [], [sz1, sz2, sz3])
    return tlist, result.expect

# Unified Translation Surface
class MathMachine:
    def __init__(self, input_num=7):
        self.input_num = input_num
        self.engine = PrimalMathEngine()
        self.vortex = LorentzVortex(N=100)
        self.fractal = generate_nand_prime_fractal(256, 3)
        self.spin_spins, self.spin_mag = simulate_1d_spin_chain()
        self.q3_tlist, self.q3_expect = quantum_3body_demo()

    def translate(self):
        a = self.input_num
        b = self.input_num + 2
        add_res, add_t1 = self.engine.add(a, b)
        mul_res, mul_t1 = self.engine.multiply(a, b)
        is_prime = self.engine.is_prime_disjoint(a)
        vortex_hist = self.vortex.run(steps=100)
        return add_res, mul_res, is_prime, vortex_hist, self.fractal, self.spin_spins, self.q3_tlist, self.q3_expect

    def visualize_translation(self):
        add_res, mul_res, is_prime, vortex_hist, fractal, spins, q3_tlist, q3_expect = self.translate()
        fig = plt.figure(figsize=(16, 12))
        gs = GridSpec(3, 3, fig)
        fig.suptitle(f'Math Machine Translation: Input {self.input_num}\nHelical NAND → Field Outputs', fontsize=16)

        # NAND Results
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.text(0.1, 0.5, f'ADD: {add_res}\nMUL: {mul_res}\nPrime: {is_prime}', fontsize=12)
        ax1.axis('off')
        ax1.set_title('Primal Math')

        # Lorentz Vortex
        ax2 = fig.add_subplot(gs[0, 1])
        for i in range(10):  # Sample trails
            ax2.plot(vortex_hist[:, i, 0], vortex_hist[:, i, 1], 'b-', alpha=0.5)
        ax2.set_title('Lorentz Vortex (EM Breath)')

        # NAND Prime Fractal
        ax3 = fig.add_subplot(gs[0, 2])
        ax3.imshow(fractal, cmap='hot', origin='lower')
        ax3.set_title('NAND Prime Fractal')

        # Dipole Gap
        ax4 = fig.add_subplot(gs[1, 0])
        x = np.linspace(-2, 2, 30)
        y = np.linspace(-2, 2, 30)
        X, Y = np.meshgrid(x, y)
        Bx, By = parallel_dipole_gap_field(X, Y)
        Bmag = np.sqrt(Bx**2 + By**2)
        ax4.streamplot(X, Y, Bx, By, color=Bmag, cmap='inferno')
        ax4.set_title('Dipole Gap (Horizon)')

        # Spin Chain
        ax5 = fig.add_subplot(gs[1, 1])
        ax5.scatter(range(len(spins)), spins, c=['red' if s > 0 else 'blue' for s in spins])
        ax5.set_title(f'Spin Chain (Mag: {self.spin_mag:.2f})')

        # Quantum 3-Body
        ax6 = fig.add_subplot(gs[1, 2])
        if q3_tlist is not None:
            ax6.plot(q3_tlist, q3_expect[0], label='sz1')
            ax6.plot(q3_tlist, q3_expect[1], label='sz2')
            ax6.plot(q3_tlist, q3_expect[2], label='sz3')
            ax6.legend()
        ax6.set_title('Quantum 3-Body (Gravity)')

        # Summary
        ax7 = fig.add_subplot(gs[2, :])
        ax7.text(0.5, 0.5, 'Translation Surface: Classical input exhales quantum fields\n0 ≠ 1 preserved, T=1 remainder in every layer', ha='center')
        ax7.axis('off')

        plt.tight_layout()
        plt.savefig('math_machine_translation.png')
        return fig

if __name__ == '__main__':
    machine = MathMachine(input_num=777)  # Your number
    machine.visualize_translation()
    plt.show()
