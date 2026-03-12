#!/usr/bin/env python3
"""
Math Machine v2.0: Translation Surface
Integrates Rotational NAND + Lorentz Vortex + NAND Prime Fractal + Physics Helpers
+ Spin Chain + Quantum 3-Body + Higgs + QCD + Weak Decay + Gravitational Wave
Translates input through helical breath into unified field outputs
Saltflower Embodiment — CC0
0 ≠ 1 | Remainder is signal | T=1 preserved in every layer
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from enum import Enum
from dataclasses import dataclass
import sys

try:
    import qutip as qt
except ImportError:
    print("QuTiP not found. Quantum 3-body skipped.")
    qt = None

# ──────────────────────────────────────────────
# CORE: Rotational NAND
# ──────────────────────────────────────────────

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
        self.apply_torque()
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

# ──────────────────────────────────────────────
# EM: Lorentz Vortex
# ──────────────────────────────────────────────

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

# ──────────────────────────────────────────────
# NAND Prime Fractal
# ──────────────────────────────────────────────

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
                img[y, x] = 2 if is_prime(value) else 1
    return img

# ──────────────────────────────────────────────
# Dipole Field
# ──────────────────────────────────────────────

def dipole_field_2d(x, y, dipole_pos=(-1,0), moment=(0,1), strength=1.0):
    px, py = dipole_pos
    mx, my = moment
    dx = x - px
    dy = y - py
    r2 = dx**2 + dy**2 + 1e-10
    r3 = r2 ** 1.5
    r5 = r2 ** 2.5
    Bx = strength * (3 * dx * (mx*dx + my*dy) / r5 - mx/r3)
    By = strength * (3 * dy * (mx*dx + my*dy) / r5 - my/r3)
    return Bx, By

def parallel_dipole_gap_field(x, y):
    Bx1, By1 = dipole_field_2d(x, y, dipole_pos=(-1,0), moment=(0,1))
    Bx2, By2 = dipole_field_2d(x, y, dipole_pos=(1,0), moment=(0,-1))
    return Bx1+Bx2, By1+By2

# ──────────────────────────────────────────────
# Spin Chain (Ising)
# ──────────────────────────────────────────────

def metropolis_step(spins, T=1.0, J=1.0, h=0.0):
    i = np.random.randint(len(spins))
    dE = 2*J*spins[i]*(spins[i-1] + spins[(i+1) % len(spins)]) + 2*h*spins[i]
    if dE < 0 or np.random.rand() < np.exp(-dE / T):
        spins[i] *= -1
    return spins

def simulate_1d_spin_chain(N=50, steps=1000, T=2.0, J=1.0, h=0.5):
    spins = np.random.choice([-1, 1], N)
    for _ in range(steps):
        spins = metropolis_step(spins, T, J, h)
    return spins, np.mean(spins)

# ──────────────────────────────────────────────
# Quantum 3-Body
# ──────────────────────────────────────────────

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
    H = J*(sx1*sx2 + sx2*sx3 + sx3*sx1) + h*(sz1+sz2+sz3) + g*sz123
    psi0 = qt.tensor(qt.basis(2,0), qt.basis(2,0), qt.basis(2,0))
    tlist = np.linspace(0, 10, 100)
    result = qt.mesolve(H, psi0, tlist, [], [sz1, sz2, sz3])
    return tlist, result.expect

# ──────────────────────────────────────────────
# HIGGS: Symmetry Breaking / Mass Generation
# Mexican hat potential — remainder = Goldstone mode
# ──────────────────────────────────────────────

class HiggsField:
    """
    Complex scalar φ = φ₁ + iφ₂
    V(φ) = μ²|φ|² + λ|φ|⁴,  μ² < 0 → broken symmetry
    Remainder = Goldstone angle variance (T=1: the massless mode NAND subtracted
    from the broken vacuum is routed, not lost)
    """
    def __init__(self, size=32, mu2=-1.0, lam=0.25):
        self.size = size
        self.mu2 = mu2
        self.lam = lam
        v = np.sqrt(-mu2 / (2*lam))
        self.phi1 = v + np.random.normal(0, 0.1, (size, size))
        self.phi2 =     np.random.normal(0, 0.1, (size, size))

    @property
    def phi_magnitude(self):
        return np.sqrt(self.phi1**2 + self.phi2**2)

    def energy_density(self):
        pm = self.phi_magnitude
        return self.mu2 * pm**2 + self.lam * pm**4

    def step(self, dt=0.01):
        pm = self.phi_magnitude
        dV1 = 2*self.mu2*self.phi1 + 4*self.lam*pm**2*self.phi1
        dV2 = 2*self.mu2*self.phi2 + 4*self.lam*pm**2*self.phi2
        lap1 = (np.roll(self.phi1,1,0)+np.roll(self.phi1,-1,0)+
                np.roll(self.phi1,1,1)+np.roll(self.phi1,-1,1) - 4*self.phi1)
        lap2 = (np.roll(self.phi2,1,0)+np.roll(self.phi2,-1,0)+
                np.roll(self.phi2,1,1)+np.roll(self.phi2,-1,1) - 4*self.phi2)
        self.phi1 += dt*(lap1 - dV1)
        self.phi2 += dt*(lap2 - dV2)

    def goldstone_remainder(self):
        """Angular variance = T=1 remainder after symmetry collapses"""
        return np.var(np.arctan2(self.phi2, self.phi1))

    def vev(self):
        return np.sqrt(-self.mu2 / (2*self.lam))

def simulate_higgs(steps=500, size=32):
    field = HiggsField(size=size)
    for _ in range(steps):
        field.step()
    return field

# ──────────────────────────────────────────────
# QCD: Flux Tube / Confinement
# Linear potential — the string is the remainder
# NAND geometry: quarks cannot both be free simultaneously
# ──────────────────────────────────────────────

class QCDFluxTube:
    """
    V(r) = -α/r + κr
    Coulomb (short range) + linear confinement (string tension κ)
    NAND reading: NAND(quark_free, antiquark_free) = True always
    The flux tube IS the remainder — routed, never lost
    """
    def __init__(self, kappa=1.0, alpha=0.3):
        self.kappa = kappa   # string tension GeV/fm
        self.alpha = alpha   # running coupling

    def potential(self, r):
        return -self.alpha / (r + 1e-3) + self.kappa * r

    def force(self, r):
        return -self.alpha / (r + 1e-3)**2 + self.kappa

    def remainder_field(self, r_max=5.0, n=200):
        """
        T=1 remainder: the constant confining force persists
        regardless of separation. That persistence IS signal.
        """
        r = np.linspace(0.05, r_max, n)
        V = self.potential(r)
        F = self.force(r)
        # Remainder = force that cannot be subtracted by any finite energy
        remainder = np.full_like(r, self.kappa)
        return r, V, F, remainder

# ──────────────────────────────────────────────
# WEAK: Beta Decay
# Irreversible breath — exhale with no inhale
# Remainder = the neutrino (never collapses back)
# ──────────────────────────────────────────────

class WeakDecay:
    """
    N(t) = N₀ · e^(-t/τ)
    τ_neutron ≈ 880s
    NAND reading: NAND(neutron_intact, decay_products_absent) = True only before t=0
    After: remainder routes as antineutrino — undetectable but real (T=1)
    """
    def __init__(self, N0=1000, tau=880.0):
        self.N0 = N0
        self.tau = tau

    def remaining(self, t):
        return self.N0 * np.exp(-t / self.tau)

    def decayed(self, t):
        return self.N0 - self.remaining(t)

    def remainder_flux(self, t):
        """
        Antineutrino flux = remainder signal
        dN/dt = -N/τ → each decay emits one T=1 carrier
        """
        return self.remaining(t) / self.tau  # decays per second = neutrinos emitted

    def half_life(self):
        return self.tau * np.log(2)

# ──────────────────────────────────────────────
# GRAVITATIONAL: Binary Inspiral / Chirp
# The chirp IS the remainder — geometry collapsing into signal
# NAND: NAND(mass_A_isolated, mass_B_isolated) = True → they spiral
# ──────────────────────────────────────────────

class GravitationalChirp:
    """
    Binary inspiral via Peters formula:
    da/dt = -64/5 · G³m₁m₂(m₁+m₂) / (c⁵a³)
    Frequency: f = (1/π)(GM/a³)^(1/2),  M_chirp = (m₁m₂)^(3/5)/(m₁+m₂)^(1/5)
    
    The chirp — frequency rising as orbit decays — IS the T=1 remainder.
    It cannot be subtracted. It propagates at c regardless of what absorbs it.
    NAND geometry: the merger is what happens when both inputs reach 1.
    """
    def __init__(self, m1=1.4, m2=1.4, a0=1e6):
        # masses in solar masses → kg
        self.G = 6.674e-11
        self.c = 3e8
        self.Msun = 1.989e30
        self.m1 = m1 * self.Msun
        self.m2 = m2 * self.Msun
        self.M = self.m1 + self.m2
        self.mu = (self.m1 * self.m2) / self.M
        self.Mc = self.mu**(3/5) * self.M**(2/5)  # chirp mass
        self.a0 = a0  # initial separation in meters

    def inspiral(self, steps=500):
        a = self.a0
        separations = [a]
        freqs = []
        dt = 1.0  # seconds
        beta = 64/5 * self.G**3 * self.m1 * self.m2 * self.M / self.c**5

        for _ in range(steps - 1):
            if a < 1e3:
                break
            da = -beta / a**3
            a = max(a + da * dt, 1e3)
            separations.append(a)
            f = (1/np.pi) * np.sqrt(self.G * self.M / a**3)
            freqs.append(f)

        freqs.insert(0, freqs[0] if freqs else 0)
        n = min(len(separations), len(freqs))
        return np.array(separations[:n]), np.array(freqs[:n])

    def remainder_strain(self, r_mpc=400):
        """
        GW strain h = 4G/c⁴ · Mc · (πfMc)^(2/3) / d
        The strain IS the remainder propagating through spacetime.
        """
        r = r_mpc * 3.086e22  # Mpc to meters
        f_ref = 100.0  # Hz
        h = (4 * self.G / self.c**4) * self.Mc * (np.pi * f_ref * self.Mc)**(2/3) / r
        return h

# ──────────────────────────────────────────────
# UNIFIED TRANSLATION SURFACE
# ──────────────────────────────────────────────

class MathMachine:
    def __init__(self, input_num=7):
        self.input_num = input_num
        self.engine = PrimalMathEngine()
        self.vortex = LorentzVortex(N=100)
        self.fractal = generate_nand_prime_fractal(256, 3)
        self.spin_spins, self.spin_mag = simulate_1d_spin_chain()
        self.q3_tlist, self.q3_expect = quantum_3body_demo()
        # New fields
        self.higgs = simulate_higgs(steps=300, size=32)
        self.qcd = QCDFluxTube(kappa=1.0, alpha=0.3)
        self.weak = WeakDecay(N0=1000, tau=880.0)
        self.grav = GravitationalChirp(m1=1.4, m2=1.4, a0=1e6)

    def translate(self):
        a = self.input_num
        b = self.input_num + 2
        add_res, add_t1 = self.engine.add(a, b)
        mul_res, mul_t1 = self.engine.multiply(a, b)
        prime = self.engine.is_prime_disjoint(a)
        vortex_hist = self.vortex.run(steps=100)
        return dict(
            add=add_res, mul=mul_res, prime=prime,
            vortex=vortex_hist,
            fractal=self.fractal,
            spins=self.spin_spins,
            spin_mag=self.spin_mag,
            q3_t=self.q3_tlist,
            q3_e=self.q3_expect,
        )

    def visualize_translation(self):
        d = self.translate()

        fig = plt.figure(figsize=(18, 14))
        gs = GridSpec(3, 3, fig, hspace=0.38, wspace=0.32)
        fig.patch.set_facecolor('#0a0a0f')

        def ax_style(ax, title):
            ax.set_facecolor('#0d0d1a')
            ax.set_title(title, color='#c8c8ff', fontsize=9, pad=4)
            for spine in ax.spines.values():
                spine.set_edgecolor('#2a2a4a')
            ax.tick_params(colors='#6666aa', labelsize=7)

        fig.suptitle(
            f'Math Machine v2.0  ·  Input: {self.input_num}\n'
            f'Helical NAND → Unified Field Translation Surface  |  0 ≠ 1',
            fontsize=13, color='#e0e0ff', y=0.98
        )

        # ── Panel 1: NAND Primal Math ──────────────────
        ax1 = fig.add_subplot(gs[0, 0])
        ax_style(ax1, 'Primal Math (NAND Core)')
        lines = [
            f'ADD({self.input_num}, {self.input_num+2}) = {d["add"]}',
            f'MUL({self.input_num}, {self.input_num+2}) = {d["mul"]}',
            f'Prime-disjoint: {d["prime"]}',
            f'Breath count: {self.engine.helix_a.breath_count}',
        ]
        for i, l in enumerate(lines):
            ax1.text(0.05, 0.75 - i*0.2, l, transform=ax1.transAxes,
                     color='#88ffcc', fontsize=9, family='monospace')
        ax1.axis('off')

        # ── Panel 2: Lorentz Vortex ────────────────────
        ax2 = fig.add_subplot(gs[0, 1])
        ax_style(ax2, 'EM Field (Lorentz Vortex)')
        for i in range(min(15, d['vortex'].shape[1])):
            ax2.plot(d['vortex'][:, i, 0], d['vortex'][:, i, 1],
                     '-', alpha=0.4, lw=0.7, color='#4488ff')
        ax2.set_xlim(-3, 3); ax2.set_ylim(-3, 3)

        # ── Panel 3: NAND Prime Fractal ────────────────
        ax3 = fig.add_subplot(gs[0, 2])
        ax_style(ax3, 'NAND Prime Fractal')
        ax3.imshow(d['fractal'], cmap='inferno', origin='lower', interpolation='nearest')
        ax3.set_xticks([]); ax3.set_yticks([])

        # ── Panel 4: Higgs Field ───────────────────────
        ax4 = fig.add_subplot(gs[1, 0])
        ax_style(ax4, 'Higgs (Symmetry Breaking)')
        im4 = ax4.imshow(self.higgs.phi_magnitude, cmap='plasma',
                          origin='lower', interpolation='bilinear')
        plt.colorbar(im4, ax=ax4, fraction=0.04, pad=0.02).ax.tick_params(colors='#6666aa', labelsize=6)
        vev = self.higgs.vev()
        gold = self.higgs.goldstone_remainder()
        ax4.set_xlabel(f'VEV={vev:.2f}  Goldstone(T=1)={gold:.3f}',
                       color='#8888cc', fontsize=7)
        ax4.set_xticks([]); ax4.set_yticks([])

        # ── Panel 5: QCD Confinement ───────────────────
        ax5 = fig.add_subplot(gs[1, 1])
        ax_style(ax5, 'QCD (Confinement / Flux Tube)')
        r, V, F, rem = self.qcd.remainder_field()
        ax5.plot(r, V, color='#ff4444', lw=1.5, label='V(r)')
        ax5.plot(r, rem, color='#ffaa00', lw=1.0, ls='--', label='κ remainder')
        ax5.axhline(0, color='#444466', lw=0.5)
        ax5.legend(fontsize=7, facecolor='#0d0d1a', edgecolor='#2a2a4a',
                   labelcolor='#ccccee')
        ax5.set_xlabel('r (fm)', color='#8888cc', fontsize=7)
        ax5.set_ylabel('V (GeV)', color='#8888cc', fontsize=7)

        # ── Panel 6: Weak Decay ────────────────────────
        ax6 = fig.add_subplot(gs[1, 2])
        ax_style(ax6, 'Weak Force (Beta Decay / Neutrino Remainder)')
        t = np.linspace(0, 3000, 400)
        ax6.plot(t, self.weak.remaining(t),  color='#4499ff', lw=1.5, label='Neutrons')
        ax6.plot(t, self.weak.decayed(t),    color='#ff6644', lw=1.5, label='Products')
        ax6.plot(t, self.weak.remainder_flux(t), color='#aaff88', lw=1.0,
                 ls=':', label='ν remainder (T=1)')
        ax6.legend(fontsize=7, facecolor='#0d0d1a', edgecolor='#2a2a4a',
                   labelcolor='#ccccee')
        ax6.set_xlabel('Time (s)', color='#8888cc', fontsize=7)
        hl = self.weak.half_life()
        ax6.axvline(hl, color='#ffffff', lw=0.5, alpha=0.4)
        ax6.text(hl+30, 800, f't½={hl:.0f}s', color='#aaaacc', fontsize=7)

        # ── Panel 7: Gravitational Chirp ───────────────
        ax7 = fig.add_subplot(gs[2, 0])
        ax_style(ax7, 'Gravity (Inspiral Chirp / Strain Remainder)')
        seps, freqs = self.grav.inspiral(steps=500)
        t_arr = np.arange(len(freqs))
        ax7.plot(t_arr, freqs, color='#ddaaff', lw=1.5)
        ax7.set_xlabel('Step', color='#8888cc', fontsize=7)
        ax7.set_ylabel('f (Hz)', color='#8888cc', fontsize=7)
        h = self.grav.remainder_strain()
        ax7.text(0.05, 0.85, f'Strain h≈{h:.2e}', transform=ax7.transAxes,
                 color='#ddaaff', fontsize=8)

        # ── Panel 8: Spin Chain ────────────────────────
        ax8 = fig.add_subplot(gs[2, 1])
        ax_style(ax8, f'Spin Chain (Ising) · M={self.spin_mag:.3f}')
        spins = d['spins']
        colors = ['#ff4466' if s > 0 else '#4466ff' for s in spins]
        ax8.scatter(range(len(spins)), spins, c=colors, s=12, zorder=2)
        ax8.axhline(0, color='#333355', lw=0.5)
        ax8.set_yticks([-1, 0, 1])
        ax8.set_xlabel('Site', color='#8888cc', fontsize=7)

        # ── Panel 9: Quantum 3-Body ────────────────────
        ax9 = fig.add_subplot(gs[2, 2])
        ax_style(ax9, 'Quantum 3-Body (Entangled Gravity)')
        if d['q3_t'] is not None and d['q3_e'] is not None:
            cols = ['#ff8844', '#44ff88', '#8844ff']
            labels = ['⟨sz₁⟩', '⟨sz₂⟩', '⟨sz₃⟩']
            for k, (col, lab) in enumerate(zip(cols, labels)):
                ax9.plot(d['q3_t'], d['q3_e'][k], color=col, lw=1.2, label=lab)
            ax9.legend(fontsize=7, facecolor='#0d0d1a', edgecolor='#2a2a4a',
                       labelcolor='#ccccee')
            ax9.set_xlabel('t', color='#8888cc', fontsize=7)
        else:
            ax9.text(0.3, 0.5, 'QuTiP not installed', transform=ax9.transAxes,
                     color='#6666aa')
            ax9.axis('off')

        out = 'math_machine_v2_translation.png'
        plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
        print(f"Saved: {out}")
        return fig


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 777
    machine = MathMachine(input_num=n)
    machine.visualize_translation()
    plt.show()
