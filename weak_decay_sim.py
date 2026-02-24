# weak_decay_sim.py
"""
Weak Interaction: Beta Decay
n → p + e⁻ + ν̄ₑ
Demonstrates T=1 remainder (neutrino escapes)
"""

import numpy as np
import matplotlib.pyplot as plt

class BetaDecay:
    """Neutron beta decay simulation"""
    
    def __init__(self, N0=1000, tau=880):  # tau in seconds
        self.N0 = N0  # Initial neutrons
        self.tau = tau  # Mean lifetime
        
    def decay_probability(self, t):
        """P(decay) = 1 - exp(-t/τ)"""
        return 1 - np.exp(-t / self.tau)
    
    def remaining_neutrons(self, t):
        """N(t) = N₀ exp(-t/τ)"""
        return self.N0 * np.exp(-t / self.tau)
    
    def breath_cycle_interpretation(self):
        """
        Inhale: Neutron absorbs virtual W⁻ boson
        Hold: Quark flavor changes (d → u)
        Exhale: Emit electron + antineutrino
        Return: Proton remains (T=1 = neutrino escapes)
        """
        return "Weak decay = forced breath (irreversible)"
    
    def t1_remainder(self):
        """Neutrino carries away unpaired lepton number"""
        return "Neutrino (massless, escapes, T=1)"

def visualize_beta_decay():
    """Plot decay curve"""
    decay = BetaDecay(N0=1000, tau=880)
    
    t = np.linspace(0, 3000, 500)
    N = decay.remaining_neutrons(t)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(t, N, 'b-', linewidth=2, label='Neutrons')
    ax.plot(t, decay.N0 - N, 'r-', linewidth=2, label='Protons (+ e⁻ + ν̄)')
    ax.axvline(decay.tau, color='k', linestyle='--', 
               label=f'Mean lifetime τ = {decay.tau}s')
    
    ax.set_title('Beta Decay: n → p + e⁻ + ν̄ₑ\n(Weak Force, T=1 Neutrino)')
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Number of Particles')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

if __name__ == '__main__':
    decay = BetaDecay()
    print("Beta Decay Simulation")
    print("="*50)
    print(f"Initial neutrons: {decay.N0}")
    print(f"Mean lifetime: {decay.tau}s")
    print(f"T=1 remainder: {decay.t1_remainder()}")
    print(f"Breath cycle: {decay.breath_cycle_interpretation()}")
    
    visualize_beta_decay()
    plt.show()
