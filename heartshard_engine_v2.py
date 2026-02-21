#!/usr/bin/env python3
"""
HeartShard v2: Completed Quantum Narrative Engine
"""
# [Full code from fetches + completions]
# ... (imports, Polarity, PolarityState, Signal, Entity, Character, Artifact, BondType, Bond, RelationshipMatrix, ExclusionEvent, TimelineDB as above)

# COMPLETE _initialize_entities()
characters = {
    'lila': Character(name='Lila', polarity=PolarityState(Polarity.POSITIVE, Polarity.NEGATIVE, Polarity.POSITIVE), archetype='quiet_wanderer', core_wound='hoards_heartshard_believes_only_for_self'),
    'theo': Character(name='Theo', polarity=PolarityState(Polarity.NEGATIVE, Polarity.POSITIVE, Polarity.NEGATIVE), archetype='branded_believer', core_wound='inherited_duty'),
    'furin': Character(name='Furin', polarity=PolarityState(Polarity.POSITIVE, Polarity.POSITIVE, Polarity.NEGATIVE), archetype='bleeding_mechanic', core_wound='self_harm_machines'),
    'chanti': Character(name='Chanti', polarity=PolarityState(Polarity.NEGATIVE, Polarity.NEGATIVE, Polarity.POSITIVE), archetype='jaded_fighter', core_wound='tilt_explosions'),
    'kai': Character(name='Kai', polarity=PolarityState(Polarity.NEGATIVE, Polarity.NEGATIVE, Polarity.NEGATIVE), archetype='abyss_child', core_wound='mother_chase'),
    'ori': Character(name='Ori', polarity=PolarityState(Polarity.POSITIVE, Polarity.NEGATIVE, Polarity.NEGATIVE), archetype='liquid_sword', core_wound='frozen_fish'),
    'ayni': Character(name='Ayni', polarity=PolarityState(Polarity.POSITIVE, Polarity.POSITIVE, Polarity.POSITIVE), archetype='stone_pillar', core_wound='downward_rolls'),
    'ion': Character(name='Ion', polarity=PolarityState(Polarity.NEGATIVE, Polarity.POSITIVE, Polarity.POSITIVE), archetype='frequency_child', core_wound='over_excitement'),
}
for name, char in characters.items():
    self.entities[name] = char
    # Birth signal for gen continuity
    char.birth_signal = Signal(source=name, target='maw', event_type='birth', friction=1.0, timestamp=0.0, entropy_delta=0.0, signal_location=char.polarity)

# Add to HeartShardEngine class
def enter_maw(self, character_name: str) -> ExclusionEvent:
    char = self.entities[character_name]
    if not char.can_enter_eye():
        return None
    # Generate birth signal for next gen
    birth_sig = Signal(
        source=char.name, target='next_gen', polarity_change=char.polarity,
        friction=char.entropy, timestamp=datetime.now().timestamp(), entropy_delta=-char.entropy,
        event_type='maw_entry', signal_location=char.polarity, generation=self.playthrough,
        lineage=char.lineage + [char.name]
    )
    self.timeline.broadcast_signal(birth_sig)
    char.inside_eye = True
    self.entered_eye.add(character_name)
    event = ExclusionEvent(character=character_name, bonds_at_entry=self.bonds.snapshot(),
                           world_state=self.timeline.get_state_snapshot(), vincent_healing=1.0 / len(self.entered_eye),
                           timestamp=datetime.now().timestamp())
    self.timeline.record_exclusion(event)
    return event

def next_generation(self, event: ExclusionEvent) -> None:
    self.playthrough += 1
    # Flip 0-2 axes for similar salt (prime-filtered random)
    flips = random.choices([0,1,2], k=random.randint(0,2), weights=[0.4,0.4,0.2])  # Prime-ish bias
    new_pol = PolarityState(*[p.flip() if i in flips else p for i,p in enumerate(event.polarity_change)])
    # Respawn child-like entity
    child_name = f"{event.character}_gen{self.playthrough}"
    child = Character(name=child_name, polarity=new_pol, generation=self.playthrough,
                      lineage=event.lineage, birth_signal=event.signal)
    self.entities[child_name] = child
    print(f"Rebirth: {child_name} emerges in {new_pol.to_tuple()} (similar salt to {event.character})")
    self.bonds.create_bond(child_name, list(self.bonds.get_bonded_to(event.character))[0] if self.bonds.get_bonded_to(event.character) else 'maw', BondType.TRUST)

def save_state(self, filename: str):
    state = {k: { 'polarity': v.polarity.to_tuple(), 'bonds': list(v.bonds), 'generation': v.generation } for k,v in self.entities.items()}
    with open(filename, 'w') as f:
        json.dump(state, f)

# [Rest of classes unchanged]
