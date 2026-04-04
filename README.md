# ActualizationOS Engine

A state-aware system for deliberate inner change, compiled from the knowledge architecture described in **ActualizationOS: A System of Inner Architecture** by Sanjay Sabnani.

## What This Is

ActualizationOS is an operating system for the mind. It provides a diagnostic framework (six internal states), a cycle of practices (ten stages), and a decision engine that matches your practice to your current condition — not your ambition.

This engine is a compiled, executable version of the system. It can be used standalone, integrated into applications, or dropped into any LLM as a system prompt for AI-assisted coaching.

**Philosophy:** Alignment over intensity. Clarity over force. Receiving over grasping. Stillness is the gate.

## Quick Start

### Web App (No Installation)

Open `index.html` in any browser. Two tabs:

- **State Assessment** — rate each of the six states, get your protocol instantly.
- **LLM System Prompt** — generate a complete system prompt, copy it, paste it into Claude, ChatGPT, or any LLM to create your own ActualizationOS coach.

No server, no dependencies, no account. Works offline. Also works hosted on GitHub Pages.

### As a Python Library

```python
from actualization_os import InternalState, Level, Engine

# Assess your current state
state = InternalState(
    emotional_tone=Level.LOW,   # agitated
    clarity=Level.MID,          # partial
    resistance=Level.HIGH,      # strong conflict
    energy=Level.MID,           # adequate
    trust=Level.LOW,            # grasping
    presence=Level.LOW,         # scattered
)

# Get your protocol
engine = Engine()
protocol = engine.assess(state)
print(protocol.describe())
```

### Interactive Terminal Assessment

```bash
python actualization_os.py
```

### As an LLM System Prompt (Python)

```python
from actualization_os import generate_system_prompt

# Generate a system prompt for any LLM (Claude, GPT, etc.)
prompt = generate_system_prompt(
    practitioner_context="I am navigating a career transition and feeling stuck."
)

# Use this as the system prompt in your LLM API call
print(prompt)
```

### Process a Setback

```python
from actualization_os import Engine, InternalState, Level

engine = Engine()
state = InternalState(
    emotional_tone=Level.LOW,
    trust=Level.LOW,
    resistance=Level.HIGH,
    clarity=Level.MID,
    energy=Level.MID,
    presence=Level.LOW,
)

analysis = engine.process_setback(
    description="I was passed over for the promotion I spent months working toward.",
    state=state,
)

print(f"Category: {analysis.category}")
print(f"Teaching prompt: {analysis.teaching_prompt}")
print(f"Recovery steps:")
for step in analysis.recovery_steps:
    print(f"  - {step}")
```

## The Six States

Before any practice, the engine assesses six dimensions:

| State | Low End | High End |
|-------|---------|----------|
| Emotional Tone | Agitated / Numb | Steady / Calm |
| Clarity | Vague / Borrowed | Specific / True |
| Resistance | High Conflict | Aligned |
| Energy | Depleted | Capable |
| Trust | Grasping / Anxious | Released / Settled |
| Presence | Scattered | Here |

Your state determines your practice. If the foundation is unstable, the engine sends you back to stillness and regulation — not forward into techniques that require a stable system.

## The Cycle

**Foundation:** Still → Regulate → Attend  
**Core Cycle:** Clarify → Align → Imprint → Act → Receive → Stabilize  
**Integration** sits between cycles, extracting lessons from setbacks.

The cycle is not a rigid staircase. You will move forward, return, recalibrate, and begin again. The engine handles this logic for you.

## Hard Constraints

The engine enforces three rules that cannot be overridden:

1. **Clarity precedes imprinting.** You cannot impress a vague desire on the subconscious.
2. **Alignment precedes imprinting.** High resistance cancels or reverses imprinting.
3. **Stillness supports all processes.** When in doubt, return to stillness.

## Integration with LLMs

The easiest path: open `index.html`, switch to the "LLM System Prompt" tab, copy, and paste into any LLM.

For programmatic use, the `generate_system_prompt()` function in Python produces the same prompt:

```python
from actualization_os import generate_system_prompt

prompt = generate_system_prompt()
# Use with Claude, GPT, Llama, Mistral, or any instruction-following model
```

## What's In This Repo

| File | For | Description |
|------|-----|-------------|
| `index.html` | Everyone | Browser app — state assessment + system prompt generator |
| `MANUAL.md` | Practitioners | Complete operating reference — states, protocols, causal rules |
| `actualization_os.py` | Developers | Python engine — importable library with decision engine |
| `LICENSE` | Legal | Business Source License 1.1 |

## Zero Dependencies

This engine is a single Python file with no external dependencies. It requires Python 3.10+ (for type syntax).

## Operating Manual

For the complete practitioner reference — the six states, decision engine, hard constraints, causal rules, setback protocol, and protocol library — see [MANUAL.md](MANUAL.md).

## License

**Business Source License 1.1** — Non-commercial use is free and unrestricted. Commercial use (selling, licensing for a fee, or including in revenue-generating products/services) requires a separate license from the author.

See [LICENSE](LICENSE) for full terms.

Contact: sanjay@crowdgather.com

## Attribution

ActualizationOS was created by **Sanjay Sabnani**.

- Book: *ActualizationOS: A System of Inner Architecture*
- Web: [sanjaysabnani.com](https://sanjaysabnani.com)

The underlying methodology used to produce this engine is proprietary and patent-pending. This code represents a compiled output only.
