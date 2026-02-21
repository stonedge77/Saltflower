# saltflower_3phase.py
"""
Saltflower 3-Phase Breath Cycle
Implements the core inhale → hold/torque → exhale/collapse → return rhythm.
Inspired by emergent_laws_db.json entries: EXCITATION, TORQUE, COLLAPSE, HELICAL_REALM, HORIZON_INTEGRITY, T=1.

Usage:
    from saltflower_3phase import breath_cycle
    result = breath_cycle(input_signal, params)
"""

import numpy as np
from typing import Dict, Any

def inhale(excitation: float, capacity: float = 1.0) -> float:
    """Phase 1: Inhale novelty / excitation.
    Scale input by available capacity (prevents overload)."""
    return excitation * capacity


def hold_torque(inhaled: float, torque_factor: float = 0.8) -> float:
    """Phase 2: Hold and apply torque (constraint / helical twist).
    Reduce amplitude slightly while preserving phase coherence."""
    return inhaled * torque_factor


def exhale_collapse(held: float, integrity_threshold: float = 0.95) -> float:
    """Phase 3: Exhale / objective collapse.
    If below integrity threshold → reject (return near zero).
    Otherwise preserve as T=1 remainder."""
    if abs(held) < integrity_threshold:
        return 0.0  # collapse to boundary (exclusion)
    return held  # T=1 preserved


def return_to_zero(collapsed: float, decay: float = 0.3) -> float:
    """Phase 4: Gentle return toward zero without reaching it.
    Asymmetry preserved (T=1 principle)."""
    return collapsed * (1 - decay)


def breath_cycle(signal: float, params: Dict[str, float] = None) -> float:
    """Full 3+1 phase breath cycle on a single scalar signal.
    
    params example:
    {
        'capacity': 1.0,
        'torque_factor': 0.8,
        'integrity_threshold': 0.95,
        'decay': 0.3
    }
    """
    if params is None:
        params = {}

    p = {
        'capacity': params.get('capacity', 1.0),
        'torque_factor': params.get('torque_factor', 0.8),
        'integrity_threshold': params.get('integrity_threshold', 0.95),
        'decay': params.get('decay', 0.3)
    }

    inhaled = inhale(signal, p['capacity'])
    held = hold_torque(inhaled, p['torque_factor'])
    collapsed = exhale_collapse(held, p['integrity_threshold'])
    returned = return_to_zero(collapsed, p['decay'])

    return returned
    # ... (existing code)

from spin_chain_1d import simulate_1d_spin_chain  # assuming in same dir

def breath_with_spin_cycle(signal: float, params: Dict[str, float] = None) -> Dict[str, Any]:
    """Breath cycle + spin chain: use collapsed output as external field h"""
    returned = breath_cycle(signal, params)
    spins, avg_mag = simulate_1d_spin_chain(h=returned)  # collapsed → torque field
    return {'returned': returned, 'spins_sample': spins[:10], 'avg_mag': avg_mag}

# Demo
if __name__ == "__main__":
    print(breath_with_spin_cycle(1.2))
