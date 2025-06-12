import json
import os

# Default configuration values
DEFAULTS = {
    "extensions": [".gif", ".png"],
    "size": [96, 96],
    "output_dir": "downloaded_images",
    "group_by": "number"
}

CONFIG_PATH = os.path.join(os.getcwd(), "settings.json")


def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Ensure any missing keys are filled in
            for k, v in DEFAULTS.items():
                data.setdefault(k, v)
            return data
        except (json.JSONDecodeError, IOError):
            pass
    # write defaults if no valid config
    save_config(DEFAULTS)
    return DEFAULTS.copy()


def save_config(config):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except IOError as e:
        print(f"Error saving config: {e}")