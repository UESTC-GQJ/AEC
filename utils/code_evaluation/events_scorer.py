from __future__ import annotations

import marshal
from pathlib import Path

_pyc_path = Path(__file__).with_name("pyc_recovered_backup") / "events_scorer.cpython-311.pyc"
_code = marshal.loads(_pyc_path.read_bytes()[16:])
exec(_code, globals(), globals())
