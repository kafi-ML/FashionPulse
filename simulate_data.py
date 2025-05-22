# simulate_data.py
import pandas as pd
import numpy as np

def simulate_product_data(n=500):
    np.random.seed(0)
    styles = ['Streetwear','Formal','Casual','Vintage','Athleisure']
    colors = ['Red','Blue','Black','White','Green','Yellow']
    seasons = ['Spring','Summer','Autumn','Winter']

    df = pd.DataFrame({
        'title': [f"Item{i}" for i in range(n)],
        'price': np.random.randint(10, 200, n),
        'gender': np.random.choice(['Men','Women','Unisex'], n),
        'color': np.random.choice(colors, n),
        'season': np.random.choice(seasons, n),
        'style': np.random.choice(styles, n),
        'pattern': [None]*n
    })

    today = pd.to_datetime('today').normalize()
    df['upload_date'] = today - pd.to_timedelta(np.random.randint(0, 90, size=n), unit='D')
    df['week'] = df['upload_date'].dt.to_period('W').apply(lambda r: r.start_time)
    
    return df
