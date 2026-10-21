
from pathlib import Path

# Change this to the folder containing the extracted dataset.
DATASET_ROOT = Path(r"D:\INTERIIT\University-Release")

if not DATASET_ROOT.exists():
    raise FileNotFoundError(
        f"Dataset folder not found: {DATASET_ROOT}\n"
        "Update DATASET_ROOT to the actual folder path."
    )

print("Dataset root:", DATASET_ROOT)
print("\nTop-level contents:")

for item in sorted(DATASET_ROOT.iterdir()):
    print("DIR " if item.is_dir() else "FILE", item.name)

print("\nLikely image folders:")

image_extensions = {".jpg", ".jpeg", ".png", ".bmp"}

for folder in DATASET_ROOT.rglob("*"):
    if not folder.is_dir():
        continue

    if folder.name.lower() in {
        "drone", "satellite", "query", "gallery", "train", "test"
    }:
        count = sum(
            1 for p in folder.rglob("*")
            if p.is_file() and p.suffix.lower() in image_extensions
        )
        if count:
            print(f"{folder}: {count:,} images")
