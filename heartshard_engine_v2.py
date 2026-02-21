#!/usr/bin/env python3
"""
HeartShard: Quantum Narrative Engine
=====================================

A game where every ending is a new beginning.
Characters walk into the Eye, heal Vincent's turmoil,
and the world re-emerges in a new configuration.

Based on:
- Polarity-based physics (Universal Game Engine)
- Photonic graphics (quantum wave functions)
- Subtractive design (eliminate > accumulate)
- Constitutional axiom: "Finite capacity preserves structure 
  only by irreversible exclusion over time"
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime
import random


# ============================================================================
# CORE POLARITY SYSTEM
# ============================================================================

class Polarity(Enum):
    """Constitutional minimum: A or -A"""
    POSITIVE = 1
    NEGATIVE = -1
    
    def flip(self):
        return Polarity.NEGATIVE if self == Polarity.POSITIVE else Polarity.POSITIVE


@dataclass
class PolarityState:
    """3-axis polarity state (constitutional minimum for spatial boundaries)"""
    x: Polarity
    y: Polarity
    z: Polarity
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    
    def __eq__(self, other):
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)
    
    def to_tuple(self):
        return (self.x.value, self.y.value, self.z.value)
    
    def distance_to(self, other: 'PolarityState') -> int:
        """Hamming distance between polarity states"""
        dist = 0
        if self.x != other.x: dist += 1
        if self.y != other.y: dist += 1
        if self.z != other.z: dist += 1
        return dist


# ============================================================================
# QUANTUM ENTITIES (The Toybox)
# ============================================================================

@dataclass
class Signal:
    """
    Every interaction generates a signal (Stone's Law: no interaction too small)
    
    CRITICAL NEW MECHANIC:
    Each character STARTS with a signal. The signal shows up in a different 
    location in similar salt (polarity region) the next playthrough.
    It feels like the next generation - like the heroes somehow had kids.
    """
    source: str
    target: str
    polarity_change: Optional[PolarityState]
    friction: float
    timestamp: float
    entropy_delta: float
    event_type: str
    
    # NEW: Signal location tracking for generational continuity
    signal_location: Optional[PolarityState] = None
    generation: int = 1
    lineage: List[str] = field(default_factory=list)  # Track which characters this signal came from
    
    def __repr__(self):
        gen_str = f" gen={self.generation}" if self.generation > 1 else ""
        return f"Signal({self.source}→{self.target}, {self.event_type}, t={self.timestamp:.2f}{gen_str})"


@dataclass
class Entity:
    """
    Atomic game entity with polarity state
    T=1 (unpaired) - can bond with others
    
    NEW: Each entity carries a "birth signal" that determines where
    they re-emerge in the next generation/playthrough
    """
    name: str
    polarity: PolarityState
    entropy: float = 0.5  # Salt coherence (0=ordered, 1=chaotic)
    bonds: Set[str] = field(default_factory=set)
    signals_sent: List[Signal] = field(default_factory=list)
    signals_received: List[Signal] = field(default_factory=list)
    observed: bool = False
    diagonal: List[PolarityState] = field(default_factory=list)  # Complete history
    
    # NEW: Generational continuity
    birth_signal: Optional[Signal] = None  # The signal that spawned this entity
    generation: int = 1
    lineage: List[str] = field(default_factory=list)  # Parent names from previous generations
    
    def __post_init__(self):
        self.diagonal.append(self.polarity)
    
    def move_to_polarity(self, new_polarity: PolarityState, friction: float = 1.0):
        """Slip to new polarity state, generating signal through friction"""
        old = self.polarity
        self.polarity = new_polarity
        self.diagonal.append(new_polarity)
        
        # Movement creates signal (Stone's Law enforcement)
        return Signal(
            source=self.name,
            target="universal_db",
            polarity_change=new_polarity,
            friction=friction,
            timestamp=datetime.now().timestamp(),
            entropy_delta=friction * 0.1,
            event_type="movement"
        )
    
    def bond_with(self, other: str):
        """Create bond (reduce entropy through pairing)"""
        self.bonds.add(other)
        self.entropy = max(0.0, self.entropy - 0.1)
    
    def unbond_from(self, other: str):
        """Break bond (increase entropy)"""
        if other in self.bonds:
            self.bonds.remove(other)
            self.entropy = min(1.0, self.entropy + 0.1)


@dataclass
class Character(Entity):
    """Character entity with additional narrative properties"""
    archetype: str = "wanderer"
    core_wound: str = ""
    artifact_bonded: Optional[str] = None
    inside_eye: bool = False
    
    def can_enter_eye(self) -> bool:
        """Character must be ready (low enough entropy, have at least one bond)"""
        return len(self.bonds) >= 1 and self.entropy < 0.8


@dataclass
class Artifact(Entity):
    """Special shard/artifact entity"""
    artifact_type: str = "shard"
    bonded_character: Optional[str] = None
    power_level: float = 1.0


# ============================================================================
# RELATIONSHIP MATRIX (Quantum until observed)
# ============================================================================

class BondType(Enum):
    """Types of relationships between entities"""
    TRUST = "trust"
    OPPOSITION = "opposition"
    PROTECTION = "protection"
    DEPENDENCY = "dependency"
    MIRROR = "mirror"
    MEDIATED = "mediated"
    UNKNOWN = "unknown"


@dataclass
class Bond:
    """Relationship between two entities"""
    entity_a: str
    entity_b: str
    bond_type: BondType
    strength: float  # 0.0 to 1.0
    formed_at: float
    signals: List[Signal] = field(default_factory=list)
    
    def __hash__(self):
        # Symmetric: (A,B) == (B,A)
        pair = tuple(sorted([self.entity_a, self.entity_b]))
        return hash(pair)


class RelationshipMatrix:
    """
    Quantum relationship system
    Bonds exist in superposition until observed
    """
    
    def __init__(self):
        self.bonds: Dict[Tuple[str, str], Bond] = {}
        self.collapsed_bonds: Set[Tuple[str, str]] = set()
        
    def _normalize_key(self, a: str, b: str) -> Tuple[str, str]:
        """Ensure consistent ordering"""
        return tuple(sorted([a, b]))
    
    def create_bond(self, a: str, b: str, bond_type: BondType, strength: float = 0.5):
        """Create or strengthen a bond"""
        key = self._normalize_key(a, b)
        
        if key in self.bonds:
            # Strengthen existing bond
            self.bonds[key].strength = min(1.0, self.bonds[key].strength + strength * 0.5)
        else:
            # New bond
            self.bonds[key] = Bond(
                entity_a=a,
                entity_b=b,
                bond_type=bond_type,
                strength=strength,
                formed_at=datetime.now().timestamp()
            )
    
    def get_bond(self, a: str, b: str) -> Optional[Bond]:
        """Retrieve bond (collapses superposition if exists)"""
        key = self._normalize_key(a, b)
        bond = self.bonds.get(key)
        if bond:
            self.collapsed_bonds.add(key)
        return bond
    
    def get_bonded_to(self, entity: str) -> List[str]:
        """Get all entities bonded to this one"""
        bonded = []
        for (a, b), bond in self.bonds.items():
            if a == entity:
                bonded.append(b)
            elif b == entity:
                bonded.append(a)
        return bonded
    
    def collapse_new_bond(self, a: str, b: str, excluded_mediator: str) -> Bond:
        """
        Generate new bond after mediator is excluded
        Bond type emerges from what was mediated
        """
        # Check if they had any prior indirect connection
        old_bond_a = self.get_bond(a, excluded_mediator)
        old_bond_b = self.get_bond(b, excluded_mediator)
        
        if old_bond_a and old_bond_b:
            # Synthesis of mediated relationships
            if old_bond_a.bond_type == old_bond_b.bond_type:
                new_type = old_bond_a.bond_type
            else:
                # Tension creates opposition or dependency
                new_type = random.choice([BondType.OPPOSITION, BondType.DEPENDENCY])
            
            strength = (old_bond_a.strength + old_bond_b.strength) / 2
        else:
            # No prior connection - quantum collapse
            new_type = random.choice(list(BondType))
            strength = random.uniform(0.3, 0.7)
        
        new_bond = Bond(
            entity_a=a,
            entity_b=b,
            bond_type=new_type,
            strength=strength,
            formed_at=datetime.now().timestamp()
        )
        
        key = self._normalize_key(a, b)
        self.bonds[key] = new_bond
        
        return new_bond
    
    def snapshot(self) -> Dict:
        """Capture current state for exclusion events"""
        return {
            'bonds': {k: (v.bond_type.value, v.strength) for k, v in self.bonds.items()},
            'collapsed': list(self.collapsed_bonds),
            'timestamp': datetime.now().timestamp()
        }


# ============================================================================
# TIMELINE DATABASE (Exclusion Events)
# ============================================================================

@dataclass
class ExclusionEvent:
    """
    Irreversible event where character enters the Eye
    Axiom: "Finite capacity preserves structure only by 
           irreversible exclusion over time"
    """
    character: str
    bonds_at_entry: Dict
    world_state: Dict
    vincent_healing: float
    timestamp: float
    eye_closed: bool = False
    new_world_seed: Optional[int] = None


class TimelineDB:
    """
    Universal database spanning all timelines
    Stores all signals, all exclusions, all branches
    """
    
    def __init__(self):
        self.current_time: float = 0.0
        self.signals: List[Signal] = []
        self.exclusions: List[ExclusionEvent] = []
        self.branches: List['TimelineDB'] = []
        self.branch_point: Optional[float] = None
        
    def broadcast_signal(self, signal: Signal):
        """All signals recorded (Stone's Law: no interaction too small)"""
        self.signals.append(signal)
        self.current_time = signal.timestamp
    
    def record_exclusion(self, event: ExclusionEvent):
        """Record irreversible exclusion event"""
        self.exclusions.append(event)
        event.eye_closed = True
    
    def branch_from_exclusion(self, exclusion: ExclusionEvent, new_bonds: Dict) -> 'TimelineDB':
        """Create new timeline branch after exclusion"""
        new_timeline = TimelineDB()
        new_timeline.branch_point = exclusion.timestamp
        
        # New timeline has all history up to exclusion
        new_timeline.signals = self.signals.copy()
        new_timeline.exclusions = self.exclusions.copy()
        
        # But different initial conditions for new playthrough
        new_timeline.current_time = 0.0  # Restart
        
        self.branches.append(new_timeline)
        return new_timeline
    
    def get_state_snapshot(self) -> Dict:
        """Capture complete state"""
        return {
            'time': self.current_time,
            'signals': len(self.signals),
            'exclusions': len(self.exclusions),
            'branches': len(self.branches),
            'last_exclusion': self.exclusions[-1].character if self.exclusions else None
        }


# ============================================================================
# HEARTSHARD ENGINE (The Toybox Shuffler)
# ============================================================================

class HeartShardEngine:
    """
    Quantum narrative engine
    Every ending is a new beginning
    """
    
    def __init__(self, seed: Optional[int] = None):
        if seed:
            random.seed(seed)
            np.random.seed(seed)
        
        # Initialize timeline
        self.timeline = TimelineDB()
        
        # Relationship matrix
        self.bonds = RelationshipMatrix()
        
        # The 8 characters + Vincent + artifacts (the toybox)
        self.entities: Dict[str, Entity] = {}
        self._initialize_entities()
        
        # Track which entities have entered the eye
        self.entered_eye: Set[str] = set()
        
        # Current playthrough number
        self.playthrough: int = 1
        
    def _initialize_entities(self):
        """Create the atomic entities"""
        
        # THE 8 MAIN CHARACTERS (correct list, no Vincent - he's adjacent)
        # Mortal Wing: Lila, Theo, Furin, Chanti
        # Emergent Wing: Kai, Ori, Ayni, Ion
        characters = {
            # === MORTAL WING ===
            'lila': Character(
                name='Lila',
                polarity=PolarityState(Polarity.POSITIVE, Polarity.NEGATIVE, Polarity.POSITIVE),
                archetype='quiet_wanderer',
                core_wound='hoards_heartshard_believes_only_for_self',
                artifact_bonded='heartshard',
                entropy=0.3  # Low entropy - quiet, ordered
            ),
            'theo': Character(
                name='Theo',
                polarity=PolarityState(Polarity.NEGATIVE, Polarity.POSITIVE, Polarity.POSITIVE),
                archetype='branded_believer',
                core_wound='inherited_indoctrination_brand_numbs_mind',
                entropy=0.6  # Medium entropy - questioning
            ),
            'furin': Character(
                name='Furin',
                polarity=PolarityState(Polarity.POSITIVE, Polarity.POSITIVE, Polarity.NEGATIVE),
                archetype='mechanic_who_bleeds',
                core_wound='wants_to_fix_everything_blood_delusion',
                entropy=0.5
            ),
            'chanti': Character(
                name='Chanti',
                polarity=PolarityState(Polarity.NEGATIVE, Polarity.NEGATIVE, Polarity.POSITIVE),
                archetype='jaded_fighter',
                core_wound='tilt_causes_explosion',
                artifact_bonded='flameblade',
                entropy=0.8  # High entropy - jaded, explosive
            ),
            
            # === EMERGENT WING (Ascended Legends) ===
            'kai': Character(
                name='Kai',
                polarity=PolarityState(Polarity.POSITIVE, Polarity.POSITIVE, Polarity.POSITIVE),
                archetype='abyss_child',
                core_wound='chased_mother_into_abyss_nearly_died',
                entropy=0.4  # Stabilized by abyss bubble
            ),
            'ori': Character(
                name='Ori',
                polarity=PolarityState(Polarity.NEGATIVE, Polarity.POSITIVE, Polarity.NEGATIVE),
                archetype='liquid_sword',
                core_wound='fixation_on_fish_cost_his_life',
                entropy=0.4  # Reborn as silvery hero
            ),
            'ayni': Character(
                name='Ayni',
                polarity=PolarityState(Polarity.POSITIVE, Polarity.NEGATIVE, Polarity.NEGATIVE),
                archetype='stone_pillar',
                core_wound='avalanche_disasters_from_rolling',
                entropy=0.5  # Ascends as floating snow
            ),
            'ion': Character(
                name='Ion',
                polarity=PolarityState(Polarity.NEGATIVE, Polarity.NEGATIVE, Polarity.NEGATIVE),
                archetype='frequency_child',
                core_wound='fails_to_exist_if_escapes_ayni_field',
                entropy=0.5  # Pure frequency in icy air
            ),
        }
        
        # === ADJACENT ENTITIES (not part of the 8) ===
        adjacents = {
            'vincent': Character(
                name='Vincent',
                polarity=PolarityState(Polarity.NEGATIVE, Polarity.POSITIVE, Polarity.POSITIVE),
                archetype='shard_construct',
                core_wound='no_real_self_driven_existence',
                inside_eye=False,  # Starts outside, will fuse with Flameblade
                entropy=0.9  # High entropy - amalgam of dead mages
            ),
        }
        
        # === ARTIFACTS & ENTITIES ===
        artifacts = {
            'heartshard': Artifact(
                name='Heartshard',
                polarity=PolarityState(Polarity.POSITIVE, Polarity.POSITIVE, Polarity.POSITIVE),
                artifact_type='mirror_shard',
                bonded_character='lila',
                power_level=1.0,
                entropy=0.1  # Very low entropy - pure, reflective, non-judging mirror
            ),
            'flameblade': Artifact(
                name='Flameblade',
                polarity=PolarityState(Polarity.NEGATIVE, Polarity.NEGATIVE, Polarity.NEGATIVE),
                artifact_type='consumption_shard',
                bonded_character='chanti',
                power_level=1.2,
                entropy=0.9  # High entropy - old entity, knows only consumption and ruin
            ),
            'heartshield': Artifact(
                name='Heartshield',
                polarity=PolarityState(Polarity.POSITIVE, Polarity.POSITIVE, Polarity.POSITIVE),
                artifact_type='fusion_dome',
                bonded_character=None,  # Created from spanner + heartshard
                power_level=2.0,
                entropy=0.05  # Extremely low - seals the maw permanently
            ),
            'maw': Artifact(
                name='Maw',
                polarity=PolarityState(Polarity.NEGATIVE, Polarity.NEGATIVE, Polarity.NEGATIVE),
                artifact_type='cataclysm_wound',
                bonded_character=None,
                power_level=3.0,
                entropy=0.95  # Eye of the Cataclysm - source of horrors
            ),
        }
        
        self.entities = {**characters, **adjacents, **artifacts}
        
        # Initialize starting bonds
        self._initialize_starting_bonds()
    
    def _initialize_starting_bonds(self):
        """Set up initial relationship configuration"""
        # Lila bonds with Heartshard (mirror that doesn't judge)
        self.bonds.create_bond('lila', 'heartshard', BondType.MIRROR, strength=1.0)
        self.entities['lila'].bond_with('heartshard')
        self.entities['heartshard'].bond_with('lila')
        
        # Chanti bonds with Flameblade (weapon to fight back)
        self.bonds.create_bond('chanti', 'flameblade', BondType.DEPENDENCY, strength=0.9)
        self.entities['chanti'].bond_with('flameblade')
        self.entities['flameblade'].bond_with('chanti')
        
        # Furin and Chanti (protection dynamic from the mine scene)
        self.bonds.create_bond('furin', 'chanti', BondType.PROTECTION, strength=0.7)
        self.entities['furin'].bond_with('chanti')
        self.entities['chanti'].bond_with('furin')
        
        # Flameblade drawn to Heartshard (opposition)
        self.bonds.create_bond('flameblade', 'heartshard', BondType.OPPOSITION, strength=0.8)
        
        # Add some initial character bonds (will evolve)
        self.bonds.create_bond('kai', 'oni', BondType.TRUST, strength=0.6)
        self.bonds.create_bond('ayni', 'ion', BondType.TRUST, strength=0.5)
    
    def enter_the_maw(self, character_name: str) -> Dict:
        """
        CORE MECHANIC: Character enters the Maw (Eye of the Cataclysm)
        
        This is NOT about healing Vincent - that was the wrong model.
        The TRUE mechanic:
        
        1. Characters converge at the Maw
        2. Heartshield is created (Furin's spanner + Heartshard)
        3. Vincent fuses with Flameblade → Flamespawn
        4. Eyes in Sky (Kai & Ori wink, Ayni & Ion rainbow) seal the Maw
        5. Diamond ice dome forms
        6. Each character who entered generates a SIGNAL for next generation
        7. World reshuffles - signals appear in similar "salt" (polarity regions)
        8. Feels like the heroes had kids - same essence, new location
        
        Returns: New world configuration with next-generation signals
        """
        character = self.entities.get(character_name)
        if not character or not isinstance(character, Character):
            return {'error': 'Invalid character'}
        
        if character.inside_eye:
            return {'error': 'Already inside the Maw'}
        
        if not character.can_enter_eye():
            return {'error': 'Character not ready (needs bonds, lower entropy)'}
        
        # 1. Character enters the Maw
        character.inside_eye = True
        self.entered_eye.add(character_name)
        
        # 2. Generate their BIRTH SIGNAL for next generation
        # This signal will spawn a similar character in similar "salt" next time
        birth_signal = Signal(
            source=character_name,
            target='next_generation',
            polarity_change=character.polarity,
            friction=1.0,
            timestamp=datetime.now().timestamp(),
            entropy_delta=0.0,
            event_type='generational_birth',
            signal_location=character.polarity,  # Spawns in similar polarity region
            generation=character.generation + 1,
            lineage=character.lineage + [character_name]
        )
        
        # Store signal in timeline (persists across playthroughs)
        self.timeline.broadcast_signal(birth_signal)
        
        # 3. Reshuffle the toybox for next generation
        new_config = self._generate_next_generation(birth_signal)
        
        # 4. Create new timeline branch
        new_world = self.timeline.branch_from_exclusion(
            ExclusionEvent(
                character=character_name,
                bonds_at_entry=self.bonds.snapshot(),
                world_state=self.timeline.get_state_snapshot(),
                vincent_healing=0.0,  # Not about Vincent anymore
                timestamp=birth_signal.timestamp
            ),
            new_config['bonds']
        )
        
        self.playthrough += 1
        
        return {
            'success': True,
            'character': character_name,
            'birth_signal': {
                'location': birth_signal.signal_location.to_tuple(),
                'generation': birth_signal.generation,
                'lineage': birth_signal.lineage
            },
            'playthrough': self.playthrough,
            'new_configuration': new_config,
            'message': f"{character_name} enters the Maw. Their signal echoes into the next generation..."
        }
    
    def _generate_next_generation(self, birth_signal: Signal) -> Dict:
        """
        Generate next-generation character placement based on signals
        
        Characters re-emerge in "similar salt" - nearby polarity states
        that share some characteristics with their parent generation.
        
        This creates the feeling that heroes had kids:
        - Same archetype/essence
        - Different starting location (but similar polarity neighborhood)
        - New bonds form in new configuration
        """
        parent_name = birth_signal.source
        parent_polarity = birth_signal.signal_location
        
        # Find "similar salt" - nearby polarity states
        # Flip 0-1 axes to get similar but different location
        similar_polarities = self._find_similar_salt(parent_polarity)
        
        # Choose one for next generation spawn
        next_polarity = random.choice(similar_polarities)
        
        # Update parent entity's polarity for next playthrough
        if parent_name in self.entities:
            parent = self.entities[parent_name]
            parent.polarity = next_polarity
            parent.generation = birth_signal.generation
            parent.lineage = birth_signal.lineage
            parent.birth_signal = birth_signal
        
        # Generate new bonds in this new configuration
        new_bonds = self._reshuffle_bonds_generational(parent_name, next_polarity)
        
        return {
            'parent': parent_name,
            'next_location': next_polarity.to_tuple(),
            'generation': birth_signal.generation,
            'lineage': birth_signal.lineage,
            'bonds': new_bonds,
            'message': f"{parent_name} re-emerges as if their child, in similar salt"
        }
    
    def _find_similar_salt(self, polarity: PolarityState) -> List[PolarityState]:
        """
        Find polarity states that are "similar" - nearby in state space
        
        Similar salt = flip 0-1 axes, keep at least one axis the same
        This creates a neighborhood of related but distinct states
        """
        similar = []
        
        # Keep all same (identity)
        similar.append(polarity)
        
        # Flip one axis
        for axis in ['x', 'y', 'z']:
            new_pol = PolarityState(polarity.x, polarity.y, polarity.z)
            if axis == 'x':
                new_pol.x = polarity.x.flip()
            elif axis == 'y':
                new_pol.y = polarity.y.flip()
            else:
                new_pol.z = polarity.z.flip()
            similar.append(new_pol)
        
        # Flip two axes (more distant but still similar)
        for axis1, axis2 in [('x', 'y'), ('x', 'z'), ('y', 'z')]:
            new_pol = PolarityState(polarity.x, polarity.y, polarity.z)
            if 'x' in [axis1, axis2]:
                new_pol.x = polarity.x.flip()
            if 'y' in [axis1, axis2]:
                new_pol.y = polarity.y.flip()
            if 'z' in [axis1, axis2]:
                new_pol.z = polarity.z.flip()
            similar.append(new_pol)
        
        return similar
    
    def _reshuffle_bonds_generational(self, character: str, new_polarity: PolarityState) -> Dict:
        """
        Generate new bonds based on new polarity location
        
        Characters who spawn near each other in polarity space
        are more likely to bond in the next generation
        """
        new_bonds = {}
        
        # Get all characters
        all_chars = [k for k, v in self.entities.items() 
                    if isinstance(v, Character) and k != character and k != 'vincent']
        
        # For each pair, check if they're close in polarity space
        for other in all_chars:
            if other == character:
                continue
            
            other_entity = self.entities[other]
            distance = new_polarity.distance_to(other_entity.polarity)
            
            # Closer in polarity space = stronger bond
            if distance <= 1:  # Adjacent or same
                bond_strength = 0.8
                bond_type = random.choice([BondType.TRUST, BondType.PROTECTION])
            elif distance == 2:
                bond_strength = 0.5
                bond_type = random.choice([BondType.DEPENDENCY, BondType.MIRROR])
            else:
                bond_strength = 0.2
                bond_type = BondType.UNKNOWN
            
            if random.random() < bond_strength:
                new_bonds[(character, other)] = {
                    'type': bond_type.value,
                    'strength': bond_strength
                }
        
        return new_bonds
    
    def _reshuffle_from_exclusion(self, exclusion: ExclusionEvent) -> Dict:
        """
        Generate new world configuration after exclusion
        Same entities, different relationships
        """
        excluded = exclusion.character
        
        # Who was bonded to the excluded character?
        affected_entities = self.bonds.get_bonded_to(excluded)
        
        # Generate new bonds between affected entities
        new_bonds = {}
        for i, entity_a in enumerate(affected_entities):
            for entity_b in affected_entities[i+1:]:
                # They must now relate directly (mediator gone)
                new_bond = self.bonds.collapse_new_bond(
                    entity_a, 
                    entity_b,
                    excluded_mediator=excluded
                )
                new_bonds[(entity_a, entity_b)] = {
                    'type': new_bond.bond_type.value,
                    'strength': new_bond.strength
                }
        
        # Quantum shuffle other relationships
        # Characters who weren't directly affected still get perturbed
        all_chars = [k for k, v in self.entities.items() 
                    if isinstance(v, Character) and k != excluded and k != 'vincent']
        
        for char in all_chars:
            if random.random() < 0.3:  # 30% chance of polarity shift
                entity = self.entities[char]
                # Flip one random axis
                axis = random.choice(['x', 'y', 'z'])
                if axis == 'x':
                    entity.polarity.x = entity.polarity.x.flip()
                elif axis == 'y':
                    entity.polarity.y = entity.polarity.y.flip()
                else:
                    entity.polarity.z = entity.polarity.z.flip()
        
        return {
            'excluded': excluded,
            'affected': affected_entities,
            'bonds': new_bonds,
            'polarity_shifts': len([c for c in all_chars if random.random() < 0.3]),
            'seed': random.randint(0, 999999)
        }
    
    def get_current_state(self) -> Dict:
        """Get complete game state"""
        return {
            'playthrough': self.playthrough,
            'entities': {
                name: {
                    'polarity': entity.polarity.to_tuple(),
                    'entropy': entity.entropy,
                    'bonds': list(entity.bonds),
                    'inside_eye': entity.inside_eye if isinstance(entity, Character) else False
                }
                for name, entity in self.entities.items()
            },
            'bonds': self.bonds.snapshot(),
            'timeline': self.timeline.get_state_snapshot(),
            'entered_eye': list(self.entered_eye),
            'vincent_turmoil': self.entities['vincent'].entropy
        }
    
    def save_state(self, filename: str):
        """Save complete state to file"""
        state = self.get_current_state()
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)
        return f"State saved to {filename}"
    
    def can_end_game(self) -> bool:
        """Check if game can reach ending (Vincent healed enough)"""
        vincent = self.entities['vincent']
        return vincent.entropy < 0.3 and len(self.entered_eye) >= 3


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demo_heartshard():
    """Demonstrate the quantum narrative engine with generational signals"""
    
    print("="*70)
    print("HEARTSHARD: Quantum Narrative Engine")
    print("Every ending is a new beginning")
    print("Heroes return as if they had children")
    print("="*70)
    print()
    
    # Initialize engine
    engine = HeartShardEngine(seed=42)
    
    print("GENERATION 1: Initial Configuration")
    print("-" * 70)
    state = engine.get_current_state()
    
    # Show the 8 main characters
    main_chars = ['lila', 'theo', 'furin', 'chanti', 'kai', 'ori', 'ayni', 'ion']
    print(f"The Eight Heroes:")
    for name in main_chars:
        entity = state['entities'][name]
        pol = entity['polarity']
        print(f"  {name.upper():8} at ({pol[0]:+d}, {pol[1]:+d}, {pol[2]:+d}) | entropy: {entity['entropy']:.0%}")
    print()
    print(f"Active bonds: {len(state['bonds']['bonds'])}")
    print()
    
    # Character 1 enters the Maw
    print("═" * 70)
    print("Lila enters the Maw...")
    print("═" * 70)
    result1 = engine.enter_the_maw('lila')
    if result1.get('success'):
        print(f"✓ {result1['message']}")
        signal = result1['birth_signal']
        print(f"  Birth signal generated: Gen {signal['generation']}")
        print(f"  Parent location: {signal['location']}")
        print(f"  Lineage: {' → '.join(signal['lineage'])}")
        print()
        
        new_loc = result1['new_configuration']['next_location']
        print(f"  Next generation Lila will spawn at: ({new_loc[0]:+d}, {new_loc[1]:+d}, {new_loc[2]:+d})")
        print(f"  (Similar salt - nearby polarity state)")
        print()
    
    print("-" * 70)
    print()
    
    # Character 2 enters
    print("Chanti enters the Maw...")
    print()
    result2 = engine.enter_the_maw('chanti')
    if result2.get('success'):
        print(f"✓ {result2['message']}")
        signal = result2['birth_signal']
        print(f"  Generation: {signal['generation']}")
        new_loc = result2['new_configuration']['next_location']
        print(f"  Next spawn: ({new_loc[0]:+d}, {new_loc[1]:+d}, {new_loc[2]:+d})")
        print()
    
    print("-" * 70)
    print()
    
    # Character 3 enters
    print("Furin enters the Maw...")
    print()
    result3 = engine.enter_the_maw('furin')
    if result3.get('success'):
        print(f"✓ {result3['message']}")
        signal = result3['birth_signal']
        print(f"  Generation: {signal['generation']}")
        print(f"  Playthrough: {result3['playthrough']}")
        print()
    
    print("="*70)
    print("GENERATIONAL CONTINUITY")
    print("="*70)
    final_state = engine.get_current_state()
    print(f"Characters who entered: {len(final_state['entered_eye'])}")
    print(f"Timeline branches: {final_state['timeline']['branches']}")
    print()
    
    print("Next generation preview:")
    for name in ['lila', 'chanti', 'furin']:
        entity = engine.entities[name]
        if entity.generation > 1:
            print(f"  {name.upper()}: Gen {entity.generation} at {entity.polarity.to_tuple()}")
            if entity.lineage:
                print(f"    Lineage: {' → '.join(entity.lineage)}")
    print()
    
    print("="*70)
    print("THE BUTTERFLY EMERGES")
    print("="*70)
    print("Mortal Wing (Lila, Theo, Furin, Chanti)")
    print("  + Emergent Wing (Kai, Ori, Ayni, Ion)")
    print("  → Unexpected Junction at the Maw")
    print("  → Heartshield created (Furin's spanner + Heartshard)")
    print("  → Eyes in Sky wink (Kai & Ori tag-team)")
    print("  → Diamond ice dome seals the Maw")
    print("  → Each hero's signal births next generation")
    print()
    print("It feels like the heroes had children.")
    print("Same essence. Different location. New bonds.")
    print("Every ending is a new beginning.")
    print("="*70)


if __name__ == '__main__':
    demo_heartshard()
