from __future__ import annotations

import re
from .models import CANFrame

_CANDUMP_RE = re.compile(
    r"^(?:\((?P<ts>[0-9]+\.[0-9]+)\)\s+)?(?P<channel>[A-Za-z0-9_.:-]+)\s+"
    r"(?P<canid>[0-9A-Fa-f]+)#(?P<data>[0-9A-Fa-f]*)$"
)


def parse_candump_line(line: str) -> CANFrame | None:
    """Parse a common candump line.

    Supported examples:
      (1718990000.123456) can0 123#DEADBEEF
      can0 18FEF100#1122334455667788
    """
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    match = _CANDUMP_RE.match(line)
    if not match:
        raise ValueError(f"Unsupported candump line: {line}")

    can_id = int(match.group("canid"), 16)
    data_hex = match.group("data") or ""
    if len(data_hex) % 2:
        raise ValueError(f"Odd-length CAN data in line: {line}")

    return CANFrame(
        timestamp=float(match.group("ts")) if match.group("ts") else None,
        channel=match.group("channel"),
        arbitration_id=can_id,
        data=bytes.fromhex(data_hex),
        is_extended_id=can_id > 0x7FF,
        is_fd=False,
    )


def read_candump(path: str) -> list[CANFrame]:
    frames: list[CANFrame] = []
    with open(path, "r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            try:
                frame = parse_candump_line(line)
            except Exception as exc:
                raise ValueError(f"{path}:{line_no}: {exc}") from exc
            if frame:
                frames.append(frame)
    return frames
