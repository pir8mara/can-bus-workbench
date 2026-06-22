# Safety Notes

CAN is not just data. CAN is connected to physical systems.

## Default rule

Start passive. Stay passive until you have a bench setup, authorization, and a specific test plan.

## Risks

- Sending frames can trigger physical behavior.
- Bad baud-rate or termination choices can disrupt a bus.
- Cheap non-isolated adapters can expose your laptop or the target to electrical damage.
- Vehicles and industrial systems may contain safety-critical nodes.
- Proprietary systems may have legal and contractual restrictions.

## Safer first experiments

- Capture from a disconnected bench harness.
- Use an isolated adapter.
- Use a current-limited power supply for bench electronics.
- Record one physical action at a time.
- Keep experiment notes with exact timestamps.
- Avoid transmit tests on a live vehicle or operational machine.

## Project transmit policy

Version 0.1 has no general send command. That is intentional. Active testing should be explicit, gated, documented, and preferably limited to a sacrificial bench system.
