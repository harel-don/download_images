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


def handle_edit(cfg):
    print("\nCurrent settings:")
    for k, v in cfg.items(): print(f"  {k}: {v}")
    print("\nLeave blank to keep current.")
    e = input(f"Extensions [{','.join(cfg['extensions'])}]: ")
    if e.strip(): cfg['extensions'] = [x.strip() for x in e.split(',')]
    s = input(f"Size WxH [{cfg['size'][0]}x{cfg['size'][1]}]: ")
    if s.strip(): w, h = s.lower().split('x'); cfg['size']=[int(w), int(h)]
    o = input(f"Output dir [{cfg['output_dir']}]: ")
    if o.strip(): cfg['output_dir']=o.strip()
    g = input(f"Group by [{cfg['group_by']}]: ")
    if g.strip(): cfg['group_by']=g.strip()
    save_config(cfg); print("Settings saved!\n")


def handle_resize(cfg):
    print("Resizing canvas..."); batch_resize(cfg['output_dir'], extensions=cfg['extensions'], min_size=cfg['size'][0]); print("Resize complete.")

def handle_sheet(cfg):
    print("Sprite-sheet → Animation")
    prompt = "Sheet file or folder path (Enter to use output dir): "
    source = input(prompt).strip()
    if not source:
        source = cfg['output_dir']
        print(f"Using default directory: {source}")

    # Build list of sheet paths (either one file or all valid images in a folder)
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

    # Prompt for optional parameters
    fw = input("Frame width (or Enter to infer): ").strip() or None
    fh = input("Frame height (or Enter to infer): ").strip() or None
    dur = int(input("Frame duration in ms [100]: ").strip() or 100)
    lp  = int(input("Loop count [0=infinite]: ").strip() or 0)

    # Convert width/height inputs to ints or None
    fw = int(fw) if fw else None
    fh = int(fh) if fh else None

    # Process each sheet
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
