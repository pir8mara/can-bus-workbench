# Workflow

## 1. Set up interface

Linux SocketCAN example:

```bash
sudo ip link set can0 down || true
sudo ip link set can0 up type can bitrate 500000
ip -details link show can0
```

For CAN FD, the setup depends on adapter support and target bitrate. Example shape:

```bash
sudo ip link set can0 up type can bitrate 500000 dbitrate 2000000 fd on
```

## 2. Capture passively

```bash
canwb capture --channel can0 --output logs/baseline.jsonl --duration 60
```

## 3. Analyze

```bash
canwb analyze logs/baseline.jsonl --output reports/baseline.md
```

## 4. Change one thing

Examples:

- ignition off vs accessory mode
- door closed vs open
- lights off vs on
- button untouched vs pressed
- bench sensor at low/mid/high position

Do not change five things and then pretend the capture will explain itself. That way lies goblin math.

## 5. Decode when possible

```bash
canwb decode logs/baseline.jsonl --dbc my_vehicle.dbc --output reports/baseline_decoded.csv
```

## 6. Use a local LLM carefully

```bash
canwb prompt-pack reports/baseline.md --output prompts/baseline_prompt.md
```

Then paste the prompt into a local model or use it as input for a local agent. The model should help create hypotheses, not invent certainty.
