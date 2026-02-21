# uwei.py — U-Wei shell sketch
import ste  # your STE module
import time
import random  # only for very light timing/poetic variance — optional

def wu_wei_narrate(result: str) -> str:
    if result == "<silence>":
        pauses = ["…", "          ", ""]
        return random.choice(pauses)  # or just return ""
    
    # minimal mirror — no addition, just reflection + dissolve
    if "entities:" in result:
        core = result.split("entities:")[1].strip().split("\n")[0]
        return f"shadow of {core} appears… then fades."
    return result  # fallback — rare

while True:
    try:
        raw = input("→ ").strip()
        if not raw:
            print("")  # empty input → empty response (wu-wei)
            continue
        
        # pass raw → STE (no pre-narration!)
        core_out = ste.reduce_text(raw)
        
        # outer reflection only
        voiced = wu_wei_narrate(core_out)
        print(voiced)
        
        # soft pause — non-forcing rhythm
        time.sleep(0.8 + random.uniform(0, 1.2))
    except KeyboardInterrupt:
        print("\n… returning to the field.")
        break