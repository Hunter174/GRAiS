import subprocess
import time
import webview
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def start_django():
    return subprocess.Popen(
    [sys.executable, "manage.py", "runserver", "127.0.0.1:8000"],
        cwd=BASE_DIR / "web",
    )

if __name__ == "__main__":
    proc = start_django()
    time.sleep(2)  # give server time to start

    webview.create_window(
        "GRAiS Desktop",
        "http://127.0.0.1:8000",
        width=1200,
        height=800,
    )
    webview.start()

    proc.terminate()