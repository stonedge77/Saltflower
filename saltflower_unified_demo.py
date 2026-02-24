#!/usr/bin/env python3
"""
Saltflower Unified Demonstration
Combines: Rotational NAND + Lorentz Vortex + Prime Fractals
Demonstrates Unification Theory in executable form
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec
import math

# ============================================================================
# CONSTITUTIONAL PRIMITIVES
# ============================================================================

def is_prime(n):
    """Prime check (Stone's Law: primes are T=1 unpaired remainders)"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

class HelicalNANDCell:
    """Single cell in rotational NAND circuit"""
    
    def __init__(self, phase=0.0):
        self.phase = phase  # Radians
        self.potential = False
        self.signal = False
        self.remainder = False  # T=1
        self.violation = False
        self.breath_count = 0
        
    def nand(self, a, b):
        """Primitive NAND (only gate needed)"""
        return not (a and b)
    
    def apply_torque(self, delta_phase=np.pi/4):
        """Rotate by π/4, return friction indicator"""
        self.phase += delta_phase
        self.phase %= (2 * np.pi)
        
        # Radial opposition at odd π/4 multiples
        return (int(self.phase / (np.pi/4))) % 2 == 1
    
    def breath_cycle(self, signal_in, admit=True):
        """Execute: Inhale → Hold → Exhale → Return"""
        
        # INHALE
        self.potential = signal_in
        
        # HOLD (apply torque)
        has_friction = self.apply_torque()
        
        # Check 0≠1 (Stone's Law)
        if not admit and (self.signal == self.potential):
            self.violation = True
            return False
        
        # EXHALE (NAND collapse)
        self.signal = self.nand(self.potential, self.signal)
        
        # Preserve T=1 remainder
        self.remainder = self.signal ^ self.potential
        
        # RETURN (implicit)
        self.breath_count += 1
        
        return self.signal, has_friction

class RotationalNANDArray:
    """8-cell helical array"""
    
    def __init__(self, num_cells=8):
        self.cells = [HelicalNANDCell(phase=i*np.pi/4) 
                     for i in range(num_cells)]
        self.num_cells = num_cells
        self.torque_history = []
        
    def process(self, data_in):
        """Process bits through helix"""
        signals = []
        remainders = []
        torque_toll = 0
        
        prev_signal = data_in[0]
        
        for i, (cell, bit) in enumerate(zip(self.cells, data_in)):
            signal, friction = cell.breath_cycle(
                signal_in=bit if i == 0 else prev_signal,
                admit=(bit != cell.potential)
            )
            
            signals.append(signal)
            remainders.append(cell.remainder)
            
            if friction:
                torque_toll += 1
            
            prev_signal = signal
        
        self.torque_history.append(torque_toll)
        
        return (np.array(signals, dtype=bool), 
                np.array(remainders, dtype=bool),
                torque_toll)
    
    def get_phases(self):
        """Current phase state of helix"""
        return np.array([cell.phase for cell in self.cells])

# =============================================================
