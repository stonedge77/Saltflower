import numpy as np

def generate_nand_fractal(size=512, max_depth=3):  # ZCR limit as depth
    img = np.zeros((size, size), dtype=int)
    mask = (1 << max_depth) - 1  # Bit mask for bounded recursion
    for x in range(size):
        for y in range(size):
            # NAND check: include if no bit overlap (subtractive exclusion)
            if not ((x & mask) & (y & mask)):
                img[y, x] = 1  # Flip y,x for standard orientation
    return img

# Example: Simulate and print small ASCII version (for text output)
small_size = 32
small_img = generate_nand_fractal(small_size)
print("Small NAND Fractal Simulation (ASCII: # = included point):")
for row in small_img:
    print(''.join(['#' if cell else ' ' for cell in row]))

# For full viz (uncomment to plot/save):
# import matplotlib.pyplot as plt
# plt.imshow(generate_nand_fractal(512), cmap='binary', origin='lower')
# plt.axis('off')
# plt.savefig('nand_fractal.png')  # Or plt.show()
