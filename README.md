# Homelab Server Rack CAD Generator

Python + CadQuery workflow for generating homelab rack CAD models and assemblies.

This project is built for iterative rack planning:
- rack frame modeling
- U-position layout
- shelf and device placement
- clearance/collision adjustments
- CAD exports for AutoCAD/Fusion workflows

## Interactive 3D viewer (GitHub Pages)

This repo includes a browser-based 3D viewer using `<model-viewer>`.

- Viewer page source: `docs/index.html`
- Web model: `docs/vevor_20u_rack.glb`
- Conversion script: `tools/convert_step_to_glb.py`

### Convert STEP -> GLB

```powershell
python tools/convert_step_to_glb.py
```

This converts:
- `models/vevor_20u_rack.step` -> `docs/vevor_20u_rack.glb`

### Publish on GitHub Pages

1. Open repo **Settings** -> **Pages**.
2. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
3. Select branch `main` and folder `/docs`.
4. Save, then wait for publish.

Expected viewer URL:
- `https://mxioi.github.io/Homelab-Server-Rack-CAD-Generator/`

## Included rack model assets

- `models/vevor_20u_rack.step` (full rack STEP model)
- `models/vevor_20u_rack.stl` (3D-viewable mesh model)

GitHub note:
- Click `models/vevor_20u_rack.stl` in the repo to open GitHub's interactive 3D viewer.

## Generated outputs

Running the generator writes STEP/STL outputs to `exports/`.

Common files:
- `exports/vevor_20u_rack.step`
- `exports/vevor_20u_loaded.step`
- `exports/vevor_20u_rack_template.step`

## Setup

Recommended Python: `3.11` (project script creates an isolated `.venv311`).

```powershell
./setup_and_generate.ps1
```

Manual alternative:

```powershell
py -3.11 -m venv .venv311
.\.venv311\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python generate_models.py
```

## CAD workflow

1. Generate exports with `python generate_models.py`.
2. Import STEP files from `exports/` into AutoCAD/Fusion.
3. Adjust dimensions/placements in `generate_models.py`.
4. Regenerate and re-import for fit validation.

## Repository scope

This repo intentionally keeps source-focused files:
- `generate_models.py`
- `requirements.txt`
- `setup_and_generate.ps1`
- `README.md`
- `models/vevor_20u_rack.step` and `models/vevor_20u_rack.stl`

Local/generated data (`exports/`, virtualenvs, caches) is excluded from version control.
