"""Campaign models (placeholder)."""
from dataclasses import dataclass, field
from typing import List


@dataclass
class Campaign:
    id: str
    name: str
    targets: List[str] = field(default_factory=list)

    def summary(self) -> str:
        return f"Campaign(id={self.id!r}, name={self.name!r}, targets={len(self.targets)})"
