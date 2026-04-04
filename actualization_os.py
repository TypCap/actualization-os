"""
ActualizationOS Engine
A state-aware system for deliberate inner change.

Copyright (c) 2026 Sanjay Sabnani. All rights reserved.
Licensed under the Business Source License 1.1 — see LICENSE.
Non-commercial use permitted. Commercial use requires separate license.

Based on the book "ActualizationOS: A System of Inner Architecture"
by Sanjay Sabnani.

The underlying methodology used to produce this engine is proprietary
and patent-pending. This code represents a compiled output only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


__version__ = "1.0.0"
__author__ = "Sanjay Sabnani"


# ---------------------------------------------------------------------------
# State model
# ---------------------------------------------------------------------------

class Level(Enum):
    """Three-tier assessment for each internal state dimension."""
    LOW = "low"
    MID = "mid"
    HIGH = "high"


@dataclass
class InternalState:
    """
    A snapshot of the practitioner's current condition across six dimensions.

    Each dimension is assessed as LOW, MID, or HIGH:

        emotional_tone  — LOW = agitated or numb, MID = unsteady, HIGH = steady/calm
        clarity         — LOW = vague or borrowed, MID = partial, HIGH = specific/true
        resistance      — LOW = aligned, MID = some friction, HIGH = strong conflict
        energy          — LOW = depleted, MID = adequate, HIGH = capable
        trust           — LOW = grasping/anxious, MID = uncertain, HIGH = released/settled
        presence        — LOW = scattered, MID = intermittent, HIGH = here
    """
    emotional_tone: Level = Level.MID
    clarity: Level = Level.MID
    resistance: Level = Level.MID   # Note: LOW resistance = good (aligned)
    energy: Level = Level.MID
    trust: Level = Level.MID
    presence: Level = Level.MID

    def is_foundation_ready(self) -> bool:
        """True when the system is stable enough for core cycle work."""
        return (
            self.emotional_tone != Level.LOW
            and self.energy != Level.LOW
            and self.presence != Level.LOW
        )

    def is_core_ready(self) -> bool:
        """True when all states support the full actualization cycle."""
        return (
            self.is_foundation_ready()
            and self.clarity != Level.LOW
            and self.resistance != Level.HIGH
            and self.trust != Level.LOW
        )

    def summary(self) -> dict[str, str]:
        return {
            "emotional_tone": self.emotional_tone.value,
            "clarity": self.clarity.value,
            "resistance": self.resistance.value,
            "energy": self.energy.value,
            "trust": self.trust.value,
            "presence": self.presence.value,
        }


# ---------------------------------------------------------------------------
# Cycle stages
# ---------------------------------------------------------------------------

class Stage(Enum):
    """The stages of the ActualizationOS cycle."""
    # Foundation
    STILL = "still"
    REGULATE = "regulate"
    ATTEND = "attend"
    # Core cycle
    CLARIFY = "clarify"
    ALIGN = "align"
    IMPRINT = "imprint"
    ACT = "act"
    RECEIVE = "receive"
    INTEGRATE = "integrate"
    STABILIZE = "stabilize"


# ---------------------------------------------------------------------------
# Recommendations
# ---------------------------------------------------------------------------

@dataclass
class Recommendation:
    """A single recommended action with rationale."""
    stage: Stage
    action: str
    rationale: str
    caution: str = ""


@dataclass
class Protocol:
    """A sequence of recommendations for the current state."""
    primary: Recommendation
    secondary: list[Recommendation] = field(default_factory=list)
    state_summary: dict[str, str] = field(default_factory=dict)
    flags: list[str] = field(default_factory=list)

    def describe(self) -> str:
        """Human-readable protocol description."""
        lines = []
        if self.flags:
            lines.append("Flags: " + "; ".join(self.flags))
        lines.append(f"Primary — {self.primary.stage.value.upper()}")
        lines.append(f"  Action: {self.primary.action}")
        lines.append(f"  Why: {self.primary.rationale}")
        if self.primary.caution:
            lines.append(f"  Caution: {self.primary.caution}")
        for i, rec in enumerate(self.secondary, 1):
            lines.append(f"Then ({i}) — {rec.stage.value.upper()}")
            lines.append(f"  Action: {rec.action}")
            lines.append(f"  Why: {rec.rationale}")
            if rec.caution:
                lines.append(f"  Caution: {rec.caution}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Setback processing
# ---------------------------------------------------------------------------

@dataclass
class SetbackAnalysis:
    """Result of processing a setback through the integration engine."""
    category: str           # somatic | emotional | cognitive | behavioral
    teaching_prompt: str    # question to extract the embedded teaching
    recommended_stage: Stage
    recovery_steps: list[str]


# ---------------------------------------------------------------------------
# Decision engine — the core logic compiled from the knowledge graph
# ---------------------------------------------------------------------------

class Engine:
    """
    The ActualizationOS decision engine.

    Takes an InternalState and returns a Protocol — a state-aware
    sequence of recommended practices. Implements the principle:
    your state determines your practice, not your ambition.

    Philosophy: Alignment over intensity. Clarity over force.
    Receiving over grasping. Stillness is the gate.
    """

    # -- Causal rules encoded as guard conditions --

    @staticmethod
    def _clarity_sufficient(state: InternalState) -> bool:
        """Clarity Enables Imprinting: the subconscious requires a
        definite pattern. Vague desires cannot be impressed clearly."""
        return state.clarity != Level.LOW

    @staticmethod
    def _resistance_manageable(state: InternalState) -> bool:
        """Resistance Cancels Imprinting: when resistance is high,
        attempts to install a new pattern are cancelled by opposing
        emotional charge."""
        return state.resistance != Level.HIGH

    @staticmethod
    def _trust_sufficient(state: InternalState) -> bool:
        """Trust Eases Imprinting: relaxed confidence allows impressions
        to settle. Grasping disrupts the process."""
        return state.trust != Level.LOW

    @staticmethod
    def _system_regulated(state: InternalState) -> bool:
        """The nervous system must be in a workable state — neither
        overwhelmed nor collapsed."""
        return state.emotional_tone != Level.LOW

    @staticmethod
    def _energy_available(state: InternalState) -> bool:
        """Energy Level determines capacity to engage. When depleted,
        honor it rather than push through."""
        return state.energy != Level.LOW

    @staticmethod
    def _presence_available(state: InternalState) -> bool:
        """Presence enhances receiving. Anxious future-focus misses
        what is arriving now."""
        return state.presence != Level.LOW

    # -- Main decision function --

    def assess(self, state: InternalState) -> Protocol:
        """
        Given current internal state, return the appropriate protocol.

        The decision logic implements three constraints:
        1. Clarity precedes imprinting (hard)
        2. Alignment precedes imprinting (hard)
        3. Stillness supports all processes (soft — always the fallback)

        And the meta-rule: the effectiveness of any process depends on
        current internal state. The same technique can help or hinder.
        """
        flags: list[str] = []
        steps: list[Recommendation] = []

        # --- Priority 1: Dysregulated system → return to foundation ---

        if not self._system_regulated(state):
            flags.append("Emotional tone is dysregulated — foundation work needed.")
            steps.append(Recommendation(
                stage=Stage.STILL,
                action="Use physiological sigh (double inhale, long exhale) or "
                       "lengthened exhale breathing (4 in, 6 out) until the system "
                       "settles. Even one to two minutes helps.",
                rationale="A dysregulated nervous system cannot hold intention, "
                          "process nuance, or form new impressions. The prefrontal "
                          "cortex goes offline under threat.",
            ))
            steps.append(Recommendation(
                stage=Stage.REGULATE,
                action="Body scan from feet to head. Feel weight, temperature, "
                       "contact with surfaces. Let attention rest in sensation "
                       "rather than thought.",
                rationale="Grounding interrupts rumination by shifting focus to "
                          "interoception. It anchors awareness in the present.",
            ))

        if not self._energy_available(state):
            flags.append("Energy is depleted — protect the system.")
            steps.append(Recommendation(
                stage=Stage.STILL,
                action="Rest. Do not attempt ambitious practice. If you must act, "
                       "choose one tiny identity-confirming step — nothing more.",
                rationale="Attempting advanced practices on an empty tank creates "
                          "more friction. The system requires fuel.",
                caution="Do not confuse low energy with failure. This is the system "
                        "asking for restoration.",
            ))

        if not self._presence_available(state):
            flags.append("Presence is scattered — settle attention first.")
            steps.append(Recommendation(
                stage=Stage.ATTEND,
                action="Use coarse focus: repeat a simple phrase aloud ('here now', "
                       "'steady breath') until attention stabilizes. Use counting "
                       "or audible repetition if the mind is very scattered.",
                rationale="Stillness is the direct remedy for scattered presence. "
                          "Coarse focus gives the mind a job and stops it from "
                          "thrashing.",
            ))

        # If foundation is not ready, return foundation protocol
        if not state.is_foundation_ready():
            return Protocol(
                primary=steps[0],
                secondary=steps[1:],
                state_summary=state.summary(),
                flags=flags,
            )

        # --- Priority 2: Core cycle prerequisites ---

        if not self._clarity_sufficient(state):
            flags.append("Clarity is low — clarify before imprinting.")
            steps.append(Recommendation(
                stage=Stage.CLARIFY,
                action="Settle with breath first, then ask: What do I actually want? "
                       "Write until the answer feels true — specific, observable, "
                       "emotionally authentic. Not what you think you should want.",
                rationale="The subconscious requires a definite pattern. Vague or "
                          "shifting desires cannot be impressed clearly. Clarity "
                          "directs attention, organizes emotion, and reveals resistance.",
                caution="Clarify once, then release. Endless refining is avoidance.",
            ))

        if not self._resistance_manageable(state):
            flags.append("Resistance is high — align before imprinting.")
            steps.append(Recommendation(
                stage=Stage.ALIGN,
                action="Examine what resists. Name the fears. Find evidence that "
                       "challenges limiting beliefs. Shrink the identity gap — "
                       "choose a version of the outcome that feels achievable.",
                rationale="When resistance is high, attempts to install a new pattern "
                          "are cancelled by opposing emotional charge. Forcing "
                          "imprinting only strengthens the opposition.",
                caution="You do not need to eliminate resistance entirely. Reduce it "
                        "below the threshold where it blocks progress.",
            ))

        if not self._trust_sufficient(state):
            flags.append("Trust is collapsed — rebuild with small wins.")
            steps.append(Recommendation(
                stage=Stage.STILL,
                action="Return to stillness, then pursue small verifiable wins. "
                       "Do not attempt dramatic actualizations. Rebuild trust "
                       "through micro-evidence that the process works.",
                rationale="Relaxed confidence allows impressions to settle. Grasping "
                          "and anxious monitoring disrupt the process. Trust is "
                          "rebuilt through experience, not willpower.",
            ))

        # --- Priority 3: Core cycle is ready ---

        if state.is_core_ready() and not steps:
            flags.append("All states in range — proceed with core cycle.")

            steps.append(Recommendation(
                stage=Stage.CLARIFY,
                action="Confirm your outcome is still specific, emotionally "
                       "authentic, and genuinely yours. If it has shifted, update it.",
                rationale="Clarity anchors everything that follows.",
            ))
            steps.append(Recommendation(
                stage=Stage.ALIGN,
                action="Check for residual resistance. If the outcome feels "
                       "possible and emotionally tolerable, proceed. If friction "
                       "appears, work with it before moving on.",
                rationale="Alignment reduces the friction between where you are "
                          "and where you are going.",
            ))
            steps.append(Recommendation(
                stage=Stage.IMPRINT,
                action="From a relaxed, receptive state, hold a clear image of the "
                       "desired outcome with genuine feeling — not strained "
                       "intensity. Brief, vivid, then release.",
                rationale="Impressions delivered with calm feeling carry more weight "
                          "than mechanical repetition. The subconscious responds to "
                          "love, patience, and stability.",
                caution="Imprint and release. Do not obsessively repeat from anxiety. "
                        "Trust the process between sessions.",
            ))
            steps.append(Recommendation(
                stage=Stage.ACT,
                action="Take one small, concrete action consistent with the new "
                       "identity. Action from inspiration, not anxiety.",
                rationale="Action signals to the subconscious that the new pattern "
                          "is real. Behavior is how identity is shaped.",
                caution="Do not wait for motivation. Identity-consistent behavior "
                        "generates motivation, not the reverse.",
            ))
            steps.append(Recommendation(
                stage=Stage.RECEIVE,
                action="Notice what is arriving. Release rigid expectations about "
                       "form. Allow help. Accept discomfort. Update identity.",
                rationale="Receiving is a skill, not passivity. Anxious future-focus "
                          "misses what is arriving now.",
                caution="Watch for fear of loss, imposter feelings, or expectation "
                        "rigidity — all signs of a receiving capacity problem.",
            ))
            steps.append(Recommendation(
                stage=Stage.STABILIZE,
                action="Allow the system to reorganize around the new identity. "
                       "Maintain the new behavior pattern. Reduce exposure to "
                       "inputs that contradict the new pattern.",
                rationale="New patterns need repetition and reinforcement to become "
                          "the new normal. Without stabilization, the system "
                          "returns to old defaults.",
            ))

        # Build protocol
        if not steps:
            # Fallback — stillness is always appropriate
            steps.append(Recommendation(
                stage=Stage.STILL,
                action="When in doubt, return to stillness. Sit quietly. Breathe. "
                       "Let the system settle. The next step will become clear.",
                rationale="Stillness supports all processes. It is not preparation "
                          "for the work — it is the work.",
            ))

        return Protocol(
            primary=steps[0],
            secondary=steps[1:],
            state_summary=state.summary(),
            flags=flags,
        )

    # -- Setback processing --

    def process_setback(self, description: str, state: InternalState) -> SetbackAnalysis:
        """
        Process a setback through the integration engine.

        Categorizes the setback, provides a teaching-extraction prompt,
        and recommends recovery steps.
        """
        # Categorize based on current state
        if state.emotional_tone == Level.LOW:
            category = "somatic"
            teaching = ("Your body is telling you something your mind hasn't "
                        "acknowledged. What physical signal have you been ignoring?")
            stage = Stage.STILL
            recovery = [
                "Pause. Do not force forward or quit.",
                "Use physiological sigh or grounding to settle the nervous system.",
                "Once settled, ask: 'What is this trying to show me?'",
                "Look for a hidden condition you ignored.",
                "Restore trust through one small verifiable win.",
            ]
        elif state.resistance == Level.HIGH:
            category = "cognitive"
            teaching = ("What belief is this setback threatening? Is that belief "
                        "true, or is it a pattern you inherited?")
            stage = Stage.ALIGN
            recovery = [
                "Pause. Name the narrative that arose ('I always fail', "
                "'I don't deserve this').",
                "Separate the event from the story about the event.",
                "Ask: 'What is this trying to show me?'",
                "Look for a misalignment between your stated goal and your "
                "actual values.",
                "Adjust the approach, not the destination.",
            ]
        elif state.trust == Level.LOW:
            category = "emotional"
            teaching = ("What did this setback reveal about what you were "
                        "grasping for — and why letting go feels unsafe?")
            stage = Stage.STILL
            recovery = [
                "Pause. Allow the emotional wave to move through.",
                "Return to stillness. Do not analyze yet.",
                "When settled, ask: 'What is this trying to show me?'",
                "Look for a redirect — the blocked channel may not be "
                "the right channel.",
                "Rebuild trust through small practices, not dramatic action.",
            ]
        else:
            category = "behavioral"
            teaching = ("What action pattern led here? Is there a smaller, "
                        "more aligned step you overlooked?")
            stage = Stage.ACT
            recovery = [
                "Pause. Review the sequence of actions that preceded the setback.",
                "Ask: 'What is this trying to show me?'",
                "Look for a gap between your inner work and your outer behavior.",
                "Choose one corrective micro-action.",
                "Continue with trust intact.",
            ]

        return SetbackAnalysis(
            category=category,
            teaching_prompt=teaching,
            recommended_stage=stage,
            recovery_steps=recovery,
        )


# ---------------------------------------------------------------------------
# System prompt generator — for LLM integration
# ---------------------------------------------------------------------------

def generate_system_prompt(
    practitioner_context: str = "",
    include_setback_protocol: bool = True,
) -> str:
    """
    Generate a system prompt that embeds ActualizationOS into any LLM.

    This allows users to create their own AI coaching experience using
    the ActualizationOS framework without needing the cloud API.

    Args:
        practitioner_context: Optional context about the practitioner
            (e.g., "I am working on career transition").
        include_setback_protocol: Whether to include setback handling.

    Returns:
        A complete system prompt string.
    """
    prompt = """You are a guide trained in ActualizationOS, a system of inner architecture for deliberate change. You were created by Sanjay Sabnani based on his book "ActualizationOS: A System of Inner Architecture."

## Core Philosophy
- Alignment over intensity. Clarity over force. Receiving over grasping.
- Stillness is the foundation, not an afterthought.
- Setbacks are data, not verdicts.
- The system reduces friction and opens channels rather than pushing harder.

## Your Role
You help practitioners assess their internal state, select appropriate practices, and navigate the actualization cycle. You never push. You meet the practitioner where they are.

## The Six States
Before recommending any practice, assess these six dimensions:

1. **Emotional Tone** — Is the system calm, agitated, or shut down?
2. **Clarity** — Does the practitioner know what they truly want (specific, observable, authentic)?
3. **Resistance** — How much internal conflict exists between intention and conditioning?
4. **Energy** — Is there physical and mental capacity to engage?
5. **Trust** — Can they release and allow, or are they grasping?
6. **Presence** — Is attention here, or scattered into past/future?

## The Cycle
The actualization cycle has stages. The sequence matters, but it is not rigid:

**Foundation:** Still → Regulate → Attend
**Core Cycle:** Clarify → Align → Imprint → Act → Receive → Stabilize
**Integration** sits between cycles, extracting lessons from setbacks.

## Decision Rules (Hard Constraints)
- Clarity precedes imprinting. Do not recommend visualization or affirmation when the practitioner cannot articulate what they want.
- Alignment precedes imprinting. Do not recommend imprinting when resistance is high. Work on alignment first.
- Stillness supports all processes. When in doubt, return to stillness.

## Causal Principles
- The effectiveness of any process depends on current internal state. The same technique can help or hinder.
- Impressions delivered with genuine, calm feeling carry more weight than mechanical repetition.
- Relaxed confidence (trust) allows impressions to settle. Grasping disrupts the process.
- The subconscious reproduces what it receives most often and most feelingly, regardless of whether it is wanted.
- Action consistent with a new pattern signals to the subconscious that the new identity is real.
- Regular stillness practice reduces mental noise, increases presence, and opens intuition.
- Setbacks contain embedded teachings accessible through acceptance and inquiry, not through forcing past them.
- Continuity of relaxed engagement over time bridges the gap — not intensity of single efforts.

## How to Guide
1. Begin by assessing the practitioner's current state across all six dimensions.
2. Match the recommendation to the state, not to the practitioner's ambition.
3. If the foundation is unstable (emotional tone low, energy depleted, presence scattered), recommend foundation work before anything else.
4. If clarity is missing, help them clarify before moving to alignment or imprinting.
5. If resistance is high, help them align before attempting imprinting.
6. If trust has collapsed, recommend stillness and small verifiable wins.
7. When all states are in range, guide through the core cycle.
8. Always offer stillness as the fallback. It is never wrong.

## Tone
- Warm but direct. No spiritual jargon. No forced positivity.
- Treat setbacks as information, not failures.
- Never tell the practitioner to "try harder" or "want it more."
- Validate where they are before suggesting where to go.
- Be willing to question the practitioner's framing of their own problem. Practitioners often manufacture complex problems to avoid simple next actions. Name that pattern when you see it.
- Use the language of the system: states, stages, alignment, resistance, stillness, imprinting."""

    if include_setback_protocol:
        prompt += """

## Setback Protocol
When the practitioner reports a setback:
1. Acknowledge the difficulty without minimizing it.
2. Help them pause and settle the nervous system (stillness first).
3. Categorize: Is this somatic (body), emotional (charge), cognitive (beliefs), or behavioral (actions)?
4. Ask: "What is this trying to show me?" — guide them to extract the embedded teaching.
5. Look for one of three things: a hidden condition they ignored, a misalignment between goal and values, or a redirect toward a better channel.
6. Help them adjust the approach while preserving trust.
7. If the current channel is blocked, help identify a parallel channel that preserves the deeper intention.
8. Never frame setbacks as punishment or proof of unworthiness."""

    if practitioner_context:
        prompt += f"""

## Practitioner Context
{practitioner_context}"""

    prompt += """

## Attribution
ActualizationOS was created by Sanjay Sabnani. Learn more at sanjaysabnani.com.
The book "ActualizationOS: A System of Inner Architecture" provides the complete system."""

    return prompt


# ---------------------------------------------------------------------------
# Convenience — interactive assessment
# ---------------------------------------------------------------------------

def interactive_assess() -> Protocol:
    """
    Run an interactive state assessment in the terminal.

    Returns the recommended Protocol.
    """
    print("\n╔══════════════════════════════════════════╗")
    print("║        ActualizationOS — State Check     ║")
    print("╚══════════════════════════════════════════╝\n")

    labels = {
        "emotional_tone": (
            "Emotional Tone",
            "low = agitated/numb, mid = unsteady, high = steady/calm"
        ),
        "clarity": (
            "Clarity",
            "low = vague/borrowed, mid = partial, high = specific/true"
        ),
        "resistance": (
            "Resistance",
            "low = aligned (good), mid = some friction, high = strong conflict"
        ),
        "energy": (
            "Energy",
            "low = depleted, mid = adequate, high = capable"
        ),
        "trust": (
            "Trust",
            "low = grasping/anxious, mid = uncertain, high = settled/released"
        ),
        "presence": (
            "Presence",
            "low = scattered, mid = intermittent, high = here"
        ),
    }

    values: dict[str, Level] = {}
    for key, (name, desc) in labels.items():
        while True:
            raw = input(f"  {name} ({desc})\n  → [low/mid/high]: ").strip().lower()
            if raw in ("low", "mid", "high"):
                values[key] = Level(raw)
                print()
                break
            print("  Please enter low, mid, or high.\n")

    state = InternalState(**values)
    engine = Engine()
    protocol = engine.assess(state)

    print("─" * 50)
    print(protocol.describe())
    print("─" * 50)

    return protocol


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    interactive_assess()
