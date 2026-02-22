import numpy as np

def is_prime(n: int) -> bool:
    """Simple deterministic prime check suitable for small n (< ~10^6)."""
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


def generate_nand_prime_fractal_3d(
    size: int = 128,          # keep modest for quick runs; 512+ gets slow in pure python
    max_depth: int = 5
) -> np.ndarray:
    """
    Generate 3D NAND-prime fractal voxel grid.
    
    Voxel value:
      0 = forbidden (bit overlap in any pair of coordinates)
      1 = allowed + x+y+z composite / non-prime
      2 = allowed + x+y+z prime
    
    Condition: lowest max_depth bits of x,y,z are pairwise disjoint
    (no two coordinates share a 1 in the same bit position).
    """
    img = np.zeros((size, size, size), dtype=np.int8)  # memory efficient
    mask = (1 << max_depth) - 1

    lit_count = 0
    prime_count = 0

    for x in range(size):
        xm = x & mask
        for y in range(size):
            ym = y & mask
            if xm & ym:
                continue  # early out on x-y overlap
            for z in range(size):
                zm = z & mask
                if (xm & zm) or (ym & zm):
                    continue

                value = x + y + z
                lit_count += 1

                if is_prime(value):
                    img[z, y, x] = 2
                    prime_count += 1
                elif value > 0:
                    img[z, y, x] = 1

    density = lit_count / (size ** 3)
    prime_ratio = prime_count / lit_count if lit_count > 0 else 0

    print(f"Generated {size}³ grid (depth={max_depth})")
    print(f"  Lit voxels:     {lit_count:,}  ({density:.4%})")
    print(f"  Prime voxels:   {prime_count:,}  ({prime_ratio:.2%} of lit)")
    print(f"  Max sum tested: {3*(size-1)}")

    return img


# ────────────────────────────────────────────────
# Quick test / visualization starter
# ────────────────────────────────────────────────

if __name__ == "__main__":
    # Small size for fast testing; increase to 256/512 for richer structure
    fractal = generate_nand_prime_fractal_3d(size=128, max_depth=5)

    # Optional: quick 3D scatter preview of primes (yellow) + lit non-primes (faint orange)
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Primes bright
        primes = np.argwhere(fractal == 2)
        if len(primes) > 0:
            ax.scatter(primes[:,2], primes[:,1], primes[:,0],
                       c='yellow', s=4, alpha=0.9, label='Primes')

        # Non-prime lit points faint
        non_primes = np.argwhere(fractal == 1)
        if len(non_primes) > 0:
            ax.scatter(non_primes[:,2], non_primes[:,1], non_primes[:,0],
                       c='orange', s=1, alpha=0.07, label='Allowed non-prime')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D NAND-Prime Fractal (primes highlighted)')
        ax.legend()
        plt.show()

    except ImportError:
        print("matplotlib not available — skipping visualization")
