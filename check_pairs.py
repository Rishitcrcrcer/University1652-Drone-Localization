
from pathlib import Path

ROOT = Path(r"D:\INTERIIT\University-Release")
TEST = ROOT / "test"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

def image_files(folder):
    if not folder.exists():
        return []
    return [
        p for p in folder.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    ]

query_dir = TEST / "query_drone"
gallery_dir = TEST / "gallery_satellite"

query_ids = {
    p.name for p in query_dir.iterdir() if p.is_dir()
}
gallery_ids = {
    p.name for p in gallery_dir.iterdir() if p.is_dir()
}

common_ids = query_ids & gallery_ids

print("Drone query ID folders:", len(query_ids))
print("Satellite gallery ID folders:", len(gallery_ids))
print("IDs appearing in both:", len(common_ids))

print("\nExample matching IDs:")
for location_id in sorted(common_ids)[:10]:
    q_images = image_files(query_dir / location_id)
    g_images = image_files(gallery_dir / location_id)

    print(
        f"ID {location_id}: "
        f"{len(q_images)} drone query image(s), "
        f"{len(g_images)} satellite gallery image(s)"
    )

    if q_images:
        print("  Query example:", q_images[0].name)
    if g_images:
        print("  Gallery example:", g_images[0].name)

print("\nTotal query images:", len(image_files(query_dir)))
print("Total satellite gallery images:", len(image_files(gallery_dir)))
