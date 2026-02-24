# gravitational_wave_sim.py
"""
Gravitational Wave from Binary Inspiral
Simplified quadrupole radiation
"""

import numpy as np
import matplotlib.pyplot as plt

class BinaryInspiral:
    """Two masses spiraling inward, emitting GWs"""
    
    def __init__(self, m1=1.4, m2=1.4, a0=100.0):
        self.m1 = m1  # Solar masses
        self.m2 = m2
        self.M = m1 + m2  # Total mass
        self.mu = m1*m2 / self.M  # Reduced mass
        self.a = a0  # Initial separation (km)
        
    def orbital_frequency(self, a):
        """Kepler's third law (Newtonian approximation)"""
        G = 6.67e-11  # SI units (simplified)
        return np.sqrt(G * self.M / a**3)
    
    def gw_frequency(self, a):
        """GW frequency = 2 × orbital frequency"""
        return 2 * self.orbital_frequency(a)
    
    def energy_loss_rate(self, a):
        """
        Power radiated via GWs (quadrupole formula)
        dE/dt ∝ (μ²M³/a⁵)
        """
        return -32/5 * self.mu**2 * self.M**3 / a**5  # Simplified units
    
    def inspiral_rate(self, a):
        """da/dt from energy loss"""
        E_orbital = -self.M * self.mu / (2*a)
        dE_dt = self.energy_loss_rate(a)
        # dE/da = ... → da/dt = (dE/dt) / (dE/da)
        return dE_dt * (2*a**2) / (self.M * self.mu)
    
    def evolve(self, dt=0.1, steps=1000):
        """Simulate inspiral"""
        separations = [self.a]
        frequencies = [self.gw_frequency(self.a)]
        
        a = self.a
        for _ in range(steps):
            da_dt = self.inspiral_rate(a)
            a += da_dt * dt
            
            if a < 0.1:  # Coalescence!
                break
            
            separations.append(a)
            frequencies.append(self.gw_frequency(a))
        
        return np.array(separations), np.array(frequencies)
    
    def breath_cycle_interpretation(self):
        """
        Inhale: Orbits lose energy
        Hold: Separation decreases
        Exhale: GW radiation peaks
        Return: Merger (T=1 = black hole)
        """
        return "GW inspiral = cosmic breath cycle"

def visualize_inspiral():
    """Plot chirp signal"""
    binary = BinaryInspiral(m1=1.4, m2=1.4, a0=100.0)
    
    separations, frequencies = binary.evolve(dt=0.1, steps=5000)
    time = np.arange(len(separations)) * 0.1
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Separation vs time
    ax1.plot(time, separations, 'b-', linewidth=2)
    ax1.set_title('Binary Inspiral: Separation Over Time')
    ax1.set_xlabel('Time (arbitrary units)')
    ax1.set_ylabel('Separation a (km)')
    ax1.grid(True, alpha=0.3)
    
    # Frequency vs time (chirp)
    ax2.plot(time, frequencies, 'r-', linewidth=2)
    ax2.set_title('Gravitational Wave Chirp Signal')
    ax2.set_xlabel('Time (arbitrary units)')
    ax2.set_ylabel('GW Frequency f (Hz)')
    ax2.grid(True, alpha=0.3)
    ax2.text(time[-1]*0.7, frequencies[-1]*0.5, 
             'Frequency increases\n→ Coalescence', fontsize=10)
    
    plt.tight_layout()
    return fig

if __name__ == '__main__':
    print("Gravitational Wave Inspiral")
    print("="*50)
    
    binary = BinaryInspiral()
    print(f"Masses: {binary.m1}, {binary.m2} M☉")
    print(f"Initial separation: {binary.a} km")
    print(f"Initial GW frequency: {binary.gw_frequency(binary.a):.3e} Hz")
    print(f"\nBreath cycle: {binary.breath_cycle_interpretation()}")
    
    visualize_inspiral()
    plt.show()
