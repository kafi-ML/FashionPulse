# utils/enrich_data.py

import pandas as pd
import re

COLOR_KEYWORDS = [
    'black', 'white', 'red', 'blue', 'green', 'yellow', 'pink', 'beige',
    'brown', 'grey', 'gray', 'orange', 'purple', 'navy', 'gold', 'silver'
]

SEASON_KEYWORDS = {
    "winter": ["wool", "coat", "long-sleeve", "thermal"],
    "summer": ["linen", "cotton", "short", "sleeveless"],
    "spring": ["floral", "lightweight"],
    "fall": ["jacket", "layer"]
}

GENDER_KEYWORDS = {
    "women": ["woman", "women", "ladies", "female"],
    "men": ["man", "men", "male", "gentleman"],
    "kids": ["kid", "child", "boy", "girl"]
}

def extract_color(text):
    text = text.lower()
    for color in COLOR_KEYWORDS:
        if color in text:
            return color
    return "unknown"

def extract_season(text):
    text = text.lower()
    for season, keywords in SEASON_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return season
    return "all-season"

def extract_gender(text):
    text = text.lower()
    for gender, keywords in GENDER_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return gender
    return "unisex"

def enrich_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    df["gender"] = df["title"].fillna("").apply(extract_gender)

    # df["color"] = df["description"].fillna("").apply(extract_color)
    # df["season"] = df["description"].fillna("").apply(extract_season)
    df["color"] = df["title"].fillna("").apply(extract_color)
    df["season"] = df["title"].fillna("").apply(extract_season)

    df.to_csv(output_csv, index=False)
    print(f"✅ Enriched data saved to {output_csv}")

if __name__ == "__main__":
    enrich_csv("data/zara_products.csv", "data/zara_enriched.csv")
