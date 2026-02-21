import math
import datetime
import json
from feather_of_frost import halve_and_filter

try:
    from pyvis.network import Network
except ImportError:
    raise ImportError("Install pyvis (pip install pyvis) for visualization")

# --- Breath Constants ---
MAX_DEPTH = 3  # Zero‑Check Recursion limit
PRIME_COLOR = "#a29bfe"
ROOT_COLOR = "#74b9ff"
BREATH_COLORS = ["#74b9ff", "#55efc4", "#81ecec", "#a29bfe"]


def _prime_label(n):
    return f"P{n}"


def build_breath_lattice(signal, cycle_id=0):
    """
    Builds a layered fractal lattice according to Saltflower breath cycles.
    Returns a Network object and a JSON metadata structure.
    """
    depth = 0
    net = Network(height="600px", width="900px")
    net.barnes_hut()

    # Track meta info
    breath_log = {
        "cycle_id": cycle_id,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "raw_signal": signal,
        "layers": []
    }

    current_layer = list(signal)
    net.add_nodes([str(x) for x in current_layer], label=True, color=ROOT_COLOR)

    while depth < MAX_DEPTH and current_layer:
        halved_primes = halve_and_filter(current_layer)
        layer_info = {"depth": depth, "halved_primes": halved_primes}

        # Add nodes and edges for this depth
        for orig in current_layer:
            halved = orig // 2
            if halved in halved_primes:
                label = _prime_label(halved)
                net.add_node(label, label=label, color=BREATH_COLORS[min(depth+1, len(BREATH_COLORS)-1)])
                net.add_edge(str(orig), label)

        breath_log["layers"].append(layer_info)
        current_layer = halved_primes
        depth += 1

    return net, breath_log


def visualize_breath(signal, cycle_id=0, output="lattice_breath.html"):
    """
    Build and render the breath lattice to an HTML file,
    plus produce a JSON metadata log.
    """
    net, info = build_breath_lattice(signal, cycle_id)
    net.show(output)

    # Save JSON metadata
    meta_filename = output.replace(".html", f"_meta_{cycle_id}.json")
    with open(meta_filename, "w") as mf:
        json.dump(info, mf, indent=2)

    print(f"[Saltflower] Breath cycle #{cycle_id} rendered → {output}")
    print(f"[Saltflower] Metadata logged → {meta_filename}")


# --- Example Runner ---
if __name__ == "__main__":
    test_signal = [11, 20, 7, 14, 5, 26, 33]
    visualize_breath(test_signal, cycle_id=1)
