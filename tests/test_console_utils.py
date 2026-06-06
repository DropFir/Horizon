"""Tests for GBK-safe console setup."""

import io
import sys

from src.console_utils import configure_stdio_encoding, create_console, safe_print


def test_console_survives_gbk_stdout_with_emoji():
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    try:
        sys.stdout = io.TextIOWrapper(io.BytesIO(), encoding="gbk", errors="strict")
        sys.stderr = io.TextIOWrapper(io.BytesIO(), encoding="gbk", errors="strict")

        configure_stdio_encoding()
        console = create_console()
        console.print("[bold cyan]🌅 Horizon - Starting aggregation...[/bold cyan]")
        console.print("[bold red]❌ Fatal error: boom[/bold red]")
        safe_print("[ERROR] fatal fallback works")
    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr
