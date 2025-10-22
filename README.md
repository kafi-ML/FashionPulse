# 👗 FashionPulse – AI-Powered Fashion Trend Tracker


FashionPulse is a demo project built to reflect real-world responsibilities of an AI Engineer at Nitex. It scrapes fashion data from global e-commerce platforms, analyzes visual and textual features using AI, and predicts emerging style trends across categories and seasons.

### 🚀 Why This Project?
This project was inspired by the Nitex job posting, which called for building intelligent systems that turn raw, chaotic fashion data into structured, trend-driven intelligence. FashionPulse is my response—demonstrating scraping, ML, image understanding, and deployment, all in one pipeline.

---

## 🔍 Features

### 🕸️ Smart Web Scraper
- Built with **Playwright** and **Scrapy**
- Scrapes product info from Zara, ASOS, Shein
- Extracts: Title, Description, Price, Category, Image URL

### 🧠 AI/ML Fashion Insight Engine
- Uses **CLIP (OpenAI)** to understand fashion images
- NLP pipeline cleans and extracts keywords from descriptions
- Predicts style category (e.g., Streetwear, Formal, Minimalist)

### 📊 Trend Prediction
- Aggregates historical data to track trending:
  - Colors
  - Silhouettes
  - Price ranges
- Uses **scikit-learn** for basic time-series modeling

### 🖥️ Interactive Dashboard
- Built with **FastAPI + Streamlit**
- Visualizes trend shifts with charts and product boards
- Filter by brand, category, or trend dimension

---

## 🧰 Tech Stack

| Area           | Tools & Libraries                          
|----------------|--------------------------------------------
| Scraping       | Playwright, Scrapy, BeautifulSoup          
| NLP            | spaCy, Transformers (HuggingFace)          
| Image Models   | CLIP, BLIP, PyTorch                       
| ML             | scikit-learn, pandas, NumPy                
| API Backend    | FastAPI, Uvicorn                           
| Frontend       | Streamlit (or React optional)              
| Deployment     | Docker, Render / GCP / Replit              

---




---

## 🧑‍💻 Author
**Abdullah Al Kafi** – AI + Data Scraping Enthusiast  
📫 kafi.official333@gmail.com | 🌐 https://www.linkedin.com/in/abdullah-al-kafi-eng/

---

## 🎯 Status
> This project is still in progess.  
> Focused on blending style, tech, and culture into code.

