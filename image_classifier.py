# utils/image_classifier.py
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from transformers import CLIPProcessor, CLIPModel
import torch

# Load pre-trained CLIP model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Define style and pattern labels
STYLE_LABELS = ["Casual", "Streetwear", "Formal", "Sporty", "Bohemian", "Vintage"]
PATTERN_LABELS = ["Floral", "Solid", "Striped", "Plaid", "Polka Dot", "Graphic"]

def classify_image(image_url, labels):
    try:
        response = requests.get(image_url, timeout=5)
        image = Image.open(BytesIO(response.content)).convert("RGB")
    except Exception:
        return "Unknown"
    
    inputs = processor(text=labels, images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)
    pred_label = labels[probs.argmax().item()]
    return pred_label

def enrich_images(csv_path_in, csv_path_out):
    df = pd.read_csv(csv_path_in)
    df["style"] = df["image"].apply(lambda url: classify_image(url, STYLE_LABELS))
    df["pattern"] = df["image"].apply(lambda url: classify_image(url, PATTERN_LABELS))
    df.to_csv(csv_path_out, index=False)
    print("✅ Image classification complete and saved to:", csv_path_out)

# Run the enrichment
if __name__ == "__main__":
    enrich_images("data/zara_enriched.csv", "data/zara_final.csv")
