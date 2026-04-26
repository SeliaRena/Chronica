from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Project-level directories
LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Package-level directories
PACKAGE_BASE = PROJECT_ROOT / "src" / "chronica"
UI_DIR = PACKAGE_BASE / "ui"

# UI subdirectories
STYLES_DIR = UI_DIR / "styles"

# Characters subdirectories
CHARACTERS_DIR = PACKAGE_BASE / "characters"