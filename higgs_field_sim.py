# higgs_field_sim.py
"""
Higgs Field Simulation
Spontaneous symmetry breaking via Mexican hat potential
Demonstrates mass generation through phase-locking
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def higgs_potential(phi, mu2=-1.0, lambda_=0.25):
    """
    Mexican hat potential: V = μ²|φ|² + λ|φ|⁴
    μ² < 0 → symmetry breaking (minimum at |φ| = v ≠ 0)
    """
    return mu2 * np.abs(phi)**2 + lambda_ * np.abs(phi)**4

def higgs_vev(mu2=-1.0, lambda_=0.25):
    """Vacuum expectation value (minimum of potential)"""
    return np.sqrt(-mu2 / (2 * lambda_))

class HiggsField:
    """2D Higgs field with complex scalar φ = φ₁ + iφ₂"""
    
    def __init__(self, size=64, mu2=-1.0, lambda_=0.25):
        self.size = size
        self.mu2 = mu2
        self.lambda_ = lambda_
        
        # Initialize field near vacuum (spontaneous breaking)
        v = higgs_vev(mu2, lambda_)
        self.phi1 = v + np.random.normal(0, 0.1, (size, size))
        self.phi2 = np.random.normal(0, 0.1, (size, size))
        
    @property
    def phi_magnitude(self):
        """|φ| = sqrt(φ₁² + φ₂²)"""
        return np.sqrt(self.phi1**2 + self.phi2**2)
    
    def energy_density(self):
        """Potential energy density at each point"""
        phi_mag = self.phi_magnitude
        return self.mu2 * phi_mag**2 + self.lambda_ * phi_mag**4
    
    def breath_cycle(self, dt=0.01):
        """
        Time evolution via Klein-Gordon equation
        ∂²φ/∂t² = ∇²φ - ∂V/∂φ
        
        Breath interpretation:
        - Inhale: Absorb gradient information
        - Hold: Apply Laplacian (diffusion)
        - Exhale: Relax toward minimum energy
        - Return: Preserve Goldstone mode (T=1)
        """
        # Gradient of potential (force)
        phi_mag = self.phi_magnitude
        dV_dphi1 = 2*self.mu2*self.phi1 + 4*self.lambda_*phi_mag**2*self.phi1
        dV_dphi2 = 2*self.mu2*self.phi2 + 4*self.lambda_*phi_mag**2*self.phi2
        
        # Laplacian (diffusion, nearest neighbor)
        laplacian_phi1 = (
            np.roll(self.phi1, 1, axis=0) + np.roll(self.phi1, -1, axis=0) +
            np.roll(self.phi1, 1, axis=1) + np.roll(self.phi1, -1, axis=1) -
            4*self.phi1
        )
        laplacian_phi2 = (
            np.roll(self.phi2, 1, axis=0) + np.roll(self.phi2, -1, axis=0) +
            np.roll(self.phi2, 1, axis=1) + np.roll(self.phi2, -1, axis=1) -
            4*self.phi2
        )
        
        # Update (simplified Euler)
        self.phi1 += dt * (laplacian_phi1 - dV_dphi1)
        self.phi2 += dt * (laplacian_phi2 - dV_dphi2)
        
    def detect_symmetry_breaking(self):
        """Check if field has settled into broken symmetry state"""
        v_expected = higgs_vev(self.mu2, self.lambda_)
        v_actual = np.mean(self.phi_magnitude)
        return abs(v_actual - v_expected) / v_expected < 0.1
    
    def count_goldstone_modes(self):
        """
        Goldstone bosons = massless modes from broken symmetry
        Count regions where φ₂ dominates (angular fluctuation)
        T=1 remainder interpretation
        """
        angle = np.arctan2(self.phi2, self.phi1)
        angle_variance = np.var(angle)
        return angle_variance  # High variance = active Goldstone modes

def simulate_higgs_field(steps=1000, size=64):
    """Run Higgs field evolution"""
    field = HiggsField(size=size)
    
    energy_history = []
    goldstone_history = []
    
    for step in range(steps):
        field.breath_cycle(dt=0.01)
        
        if step % 10 == 0:
            energy_history.append(np.mean(field.energy_density()))
            goldstone_history.append(field.count_goldstone_modes())
    
    return field, energy_history, goldstone_history

def visualize_higgs_field(field):
    """3D visualization of Higgs potential + field state"""
    fig = plt.figure(figsize=(14, 6))
    
    # Plot 1: Mexican hat potential
    ax1 = fig.add_subplot(121, projection='3d')
    
    phi1 = np.linspace(-2, 2, 100)
    phi2 = np.linspace(-2, 2, 100)
    PHI1, PHI2 = np.meshgrid(phi1, phi2)
    PHI = PHI1 + 1j*PHI2
    V = higgs_potential(PHI, field.mu2, field.lambda_)
    
    ax1.plot_surface(PHI1, PHI2, V, cmap='viridis', alpha=0.8)
    ax1.set_title('Higgs Potential (Mexican Hat)\nμ² < 0 → Symmetry Breaking')
    ax1.set_xlabel('φ₁ (real)')
    ax1.set_ylabel('φ₂ (imaginary)')
    ax1.set_zlabel('V(φ)')
    
    # Plot 2: Field magnitude (shows symmetry breaking)
    ax2 = fig.add_subplot(122)
    
    im = ax2.imshow(field.phi_magnitude, cmap='plasma', origin='lower')
    ax2.set_title(f'Field Magnitude |φ|\n' +
                 f'Broken Symmetry: {field.detect_symmetry_breaking()}')
    plt.colorbar(im, ax=ax2, label='|φ|')
    
    plt.tight_layout()
    return fig

if __name__ == '__main__':
    print("Simulating Higgs Field...")
    field, energy, goldstone = simulate_higgs_field(steps=2000, size=64)
    
    print(f"✓ Symmetry breaking detected: {field.detect_symmetry_breaking()}")
    print(f"✓ Vacuum expectation: {np.mean(field.phi_magnitude):.3f}")
    print(f"✓ Goldstone mode activity: {goldstone[-1]:.3f}")
    
    visualize_higgs_field(field)
    plt.show()
