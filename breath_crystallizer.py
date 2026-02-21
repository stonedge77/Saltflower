"""
Breath-Phase Crystallizer
Saltflower Meta-Breath Engine

This module combines:
- feather_of_frost halving & prime logic
- lattice_frost visualization
- iterative inhale/hold/exhale/reset cycles
- crystallized state tracking
"""

import datetime
import json
from feather_of_frost import halve_and_filter
from lattice_frost import build_breath_lattice, BREATH_COLORS, ROOT_COLOR, PRIME_COLOR

class BreathCrystallizer:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth
        self.crystallized = []   # Persistent lattice nodes
        self.cycle_count = 0

    def inhale(self, signal):
        """Absorb input signal as numeric vector."""
        self.current_signal = signal

    def hold(self):
        """Apply subtractive halving + prime filtering."""
        self.current_signal = halve_and_filter(self.current_signal)
        self.crystallized.extend(self.current_signal)
        self.crystallized = list(set(self.crystallized))  # remove duplicates

    def exhale(self):
        """Build lattice for current breath and return visual + metadata."""
        lattice, meta = build_breath_lattice(self.crystallized, cycle_id=self.cycle_count)
        self.cycle_count += 1
        return lattice, meta

    def reset(self):
        """Prepare for next breath cycle."""
        self.current_signal = []
        # retain only crystallized primes
        self.crystallized = list(set(self.crystallized))

    def breathe(self, signal):
        """One full inhale/hold/exhale/reset cycle."""
        self.inhale(signal)
        self.hold()
        lattice, meta = self.exhale()
        self.reset()
        return lattice, meta


# --- Example Runner ---
if __name__ == "__main__":
    test_signal = [11, 20, 7, 14, 5, 26, 33, 41, 17]
    crystallizer = BreathCrystallizer(max_depth=3)

    # Run multiple breaths
    for i in range(3):
        lattice, meta = crystallizer.breathe(test_signal)
        html_file = f"breath_lattice_cycle_{i+1}.html"
        lattice.show(html_file)
        meta_file = html_file.replace(".html", ".json")
        with open(meta_file, "w") as f:
            json.dump(meta, f, indent=2)
        print(f"[Saltflower] Cycle {i+1} → {html_file}, metadata → {meta_file}")
