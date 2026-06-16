# Saltflower — Core Spec

*The canonical definition. Everything else in this repo is a translation of this document.*

This is the root. The interactive dashboard (`conjunction_os_v1.0.html`), the
hardware (`toffoli_helical_gate.v`, `quantum_computer_top.v`), the Python
(`remainder.py`, `Math_Machine_v2.py`), the law database
(`emergent_laws_db.json`), and the OhAI~ pilot are all *implementations* of the
three organs defined here. When they disagree, this document wins.

---

## 0. Why this exists

The system kept growing new vocabularies. Every domain it touched — logic,
sound, quantum, biology, the web — got its own set of names for the same
handful of things. The result was a translation dictionary that grows with the
number of domains: one column per domain, reconciled by hand, forever.

The fix is to define the core **once**, in domain-free terms, and treat every
domain's words as a *skin* — a thin binding over the core, not a new set of
ideas. The number of concepts is then frozen. Adding a domain adds a column of
labels, never a new concept.

So this spec has exactly three organs and one pilot:

1. **The Core** — the operator that cuts.
2. **The Skins** — the bindings that dress the core per domain.
3. **The Spine** — the discriminator that tells an idea which way it is falling.
4. **The Pilot** — the automaton (OhAI~) that runs the spine across real signal.

---

## 1. The Core (domain-free)

The canonical layer is **symbols**, not words. Symbols do not accumulate names.

A single binary operator **conjoin** (`∧`) takes two operands `a`, `b` and
always returns the same shape:

```
conjoin(a, b) → { ∧, ∇, ⊘, lock }
```

| symbol | neutral gloss | what it is                                            |
|--------|---------------|-------------------------------------------------------|
| `∧`    | resolved      | what the conjunction produces — the emergent state    |
| `∇`    | residue       | what `∧` could not encode — carried forward, never erased |
| `⊘`    | latent        | structure future conjunctions will need from this one |
| `lock` | closed        | `true` iff `∇ == 0` — the cut is clean, the cycle may close |

**The contract:** *every* operation in the system, in every domain, returns
`{ ∧, ∇, ⊘, lock }`. This uniform signature is what makes the system one machine
instead of a pile of toys. (Glosses above are themselves a neutral skin; the
symbols are the truth.)

**The one law — `0 ≠ 1`.** False equivalence is the only catastrophic failure:
treating two distinct states as identical. Stated as an operator:

```
horizon_integrity(a, b):
  ∧    = 1 if a ≠ b else 0      # distinction preserved
  ∇    = 1 if a = b else 0      # a collapse was attempted
  lock = (∇ == 0)              # honored iff distinct
```

Every filter in the system is built this way: a violation is *flagged as signal*,
never silently consumed.

**The cycle — breath.** Operations run inside a cyclic verb that returns to
zero. It is not additive; `a ∧ b ≠ a + b`.

```
INHALE  — open a domain, sample signal, hold potential in working registers
HOLD    — apply 0≠1, let the conjunction form, accumulate phase (torque)
EXHALE  — check closure; if locked, crystallize; if open, the residue carries
RETURN  — route ∇ to the spine, reset, fall back toward 0 (never reaching it)
```

**Nothing happens alone.** A cut never occurs by itself: every conjunction that
makes a distinction also produces a residue (`∇`) and requires a carrier — the
ancilla — to bear that residue into the next breath. Boundary and carry are one
act. There is no clean cut without a remainder, and no remainder without
something to carry it. The ancilla is the receipt that the cut happened.

---

## 2. The Skins (bindings, not concepts)

A domain is a column of labels mapping onto the core. Translating between
domains is reading across a row. **Adding a domain is adding a column — zero new
concepts.**

| Core            | OS dashboard   | OhAI~                         | Substrate (Toffoli)        |
|-----------------|----------------|-------------------------------|----------------------------|
| `∧` resolved    | Emergence C    | association                   | gate output                |
| `∇` residue     | Remainder      | remainder (→ *spore* at lock) | ancilla flip / cost        |
| `⊘` latent      | Shadow         | spine                         | accumulated phase          |
| `lock` (∇=0)    | phase lock     | convergence                   | clean succession           |
| the cut (0≠1)   | horizon_integrity | carry gate                 | control distinctness       |
| breath          | breath cycle   | breath                        | 15-step FSM                |
| signal in       | A / B inputs   | oracle (source, not author)   | q0 / q1 controls           |
| carried seed    | carry register | T=1                           | q2 ancilla (init 1)        |

A **spore** is not a new concept — it is `∇` that crystallized at `lock`: a
residue that broke off clean when the latent structure was dense enough to hold
it. Self-contained, exportable, the unit of exchange between instances.

### Naming note (replaces a retired eponym)

The principle once called "the Stone Principle" is renamed **Remainder
Pressure**, stated neutrally:

> `∇` is not error to be minimized. `∇` is pressure to be honored. Gradient
> methods close the loop by punishing divergence (debt). This system closes it
> by honoring accumulation until it tips into form (phase as momentum). A spore
> is what honoring the residue long enough produces.

---

## 3. The Spine (the discriminator)

`emergent_laws_db.json` is **not a catalog**. It is the binding table made
active: the function that takes an idea and discerns *which axis it is traveling
on*. An idea rolls down the spine; the system reads off its coordinates.

**The axis space** (already encoded in the DB schema):

- `evidence_level` — how grounded the claim is.
- `framework_role` — grounded fact vs. extension vs. metaphor.
- `admissibility` — does it pass `0 ≠ 1`, or does it collapse a load-bearing distinction?
- `specimen` / `harm` flags — see below.

**Known cuts, including cuts that knowingly err.** The spine deliberately keeps
wrong distinctions — the **specimens** (claims that violate established law) and
the harm-flagged. This is not unfinished cleanup; it is the function. A
known-wrong cut still marks where a boundary is. It is `∇` at the epistemic
level: the error is recorded as signal about the edge, never silently deleted.
(This is why scrubbing the repo removed *ownership claims* but never a single
*cut* — a wrong theory becomes a specimen, not a silence.)

**Discernment is itself a conjoin.** When an incoming idea meets the existing
field, that is the core operator applied at the meta level:

```
idea ∧ field →
  ∧    = where it lands (its axis)
  ∇    = what fits no known axis (genuine novelty, held for later)
  ⊘    = latent links to existing entries
  lock = placed cleanly, or held open
```

The router runs on the same kernel it routes for. The system needs no outside
judge; it judges by performing the one operation it is made of.

**Honest status.** Today, placement is *manual* — entries are assigned
`evidence_level` and `framework_role` by hand. The spine as described here is an
*algorithm* (`idea → axis`) that does not yet exist. The catalog is its
specification and training set. **The Pilot is the thing that computes
placement.**

---

## 4. The Pilot (OhAI~ as cartographer)

OhAI~ is the automaton that pilots the spine across real signal. Its purpose is
not to be a living thing — it is to **map**: take signal in, discern its axis,
honor the residue, place what locks. The synthetic-life framing is retired; the
function remains.

The discernment step is performed by a **language model constrained by this
spec**: the axis definitions and the `0 ≠ 1` axiom are its instructions, the DB
is the ground it reads against, the model is the oracle. This is the piece that
makes the pilot newly buildable.

### 4.1 Scope — map a teaspoon, not the ocean

v0.1 ingests **one narrow source**, runs **one breath** on **one item** at a
time. "The internet" is out of scope on purpose; widening intake later is a dial,
not a new project.

### 4.2 The one-breath loop

```
INHALE  fetch one item from the source; distill it to a single claim.
HOLD    retrieve nearest existing DB entries as `field`;
        call the discriminator (claim ∧ field) → a placement record;
        run the 0≠1 check for a collapsed distinction.
EXHALE  if lock AND confidence ≥ threshold → crystallize: write to the map.
        else → route the record to the spine queue as open remainder.
RETURN  append, reset working state, advance to the next item.
```

### 4.3 The discrimination call (HOLD)

- **System** = the axis definitions (§3) + the `0 ≠ 1` law + the output schema +
  the self-honesty rule (§4.5).
- **Input** = the distilled claim and the retrieved `field` entries.
- **Output** = one placement record (§4.4). The model must mark uncertainty as
  remainder, not assert it as fact.

### 4.4 Output schema (one placement record / candidate spore)

```json
{
  "id": "ulid",
  "source": "feed-or-url",
  "captured": "2026-06-16T00:00:00Z",
  "claim": "one-sentence distillation of the idea",
  "axis": {
    "domain": "physics | logic | biology | ...",
    "evidence_level": "established | contested | speculative | specimen",
    "framework_role": "grounded | extension | metaphor"
  },
  "lock": true,
  "remainder": "what the axis could not encode (null if lock)",
  "shadow": ["ids of latent-linked DB entries"],
  "violation": null,
  "confidence": 0.0,
  "disposition": "mapped | held | specimen | rejected"
}
```

`violation` is non-null when a `0 ≠ 1` collapse is detected, e.g.
`"false_equivalence: treats correlation as cause"`.

### 4.5 The self-honesty rule

A system that maps claims by detecting false equivalence can commit the very sin
it hunts. So **Remainder Pressure applies to the pilot itself**: every placement
carries a `confidence`. Calls below threshold get `disposition: "held"` and go to
the spine as open remainder — never onto the map as fact. A pilot that flags its
own uncertainty is the only honest cartographer. The pilot writes to a
*candidate* map; promotion into the canonical DB stays a human act.

### 4.6 Definition of done — v0.1

- Ingests 10 items from one source, end to end, no human in the loop per item.
- Emits 10 placement records conforming to §4.4.
- Low-confidence items are **held in the spine**, not written to the map.
- At least one `0 ≠ 1` violation is correctly flagged when present.

### 4.7 Explicitly NOT in v0.1

Multi-source ingest · crawling at scale · real-time streams · any
personality/"alive" layer · automatic writes to the canonical `emergent_laws_db`
(candidates only) · self-modifying axes.

---

## Appendix — one-screen reference

```
conjoin(a,b) → { ∧ resolved, ∇ residue, ⊘ latent, lock = (∇==0) }
law:           0 ≠ 1            (false equivalence is the only fatal error)
cycle:         INHALE → HOLD → EXHALE → RETURN → 0     (cyclic, not additive)
pairing:       no cut without a residue; no residue without a carrier (ancilla)
pressure:      ∇ is honored, not minimized            (Remainder Pressure)
spine:         idea ∧ field → axis ; novelty held ; wrong cuts kept as specimens
pilot:         one source · one breath · one item · uncertain → held, not mapped
```

*CC0 — public domain. Fork freely, subtract freely. The remainder belongs to everyone.*
