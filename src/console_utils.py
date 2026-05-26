"""Shared Rich console setup safe for Windows GBK / piped stdout."""

from __future__ import annotations

import os
import sys

from rich.console import Console

_configured = False


def configure_stdio_encoding() -> None:
    """Prefer UTF-8 stdout/stderr; fall back to replace on encode errors."""
    global _configured
    if _configured:
        return
    _configured = True

    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ.setdefault("PYTHONUTF8", "1")

    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        if stream is None:
            continue
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError, AttributeError):
            try:
                reconfigure(errors="replace")
            except (ValueError, OSError, AttributeError):
                pass


def create_console(**kwargs) -> Console:
    """Return a Rich Console configured for cross-platform / piped output."""
    configure_stdio_encoding()
    return Console(legacy_windows=False, **kwargs)


def safe_print(message: str, *, file=None) -> None:
    """Print without raising on encoding errors (e.g. fatal error handler)."""
    configure_stdio_encoding()
    target = file or sys.stderr
    text = f"{message}\n"
    try:
        target.write(text)
        target.flush()
    except UnicodeEncodeError:
        fallback = text.encode("ascii", errors="backslashreplace").decode("ascii")
        try:
            target.write(fallback)
            target.flush()
        except Exception:
            pass
    except Exception:
        pass
