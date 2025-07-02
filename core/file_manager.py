# core/file_manager.py

import json
import os
from typing import Any, Dict, List

# Root-relative path to data directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "sessions")
API_PROFILES_FILE = os.path.join(DATA_DIR, "api_profiles.json")


def ensure_data_dir():
    """Ensure the sessions/ directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


def get_session_file_path(mode: str) -> str:
    """Generate file path based on mode (e.g., 'AI Chat')."""
    filename = f"{mode.strip().lower().replace(' ', '_')}_sessions.json"
    return os.path.join(DATA_DIR, filename)


def save_sessions(mode: str, session_data: Dict[str, Any]) -> None:
    """Save chat sessions for a given mode."""
    ensure_data_dir()
    with open(get_session_file_path(mode), "w", encoding="utf-8") as f:
        json.dump(session_data, f, indent=2)


def load_sessions(mode: str) -> Dict[str, Any]:
    """Load chat sessions for a given mode."""
    path = get_session_file_path(mode)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def save_api_profiles(profiles: List[str]) -> None:
    """Save a list of custom API profile names."""
    ensure_data_dir()
    with open(API_PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2)


def load_api_profiles() -> List[str]:
    """Load saved API profile names."""
    if os.path.exists(API_PROFILES_FILE):
        try:
            with open(API_PROFILES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []
