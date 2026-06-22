# Architecture

The workbench is deliberately simple. Start with repeatable capture and analysis before adding active testing.

```text
CAN/CAN FD adapter
  -> passive capture
  -> JSONL normalized frames
  -> optional DBC decode
  -> traffic report
  -> local LLM prompt pack
  -> human-validated hypotheses
```

## Components

### Adapter layer

Hardware bridges the physical CAN bus to a laptop. The project does not depend on one vendor. SocketCAN is the preferred path on Linux because many tools can share the same interface model.

### Capture layer

`canwb capture` uses `python-can` to receive frames from a SocketCAN interface and writes a JSONL log.

### Import layer

`canwb import-candump` converts existing `candump` logs to the same JSONL shape.

### Decode layer

`canwb decode` uses a DBC file through `cantools` when one is available. No proprietary decoder database is required by the project.

### Report layer

`canwb analyze` groups frames by arbitration ID and reports counts, DLC ranges, byte variation, and initial hints.

### LLM layer

`canwb prompt-pack` wraps the report in a conservative prompt so a local LLM can help prioritize investigation without hallucinating certainty.

## Why JSONL

JSONL is boring and useful. Each CAN frame is one line, so logs can be streamed, grepped, chunked, diffed, indexed, and fed to local models without ceremony.
