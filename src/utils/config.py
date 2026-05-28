"""Global configuration"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data directory
DATA_DIR = PROJECT_ROOT / "data"
BLOCKS_LIBRARY_PATH = DATA_DIR / "blocks_library.json"

# GUI Constants
GRID_SIZE = 20
BLOCK_WIDTH = 120
BLOCK_HEIGHT = 80
CANVAS_BACKGROUND_COLOR = "#f0f0f0"
BLOCK_BACKGROUND_COLOR = "#3498db"
BLOCK_TEXT_COLOR = "#ffffff"
