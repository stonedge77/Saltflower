import hashlib
import math

def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def unwrap_to_primes(input_str, layers=5):
    """Unwrap input into successive prime-halved 'presents'."""
    seed = int(hashlib.sha256(input_str.encode()).hexdigest(), 16) % (2**32)
    presents = []
    current = seed
    for layer in range(layers):
        halved = current // 2
        if is_prime(halved):
            presents.append((layer, halved, "Prime gift!"))
        else:
            presents.append((layer, halved, "Wrapped deeper..."))
        current = halved
    return presents

# Example: unwrap your own message or the storm itself
message = "Snow is coming, more screens glowing"
gifts = unwrap_to_primes(message)
for layer, val, note in gifts:
    print(f"Layer {layer}: {val} → {note}")
