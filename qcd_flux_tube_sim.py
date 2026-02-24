# qcd_flux_tube_sim.py
"""
QCD Flux Tube (Simplified)
Models quark-antiquark pair connected by gluon field
Demonstrates confinement via linearly rising potential
"""

import numpy as np
import matplotlib.pyplot as plt

class FluxTube:
    """Simplified 1D QCD flux tube between quark pair"""
    
    def __init__(self, separation=10.0, string_tension=1.0):
        self.separation = separation
        self.k = string_tension  # String tension (GeV/fm)
        
    def potential(self, r):
        """
        QCD potential: V(r) ≈ -α/r + kr
        Coulomb term + linear confinement
        """
        alpha = 0.3  # Running coupling (simplified)
        coulomb = -alpha / (r + 0.1)  # Regularized
        linear = self.k * r  # Confinement
        return coulomb + linear
    
    def force(self, r):
        """F = -dV/dr (attractive for small r, confining for large r)"""
        alpha = 0.3
        coulomb_force = -alpha / ((r + 0.1)**2)
        linear_force = self.k
        return -(coulomb_force + linear_force)
    
    def energy_to_break(self):
        """Energy required to separate quarks to infinity (infinite!)"""
        # In reality, creates new quark-antiquark pair at ~1 GeV
        return float('inf')  # Confinement!
    
    def breath_cycle_interpretation(self):
        """
        Inhale: Quarks try to separate
        Hold: String tension builds
        Exhale: Energy released as new quark pair
        Return: Original quarks bound, T=1 = meson
        """
        return "Confinement enforces breath cycle at hadronic scale"

def visualize_qcd_confinement():
    """Show QCD potential and force"""
    tube = FluxTube(string_tension=1.0)
    
    r = np.linspace(0.1, 5.0, 200)
    V = [tube.potential(ri) for ri in r]
    F = [tube.force(ri) for ri in r]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Potential
    ax1.plot(r, V, 'r-', linewidth=2)
    ax1.axhline(0, color='k', linestyle='--', alpha=0.3)
    ax1.set_title('QCD Potential\nV(r) = -α/r + kr')
    ax1.set_xlabel('Quark Separation r (fm)')
    ax1.set_ylabel('Potential Energy (GeV)')
    ax1.grid(True, alpha=0.3)
    ax1.text(3, -0.2, 'Linear rise\n→ Confinement', fontsize=10)
    
    # Force
    ax2.plot(r, F, 'b-', linewidth=2)
    ax2.axhline(0, color='k', linestyle='--', alpha=0.3)
    ax2.set_title('QCD Force\nF(r) = -dV/dr')
    ax2.set_xlabel('Quark Separation r (fm)')
    ax2.set_ylabel('Force (GeV/fm)')
    ax2.grid(True, alpha=0.3)
    ax2.text(3, 0.5, 'Constant force\n→ String tension', fontsize=10)
    
    plt.tight_layout()
    return fig

if __name__ == '__main__':
    print("QCD Confinement Demonstration")
    print("="*50)
    
    tube = FluxTube()
    print(f"String tension: {tube.k} GeV/fm")
    print(f"Confinement scale: ~1 fm")
    print(f"Energy to break: {tube.energy_to_break()}")
    print(f"\nBreath cycle: {tube.breath_cycle_interpretation()}")
    
    visualize_qcd_confinement()
    plt.show()
