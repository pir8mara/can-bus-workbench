# Decoder Strategy

Vendors sell decoder packs because raw CAN is not self-describing.

A raw frame might look like this:

```text
0x123  00 10 7F 00 AA 55 01 00
```

A DBC file tells software how to interpret it:

```text
message 0x123 = ExampleStatus
byte 2 bit 0..7 = temperature_raw
scale = 0.5
offset = -40
unit = C
```

## Strategy

1. Use public or authorized DBC files where available.
2. Treat paid decoders as convenience, not magic.
3. Assume OEM-proprietary signals will still need reverse engineering.
4. Keep every inferred signal labeled as inferred until validated.
5. Store your own DBC fragments as you confirm fields.

## Good signal evidence

A candidate signal becomes more credible when:

- It changes only when the physical input changes.
- It changes in the expected direction.
- It repeats across captures.
- It scales plausibly.
- It survives ignition cycles or resets.
- It does not break when nearby unrelated inputs change.

## Bad signal evidence

Weak evidence includes:

- One capture only.
- Many things changed at once.
- The signal looks plausible but has no experiment label.
- The value is from an LLM guess.
- The value matches wishful thinking. The CAN bus does not care about our feelings.
