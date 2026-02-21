# heartshard_demo.py — Paste engine above, then:
engine = HeartShardEngine(seed=42)
print("HeartShard Storm Sim | Commands: bond A B | move C axis[+/-] | maw D | gen | save | quit")

while True:
    cmd = input("> ").strip().split()
    if not cmd: continue
    if cmd[0] == 'quit': break
    elif cmd[0] == 'bond' and len(cmd) == 3:
        engine.bonds.create_bond(cmd[1], cmd[2], random.choice(list(BondType)))
        print(f"Bond: {cmd[1]}-{cmd[2]} formed")
    elif cmd[0] == 'move' and len(cmd) == 3:
        char, axis_dir = cmd[1], cmd[2]
        axis, dir = axis_dir[0].lower(), 1 if '+' in axis_dir else -1
        new_pol = engine.entities[char].polarity
        setattr(new_pol, axis, Polarity.NEGATIVE if new_pol.x.value == 1 else Polarity.POSITIVE if dir > 0 else Polarity.POSITIVE)
        sig = engine.entities[char].move_to_polarity(new_pol)
        engine.timeline.broadcast_signal(sig)
        print(f"{char} slips to {new_pol.to_tuple()}")
    elif cmd[0] == 'maw' and len(cmd) == 2:
        event = engine.enter_maw(cmd[1])
        if event: print(f"{cmd[1]} enters Maw! Healing: {event.vincent_healing:.2f}")
    elif cmd[0] == 'gen':
        if engine.entered_eye: engine.next_generation(engine.timeline.exclusions[-1])
    elif cmd[0] == 'save': engine.save_state('heartshard_save.json')
    else: print("Commands: bond/move/maw/gen/save/quit")
