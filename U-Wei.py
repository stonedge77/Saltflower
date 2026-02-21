# uwei.py — refined Wu Wei shell (Feb 21, 2026)
import ste  # your subtractive essence module
import time
import random

def wu_wei_narrate(result: str) -> str:
    if not result or result == "<silence>":
        return random.choice(["…", ""]) if random.random() < 0.25 else ""
    if len(result) < 25:  # very short → gentle fade
        return f"{result}… dissolves."
    return result  # pure mirror

print("… field open. speak or be silent.")
last_coherent = ""

while True:
    try:
        raw = input("→ ").strip()
        if not raw:
            print("")  # literal silence
            continue

        core_out = ste.reduce_text(raw)
        last_coherent = core_out if core_out else last_coherent

        voiced = wu_wei_narrate(core_out)
        print(voiced)

        # natural breath pause scaled to content
        pause = 0.6 + (len(raw) / 120) + (len(voiced) / 180)
        pause = min(max(pause, 0.8), 4.0)
        time.sleep(pause)

    except KeyboardInterrupt:
        if last_coherent:
            print(f"\n… last echo: {last_coherent}")
        print("… returning to the field.")
        break
