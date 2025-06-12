import os
import shutil


def group_by_number(directory):
    """
    Moves files into subfolders based on the first numeric token in each filename.
    E.g. 'Spr 5b 004 s.png' → subfolder '004/'.
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