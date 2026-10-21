
from pathlib import Path
import xml.etree.ElementTree as ET
import csv

# Change this to the folder containing your KML files
KML_FOLDER = Path(r"D:\INTERIIT\university1652-first-key\first-key")
OUTPUT_CSV = Path(r"D:\INTERIIT\kml_coordinates.csv")

NS = {"kml": "http://www.opengis.net/kml/2.2"}

rows = []

for file in KML_FOLDER.rglob("*.kml"):
    try:
        root = ET.parse(file).getroot()

        for placemark in root.findall(".//kml:Placemark", NS):
            name = placemark.findtext("kml:name", default="", namespaces=NS)

            for point in placemark.findall(".//kml:Point", NS):
                coord = point.findtext(
                    "kml:coordinates", default="", namespaces=NS
                ).strip()

                if not coord:
                    continue

                # KML order is longitude, latitude, altitude
                values = coord.split(",")
                longitude = float(values[0])
                latitude = float(values[1])
                altitude = float(values[2]) if len(values) > 2 else None

                rows.append([
                    file.name, name, latitude, longitude, altitude
                ])

    except Exception as e:
        print(f"Could not read {file}: {e}")

with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "kml_filename", "placemark_name",
        "latitude", "longitude", "altitude"
    ])
    writer.writerows(rows)

print(f"Extracted {len(rows)} coordinate points.")
print(f"Saved to: {OUTPUT_CSV}")
