#!/usr/bin/env python3
"""Desktop launcher for the Research Assistant UI.

Starts the Flask app in a background thread, then opens a native OS window
(via pywebview) pointed at it. Works on Linux (GTK/Qt), macOS, and Windows.

Usage:
    python desktop.py

Falls back to opening the system browser if pywebview is not installed.
"""
from __future__ import annotations

import logging
import socket
import sys
import threading
import time
from contextlib import closing

logger = logging.getLogger("research-assistant.desktop")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def _pick_free_port(preferred: int = 5050) -> int:
    """Try the preferred port; if taken, ask the OS for a free one."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        try:
            s.bind(("127.0.0.1", preferred))
            return preferred
        except OSError:
            pass
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _wait_for_server(host: str, port: int, timeout: float = 10.0) -> bool:
    """Poll the server until it accepts connections or we time out."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.settimeout(0.5)
            try:
                s.connect((host, port))
                return True
            except OSError:
                time.sleep(0.1)
    return False


def _start_flask(host: str, port: int) -> None:
    """Run the Flask app. Imports lazily so import errors surface clearly."""
    from research_assistant.web.app import app
    # Disable the reloader — would spawn a second process, which collides with pywebview.
    app.run(host=host, port=port, debug=False, use_reloader=False, threaded=True)


def main() -> int:
    host = "127.0.0.1"
    port = _pick_free_port(5050)
    url = f"http://{host}:{port}"

    server_thread = threading.Thread(
        target=_start_flask, args=(host, port), daemon=True, name="flask-server"
    )
    server_thread.start()

    if not _wait_for_server(host, port, timeout=15.0):
        logger.error("Flask did not come up on %s within 15s", url)
        return 1

    logger.info("Research Assistant ready at %s", url)

    try:
        import webview  # type: ignore[import-not-found]
    except ImportError:
        logger.warning("pywebview not installed — falling back to system browser.")
        logger.warning("Install with: pip install pywebview")
        import webbrowser
        webbrowser.open(url)
        try:
            # Keep the script alive so the Flask thread isn't killed.
            while server_thread.is_alive():
                server_thread.join(timeout=1.0)
        except KeyboardInterrupt:
            pass
        return 0

    webview.create_window(
        title="Research Assistant",
        url=url,
        width=1280,
        height=860,
        min_size=(900, 600),
        text_select=True,
        confirm_close=False,
    )
    webview.start(debug=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
