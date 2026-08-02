import json
from pathlib import Path

for f in Path("src/database/foods").glob("*.json"):
    d=json.loads(f.read_text())
    assert "nutrition" in d
    assert "protein" in d["nutrition"]
print("Food database validation passed.")
