
import pandas as pd
from pathlib import Path

csv_path = Path(r"D:\INTERIIT\kml_coordinates.csv")
gallery = Path(
    r"D:\INTERIIT\University-Release\test\gallery_satellite"
)

df = pd.read_csv(csv_path)
df["kml_id"] = df["kml_filename"].astype(str).str.replace(
    ".kml", "", regex=False
).str.zfill(4)

gallery_ids = {
    p.name for p in gallery.iterdir()
    if p.is_dir()
}

kml_ids = set(df["kml_id"])
matched = kml_ids & gallery_ids

print("KML coordinate rows:", len(df))
print("Unique KML IDs:", len(kml_ids))
print("Satellite gallery IDs:", len(gallery_ids))
print("IDs present in both:", len(matched))
print("\nSample coordinate records:")
print(df[["kml_filename", "placemark_name",
          "latitude", "longitude"]].head(10).to_string(index=False))

print("\nSample matching IDs:", sorted(matched)[:10])
