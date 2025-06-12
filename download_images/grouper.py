import os
import shutil


def group_by_number(directory, mode=None):
    """
    Moves files into subfolders based on the first numeric token in each filename.
    The optional `mode` param is ignored (legacy support).
    """
    """
    Moves files into subfolders based on the first numeric token in each filename.
    """
    for filename in os.listdir(directory):
        src = os.path.join(directory, filename)
        if not os.path.isfile(src):
            continue

        name, _ = os.path.splitext(filename)
        key = next(
            (p for p in name.replace('_', ' ').split() if p.isdigit()),
            None
        )
        if not key:
            continue

        dest_dir = os.path.join(directory, key)
        os.makedirs(dest_dir, exist_ok=True)
        shutil.move(src, os.path.join(dest_dir, filename))
        print(f"Moved {filename} → {key}/")


def group_images(directory, mode="number"):
    """
    Dispatches grouping based on the given mode.
    Currently supports:
      - 'number': group by numeric ID in filename
    """
    if mode == "number":
        group_by_number(directory)
    else:
        print(f"⚠️  Unknown grouping mode '{mode}'")
