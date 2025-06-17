import os
from PIL import Image

def sheet_to_animation(
    sheet_path: str,
    output_path: str = None,
    frame_width: int = None,
    frame_height: int = None,
    duration: int = 100,
    loop: int = 0
):
    """
    Slice a sprite sheet into equal frames and write out a looping GIF (or APNG).
    - sheet_path: path to .png/.gif sprite‐sheet
    - output_path: where to save (defaults to same base name + .gif)
    - frame_width/height: if omitted, defaults to sheet height (square frames)
    - duration: ms per frame
    - loop: 0=infinite
    """
    im = Image.open(sheet_path)
    w, h = im.size

    # infer square frames = sheet height, unless overridden:
    fw = frame_width or frame_height or h
    fh = frame_height or frame_width or h

    # compute grid
    cols = w // fw
    rows = h // fh
    if cols * fw != w or rows * fh != h:
        raise ValueError(f"Sheet {w}×{h} not divisible by {fw}×{fh} frames")

    # crop out each frame
    frames = []
    for row in range(rows):
        for col in range(cols):
            left = col * fw
            top  = row * fh
            frames.append(im.crop((left, top, left + fw, top + fh)))

    # decide output filename
    base, _ = os.path.splitext(sheet_path)
    out = output_path or (base + '.gif')

    # save as animated GIF / APNG
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=loop,
        disposal=2,  # restore background before each frame
        transparency=0  # keep fully transparent pixels clear
    )
    print(f"✅ Created animation: {out} ({len(frames)} frames)")
