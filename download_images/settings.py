import json
import os

CONFIG_FILE = os.path.join(os.getcwd(), 'settings.json')
DEFAULTS = {
    "extensions": [".gif", ".png"],
    "size": [96, 96],
    "output_dir": "downloaded_images",
    "group_by": "number"
}


def load_config():
    # Attempt to read existing, else create defaults
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
            # fill in any missing keys
            for k, v in DEFAULTS.items():
                cfg.setdefault(k, v)
            return cfg
        except Exception:
            pass
    # Write defaults back
    save_config(DEFAULTS)
    return DEFAULTS.copy()


def save_config(cfg):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, indent=2)
    except IOError as e:
        print(f"⚠ Could not save settings: {e}")