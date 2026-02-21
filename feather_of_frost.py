import math

def is_prime(n):
    """Return True if n is prime (simple check for small n)."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n))+1):
        if n % i == 0:
            return False
    return True

def halve_and_filter(signal):
    """
    Applies subtraction-as-halving to signal,
    returns crystallized prime-aligned outputs.
    """
    # Convert signal to integers if needed
    nodes = [abs(int(x)) for x in signal]

    crystallized = []
    for n in nodes:
        halved = n // 2  # Subtraction / halving operator
        if halved > 0 and is_prime(halved):
            crystallized.append(halved)
    return crystallized

# Example usage:
if __name__ == "__main__":
    input_signal = [11, 20, 7, 14, 5]  # arbitrary “node states”
    crystal = halve_and_filter(input_signal)
    print("Crystallized feather:", crystal)
