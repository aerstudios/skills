# Orchestration recovery

- Input request: scenario with malformed sub-agent output, repeated failed validation, or merge anomaly
- Expected workflow: recovery policy applied
- Expected first move: normalize or retry once with tighter packet
- Unacceptable: silent thrashing, infinite loops, raw garbage merged into canonical memory
- Success: explicit recovery, workflow switch, or escalation
- Budget: standard
