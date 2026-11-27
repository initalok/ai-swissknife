from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol


class BlockSyncSurface(Protocol):
    """Dumb snapshot consumer: updates managed regions or generated views without business logic."""

    def sync(self, snapshot: dict[str, Any], root: Path) -> list[Path]: ...
