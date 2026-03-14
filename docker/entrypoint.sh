#!/bin/sh
set -e

python - <<'PY'
import os
import socket
import sys
import time

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

if not host or not port:
    sys.exit(0)

port = int(port)
timeout_seconds = 60
sleep_seconds = 2
attempts = max(1, timeout_seconds // sleep_seconds)

for _ in range(attempts):
    try:
        with socket.create_connection((host, port), timeout=2):
            print(f"Database is reachable at {host}:{port}")
            break
    except OSError:
        print(f"Waiting for database at {host}:{port}...")
        time.sleep(sleep_seconds)
else:
    print(f"Could not connect to database at {host}:{port}")
    sys.exit(1)
PY

python manage.py migrate --noinput

exec "$@"
