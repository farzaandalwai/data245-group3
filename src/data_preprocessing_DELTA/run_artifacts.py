"""Development artifact publishing; no fitting or final-evaluation authority."""
from contextlib import contextmanager
from pathlib import Path
import os
import platform
import re
import shutil
import subprocess
import tempfile

import numpy as np
import pandas as pd

from src.features_DELTA.bundle import sha256

ROOT = Path(__file__).resolve().parents[2]


def checked_run_id(run_id):
    if not isinstance(run_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", run_id):
        raise ValueError("run_id must contain only letters, digits, hyphen or underscore")
    return run_id


def source_snapshot(paths):
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    return {"base_commit": git("rev-parse", "HEAD"),
            "branch": git("branch", "--show-current"),
            "working_tree_dirty": bool(git("status", "--porcelain")),
            "files_sha256": {name: sha256(ROOT / name) for name in paths}}


def environment():
    return {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__}


def inventory(directory):
    directory = Path(directory)
    return {p.relative_to(directory).as_posix(): {"bytes": p.stat().st_size, "sha256": sha256(p)}
            for p in sorted(directory.rglob("*")) if p.is_file()}


def check_destination(destination, *, inputs):
    """Reject unsafe/colliding output before reading data or fitting."""
    destination = Path(destination)
    resolved = destination.resolve()
    if any(resolved.is_relative_to(Path(p).resolve()) for p in inputs):
        raise ValueError("Output must be separate from immutable input directories")
    if destination.exists():
        raise FileExistsError(f"Immutable run already exists: {destination}")
    return destination


@contextmanager
def new_run(destination, *, inputs):
    """Publish complete output once, outside all input directories."""
    destination = check_destination(destination, inputs=inputs)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".delta-devgru-", dir=destination.parent))
    try:
        yield temporary
        if destination.exists():
            raise FileExistsError(f"Immutable run already exists: {destination}")
        os.rename(temporary, destination)
    finally:
        if temporary.exists():
            # Delete only this call's verified temporary child, never the destination.
            if (temporary.resolve().parent != destination.parent.resolve()
                    or not temporary.name.startswith(".delta-devgru-")):
                raise RuntimeError("Unexpected temporary artifact path")
            shutil.rmtree(temporary)
