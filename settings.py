from pathlib import Path

# Main project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Project information
PROJECT_NAME = "DriftShield"
PROJECT_VERSION = "1.0.0"
PROJECT_TAGLINE = "Detect the Drift. Protect the Performance."

# Application directories
DATA_DIR = BASE_DIR / "data"
REFERENCE_DATA_DIR = DATA_DIR / "reference"
INCOMING_DATA_DIR = DATA_DIR / "incoming"

REPORTS_DIR = BASE_DIR / "reports"

# Database configuration
DATABASE_PATH = BASE_DIR / "driftshield.db"

# Create required directories
for directory in [
    REFERENCE_DATA_DIR,
    INCOMING_DATA_DIR,
    REPORTS_DIR
]:
    directory.mkdir(parents=True, exist_ok=True)

print(f"{PROJECT_NAME} configuration loaded successfully!")