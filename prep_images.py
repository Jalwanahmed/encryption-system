# prep_images.py
from PIL import Image
import os
import glob

os.makedirs("test_data", exist_ok=True)

# Maps target name -> the SIPI code to search for (handles .tif or .tiff automatically)
sources = {
    "baboon":  "4.2.03",
    "peppers": "4.2.07",
    "moon":    "5.1.09",
}

for name, code in sources.items():
    matches = glob.glob(f"test_data/{code}.*")
    if not matches:
        print(f"WARNING: no file found for {code} in test_data/ — skipping {name}")
        continue

    src_path = matches[0]
    img = Image.open(src_path).convert("L")   # force grayscale
    img = img.resize((256, 256))                # force consistent size
    out_path = f"test_data/{name}.png"
    img.save(out_path)
    print(f"Saved {out_path} — size {img.size}, mode {img.mode} (from {src_path})")