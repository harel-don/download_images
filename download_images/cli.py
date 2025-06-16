import os
from download_images.settings import load_config, save_config
from download_images.downloader import get_image_urls, is_valid_extension, download_image, save_image
from download_images.grouper import group_images
from download_images.resizer import batch_resize

MENU = [
    "\nSelect operation mode:",
    "1) Download images",
    "2) Group images",
    "3) Both",
    "4) Edit settings",
    "5) Resize canvas",
    "6) Exit"
]

def display_menu():
    for line in MENU:
        print(line)

def handle_download(cfg):
    out = cfg['output_dir']
    size = cfg['size']
    url = input('Page URL: ')
    for u in get_image_urls(url):
        if is_valid_extension(u, cfg['extensions']):
            ok, tup = download_image(u, size)
            if ok:
                save_image(tup, u, out)
    print(f"Downloaded to '{out}'")

def handle_group(cfg):
    print("Grouping...")
    group_images(cfg['output_dir'], cfg['group_by'])
    print("Grouping done.")

def handle_edit(cfg):
    print("\nCurrent settings:")
    for k, v in cfg.items():
        print(f"  {k}: {v}")
    print("\nLeave blank to keep.")
    e = input(f"Extensions [{','.join(cfg['extensions'])}]: ")
    if e.strip(): cfg['extensions'] = [x.strip() for x in e.split(',')]
    s = input(f"Size WxH [{cfg['size'][0]}x{cfg['size'][1]}]: ")
    if s.strip(): w, h = s.lower().split('x'); cfg['size'] = [int(w), int(h)]
    o = input(f"Output dir [{cfg['output_dir']}]: ")
    if o.strip(): cfg['output_dir'] = o.strip()
    g = input(f"Group by [{cfg['group_by']}]: ")
    if g.strip(): cfg['group_by'] = g.strip()
    save_config(cfg)
    print("Settings saved!\n")

def handle_resize(cfg):
    print("Resizing canvas...")
    batch_resize(cfg['output_dir'], extensions=cfg['extensions'], min_size=cfg['size'][0])
    print("Resize complete.")

def main():
    cfg = load_config()
    os.makedirs(cfg['output_dir'], exist_ok=True)
    while True:
        display_menu()
        ch = input('Enter 1-6: ').strip()
        if ch == '6':
            print('Goodbye!')
            break
        if ch == '4':
            handle_edit(cfg)
        if ch in ('1', '3'):
            handle_download(cfg)
        if ch in ('2', '3'):
            handle_group(cfg)
        if ch == '5':
            handle_resize(cfg)
        if input("\nPress Enter to return or 'exit': ").strip().lower() == 'exit':
            print('Goodbye!')
            break

if __name__ == '__main__':
    main()