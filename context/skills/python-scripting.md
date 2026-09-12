---
name: python-scripting
description: Procedural guidance and JIT best practices for authoring, running, and testing Python scripts with uv, PEP 723 inline metadata, and the --with pattern.
globs: ["**/*.py", "**/pyproject.toml", "context/scripts/**/*", "scripts/**/*"]
---

# Python Scripting Skill

**Invariant: Zero-Tolerance Fail-Fast**: NEVER fallback to bare `python`, `python3`, `pip`, or ad-hoc `PYTHONPATH` if `uv` fails. Escalate or fix.

**The Ephemeral `--with` Pattern**: Use `uv run --with <pkg>` for ad-hoc dependencies.

- Pytest: `uv run --with pytest pytest <path>`
- Script w/ PyYAML: `uv run --with pyyaml python script.py`
- Linter: `uv run --with ruff ruff check --fix script.py`
- Formatter: `uv run --with ruff ruff format script.py`

**Standalone Scripts (PEP 723)**: For self-contained scripts, use inline metadata:

```python
# /// script
# dependencies = ["pyyaml>=6.0", "rich>=13.0.0"]
# ///
#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
if __name__ == "__main__": sys.exit(main())
```

Run via: `uv run python script.py`.

**Monorepo/Service Execution**:

- Target project: `uv run --project services/<name> python -m service.main`
- Add dep: `uv add --project services/<name> pydantic`
- Sync: `uv sync --project services/<name>`
- CLI Tool: `uvx <tool>` (e.g., `uvx ruff check .`)

**Authoring Standards**:

1. `from __future__ import annotations` first.
2. Use Type Hints.
3. CLI Parsing: `argparse` (include `--dry-run`, `--verbose`, `--quiet`, `--fix`).
4. Path Resolution: Use `pathlib.Path` relative to `__file__`. No `os.path`.
5. Deterministic Exit: `0` success, non-zero failure.
6. No destructive imports: use `if __name__ == "__main__": main()`.
7. No multiline inline bash strings for Python scripts; use temporary files instead.

**Quality Verification**:

- Syntax: `uv run python -m py_compile <file>`
- Lint: `uv run --with ruff ruff check --fix <file>`
- Format: `uv run --with ruff ruff format <file>`
- Test: `uv run --with pytest pytest <path> -v`

