# Update Policy

This document defines how bootstrap handles missing, partial, current, and outdated orchestration scaffolds.

## Classification

Bootstrap should classify the target repo state as one of:

- `missing`
- `partial`
- `current`
- `outdated`

## Missing

If the scaffold is missing:

1. explain what will be created
2. ask once before making repo-visible changes
3. create the minimal scaffold only
4. report exactly what was created

## Partial

If the scaffold is partial:

1. repair conservatively in place
2. create only missing required pieces
3. preserve existing curated files
4. ask before overwriting, renaming, or migrating anything

## Current

If the scaffold is current:

- do nothing
- report that the repo already satisfies the minimum scaffold contract

## Outdated

If the scaffold is outdated:

1. warn briefly
2. explain the available update
3. update only on confirmation
4. preserve local overlays and curated artifacts

## Drift

If managed files appear heavily drifted:

- do not overwrite silently
- warn that manual review is needed
- preserve user changes

## Non-goals

Bootstrap is not a free-form migration engine. Its job is safe install/repair/update of the minimal scaffold.
