#!/usr/bin/env python3
"""
Scan the scenes directory, auto-generate sequence.json where missing,
and write catalog.json for the scene library viewer.

Run from webxr_viewer/ before starting the server:
    python3 gen_catalog.py

Add a new scene:
    1. Put PLY frames under  scenes/<your_scene>/assets/frame_*.ply
    2. Re-run this script
    3. Refresh the browser — the scene appears automatically
"""
from __future__ import annotations

import json
from pathlib import Path

VIEWER_ROOT = Path(__file__).parent
SCENES_ROOT = VIEWER_ROOT / "scenes"
CATALOG_OUT = VIEWER_ROOT / "catalog.json"


def find_scene_dirs(root: Path) -> list[Path]:
    """Recursively find directories that contain PLY assets or a sequence.json."""
    results = []
    for candidate in sorted(root.rglob("*")):
        if not candidate.is_dir() or candidate.name == "assets":
            continue
        assets_dir = candidate / "assets"
        has_plys = assets_dir.is_dir() and any(assets_dir.glob("*.ply"))
        has_seq = (candidate / "sequence.json").exists()
        if has_plys or has_seq:
            results.append(candidate)
    return results


def ensure_sequence_json(scene_dir: Path) -> Path | None:
    seq_path = scene_dir / "sequence.json"
    if seq_path.exists():
        return seq_path

    assets_dir = scene_dir / "assets"
    plys = sorted(p for p in assets_dir.iterdir() if p.suffix.lower() == ".ply")
    if not plys:
        return None

    seq = {
        "version": 1,
        "name": scene_dir.name,
        "fps": 12.0,
        "autoplay": True,
        "frames": [
            {"index": i, "filename": p.name, "url": f"assets/{p.name}"}
            for i, p in enumerate(plys)
        ],
    }
    seq_path.write_text(json.dumps(seq, indent=2), encoding="utf-8")
    print(f"  [new] {seq_path.relative_to(VIEWER_ROOT)}")
    return seq_path


def build_entry(scene_dir: Path, seq_path: Path) -> dict:
    with open(seq_path, encoding="utf-8") as f:
        seq = json.load(f)

    scene_id = scene_dir.name
    title = seq.get("name", scene_id).replace("_", " ").title()
    rel_seq = f"/{seq_path.relative_to(VIEWER_ROOT).as_posix()}"

    entry: dict = {
        "title": title,
        "id": scene_id,
        "sequence": rel_seq,
        "frames": len(seq.get("frames", [])),
        "fps": seq.get("fps", 12.0),
        "tags": ["PLY"],
    }

    # A manifest-managed background is loaded by the sequence reader itself.
    # Keep deferLoad only as a legacy fallback for scenes without that field.
    bg = scene_dir / "assets" / "background.ply"
    if not seq.get("background") and bg.exists():
        entry["deferLoad"] = f"/{bg.relative_to(VIEWER_ROOT).as_posix()}"
        entry["deferFilename"] = "background.ply"
        entry["tags"].append("Deferred background")

    return entry


def main() -> None:
    print(f"Scanning {SCENES_ROOT.relative_to(VIEWER_ROOT)} ...")
    scene_dirs = find_scene_dirs(SCENES_ROOT)

    if not scene_dirs:
        print("  No scenes found.")
        return

    catalog = []
    for scene_dir in scene_dirs:
        seq_path = ensure_sequence_json(scene_dir)
        if seq_path is None:
            print(f"  [skip] {scene_dir.name} — no PLY files")
            continue
        entry = build_entry(scene_dir, seq_path)
        catalog.append(entry)
        print(f"  [ok]  {entry['title']}  ({entry['frames']} frames)  →  {entry['sequence']}")

    CATALOG_OUT.write_text(json.dumps(catalog, indent=2), encoding="utf-8")
    print(f"\n{len(catalog)} scene(s) written to {CATALOG_OUT.name}")


if __name__ == "__main__":
    main()
