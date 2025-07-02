import importlib
import os
from typing import Callable

from dotenv import load_dotenv
import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG, filename="app.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

def log_error(error_msg):
    logging.error(error_msg)

load_dotenv()

# Built-in API registry
BUILT_IN_APIS = {
    "deepseek": "openrouter_internal",  # Use fake internal tag
}

# Load environment variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Validate the keys
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is missing in the .env file.")


# ------------------- Built-in OpenRouter Query ------------------- #
def query_openrouter(prompt: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [{"role": "user", "content": prompt}],
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        log_error(f"OpenRouter Error: {e}")
        return f"❌ Error querying OpenRouter: {e}"


# ------------------- Public Interface ------------------- #
def normalize_name(name: str) -> str:
    return name.strip().lower().replace(" ", "_")


def query_api(text: str, profile_name: str) -> str:
    profile_key = profile_name.strip().lower()

    # Handle built-in API directly
    if profile_key == "deepseek":
        return query_openrouter(text)

    try:
        module_name = normalize_name(profile_name)
        api_module = importlib.import_module(f"foxchat.apis.{module_name}")
        query_func: Callable[[str], str] = getattr(api_module, "query", None)
        if not callable(query_func):
            return f"⚠️ API module '{module_name}' does not implement a callable `query(text)`."
        return query_func(text)

    except ModuleNotFoundError:
        return f"⚠️ API module not found: 'foxchat.apis.{module_name}'"

    except Exception as e:
        return f"❌ Error while querying '{profile_name}': {str(e)}"
