# CAN Bus Workbench

A local-first CAN/CAN FD reverse-engineering starter kit for laptop-based analysis.

This project avoids vendor decoder lock-in by using open file formats, local logs, DBC files when available, and repeatable analysis notes.

## What this does

- Capture CAN frames from SocketCAN-compatible interfaces.
- Import existing `candump` text logs.
- Store captures as JSONL for easy scripting and LLM-assisted review.
- Decode frames with DBC files when available.
- Generate a basic traffic report by arbitration ID.
- Create a prompt pack for a local LLM so the model can help reason about signals without needing live bus access.
- Keep transmit functionality out of the default path. The first version is deliberately listen-first.

## What this does not do yet

- It does not brute-force UDS services.
- It does not transmit frames by default.
- It does not bypass vehicle security.
- It does not ship proprietary decoder databases.
- It does not pretend raw CAN bytes magically become truth without validation.

## Suggested hardware tiers

| Tier | Examples | Notes |
|---|---|---|
| Low-cost lab | CANable 2.0, MKS CANable clones, ODrive USB-CAN | Fine for bench learning. Be cautious around expensive systems. |
| Safer hobby/prototype | Isolated CANable Pro, Entree V2, isolated USB-CAN FD adapters | Better for real devices and CAN FD experiments. |
| Professional | PEAK PCAN-USB FD, Kvaser Leaf, Intrepid ValueCAN | Better drivers, isolation, timestamping, support, and less weirdness. |

## Requirements

Recommended environment:

- Linux, because SocketCAN is the cleanest open CAN interface.
- Python 3.11 or newer.
- A CAN/CAN FD adapter supported by SocketCAN, slcan, vendor tools, or a bridge mode compatible with `python-can`.

Optional Python dependencies are listed in `requirements.txt`.

## Quick start

From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Analyze the sample log:

```bash
canwb import-candump examples/sample_candump.log --output examples/sample_capture.jsonl
canwb analyze examples/sample_capture.jsonl --output examples/sample_report.md
canwb prompt-pack examples/sample_report.md --output examples/sample_prompt_pack.md
```

Decode with a DBC file:

```bash
canwb decode examples/sample_capture.jsonl --dbc path/to/vehicle.dbc --output decoded.csv
```

Capture from SocketCAN:

```bash
sudo ip link set can0 up type can bitrate 500000
canwb capture --channel can0 --output logs/capture.jsonl --duration 30
```

## Project layout

```text
can-bus-workbench/
  README.md
  pyproject.toml
  requirements.txt
  src/can_workbench/
    cli.py
    capture.py
    candump.py
    decode.py
    report.py
    llm.py
    models.py
  docs/
    architecture.md
    safety.md
    workflow.md
    decoder-strategy.md
    hardware-notes.md
    roadmap.md
  examples/
    sample_candump.log
    sample_vehicle.dbc
  tests/
    test_candump.py
    test_report.py
  scripts/
    setup_socketcan.sh
```

## Core idea

The adapter is just the door. The real value is the workflow:

```text
CAN interface
  -> local capture
  -> open log format
  -> optional DBC decode
  -> traffic analysis
  -> human notes
  -> local LLM prompt pack
  -> repeatable reverse-engineering hypotheses
```

## Safety posture

This project starts with passive capture and offline analysis because that is the least stupid starting point. Transmitting CAN frames on a real vehicle or industrial system can cause physical behavior. Treat that like you are touching machinery, not like you are sending harmless packets on a toy network.

See `docs/safety.md` before doing anything spicy.
