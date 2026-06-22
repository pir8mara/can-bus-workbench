from __future__ import annotations


def build_prompt_pack(report_text: str) -> str:
    return f"""# Local LLM Prompt Pack: CAN Reverse Engineering

You are helping analyze a passive CAN bus capture. Do not suggest transmitting frames unless the user explicitly asks for an active testing plan and confirms they are working on an authorized bench system.

## Ground rules

- Treat this as physical-system analysis, not ordinary network traffic.
- Prefer hypotheses over declarations.
- Separate known decoded values from inferred values.
- Recommend repeatable experiments that change one input at a time.
- Do not assume a signal is speed, RPM, brake, steering, or throttle without correlation evidence.

## Analysis tasks

1. Identify arbitration IDs worth prioritizing.
2. Suggest which IDs look static, periodic, counter-like, sensor-like, or checksum-like.
3. Propose safe passive capture experiments.
4. Suggest DBC fields to create after correlation is validated.
5. List uncertainty and next evidence needed.

## Capture report

{report_text}
"""
