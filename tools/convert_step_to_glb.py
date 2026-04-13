from pathlib import Path

import cadquery as cq


def convert_step_to_glb(step_path: Path, glb_path: Path) -> None:
    imported = cq.importers.importStep(str(step_path))
    if isinstance(imported, cq.Assembly):
        assy = imported
        assy.name = step_path.stem
    else:
        assy = cq.Assembly(name=step_path.stem)
        assy.add(imported, name=f"{step_path.stem}_part", color=cq.Color(0.2, 0.2, 0.2))
    glb_path.parent.mkdir(parents=True, exist_ok=True)
    assy.export(str(glb_path))


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    step_file = root / "models" / "vevor_20u_rack.step"
    glb_file = root / "docs" / "vevor_20u_rack.glb"

    if not step_file.exists():
        raise FileNotFoundError(f"STEP file not found: {step_file}")

    convert_step_to_glb(step_file, glb_file)
    print(f"Generated: {glb_file}")


if __name__ == "__main__":
    main()
