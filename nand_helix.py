# nand_helix.py — weird 1D NAND feedback with helical offset
import numpy as np

def nand(a, b): return not (a and b)

def step(state, delay=1):
    n = len(state)
    new = np.zeros(n, dtype=bool)
    for i in range(n):
        # "helical" — look back delay steps (wrap around)
        a = state[i]
        b = state[(i - delay) % n]
        new[i] = nand(a, b)
    return new

state = np.random.choice([True, False], 80)
for t in range(300):
    state = step(state, delay=3)  # change delay = twist rate
    if t % 50 == 0:
        print(f"t={t:3d}  mag={np.mean(state):.3f}  pattern={''.join('█' if x else ' ' for x in state)}")
