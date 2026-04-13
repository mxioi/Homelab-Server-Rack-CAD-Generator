# CAD Skills Guide for LLMs

This document is a practical skill file for LLM agents working on CAD tasks, especially script-driven CAD with Python and CadQuery.

## 1) What CAD is

CAD (Computer-Aided Design) is software-driven geometric modeling used to create, edit, analyze, and exchange technical designs.

Core CAD goals:
- define geometry precisely
- preserve design intent (parametric constraints)
- support manufacturing and documentation
- exchange models between tools (neutral and native formats)

In practice, CAD models are usually one or more of:
- **wireframe** (edges only)
- **surface** (faces without guaranteed volume)
- **solid** (watertight volumetric geometry)
- **mesh** (triangle/polygon approximation)

## 2) How CAD geometry is represented

Major representations and when to use them:

1. **CSG (Constructive Solid Geometry)**
- Build shapes by combining primitives (box, cylinder, sphere) with booleans (union/cut/intersect).
- Great for scriptability and parametric logic.

2. **B-Rep (Boundary Representation)**
- Solids defined by topological entities: vertex, edge, wire, face, shell, solid.
- Used by most mechanical CAD kernels for precise solids.
- Typically backed by analytic/NURBS geometry.

3. **NURBS / B-Splines**
- Smooth curves/surfaces for freeform and high-quality precision geometry.

4. **Mesh**
- Triangulated approximation of geometry (STL/OBJ/3MF).
- Great for visualization/3D printing, weaker for CAD edits.

## 3) Common CAD toolset (operations)

Essential modeling operations:
- sketch primitives: line, arc, circle, rectangle, polygon, spline
- constraints: coincident, parallel, perpendicular, tangent, equal, concentric
- dimensions: driving parameters for size/position
- feature ops: extrude, revolve, sweep, loft
- boolean ops: union/add, cut/subtract, intersect/common
- detail ops: fillet, chamfer, shell, draft
- repetition ops: linear/circular pattern, mirror
- assembly ops: placement/mates, interference checks, exploded views

For LLMs: prefer robust primitives and booleans first, then add detail features incrementally.

## 4) CAD kernels and "what CAD is made of"

Most CAD apps are built on a geometry kernel. The kernel provides math + topology + boolean + meshing engines.

Examples:
- **OpenCascade (OCCT)**: open-source kernel, strong B-Rep/NURBS/topology stack
- **Parasolid** (commercial)
- **ACIS** (commercial)

CadQuery uses **OCP** (Python bindings) over **OpenCascade**, so CadQuery scripts are a high-level Python layer over OCCT capabilities.

## 5) CAD file formats (practical matrix)

### Native/authoring formats
- **DWG**: AutoCAD native format, broad drafting/CAD ecosystem support.
- **DXF**: exchange-friendly text/binary format for 2D/3D data (very common for profiles and drawings).

### Neutral precise CAD exchange
- **STEP (.step/.stp)**: preferred for precise mechanical solid exchange across tools.
- **IGES (.igs/.iges)**: older neutral format, still used, often weaker than STEP for modern solid workflows.
- **SAT** (ACIS): precise exchange where ACIS workflows are involved.

### Mesh formats
- **STL**: ubiquitous for 3D printing; no units/materials by default, no parametrics.
- **3MF**: modern additive format with richer metadata/material capabilities.
- **OBJ/glTF/VRML**: visualization/rendering/web pipelines.

### LLM rule of thumb
- For AutoCAD/mechanical editing: export **STEP** first.
- For printing/prototyping: export **STL/3MF**.
- For 2D cut profiles: export **DXF**.

## 6) Python CAD module used in this project

Primary module:
- `cadquery==2.7.0`

Kernel binding layer:
- `cadquery-ocp==7.8.1.1.post1` (OpenCascade via OCP)

Important runtime packages observed in this environment:
- `vtk`, `ezdxf`, `numpy`, `nlopt`, `casadi`, `trame*`, plotting/support libs

Why this stack works for LLM-driven CAD:
- Python-native parametric scripts
- robust B-Rep solid ops from OCCT
- direct export to STEP/STL/DXF and assembly export support
- deterministic regeneration from script edits

## 7) CadQuery capabilities that matter for LLMs

Core modeling:
- `Workplane().box()/cylinder()/sphere()`
- sketch + `extrude`, `revolve`, `loft`, `sweep`
- `union`, `cut`, `intersect`
- selectors and workplanes (`faces(">Z")`, `workplane()`, etc.)

Assemblies:
- `cq.Assembly()`
- `add(part, name=..., loc=..., color=...)`
- export assembly to STEP

Import/export notes:
- CadQuery import supports STEP/DXF and OCCT internal formats.
- CadQuery export supports STEP/STL/DXF and several mesh/view formats.
- CadQuery itself does not carry parametric history through exchange files; Python script is the parametric source of truth.

## 8) Skill workflow for LLM CAD tasks

When asked to create or modify CAD:

1. **Lock units and coordinate conventions first**
- use mm unless told otherwise
- define axis meaning (example: X=left/right, Y=front/back, Z=up)

2. **Create parameter block at top**
- dimensions, clearances, offsets, thicknesses as named constants

3. **Build from coarse to fine**
- start with envelopes and mounting references
- then cutouts/connectors/features
- then visual details

4. **Prevent collisions iteratively**
- place parts with explicit clearances
- update one cluster at a time and regenerate

5. **Export both precision and manufacturing views**
- STEP for CAD editing
- STL for print/prototype

6. **Preserve explainability**
- keep part names stable
- keep placements in readable translated values

## 9) Common failure modes (and mitigations)

1. **Axis confusion after import (front/left swapped)**
- Mitigation: add a tiny axis marker part or documented axis map in script/README.

2. **Boolean instability from tiny overlaps**
- Mitigation: use small intentional overlaps/tolerances (0.1-0.5 mm) where needed.

3. **Over-detailed early models causing chaos**
- Mitigation: lock envelope first, detail later.

4. **Using mesh for editable CAD workflows**
- Mitigation: keep STEP as master exchange for AutoCAD editing.

5. **Visual-only placement that collides physically**
- Mitigation: parametric placement constraints and clearance constants.

## 10) Minimal acceptance checklist for LLM output

- model regenerates without errors
- units are declared and consistent
- no obvious part collisions in target assembly view
- rack/device mount features align with intended planes
- outputs generated: STEP + STL (and DXF when 2D profile needed)
- README documents assumptions and unverified dimensions

## 11) Suggested prompt template for future CAD LLM tasks

"Use `generate_models.py` as the parametric source. Keep units in mm and preserve axis convention. Make changes in small steps: (1) update parameter block, (2) adjust placement, (3) regenerate exports, (4) report exact files touched and remaining assumptions. Prefer STEP-valid solids and avoid mesh-only workflows unless explicitly asked."

## References used for this skill file

- CadQuery introduction: https://cadquery.readthedocs.io/en/latest/intro.html
- CadQuery import/export docs: https://cadquery.readthedocs.io/en/latest/importexport.html
- OpenCascade modeling data overview: https://dev.opencascade.org/doc/overview/html/occt_user_guides__modeling_data.html
- Apple TV 4K technical specs (used in prior modeling dimensions): https://www.apple.com/uk/apple-tv-4k/specs/
