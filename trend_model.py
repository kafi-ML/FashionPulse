# trend_model.py
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def prepare_training_data(style_time):
    rows = []
    for style in style_time['style'].unique():
        grp = style_time[style_time['style']==style].sort_values('week').reset_index(drop=True)
        for i in range(len(grp)-1):
            rows.append({
                'count': int(grp.loc[i,'count']),
                'hashtag': int(grp.loc[i,'hashtag_count']),
                'next_up': int(grp.loc[i+1,'count'] > grp.loc[i,'count'])
            })
    return pd.DataFrame(rows)

def train_model(trend_df):
    X = trend_df[['count','hashtag']]
    y = trend_df['next_up']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    print("Accuracy:", model.score(X_test, y_test))
    print("Classification Report:\n", classification_report(y_test, y_pred))
