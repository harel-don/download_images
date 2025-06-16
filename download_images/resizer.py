import os
from PIL import Image, ImageSequence

MIN_SIZE = 96

def expand_canvas(frame: Image.Image, new_w: int, new_h: int) -> Image.Image:
    """
    Return a new RGBA image of size (new_w,new_h) with `frame` pasted
    centered horizontally and aligned to bottom, preserving alpha.
    """
    canvas = Image.new('RGBA', (new_w, new_h), (0, 0, 0, 0))
    w, h = frame.size
    x = (new_w - w) // 2
    y = new_h - h
    frame_rgba = frame.convert('RGBA')
    canvas.paste(frame_rgba, (x, y), frame_rgba)
    return canvas


def process_image(path: str, min_size: int = MIN_SIZE) -> None:
    """
    Expand canvas for static and animated images, preserving transparency.
    Handles both GIF and APNG.
    """
    im = Image.open(path)
    w, h = im.size
    new = max(min_size, w, h)
    ext = os.path.splitext(path)[1].lower()

    if getattr(im, 'is_animated', False):
        # Process each frame
        frames = []
        durations = []
        for fr in ImageSequence.Iterator(im):
            new_frame = expand_canvas(fr, new, new)
            frames.append(new_frame)
            durations.append(fr.info.get('duration', 100))

        # Save animated PNG or GIF accordingly
        save_kwargs = {
            'save_all': True,
            'append_images': frames[1:],
            'loop': 0
        }
        if ext == '.gif':
            # GIF parameters
            save_kwargs.update({
                'duration': durations,
                'disposal': 2,
                'transparency': 0
            })
            frames[0].save(path, format='GIF', **save_kwargs)
        elif ext == '.png':
            # APNG support (Pillow >=7.0)
            save_kwargs.update({
                'duration': durations
            })
            frames[0].save(path, format='PNG', **save_kwargs)
        else:
            # Other animated formats fallback to first frame
            new_im = expand_canvas(im, new, new)
            new_im.save(path)
    else:
        # Static image: expand and save as PNG if original was PNG, else keep format
        new_im = expand_canvas(im, new, new)
        if ext == '.png':
            new_im.save(path, format='PNG')
        elif ext == '.gif':
            new_im.save(path, format='GIF')
        else:
            new_im.save(path)


def batch_resize(directory: str, extensions=None, min_size: int = MIN_SIZE) -> None:
    """
    Walk `directory` and process each image matching extensions.
    """
    ext_set = set(ext.lower() for ext in (extensions or ['.gif', '.png']))
    for fn in os.listdir(directory):
        _, ext = os.path.splitext(fn)
        if ext.lower() not in ext_set:
            continue
        path = os.path.join(directory, fn)
        if not os.path.isfile(path):
            continue
        try:
            process_image(path, min_size)
            print(f"🔧 Resized {fn}")
        except Exception as e:
            print(f"⚠️ Failed resizing {fn}: {e}")