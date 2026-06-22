from __future__ import annotations

import time
from .models import CANFrame, write_jsonl


def capture_socketcan(channel: str, output: str, duration: float | None = None) -> int:
    """Capture CAN frames through python-can and write JSONL.

    This intentionally receives only. Transmission support belongs behind an explicit safety gate.
    """
    import can  # optional at runtime

    frames: list[CANFrame] = []
    deadline = time.time() + duration if duration else None

    with can.Bus(interface="socketcan", channel=channel) as bus:
        while True:
            if deadline and time.time() >= deadline:
                break
            msg = bus.recv(timeout=0.5)
            if msg is None:
                continue
            frames.append(
                CANFrame(
                    timestamp=float(msg.timestamp) if msg.timestamp else None,
                    channel=channel,
                    arbitration_id=int(msg.arbitration_id),
                    data=bytes(msg.data),
                    is_extended_id=bool(msg.is_extended_id),
                    is_fd=bool(getattr(msg, "is_fd", False)),
                )
            )

    write_jsonl(output, frames)
    return len(frames)
