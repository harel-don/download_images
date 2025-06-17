# Download Images Toolkit

A simple, configurable Python command-line tool to:

1. **Download** web images matching size and file-type criteria  
2. **Group** downloaded images into subfolders (by numeric ID)  
3. **Resize Canvas** of existing images to ensure a minimum square size (e.g., 96×96), preserving transparency and animation  
4. **Sprite-sheet → Animation**: slice and assemble sprite sheets into looping GIFs/APNGs  

---

## 📦 Project Structure
```
Download Images/              # Project root
├── downloaded_images/        # Output folder (auto‐created)
├── download_images/          # Python package modules
│   ├── __init__.py
│   ├── downloader.py         # Scrape & download logic
│   ├── grouper.py            # Image grouping logic
│   ├── resizer.py            # Canvas‐expansion logic
│   ├── sheet_assembler.py    # Sprite‐sheet slicing + animation
│   └── cli.py                # Main CLI entry point
├── settings.json             # User settings (extensions, sizes, etc.)
└── README.md                 # This file
```

---

## ⚙️ Installation

1. **Clone** or download this repository:  
   ```bash
   git clone https://github.com/YOUR_USERNAME/download_images.git
   cd download_images
   ```

2. **Install** dependencies (recommended in a virtualenv):  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # macOS/Linux
   .\.venv\Scripts\activate   # Windows PowerShell

   pip install --upgrade pip
   pip install requests beautifulsoup4 pillow
   ```

3. **Initialize** settings (auto‐generated on first run):  
   A `settings.json` will be created with defaults:
   ```json
   {
     "extensions": [".gif", ".png"],
     "sizes": [[96, 96]],
     "output_dir": "downloaded_images",
     "group_by": "number",
     "sheet_frame_width": null,
     "sheet_frame_height": null,
     "sheet_duration": 100,
     "sheet_loop": 0
   }
   ```

---

## 🚀 Usage

Run the CLI tool:

```bash
python -m download_images.cli
```

You’ll see:

```
Select operation mode:
1) Download images
2) Group images
3) Both
4) Edit settings
5) Resize canvas
6) Sprite-sheet → Animation
7) Exit
```

### 1) Download images  
- **Prompt**: Enter a webpage URL  
- **Action**: Scrapes `<img>` tags (supports `src`/`data-src`), filters by extensions and any size in `settings.json ▶ sizes`, and saves raw files to `downloaded_images/`.

### 2) Group images  
- **Action**: Scans `downloaded_images/`, extracts the first numeric token from each filename (e.g. `004` in `Spr 5b 004.png`), creates subfolders named by that token, and moves files accordingly.

### 3) Both  
- **Action**: Runs Download then Group in sequence.

### 4) Edit settings  
- **Action**: Interactive prompts to adjust:
  - **Extensions** (comma-separated, e.g. `.gif,.png,.jpg`)  
  - **Sizes** (comma-separated WxH pairs, e.g. `96x96,128x128`)  
  - **Output directory**  
  - **Group by** mode (`number`)  
  - **Sprite-sheet settings**:
    - `sheet_frame_width`        – explicit frame width (or leave blank to infer)  
    - `sheet_frame_height`       – explicit frame height (or leave blank to infer)  
    - `sheet_duration`           – ms per frame (default `100`)  
    - `sheet_loop`               – loop count (`0` = infinite)  
- **Persistence**: Writes updates to `settings.json`.

### 5) Resize canvas  
- **Action**: For each image in `downloaded_images/`:
  - Computes the larger dimension vs. each size in `sizes` and pads to that square.  
  - Creates a transparent canvas, centers the original horizontally, aligns bottom.  
  - Preserves GIF/APNG animation & transparency.

### 6) Sprite-sheet → Animation  
- **Action**: Takes one or more sprite-sheet files (PNG/GIF) and assembles them into looping animations.  
- **Input**: Enter a file path, press **Enter** to default to `output_dir/`.  
- **Settings**:
  - `sheet_frame_width`  – if set, forces frame width; else infers from sheet height  
  - `sheet_frame_height` – if set, forces frame height; else infers from sheet height  
  - `sheet_duration`     – ms per frame  
  - `sheet_loop`         – loop count  
- **Example**:
  ```bash
  python -m download_images.cli
  # Choose 6) Sprite-sheet → Animation
  # Press Enter to use downloaded_images/
  ```

### 7) Exit  
- **Action**: Quit the application.

---

## 🎨 Example Workflow

1. **Download & group**:
   ```bash
   python -m download_images.cli
   # Enter 3) Both
   # URL: https://archives.bulbagarden.net/wiki/Category:Black_2_and_White_2_sprites
   ```

2. **Resize small images** to 96×96:
   ```bash
   python -m download_images.cli
   # Enter 5) Resize canvas
   ```

3. **Build animations** from sprite sheets:
   ```bash
   python -m download_images.cli
   # Enter 6) Sprite-sheet → Animation
   # Press Enter to use downloaded_images/
   ```

4. **Browse** results:
   ```bash
   tree downloaded_images
   ```

---

## 👩‍💻 Customization
- Edit `settings.json` manually or via **4) Edit settings**.  
- To remove a menu option, delete its block in `cli.py`.  
- To add new grouping modes, extend `group_images()` in `grouper.py`.  

---

## 📄 License
MIT © Harel Don-Yehiya

Feel free to fork, modify, and contribute!
