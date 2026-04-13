---
name: cad-rack-modeling
description: Build or refine parametric CAD rack assemblies with CadQuery, including U-mount alignment, collision reduction, and STEP/STL exports. Use for rack layout, device placement, and fit-check updates.
argument-hint: [goal-or-part]
allowed-tools: Read Glob Grep Bash(ls *) Bash(python *) Bash(pwsh *)
---

# CAD Rack Modeling Skill

Use this skill for practical mechanical planning in this repo:
- rack frame and U positions
- shelf and device placement
- mount realism (rails, ears, standoffs, hole patterns)
- collision reduction
- export regeneration for CAD tools

Arguments: `$ARGUMENTS`

## Required operating rules

1. Keep the model parametric. Update constants and placement values, not random geometry hacks.
2. Preserve unit consistency in millimeters.
3. Preserve axis clarity for this project. Treat Fusion-import orientation checks as required.
4. Never claim exact physical accuracy unless dimensions were verified from official specs or measured values.
5. After every geometry update, regenerate exports and verify that generation succeeds.

## Workflow

1. Scope
- Restate the requested layout change in one short sentence.
- Identify impacted parts in `generate_models.py`.

2. Inspect
- Read only relevant sections.
- Keep edits localized.

3. Update model
- Prefer these update points:
  - `RACK` constants
  - `make_vevor_rack()` for frame, rails, hole patterns, casters
  - `make_homelab_layout()` for shelves and device placement
- For mount realism, align device front faces to rack front mount plane.
- For shelf realism, keep objects within shelf footprint unless user explicitly wants overhang.

4. Collision pass
- Check likely overlap clusters:
  - bottom shelf: laptop, NAS, Time Capsule
  - upper shelf: Switch dock, Sky box, Apple TV, Wii, Hue bridge, PSUs
  - U gear: patch panel, UDM Pro, USP-RPS, Raspberry Pi
- Resolve overlap by shifting depth/width first, then size envelopes if still required.

5. Regenerate exports
- Run the generator using project venv Python.
- Confirm key files update in `exports/`.

6. Report
- List changed files.
- List assumptions that still need real-world measurements.
- Highlight any remaining known fit uncertainty.

## Verification checklist (must pass)

- `generate_models.py` runs without errors.
- `exports/vevor_20u_loaded.step` is regenerated.
- `exports/vevor_20u_rack.step` is regenerated.
- U-mounted devices are visually aligned to front mount plane.
- No obvious object intersections in requested problem areas.

Use `checklist.md` before final response.

## Output format for responses

- What was adjusted
- Files changed
- What was regenerated
- Remaining assumptions

## Supporting files

- `reference.md`: CAD conventions, formats, and CadQuery-specific guidance
- `examples.md`: common adjustment patterns for this rack project
- `checklist.md`: final pre-response QA list
