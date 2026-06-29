# Transcripts and Metrics

This document defines:

- what runtime transcript data the orchestration system captures
- when richer debug capture is enabled
- which operational metrics matter for evaluating the system
- how transcript and metric data should be used without polluting canonical task memory

## Core principles

### 1. Canonical memory and transcripts are different things

Canonical task memory lives in:

- `active.json`
- `history.jsonl`
- `closure.json`
- `archive/`

Transcripts are a compact operational record of orchestration behavior.

### 2. Capture compactly by default

Default transcript capture should be:

- structured
- compact
- summary-first
- cheap to persist
- useful for later debugging and eval promotion

Do not capture full raw prompt/response payloads by default.

### 3. Increase detail only around anomalies

Fuller capture is for debugging and recovery, not normal operation.

## Transcript storage

Per task:

```text
.agents/state/tasks/tsk_001/
  transcript.jsonl
```

## Default transcript event model

Each transcript entry should be one JSON object per line.

Recommended baseline fields:

- `timestamp`
- `actor`
- `eventType`
- `taskId`
- `clusterId`
- `summary`
- `relatedIds`
- `debugPayloadRef`

Suggested event types:

- `task-created`
- `task-resolved`
- `workflow-selected`
- `clarification-requested`
- `clarification-resolved`
- `packet-dispatched`
- `subagent-response`
- `skill-invoked`
- `skill-artifact-translated`
- `delta-merged`
- `validation-result`
- `operational-fact-discovered`
- `operational-fact-superseded`
- `compaction-run`
- `debug-mode-enabled`
- `debug-mode-disabled`
- `escalation`
- `bootstrap-invoked`
- `bootstrap-result`

## Debug mode

Debug mode enables richer capture for a bounded period.

### Debug mode triggers

Debug mode may be enabled:

- explicitly by user request
- automatically after orchestration anomalies

Automatic triggers include:

- malformed sub-agent output
- state merge conflict
- revision or lock anomaly
- repeated failed fix/validate loops
- repeated packet misfit
- unexpected workflow recovery path
- contradictory validation that meaningfully changes the branch

### Debug mode scope

Recommended default:

- next 1–2 sub-agent turns, or
- until the current anomaly/cluster is resolved

Then revert to compact summary mode unless the user keeps debug mode enabled.

## Primary operational metrics

Track at least:

1. task success rate
2. median delegations per successful task
3. clarification rate
4. unnecessary clarification rate
5. fix/validate loop count
6. escalation rate
7. memory growth per task
8. debug mode incidence
9. budget adherence
10. workflow selection accuracy

Useful secondary metrics include how often operational facts prevented repeated failed command attempts or improved command/tool selection within a task.

Metrics should always be interpreted under the system priority order:

1. correctness
2. memory coherence
3. token efficiency
4. autonomy
5. convenience

## Promotion of transcripts into evals

Transcripts are runtime artifacts by default.

A transcript or part of one may be promoted into a committed eval/golden artifact only when:

- it captures a representative success/failure mode
- it is redacted and curated
- it tests a behavior the team wants to preserve or improve

Do not automatically commit raw transcripts.
