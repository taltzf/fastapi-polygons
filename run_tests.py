import subprocess
import time
import sys
import os
import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"
SERVER_CMD = ["uvicorn", "app.main:app", "--reload"]


def wait_for_server(url, timeout=10):
    """Wait until the FastAPI server is ready"""
    for _ in range(timeout * 2):
        try:
            requests.get(url)
            return True
        except:
            time.sleep(0.5)
    return False


def main():
    # Start FastAPI server in background
    server_proc = subprocess.Popen(SERVER_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Starting FastAPI server...")

    if not wait_for_server(BASE_URL):
        print("Server did not start in time")
        server_proc.terminate()
        sys.exit(1)

    print("Server is ready. Running Playwright tests...")

    # Run Playwright tests
    retcode = pytest.main(["-v", "-m", "ui", "--maxfail=1", "--disable-warnings"])

    # Shut down server
    print("Shutting down server...")
    server_proc.terminate()
    server_proc.wait()

    sys.exit(retcode)


if __name__ == "__main__":
    main()
