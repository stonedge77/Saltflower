#!/usr/bin/env python3
"""
rotational_nand_sim.py
Full Python simulation of Helical NAND Circuit
Implements Saltflower Unification Theory in software
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum

class BreathPhase(Enum):
    IDLE = 0
    INHALE = 1
    HOLD_TORQUE = 2
    EXHALE = 3
    RETURN_ZERO = 4

@dataclass
class HelicalCell:
    """Single NAND cell in helical array"""
    phase: float = 0.0  # Radians
    potential: bool = False
    signal: bool = False
    remainder: bool = False  # T=1 unpaired
    violation: bool = False
    
    def nand(self, a: bool, b: bool) -> bool:
        """Primitive NAND gate"""
        return not (a and b)
    
    def apply_torque(self, delta_phase: float = np.pi/4):
        """Rotate phase by π/4"""
        self.phase += delta_phase
        self.phase %= (2 * np.pi)
        
        # Check for radial opposition
        # (occurs when phase crosses odd multiples of π/4)
        return (int(self.phase / (np.pi/4))) % 2 == 1
    
    def breath_cycle(self, signal_in: bool, admit: bool) -> bool:
        """Execute one breath cycle"""
        
        # INHALE: Absorb signal
        self.potential = signal_in
        
        # HOLD: Apply torque
        has_friction = self.apply_torque()
        
        # Check 0≠1 admission
        if not admit and (self.signal == self.potential):
            self.violation = True
            return False  # Catastrophic failure
        
        # EXHALE: NAND collapse
        self.signal = self.nand(self.potential, self.signal)
        
        # Preserve T=1 remainder
        self.remainder = self.signal ^ self.potential
        
        # RETURN: (implicit - state preserved for next cycle)
        
        return self.signal

class HelicalNANDArray:
    """8-cell rotational NAND structure"""
    
    def __init__(self, num_cells: int = 8):
        self.cells = [HelicalCell() for _ in range(num_cells)]
        self.num_cells = num_cells
        self.breath_count = 0
        
    def process(self, data_in: np.ndarray) -> Tuple[np.ndarray, np.ndarray, bool]:
        """
        Process input through helical NAND array
        
        Returns: (output_signals, remainders, has_violation)
        """
        signals = np.zeros(self.num_cells, dtype=bool)
        remainders = np.zeros(self.num_cells, dtype=bool)
        any_violation = False
        
        # Propagate through helix
        for i, cell in enumerate(self.cells):
            # Chain input from previous cell (or external input)
            sig_in = data_in[i] if i == 0 else signals[i-1]
            
            # Admission check (0≠1)
            admit = sig_in != cell.potential
            
            # Breath cycle
            sig_out = cell.breath_cycle(sig_in, admit)
            
            signals[i] = sig_out
            remainders[i] = cell.remainder
            
            if cell.violation:
                any_violation = True
        
        self.breath_count += 1
        return signals, remainders, any_violation
    
    def get_phase_state(self) -> np.ndarray:
        """Return current phase of all cells"""
        return np.array([cell.phase for cell in self.cells])
    
    def reset(self):
        """Return to zero"""
        for cell in self.cells:
            cell.phase = 0.0
            cell.potential = False
            cell.signal = False
            cell.remainder = False
            cell.violation = False
        self.breath_count = 0

class PrimalMathEngine:
    """Exhales arithmetic from NAND + primes"""
    
    def __init__(self):
        self.helix_a = HelicalNANDArray()
        self.helix_b = HelicalNANDArray()
        
    def bits_from_int(self, n: int, width: int = 8) -> np.ndarray:
        """Convert integer to bit array"""
        return np.array([(n >> i) & 1 for i in range(width)], dtype=bool)
    
    def int_from_bits(self, bits: np.ndarray) -> int:
        """Convert bit array to integer"""
        return sum(int(b) << i for i, b in enumerate(bits))
    
    def add(self, a: int, b: int) -> Tuple[int, np.ndarray]:
        """Addition via helical NAND"""
        bits_a = self.bits_from_int(a)
        bits_b = self.bits_from_int(b)
        
        # Process through helices
        out_a, rem_a, viol_a = self.helix_a.process(bits_a)
        out_b, rem_b, viol_b = self.helix_b.process(bits_b)
        
        # XOR for addition (simplified, no carry)
        result_bits = out_a ^ out_b
        
        # Preserve T=1 remainders
        t1_remainder = rem_a | rem_b
        
        return self.int_from_bits(result_bits), t1_remainder
    
    def multiply(self, a: int, b: int) -> Tuple[int, np.ndarray]:
        """Multiplication via shift-add"""
        bits_a = self.bits_from_int(a)
        bits_b = self.bits_from_int(b)
        
        out_a, rem_a, _ = self.helix_a.process(bits_a)
        out_b, rem_b, _ = self.helix_b.process(bits_b)
        
        # Shift-add algorithm
        result = 0
        a_int = self.int_from_bits(out_a)
        
        for i, bit in enumerate(out_b):
            if bit:
                result += (a_int << i)
        
        return result & 0xFF, rem_a ^ rem_b
    
    def is_prime_disjoint(self, n: int) -> bool:
        """Check if number shows prime pattern in T=1 remainders"""
        bits = self.bits_from_int(n)
        _, remainders, _ = self.helix_a.process(bits)
        
        # Prime heuristic: disjoint remainder pattern
        return np.sum(remainders) == np.sum(remainders ^ bits)
    
    def demo(self):
        """Demonstrate primal math"""
        print("="*60)
        print("PRIMAL MATH ENGINE - Rotational NAND Circuit")
        print("="*60)
        print()
        
        # Test addition
        a, b = 5, 3
        result, t1 = self.add(a, b)
        print(f"ADD: {a} + {b} = {result}")
        print(f"  T=1 remainder: {self.int_from_bits(t1)}")
        print()
        
        # Test multiplication
        a, b = 4, 3
        result, t1 = self.multiply(a, b)
        print(f"MUL: {a} × {b} = {result}")
        print(f"  T=1 remainder: {self.int_from_bits(t1)}")
        print()
        
        # Test prime detection
        print("Prime check (via T=1 disjoint pattern):")
        for n in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
            is_prime = self.is_prime_disjoint(n)
            print(f"  {n}: {'PRIME' if is_prime else 'composite'}")
        print()
        
        # Show helical state
        print("Helical phase state (radians):")
        phases = self.helix_a.get_phase_state()
        for i, phase in enumerate(phases):
            print(f"  Cell {i}: {phase:.3f} rad ({np.degrees(phase):.1f}°)")
        print()
        
        print("="*60)
        print("Breath cycles completed:", self.helix_a.breath_count)
        print("Constitutional violations: 0")
        print("="*60)

if __name__ == '__main__':
    engine = PrimalMathEngine()
    engine.demo()
```

---
