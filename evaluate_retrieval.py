
from pathlib import Path
import time

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import models

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
ROOT = Path(r"D:\INTERIIT\University-Release")
TEST = ROOT / "test"

QUERY_DIR = TEST / "query_drone"
GALLERY_DIR = TEST / "gallery_satellite"

BATCH_SIZE = 16
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# --------------------------------------------------
# CHECK PATHS
# --------------------------------------------------
if not QUERY_DIR.exists():
    raise FileNotFoundError(f"Query directory not found: {QUERY_DIR}")

if not GALLERY_DIR.exists():
    raise FileNotFoundError(f"Gallery directory not found: {GALLERY_DIR}")

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", DEVICE)

# --------------------------------------------------
# COLLECT IMAGES
# --------------------------------------------------
def get_images(folder):
    return sorted(
        p for p in folder.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    )

# One query image per location for the first benchmark.
query_paths = []
query_ids = []

for location_folder in sorted(QUERY_DIR.iterdir()):
    if not location_folder.is_dir():
        continue

    images = get_images(location_folder)
    if not images:
        continue

    # Prefer image-01.jpeg when available.
    preferred = [
        p for p in images
        if p.name.lower() == "image-01.jpeg"
    ]
    chosen = preferred[0] if preferred else images[0]

    query_paths.append(chosen)
    query_ids.append(location_folder.name)

# One satellite image per gallery location.
gallery_paths = []
gallery_ids = []

for location_folder in sorted(GALLERY_DIR.iterdir()):
    if not location_folder.is_dir():
        continue

    images = get_images(location_folder)
    if not images:
        continue

    gallery_paths.append(images[0])
    gallery_ids.append(location_folder.name)

print("Drone queries:", len(query_paths))
print("Satellite gallery images:", len(gallery_paths))

if not query_paths or not gallery_paths:
    raise RuntimeError("No images found. Check the dataset folders.")

# --------------------------------------------------
# PRETRAINED RESNET50 EMBEDDING MODEL
# --------------------------------------------------
weights = models.ResNet50_Weights.DEFAULT
model = models.resnet50(weights=weights)
model.fc = torch.nn.Identity()
model = model.to(DEVICE).eval()

preprocess = weights.transforms()

print("Embedding model ready.")

# --------------------------------------------------
# COMPUTE EMBEDDINGS IN BATCHES
# --------------------------------------------------
@torch.inference_mode()
def embed_images(paths, label):
    all_embeddings = []
    total = len(paths)
    started = time.perf_counter()

    for start in range(0, total, BATCH_SIZE):
        batch_paths = paths[start:start + BATCH_SIZE]
        tensors = []

        for path in batch_paths:
            try:
                with Image.open(path) as img:
                    tensors.append(preprocess(img.convert("RGB")))
            except Exception as exc:
                raise RuntimeError(
                    f"Could not load image: {path}"
                ) from exc

        batch = torch.stack(tensors).to(DEVICE)
        embeddings = model(batch)
        embeddings = F.normalize(embeddings, p=2, dim=1)

        all_embeddings.append(embeddings.cpu())

        done = min(start + len(batch_paths), total)
        if done == total or done % 200 < BATCH_SIZE:
            print(f"{label}: {done}/{total}")

    elapsed = time.perf_counter() - started
    return torch.cat(all_embeddings, dim=0), elapsed

query_embeddings, query_seconds = embed_images(
    query_paths, "Drone queries"
)

gallery_embeddings, gallery_seconds = embed_images(
    gallery_paths, "Satellite gallery"
)

# --------------------------------------------------
# RETRIEVAL AND METRICS
# --------------------------------------------------
# Cosine similarity because embeddings are L2-normalized.
similarities = query_embeddings @ gallery_embeddings.T

gallery_id_array = np.array(gallery_ids, dtype=str)
query_id_array = np.array(query_ids, dtype=str)

top_k = min(5, len(gallery_ids))
top_scores, top_indices = torch.topk(
    similarities, k=top_k, dim=1
)

rank1_correct = []
rank5_correct = []
rows = []

for i, query_id in enumerate(query_ids):
    ranked_ids = gallery_id_array[
        top_indices[i].numpy()
    ].tolist()

    correct = [
        gallery_id == query_id
        for gallery_id in ranked_ids
    ]

    rank1_correct.append(correct[0])
    rank5_correct.append(any(correct))

    rows.append({
        "query_id": query_id,
        "query_image": str(query_paths[i]),
        "top1_gallery_id": ranked_ids[0],
        "top1_similarity": float(top_scores[i, 0]),
        "top1_correct": correct[0],
        "top5_correct": any(correct),
        "top5_gallery_ids": ", ".join(ranked_ids),
    })

results = pd.DataFrame(rows)

recall1 = float(np.mean(rank1_correct))
recall5 = float(np.mean(rank5_correct))

# --------------------------------------------------
# SAVE AND REPORT
# --------------------------------------------------
results_path = OUTPUT_DIR / "retrieval_results.csv"
results.to_csv(results_path, index=False)

print("\n========== RESULTS ==========")
print(f"Queries evaluated: {len(query_ids)}")
print(f"Gallery images: {len(gallery_ids)}")
print(f"Recall@1: {recall1:.4f} ({recall1 * 100:.2f}%)")
print(f"Recall@5: {recall5:.4f} ({recall5 * 100:.2f}%)")
print(f"Query embedding time: {query_seconds:.2f} seconds")
print(f"Gallery embedding time: {gallery_seconds:.2f} seconds")
print(f"Retrieval matrix time: included in overall run")
print(f"Results saved to: {results_path.resolve()}")

print("\nSample predictions:")
print(results.head(10).to_string(index=False))
