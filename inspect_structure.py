
from pathlib import Path

ROOT = Path(r"D:\INTERIIT\University-Release")

print("========== README ==========")
print((ROOT / "readme.txt").read_text(
    encoding="utf-8", errors="replace"
)[:10000])

for split in ("train", "test"):
    folder = ROOT / split
    print(f"\n========== {split.upper()} ==========")

    if not folder.exists():
        print("Folder not found")
        continue

    for item in sorted(folder.iterdir()):
        if item.is_dir():
            examples = list(item.iterdir())[:5]
            print(f"\nDIR: {item.name}")
            for example in examples:
                print("   ", example.name)
        else:
            print("FILE:", item.name)
