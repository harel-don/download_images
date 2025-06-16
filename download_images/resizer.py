import os
from PIL import Image, ImageSequence

# Target minimum size (can be made configurable via settings if desired)
MIN_SIZE = 96


def expand_canvas(frame: Image.Image, new_w: int, new_h: int) -> Image.Image:
    """
    Return a new image of size (new_w,new_h) with `frame` pasted
    centered horizontally and aligned to the bottom, background transparent.
    """
    mode = 'RGBA' if frame.mode in ('RGBA','LA') else 'RGB'
    bg_color = (0, 0, 0, 0) if mode=='RGBA' else (0, 0, 0)
    canvas = Image.new(mode, (new_w, new_h), bg_color)
    # compute offsets
    w, h = frame.size
    x = (new_w - w) // 2
    y = new_h - h
    if frame.mode != mode:
        frame = frame.convert(mode)
    canvas.paste(frame, (x, y), frame if 'A' in mode else None)
    return canvas


def process_image(path: str, min_size: int = MIN_SIZE) -> None:
    """
    Resize the image at `path` by expanding its canvas so that
    both dimensions >= min_size (or the larger of its own dims).
    Animated GIF frames are each processed and repackaged.
    """
    im = Image.open(path)
    w, h = im.size
    # determine new square size
    new_size = max(min_size, w, h)

    if getattr(im, 'is_animated', False):
        frames = []
        durations = []
        for frame in ImageSequence.Iterator(im):
            new_frame = expand_canvas(frame, new_size, new_size)
            frames.append(new_frame)
            durations.append(frame.info.get('duration', 100))
        # overwrite original GIF
        frames[0].save(
            path,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=0,
            disposal=2
        )
    else:
        new_im = expand_canvas(im, new_size, new_size)
        new_im.save(path)


def batch_resize(directory: str, extensions=None, min_size: int = MIN_SIZE) -> None:
    """
    Walk `directory` (non-recursive) and call `process_image` on each file
    whose extension is in `extensions` (list of ".gif", ".png", etc.).
    """
    ext_set = set(ext.lower() for ext in (extensions or ['.gif','.png']))
    for fn in os.listdir(directory):
        _, ext = os.path.splitext(fn)
        if ext.lower() not in ext_set:
            continue
        path = os.path.join(directory, fn)
        if not os.path.isfile(path):
            continue
        try:
            process_image(path, min_size)
            print(f"🔧 Resized canvas for {fn}")
        except Exception as e:
            print(f"⚠️ Failed resizing {fn}: {e}")