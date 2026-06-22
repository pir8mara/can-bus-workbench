# Hardware Notes

## Adapter features worth caring about

| Feature | Why it matters |
|---|---|
| CAN FD support | Needed for newer systems using larger/faster CAN FD frames. |
| Galvanic isolation | Helps protect laptop and target from ground/power weirdness. |
| Listen-only mode | Reduces risk of accidentally disturbing a bus. |
| SocketCAN support | Makes Linux tooling much easier. |
| Timestamp quality | Matters when correlating events and comparing buses. |
| Dual channels | Useful when comparing two buses or gateway behavior. |
| Termination control | Useful on a bench, dangerous if misunderstood on an existing bus. |

## Practical recommendation

For learning, start cheap but isolated if possible. For client work or expensive equipment, use professional hardware. The cheapest adapter that works on a desk may be the most expensive adapter if it lets the magic smoke out of something important.
