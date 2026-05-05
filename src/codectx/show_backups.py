"""Inspect the latest rolling backup for the default output file."""

from __future__ import annotations

import json
from pathlib import Path


backup_file = Path("project.ctx.json.backup")

if not backup_file.exists():
    print("No backup file found.")
else:
    with backup_file.open("r", encoding="utf-8") as handle:
        backup = json.load(handle)
    print("LATEST BACKUP:")
    print(f"analysis_time: {backup.get('analysis_time')}")
