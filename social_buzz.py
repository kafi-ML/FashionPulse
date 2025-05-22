# social_buzz.py
import numpy as np

def simulate_hashtags(df):
    np.random.seed(1)
    style_time = df.groupby(['style','week']).size().reset_index(name='count')
    style_time = style_time.sort_values(['style','week'])

    style_time['hashtag_count'] = (style_time['count'] * 
        (1 + np.random.uniform(-0.3, 0.5, size=len(style_time))))
    style_time['hashtag_count'] = style_time['hashtag_count'].clip(lower=0).astype(int)

    return style_time
