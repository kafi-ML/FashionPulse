import os
import pandas as pd
import requests
from urllib.parse import urlparse

# Paths
INPUT_CSV = "data/zara_final.csv"
OUTPUT_CSV = "data/zara_final_with_images.csv"
IMAGE_DIR = "data/images"

# Ensure image directory exists
os.makedirs(IMAGE_DIR, exist_ok=True)

# Load the dataset
df = pd.read_csv(INPUT_CSV)

# Prepare headers to avoid 403 errors
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.zara.com/"
}

# Track local paths
local_paths = []

# Download logic
for idx, row in df.iterrows():
    image_url = row.get("image", "")
    
    # Skip invalid or placeholder URLs
    if (
        not image_url
        or not isinstance(image_url, str)
        or "transparent-background.png" in image_url
    ):
        local_paths.append("")  # Leave blank if unusable
        continue

    try:
        ext = os.path.splitext(urlparse(image_url).path)[-1]
        filename = f"img_{idx}{ext if ext else '.jpg'}"
        filepath = os.path.join(IMAGE_DIR, filename)

        response = requests.get(image_url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(response.content)
            local_paths.append(filepath)
        else:
            print(f"Failed to download {image_url}: HTTP {response.status_code}")
            local_paths.append("")
    except Exception as e:
        print(f"Error downloading {image_url}: {e}")
        local_paths.append("")

# Add the new column and save
df["image_path"] = local_paths
df.to_csv(OUTPUT_CSV, index=False)

print(f"\n✅ Image download complete. Updated file saved to: {OUTPUT_CSV}")
