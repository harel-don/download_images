import os
from download_images.settings import load_config, save_config
from download_images.downloader    import get_image_urls, is_valid_extension, download_image, save_image
from download_images.grouper       import group_images
from download_images.resizer       import batch_resize
from download_images.sheet_assembler import sheet_to_animation

MENU = [
    "\nSelect operation mode:",
    "1) Download images",
    "2) Group images",
    "3) Both",
    "4) Edit settings",
    "5) Resize canvas",
    "6) Sprite-sheet → Animation",
    "7) Exit",
]

def display_menu():
    for line in MENU:
        print(line)

def handle_download(cfg):
    out = cfg['output_dir']; size = cfg['size']
    url = input('Page URL: ').strip()
    if not url: print("No URL provided."); return
    for u in get_image_urls(url):
        if is_valid_extension(u, cfg['extensions']):
            ok, tup = download_image(u, size)
            if ok: save_image(tup, u, out)
    print(f"Downloaded to '{out}'")

def handle_group(cfg):
    print("Grouping images..."); group_images(cfg['output_dir'], cfg['group_by']); print("Grouping complete.")


def handle_edit(config):
    print("Current settings:")
    for key, val in config.items():
        print(f"  {key}: {val}")
    print("\nEnter new values or leave blank to keep current.")

    new_ext = input(f"Extensions (comma-separated) [{','.join(config['extensions'])}]: ")
    if new_ext.strip():
        config['extensions'] = [e.strip() for e in new_ext.split(',')]

    new_size = input(f"Size WxH [{config['size'][0]}x{config['size'][1]}]: ")
    if new_size.strip():
        w, h = new_size.lower().split('x')
        config['size'] = [int(w), int(h)]

    new_out = input(f"Output directory [{config['output_dir']}]: ")
    if new_out.strip():
        config['output_dir'] = new_out.strip()

    new_group = input(f"Group by ('number') [{config['group_by']}]: ")
    if new_group.strip():
        config['group_by'] = new_group.strip()

    # ——— Sprite-sheet settings ———
    new_sfw = input(f"Sheet frame width (or Enter for auto) [{config.get('sheet_frame_width')}]: ")
    if new_sfw.strip():
        config['sheet_frame_width'] = int(new_sfw)

    new_sfh = input(f"Sheet frame height (or Enter for auto) [{config.get('sheet_frame_height')}]: ")
    if new_sfh.strip():
        config['sheet_frame_height'] = int(new_sfh)

    new_dur = input(f"Sheet animation duration ms [{config.get('sheet_duration')}]: ")
    if new_dur.strip():
        config['sheet_duration'] = int(new_dur)

    new_loop = input(f"Sheet animation loop count [{config.get('sheet_loop')}]: ")
    if new_loop.strip():
        config['sheet_loop'] = int(new_loop)

    save_config(config)
    print("Settings saved.")


def handle_resize(cfg):
    print("Resizing canvas..."); batch_resize(cfg['output_dir'], extensions=cfg['extensions'], min_size=cfg['size'][0]); print("Resize complete.")

def handle_sheet(cfg):
    print("Sprite-sheet → Animation")
    prompt = "Sheet file or folder path (Enter to use output dir): "
    source = input(prompt).strip()
    if not source:
        source = cfg['output_dir']
        print(f"Using default directory: {source}")

    # Collect .png/.gif files from directory or accept a single file
    exts = cfg.get("extensions", [".png", ".gif"])
    if os.path.isdir(source):
        sheet_paths = []
        for fname in os.listdir(source):
            path = os.path.join(source, fname)
            ext = os.path.splitext(fname)[1].lower()
            if os.path.isfile(path) and ext in exts:
                sheet_paths.append(path)
        if not sheet_paths:
            print(f"❗️ No sprite-sheet files found in: {source}")
            return
    else:
        ext = os.path.splitext(source)[1].lower()
        if ext not in exts:
            print(f"❗️ Not a supported sheet file: {source}")
            return
        sheet_paths = [source]

    # Load sprite-sheet settings (None means infer from sheet)
    fw  = cfg.get('sheet_frame_width')    # frame width
    fh  = cfg.get('sheet_frame_height')   # frame height
    dur = cfg.get('sheet_duration', 100)  # ms per frame
    lp  = cfg.get('sheet_loop', 0)        # loop count

    # Process each sheet file
    for sheet in sheet_paths:
        try:
            sheet_to_animation(
                sheet_path=sheet,
                frame_width=fw,
                frame_height=fh,
                duration=dur,
                loop=lp
            )
        except Exception as e:
            print(f"⚠️ Failed on {sheet}: {e}")


def main():
    cfg = load_config()
    os.makedirs(cfg['output_dir'], exist_ok=True)
    while True:
        display_menu()
        choice = input("Enter 1-7: ").strip()
        if choice == '7':
            print("Goodbye!")
            break
        if choice in ('1','3'):  handle_download(cfg)
        if choice in ('2','3'):  handle_group(cfg)
        if choice == '4':        handle_edit(cfg)
        if choice == '5':        handle_resize(cfg)
        if choice == '6':        handle_sheet(cfg)

        if input("\nPress Enter to continue or type 'exit': ").strip().lower() == 'exit':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
