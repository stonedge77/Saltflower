import math
from feather_of_frost import halve_and_filter

# Visualization dependency
try:
    from pyvis.network import Network
except ImportError:
    raise ImportError("Install pyvis (pip install pyvis) to enable lattice visualization")

def build_lattice(signal):
    """
    Build nodes and connections between halved & crystallized primes.
    """
    primes = halve_and_filter(signal)
    net = Network(height="500px", width="800px")
    net.barnes_hut()

    # Add root nodes
    for idx, val in enumerate(signal):
        net.add_node(val, label=str(val), color="#74b9ff")

    # Connect to halved primes
    for orig in signal:
        halved = orig // 2
        if halved in primes:
            net.add_node(halved, label=f"P{halved}", color="#a29bfe")
            net.add_edge(orig, halved)

    return net

if __name__ == "__main__":
    # Example signal
    signal = [11, 20, 7, 14, 5, 26, 33]
    lattice = build_lattice(signal)
    lattice.show("saltflower_lattice.html")