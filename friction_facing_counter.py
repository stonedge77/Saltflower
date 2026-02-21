# friction_facing_counter.py — count facing contradictions per rotation step
import numpy as np

def count_facing_contradictions(matrix):
    """Count positions where neighboring bits face each other in opposition"""
    rows, cols = matrix.shape
    count = 0
    # horizontal facing
    count += np.sum(matrix[:, :-1] != matrix[:, 1:])
    # vertical facing
    count += np.sum(matrix[:-1, :] != matrix[1:, :])
    return count

N = 16
state = np.random.randint(0, 2, (N, N))

total_friction = 0
for turn in range(360 // 45):  # π/4 steps = 8 turns for full cycle
    # "rotate" matrix (simple shift as proxy)
    state = np.roll(state, shift=1, axis=0)
    state = np.roll(state, shift=1, axis=1)
    
    friction = count_facing_contradictions(state)
    total_friction += friction
    print(f"Turn {turn+1:2d}/8  facing contradictions: {friction:3d}  cumulative: {total_friction:4d}")

print(f"Total friction over full rotation: {total_friction}")
