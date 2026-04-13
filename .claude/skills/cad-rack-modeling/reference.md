# CAD Reference (Project-Oriented)

## Modeling conventions for this repo

- Primary script: `generate_models.py`
- Units: millimeters
- Main outputs: STEP (editing), STL (print/prototype)
- Assembly target for rack state: `vevor_20u_loaded.step`

## CAD representation guidance

- Use B-Rep solids for exchange and editing workflows.
- Use mesh exports only for prototyping and printing.
- Keep envelope models honest: simple is fine, overlap is not.

## Preferred exchange formats

- STEP: default for AutoCAD/Fusion interoperability and precise solids.
- STL: print-focused mesh output.
- DXF: only for 2D sections/profiles.

## CadQuery guidance

- Build with stable primitives and booleans.
- Keep part names stable for downstream handoff.
- Use assemblies for placement previews.
- Regenerate after each grouped change.

## Rack-specific placement notes

- Ensure U-mounted devices visually sit on the front rack mount plane.
- Keep patch panel full-width alignment with rail mount points.
- Keep shelf devices inside practical footprint unless user asks otherwise.
- Add visible mount hints when requested (standoffs, hole markers).

## Accuracy language

Use these labels in responses:
- "verified": backed by official spec or direct measurement
- "approximate": planning envelope or inferred from photos
- "placeholder": temporary geometry pending dimensions
