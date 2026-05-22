"""pytest configuration shared by every test module.

Putting the repo root on sys.path means tests work both inside an editable
install (`pip install -e .`) and without one (a fresh clone, no install).
"""
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
