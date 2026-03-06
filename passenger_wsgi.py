"""Passenger entrypoint (used by Apache/Hostinger Python app setups)."""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from wsgi import application  # noqa: E402
