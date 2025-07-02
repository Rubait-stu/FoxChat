# core/utils.py

import os
from PyQt6.QtGui import QIcon

# Root directory of the project
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
ICON_DIR = os.path.join(PROJECT_ROOT, "assets", "icons")
FILETYPE_DIR = os.path.join(ICON_DIR, "filetypes")
DEFAULT_ICON = os.path.join(FILETYPE_DIR, "default.png")


def load_icon(name: str) -> QIcon:
    """
    Load an icon by filename from assets/icons or assets/icons/filetypes.
    Falls back to a default icon if not found.
    """
    primary_path = os.path.join(ICON_DIR, name)
    fallback_path = os.path.join(FILETYPE_DIR, name)

    if os.path.exists(primary_path):
        return QIcon(primary_path)
    elif os.path.exists(fallback_path):
        return QIcon(fallback_path)
    elif os.path.exists(DEFAULT_ICON):
        return QIcon(DEFAULT_ICON)

    return QIcon()  # Return empty icon if nothing is found
