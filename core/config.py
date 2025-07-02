# config/config.py

import os

# App constants
APP_NAME = "FoxChat"

# Default API profiles (empty for now; user can add custom later)
API_PROFILES = {
    # Example profile format:
    # "OpenAI": {
    #    "name": "OpenAI GPT-4",
    #    "endpoint": "https://api.openai.com/v1/chat/completions",
    #    "api_key": "",
    #    "type": "openai",
    # },
}

# Path to themes folder (relative to project root)
THEMES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "themes")


def load_theme(app, mode="colorful"):
    """
    Load QSS stylesheet from themes folder and apply to QApplication.

    Args:
        app (QApplication): The QApplication instance.
        mode (str): Theme mode - "colorful", "light", or "dark".
    """
    theme_file = os.path.join(THEMES_DIR, f"{mode}.qss")
    if not os.path.isfile(theme_file):
        print(f"Theme file not found: {theme_file}")
        return

    with open(theme_file, "r", encoding="utf-8") as f:
        qss = f.read()
        app.setStyleSheet(qss)
