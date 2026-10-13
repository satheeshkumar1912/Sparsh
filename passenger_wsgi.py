"""cPanel / Passenger entry point. Application root must be this project folder."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND = ROOT / "backend"
backend_path = str(BACKEND)
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from config.wsgi import application  # noqa: E402
