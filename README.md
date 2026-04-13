# GPU + PSU Rackmount CAD Starter

This folder contains a Python + CadQuery workflow to generate approximate 3D CAD models for:

- AMD Radeon Vega Frontier Edition (air)
- Corsair RM750x 750W PSU
- Chenyang Oculink adapter + cable

The output is generated in CAD-friendly formats so you can open or import in AutoCAD.

## What this currently generates

- `exports/gpu_frontier_air.step`
- `exports/psu_rm750x.step`
- `exports/oculink_adapter.step`
- `exports/oculink_cable.step`
- `exports/rack_gpu_holder.step`
- `exports/rack_holder_fit.step` (holder with single GPU + Oculink fit check)
- `exports/rackmount_parts.step` (assembly)
- `exports/vevor_20u_rack.step` (standalone rack only)
- `exports/vevor_20u_rack_template.step` (standalone rack + placement zones)
- `exports/zone_gpu.step`, `exports/zone_oculink.step`, `exports/zone_psu.step`
- `exports/vevor_20u_loaded.step` (rack populated to match your current install layout)

Optional mesh exports are also created as STL files.

## Dimension assumptions used (mm)

- GPU (AMD Frontier air): `267 x 111 x 40` (double-slot envelope)
- PSU (Corsair RM750x): `160 x 150 x 86`
- Oculink adapter board (from measured image): `174 x 47.3 x 1.6`
- Oculink total height envelope with connectors/caps: `~14`

## Included detail features

- GPU: blower recess, PCIe edge tab/contacts, side mounting bracket, top dual 8-pin power blocks
- PSU: top fan opening/ring, rear AC inlet + rocker switch geometry, front modular connector field
- Oculink adapter: PCIe x16 slot body, 24-pin ATX connector block, switch, capacitors, Oculink cable segments
- Rack holder: horizontal GPU channel, Oculink support pad, anti-bend bridge, rack ear slots, tie-down loops

## Rack holder assumptions

- Rack type target: 19-inch open frame style (VEVOR class)
- Rack-mount hole center spacing assumed: `465 mm`
- Holder depth for print + support: `320 mm`
- Printed holder channel clearances are intentionally loose for first-fit validation

## Standalone rack model

- `vevor_20u_rack` is exported as a separate part so you can manually place GPU, Oculink adapter, and PSU in AutoCAD.
- Dimensions are based on your provided product image: `23.0 x 20.1 x 38.7 in` (approx `585 x 510 x 982 mm`).
- Includes simplified 1U hole-center pattern at `44.45 mm` pitch on front and rear mounting rails.
- Includes simplified caster geometry at the base.
- `vevor_20u_rack_template.step` adds three colored marker volumes for quick placement:
  - `zone_gpu`
  - `zone_oculink`
  - `zone_psu`

## Loaded rack layout included

- Top panel added to prevent items falling through.
- Shelf at `U1` (larger): Terramaster 4-bay enclosure, Time Capsule, Lenovo P52s on top.
- Shelf at `U17-U20` (smaller): Wii in stand, Nintendo Switch, Apple TV, Sky box, small PSU blocks, joycons.
- Shelf at `U17-U20` (smaller): Wii in stand, Wii PSU, Nintendo Switch dock, Apple TV, Sky box, Minisforum MS-A1, Hue bridge stack, joycons, small UniFi PSU.
- `U13`: UDM Pro placeholder.
- `U14`: USP-RPS placeholder.
- `U15`: blank space with Raspberry Pi placeholder resting on the RPS area.
- `U16`: 1U patch panel placeholder.

## Dimension updates used in latest layout pass

- Apple TV 4K modeled at `93 x 93 x 31 mm` (Apple tech specs).
- Hue Bridge modeled at `89 x 89 x 26 mm` envelope.
- Nintendo Switch dock modeled in vertical orientation with `~40 x 173 x 104 mm` envelope.
- Joy-Con placeholders reduced to handheld-scale envelopes (`~28 x 36 x 102 mm` each).
- Sky Mini dimensions are still approximate planning envelopes and should be verified with direct measurement.

## Accuracy notes

- This is a mechanical planning model, not an exact production reverse-engineered CAD.
- Connector interior pin cavities, exact grille perforation patterns, and exact screw hole standards are simplified.
- For fabrication, verify with calipers and vendor drawings, then replace dimensions in `generate_models.py`.
- For load-bearing use, print orientation/material and reinforcement are critical; validate strength before production deployment.

## Setup

Python requirement: **3.10, 3.11, or 3.12** (CadQuery is not currently published for Python 3.14).

### Option A: one command helper (PowerShell)

```powershell
./setup_and_generate.ps1
```

This creates an isolated local environment in `.venv311`.

### Option B: manual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python generate_models.py
```

## AutoCAD workflow

1. Open AutoCAD.
2. Use `IMPORT` and select the STEP files from `exports`.
3. Position parts and check clearances.
4. If dimensions change, update `generate_models.py` parameters and regenerate.

## Files

- `requirements.txt` - Python dependencies
- `generate_models.py` - model generation and export
- `setup_and_generate.ps1` - optional setup helper
