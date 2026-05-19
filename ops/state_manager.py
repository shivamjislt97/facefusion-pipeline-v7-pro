import hashlib
import json
from pathlib import Path


class PipelineStateStore:
    def __init__(self, state_file: str | Path):
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict:
        if not self.state_file.exists():
            return {}
        try:
            return json.loads(self.state_file.read_text(errors="ignore"))
        except Exception:
            return {}

    def save(self, data: dict) -> None:
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(data or {}, indent=2))


def compute_idempotency_key(*parts) -> str:
    h = hashlib.sha256()
    for part in parts:
        h.update(str(part).encode("utf-8", errors="ignore"))
        h.update(b"|")
    return h.hexdigest()


def validate_output_media(path: str | Path) -> tuple[bool, str]:
    p = Path(path)
    if not p.exists():
        return False, "output path missing"
    if not p.is_file():
        return False, "output path is not a file"
    if int(p.stat().st_size or 0) <= 0:
        return False, "output file empty"
    return True, f"size={int(p.stat().st_size)}"
