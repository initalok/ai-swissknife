from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol


class SurfaceRenderer(Protocol):
    """Dumb snapshot consumer contract: performs zero data loading or business logic."""

    def render(self, snapshot: dict[str, Any], root: Path) -> list[Path]: ...
