# utils/scrape_zara_product_images.py

import os
import time
import urllib.request
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# Load CSV with product page links
df = pd.read_csv("data/zara_final.csv")  # Must have column: product_url
output_dir = "data/product_images"
os.makedirs(output_dir, exist_ok=True)

options = uc.ChromeOptions()
options.add_argument("--headless")  # Optional: remove to see browser
driver = uc.Chrome(options=options)

for idx, row in df.iterrows():
    url = row.get("product_url", "")
    if not isinstance(url, str) or not url.startswith("http"):
        continue

    try:
        driver.get(url)
        time.sleep(3)

        # Find product image containers (Zara uses <img> with srcset)
        images = driver.find_elements(By.CSS_SELECTOR, "img")

        downloaded = 0
        for i, img in enumerate(images):
            src = img.get_attribute("src")
            if src and "static.zara.net/photos/" in src and src.endswith(".jpg"):
                save_path = os.path.join(output_dir, f"product_{idx}_{i}.jpg")
                urllib.request.urlretrieve(src, save_path)
                downloaded += 1

        print(f"✅ Row {idx} - {downloaded} images downloaded.")

    except Exception as e:
        print(f"❌ Failed at row {idx} - {url}: {e}")

driver.quit()
