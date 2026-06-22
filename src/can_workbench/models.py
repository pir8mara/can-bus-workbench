from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
import json


@dataclass(frozen=True)
class CANFrame:
    """A small, JSON-friendly representation of a CAN or CAN FD frame."""

    timestamp: float | None
    channel: str | None
    arbitration_id: int
    data: bytes
    is_extended_id: bool = False
    is_fd: bool = False

    @property
    def id_hex(self) -> str:
        width = 8 if self.is_extended_id else 3
        return f"0x{self.arbitration_id:0{width}X}"

    def to_json_obj(self) -> dict[str, Any]:
        obj = asdict(self)
        obj["arbitration_id"] = self.arbitration_id
        obj["id_hex"] = self.id_hex
        obj["data"] = self.data.hex().upper()
        obj["dlc"] = len(self.data)
        return obj

    def to_json_line(self) -> str:
        return json.dumps(self.to_json_obj(), sort_keys=True)

    @classmethod
    def from_json_obj(cls, obj: dict[str, Any]) -> "CANFrame":
        arbitration_id = obj.get("arbitration_id")
        if arbitration_id is None:
            arbitration_id = int(str(obj["id_hex"]).replace("0x", ""), 16)
        data = obj.get("data", "")
        if isinstance(data, str):
            data_bytes = bytes.fromhex(data)
        else:
            data_bytes = bytes(data)
        return cls(
            timestamp=obj.get("timestamp"),
            channel=obj.get("channel"),
            arbitration_id=int(arbitration_id),
            data=data_bytes,
            is_extended_id=bool(obj.get("is_extended_id", arbitration_id > 0x7FF)),
            is_fd=bool(obj.get("is_fd", False)),
        )


def load_jsonl(path: str) -> list[CANFrame]:
    frames: list[CANFrame] = []
    with open(path, "r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                frames.append(CANFrame.from_json_obj(json.loads(line)))
            except Exception as exc:
                raise ValueError(f"Could not parse JSONL frame at {path}:{line_no}: {exc}") from exc
    return frames


def write_jsonl(path: str, frames: list[CANFrame]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        for frame in frames:
            handle.write(frame.to_json_line() + "\n")
