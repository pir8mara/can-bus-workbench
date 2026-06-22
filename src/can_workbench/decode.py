from __future__ import annotations

import csv
from typing import Any
from .models import CANFrame


def decode_with_dbc(frames: list[CANFrame], dbc_path: str, output_csv: str) -> tuple[int, int]:
    """Decode frames using cantools and write a flat CSV.

    Returns `(decoded_count, unknown_count)`.
    """
    import cantools  # optional at runtime

    db = cantools.database.load_file(dbc_path)
    decoded_rows: list[dict[str, Any]] = []
    unknown = 0

    for frame in frames:
        try:
            message = db.get_message_by_frame_id(frame.arbitration_id)
            decoded = message.decode(frame.data, decode_choices=True, scaling=True)
        except Exception:
            unknown += 1
            continue
        row: dict[str, Any] = {
            "timestamp": frame.timestamp,
            "channel": frame.channel,
            "id_hex": frame.id_hex,
            "message": message.name,
        }
        row.update(decoded)
        decoded_rows.append(row)

    fieldnames: list[str] = []
    for row in decoded_rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    with open(output_csv, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames or ["timestamp", "channel", "id_hex", "message"])
        writer.writeheader()
        writer.writerows(decoded_rows)

    return len(decoded_rows), unknown
