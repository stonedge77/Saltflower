import numpy as np
import math

def is_prime(n):
    """Simple prime check for small n."""
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

def generate_nand_prime_fractal(size=512, max_depth=3):
    """Generate NAND fractal with prime overlay."""
    img = np.zeros((size, size), dtype=int)
    mask = (1 << max_depth) - 1  # ZCR-bounded bit mask
    for x in range(size):
        for y in range(size):
            # NAND inclusion: no bit overlap
            if not ((x & mask) & (y & mask)):
                value = x + y  # Derive value for prime check (subtractive tie-in)
                if is_prime(value):
                    img[y, x] = 2  # Prime point
                else:
                    img[y, x] = 1  # Non-prime point
    return img

# For visualization (uncomment for full plot):
# import matplotlib.pyplot as plt
# plt.imshow(generate_nand_prime_fractal(512), cmap='hot', origin='lower')  # 'hot' colors primes distinctly
# plt.axis('off')
# plt.show()  # Or savefig('nand_prime_fractal.png')
