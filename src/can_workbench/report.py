from __future__ import annotations

from collections import Counter, defaultdict
from statistics import mean
from .models import CANFrame


def _byte_variation(values: list[bytes]) -> list[int]:
    max_len = max((len(v) for v in values), default=0)
    result: list[int] = []
    for idx in range(max_len):
        seen = {v[idx] for v in values if len(v) > idx}
        result.append(len(seen))
    return result


def build_report(frames: list[CANFrame]) -> str:
    by_id: dict[int, list[CANFrame]] = defaultdict(list)
    for frame in frames:
        by_id[frame.arbitration_id].append(frame)

    lines: list[str] = []
    lines.append("# CAN Capture Report")
    lines.append("")
    lines.append(f"Total frames: {len(frames)}")
    lines.append(f"Unique arbitration IDs: {len(by_id)}")
    lines.append("")

    if not frames:
        lines.append("No frames found.")
        return "\n".join(lines) + "\n"

    counts = Counter(frame.arbitration_id for frame in frames)
    lines.append("## Arbitration ID summary")
    lines.append("")
    lines.append("| ID | Frames | DLC min/max | Avg DLC | Byte variation | First data | Notes |")
    lines.append("|---|---:|---|---:|---|---|---|")

    for arb_id, count in counts.most_common():
        id_frames = by_id[arb_id]
        payloads = [f.data for f in id_frames]
        dlcs = [len(p) for p in payloads]
        variation = _byte_variation(payloads)
        first_data = payloads[0].hex().upper()
        note_parts: list[str] = []
        if count == 1:
            note_parts.append("single observation")
        if variation and max(variation) == 1:
            note_parts.append("static payload")
        if variation and max(variation) > 16:
            note_parts.append("high byte movement")
        notes = ", ".join(note_parts) or "observe with correlated physical input"
        lines.append(
            f"| 0x{arb_id:X} | {count} | {min(dlcs)}/{max(dlcs)} | {mean(dlcs):.1f} | "
            f"{variation} | `{first_data}` | {notes} |"
        )

    lines.append("")
    lines.append("## Reverse-engineering hints")
    lines.append("")
    lines.append("- Static payloads may be status, heartbeat, mode, padding, or simply not exercised in this capture.")
    lines.append("- Bytes with small changes may be counters, flags, rolling state, or low-resolution sensors.")
    lines.append("- Bytes with large continuous changes are candidates for speed, RPM, temperature, pressure, position, or checksums.")
    lines.append("- Repeat the capture while changing one physical input at a time. Label the experiment immediately. Future-you is not trustworthy enough to remember it later.")
    return "\n".join(lines) + "\n"
