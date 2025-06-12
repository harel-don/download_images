import os
from download_images.downloader import (
    get_image_urls, is_valid_extension,
    download_image, save_image
)
from download_images.grouper import group_by_number
from download_images.settings import load_config, save_config

# --- Messages ---
MSG_MENU = ('Select operation mode:',
    '1) Download images',
    '2) Group images',
    '3) Both',
    '4) Edit settings',
    '5) Exit'
)
MSG_EXIT = 'Goodbye!'
MSG_ENTER_URL = 'Page URL: '
MSG_DOWNLOADED = "Downloaded images to '{out_dir}'"
MSG_GROUPING = 'Grouping images...'
MSG_GROUPED = 'Grouping complete.'
MSG_RETURN_PROMPT = "Press Enter to return to menu, or type 'exit' to quit: "


def display_menu():
    for line in MSG_MENU:
        print(line)


def handle_download(config):
    out_dir = config['output_dir']
    url = input(MSG_ENTER_URL)
    urls = get_image_urls(url)
    for u in urls:
        if is_valid_extension(u, config['extensions']):
            ok, tup = download_image(u, config['size'])
            if ok:
                save_image(tup, u, out_dir)
    print(MSG_DOWNLOADED.format(out_dir=out_dir))


def handle_group(config):
    out_dir = config['output_dir']
    print(MSG_GROUPING)
    group_by_number(out_dir, config['group_by'])
    print(MSG_GROUPED)


def handle_edit(config):
    print("Current settings:")
    for key, val in config.items():
        print(f"  {key}: {val}")
    print("Enter new values or leave blank to keep current.")

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

    save_config(config)
    print("Settings saved.")


def main():
    config = load_config()
    os.makedirs(config['output_dir'], exist_ok=True)

    while True:
        display_menu()
        choice = input('Enter 1-5: ').strip()

        if choice == '5':
            print(MSG_EXIT)
            break
        if choice == '4':
            handle_edit(config)
        if choice in ('1', '3'):
            handle_download(config)
        if choice in ('2', '3'):
            handle_group(config)

        again = input(MSG_RETURN_PROMPT).strip().lower()
        if again == 'exit':
            print(MSG_EXIT)
            break

if __name__ == '__main__':
    main()