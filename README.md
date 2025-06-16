# Download Images Toolkit

A simple, configurable Python command-line tool to:

1. **Download** web images matching size and file-type criteria
2. **Group** downloaded images into subfolders (by numeric ID)
3. **Resize Canvas** of existing images to ensure a minimum square size (e.g., 96×96), preserving transparency and animation

---

## 📦 Project Structure
```
Download Images/              # Project root
├── downloaded_images/        # Output folder (auto-created)
├── download_images/          # Python package modules
│   ├── __init__.py
│   ├── downloader.py         # Scrape & download logic
│   ├── grouper.py            # Image grouping logic
│   ├── resizer.py            # Canvas-expansion logic
│   └── cli.py                # Main CLI entry point
├── settings.json             # User settings (extensions, size, etc.)
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

3. **Initialize** settings (auto-generated on first run):
   - A `settings.json` file will appear with default values for:  
     • `extensions`: [".gif", ".png"]  
     • `size`: [96, 96]  
     • `output_dir`: "downloaded_images"  
     • `group_by`: "number"

---

## 🚀 Usage

Run the CLI tool:
```bash
python -m download_images.cli
```

You will see a menu:
```
Select operation mode:
1) Download images
2) Group images
3) Both
4) Edit settings
5) Resize canvas
6) Exit
```

### 1) Download images
- **Prompt**: Enter a webpage URL
- **Action**: Scrapes all `<img>` elements (supports `src` and `data-src`), filters by file extension and exact size from settings, and saves raw files into `downloaded_images/`.

### 2) Group images
- **Action**: Scans `downloaded_images/`, extracts the first numeric token in each filename (e.g. `004` in `Spr 5b 004.png`), makes subfolders named by that number, and moves each file into its corresponding folder.

### 3) Both
- **Action**: Performs Download then Group in sequence.

### 4) Edit settings
- **Action**: Opens an interactive prompt to adjust:
  - **Extensions** (comma-separated)
  - **Size** (e.g. `96x96`)
  - **Output directory**
  - **Grouping mode** (currently only `number`)
- **Persistence**: Writes to `settings.json` so your preferences are remembered on next run.

### 5) Resize canvas
- **Action**: Walks `downloaded_images/` and for each image:
  - Determines the larger of width or height vs. the minimum size
  - Creates a new transparent canvas of that square size
  - Pastes each frame (if animated) or the static image centered horizontally and aligned bottom
  - Saves back to the original file path, preserving GIF/APNG animation and transparency

### 6) Exit
- **Action**: Quit the tool.

---

## 🎨 Example Workflow

1. **Download and group sprites** from Bulbapedia:
   ```bash
   python -m download_images.cli
   # Choose 3) Both
   # Paste: https://archives.bulbagarden.net/wiki/Category:Black_2_and_White_2_sprites
   ```

2. **Resize** any small images to ensure 96×96 canvas:
   ```bash
   python -m download_images.cli
   # Choose 5) Resize canvas
   ```

3. **View** organized files in `downloaded_images/`:
   ```bash
   tree downloaded_images
   ```

---

## 👩‍💻 Customization
- You can modify defaults in `settings.json`, or use the **4) Edit settings** menu.
- To remove the temporary **Resize canvas** option, simply delete its block in `cli.py` (option 5).
- To add more grouping strategies (e.g. `prefix`), extend `group_images()` in `grouper.py`.

---

## 📄 License
MIT © Harel Don-Yehiya

Feel free to fork and contribute!
